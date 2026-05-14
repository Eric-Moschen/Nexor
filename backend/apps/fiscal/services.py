from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.financeiro.services import FinanceiroService
from apps.fiscal.enums import StatusNFe, TipoEventoFiscal, TipoOperacao
from apps.fiscal.integrations.certificate_manager import CertificateManager
from apps.fiscal.integrations.danfe_generator import DanfeGenerator
from apps.fiscal.integrations.sefaz_client import SefazClient
from apps.fiscal.integrations.xml_builder import NFeXmlBuilder
from apps.fiscal.models import EmpresaFiscal, EventoFiscal, ItemNotaFiscal, NotaFiscal
from apps.fiscal.validators import only_digits, validate_cep, validate_cfop, validate_cnpj, validate_cpf_cnpj, validate_ibge, validate_ncm
from apps.estoque.services import EstoqueService


class FiscalService:
    def __init__(self, sefaz_client=None, xml_builder=None, danfe_generator=None, certificate_manager=None):
        self.sefaz_client = sefaz_client or SefazClient()
        self.xml_builder = xml_builder or NFeXmlBuilder()
        self.danfe_generator = danfe_generator or DanfeGenerator()
        self.certificate_manager = certificate_manager or CertificateManager()

    @transaction.atomic
    def salvar_empresa(self, *, usuario, senha_certificado="", **dados):
        validate_cnpj(dados["cnpj"])
        validate_ibge(dados["municipio_ibge"])
        validate_cep(dados["cep"])
        dados["cnpj"] = only_digits(dados["cnpj"])
        dados["cep"] = only_digits(dados["cep"])
        if senha_certificado:
            dados["certificado_senha_protegida"] = self.certificate_manager.protect_password(senha_certificado)
        empresa = EmpresaFiscal.objects.create(created_by=usuario, updated_by=usuario, **dados)
        return empresa

    @transaction.atomic
    def criar_nfe(self, *, usuario, itens, **dados):
        if not itens:
            raise ValidationError("NFe precisa ter ao menos um item.")
        nota = NotaFiscal.objects.create(usuario_responsavel=usuario, created_by=usuario, updated_by=usuario, **dados)
        for item in itens:
            self._criar_item(nota, item)
        self.recalcular_totais(nota)
        self.registrar_evento(nota, TipoEventoFiscal.VALIDACAO, "NFe criada em rascunho", usuario=usuario)
        return nota

    @transaction.atomic
    def validar_nfe(self, *, nota_id, usuario):
        nota = NotaFiscal.objects.select_for_update().prefetch_related("itens").get(id=nota_id)
        if nota.status == StatusNFe.AUTORIZADA:
            raise ValidationError("NFe autorizada nao pode ser alterada.")
        if not nota.itens.exists():
            raise ValidationError("NFe sem item nao pode ser enviada.")
        self._validar_dados_fiscais(nota)
        nota.status = StatusNFe.VALIDADA
        nota.save(update_fields=["status", "updated_at"])
        self.registrar_evento(nota, TipoEventoFiscal.VALIDACAO, "NFe validada com sucesso", usuario=usuario)
        return nota

    @transaction.atomic
    def assinar_nfe(self, *, nota_id, usuario):
        nota = NotaFiscal.objects.select_for_update().get(id=nota_id)
        if nota.status != StatusNFe.VALIDADA:
            raise ValidationError("Apenas NFe validada pode ser assinada.")
        if not self.certificate_manager.validate_certificate(nota.emitente):
            raise ValidationError("Certificado digital A1 nao configurado.")
        nota.xml_autorizado = self.xml_builder.build(nota)
        nota.status = StatusNFe.ASSINADA
        nota.save(update_fields=["xml_autorizado", "status", "updated_at"])
        self.registrar_evento(nota, TipoEventoFiscal.ASSINATURA, "XML assinado e preparado", usuario=usuario)
        return nota

    @transaction.atomic
    def enviar_nfe(self, *, nota_id, usuario):
        nota = NotaFiscal.objects.select_for_update().prefetch_related("itens", "itens__produto").get(id=nota_id)
        if nota.status != StatusNFe.ASSINADA:
            raise ValidationError("Apenas NFe assinada pode ser enviada.")
        response = self.sefaz_client.enviar_nfe(nota.xml_autorizado, nota.ambiente)
        nota.status = StatusNFe.AUTORIZADA if response.autorizado else StatusNFe.REJEITADA
        nota.protocolo = response.protocolo
        if response.autorizado:
            nota.chave_acesso = self._gerar_chave_acesso(nota)
            nota.xml_autorizado = response.xml_retorno or nota.xml_autorizado
            self._integrar_estoque(nota, usuario)
            self._integrar_financeiro(nota, usuario)
            evento = TipoEventoFiscal.AUTORIZACAO
            mensagem = "NFe autorizada com sucesso"
        else:
            nota.motivo_rejeicao = response.mensagem
            evento = TipoEventoFiscal.REJEICAO
            mensagem = response.mensagem
        nota.save(update_fields=["status", "protocolo", "chave_acesso", "xml_autorizado", "motivo_rejeicao", "updated_at"])
        self.registrar_evento(nota, evento, mensagem, codigo=response.codigo, protocolo=response.protocolo, xml=response.xml_retorno, usuario=usuario)
        from apps.core.events.base import InternalEvent, NFE_AUTORIZADA, NFE_REJEITADA
        from apps.core.events.dispatcher import EventDispatcher

        EventDispatcher().publish(InternalEvent(
            name=NFE_AUTORIZADA if response.autorizado else NFE_REJEITADA,
            module="fiscal",
            aggregate_type="fiscal.NotaFiscal",
            aggregate_id=str(nota.id),
            payload={"title": "NFe autorizada" if response.autorizado else "NFe rejeitada", "message": mensagem, "valor_total": str(nota.valor_total), "protocolo": response.protocolo},
            user=usuario,
        ))
        return nota

    @transaction.atomic
    def cancelar_nfe(self, *, nota_id, usuario, justificativa):
        nota = NotaFiscal.objects.select_for_update().get(id=nota_id)
        if nota.status != StatusNFe.AUTORIZADA:
            raise ValidationError("Apenas NFe autorizada pode ser cancelada.")
        response = self.sefaz_client.cancelar_nfe(nota, justificativa)
        nota.status = StatusNFe.CANCELADA
        nota.xml_cancelamento = response.xml_retorno
        nota.save(update_fields=["status", "xml_cancelamento", "updated_at"])
        self.registrar_evento(nota, TipoEventoFiscal.CANCELAMENTO, justificativa, codigo=response.codigo, protocolo=response.protocolo, xml=response.xml_retorno, usuario=usuario)
        return nota

    def gerar_danfe(self, *, nota_id):
        nota = NotaFiscal.objects.get(id=nota_id)
        if nota.status not in {StatusNFe.AUTORIZADA, StatusNFe.CANCELADA}:
            raise ValidationError("DANFE disponivel apenas para NFe autorizada ou cancelada.")
        nota.danfe_pdf.save(f"danfe-{nota.numero}-{nota.serie}.pdf", self.danfe_generator.generate(nota), save=True)
        return nota.danfe_pdf

    def recalcular_totais(self, nota):
        valor_produtos = sum((item.valor_total for item in nota.itens.all()), Decimal("0.00"))
        nota.valor_produtos = valor_produtos
        nota.valor_total = valor_produtos + nota.valor_frete - nota.valor_desconto
        nota.save(update_fields=["valor_produtos", "valor_total", "updated_at"])

    def registrar_evento(self, nota, tipo, mensagem, codigo="", protocolo="", xml="", usuario=None):
        return EventoFiscal.objects.create(
            nota_fiscal=nota,
            tipo_evento=tipo,
            codigo_retorno=codigo,
            mensagem=mensagem,
            protocolo=protocolo,
            xml_retorno=xml,
            usuario_responsavel=usuario,
        )

    def _criar_item(self, nota, item):
        produto_fiscal = getattr(item["produto"], "dados_fiscais", None)
        if not produto_fiscal:
            raise ValidationError("Produto fiscal completo obrigatorio.")
        validate_ncm(produto_fiscal.ncm)
        validate_cfop(item.get("cfop") or produto_fiscal.cfop_padrao)
        quantidade = Decimal(str(item["quantidade"]))
        valor_unitario = Decimal(str(item["valor_unitario"]))
        desconto = Decimal(str(item.get("desconto", 0)))
        if quantidade <= 0:
            raise ValidationError("Quantidade deve ser maior que zero.")
        if valor_unitario < 0:
            raise ValidationError("Valor unitario nao pode ser negativo.")
        valor_bruto = quantidade * valor_unitario
        valor_total = (valor_bruto - desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        base = valor_total
        return ItemNotaFiscal.objects.create(
            nota_fiscal=nota,
            produto=item["produto"],
            descricao=item.get("descricao") or item["produto"].nome,
            cfop=item.get("cfop") or produto_fiscal.cfop_padrao,
            ncm=produto_fiscal.ncm,
            cst_csosn=produto_fiscal.cst_csosn,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            desconto=desconto,
            base_icms=base,
            valor_icms=self._calcular_imposto(base, produto_fiscal.aliquota_icms),
            base_pis=base,
            valor_pis=self._calcular_imposto(base, produto_fiscal.aliquota_pis),
            base_cofins=base,
            valor_cofins=self._calcular_imposto(base, produto_fiscal.aliquota_cofins),
            base_ipi=base,
            valor_ipi=self._calcular_imposto(base, produto_fiscal.aliquota_ipi),
        )

    def _validar_dados_fiscais(self, nota):
        validate_cnpj(nota.emitente.cnpj)
        validate_ibge(nota.emitente.municipio_ibge)
        if nota.destinatario_cliente and not hasattr(nota.destinatario_cliente, "dados_fiscais"):
            raise ValidationError("Cliente fiscal completo obrigatorio.")
        if nota.destinatario_fornecedor and not hasattr(nota.destinatario_fornecedor, "dados_fiscais"):
            raise ValidationError("Fornecedor fiscal completo obrigatorio.")
        destinatario_fiscal = getattr(nota.destinatario_cliente or nota.destinatario_fornecedor, "dados_fiscais", None)
        if destinatario_fiscal:
            validate_cpf_cnpj(destinatario_fiscal.cpf_cnpj)
            validate_ibge(destinatario_fiscal.municipio_ibge)
            validate_cep(destinatario_fiscal.cep)
        for item in nota.itens.all():
            validate_ncm(item.ncm)
            validate_cfop(item.cfop)

    def _integrar_estoque(self, nota, usuario):
        if not nota.natureza_operacao.movimenta_estoque:
            return
        service = EstoqueService()
        for item in nota.itens.all():
            if nota.tipo_operacao == TipoOperacao.VENDA:
                service.registrar_saida(produto_id=item.produto_id, quantidade=item.quantidade, usuario=usuario, observacao=f"NFe {nota.numero}/{nota.serie}")
            elif nota.tipo_operacao == TipoOperacao.COMPRA:
                service.registrar_entrada(produto_id=item.produto_id, quantidade=item.quantidade, usuario=usuario, observacao=f"NFe {nota.numero}/{nota.serie}")

    def _integrar_financeiro(self, nota, usuario):
        if not nota.natureza_operacao.gera_financeiro or not nota.categoria_financeira or not nota.centro_custo:
            return
        service = FinanceiroService()
        if nota.tipo_operacao == TipoOperacao.VENDA and nota.destinatario_cliente:
            nota.conta_receber = service.criar_conta_receber(
                usuario=usuario,
                cliente=nota.destinatario_cliente,
                descricao=f"NFe {nota.numero}/{nota.serie}",
                categoria=nota.categoria_financeira,
                centro_custo=nota.centro_custo,
                valor_original=nota.valor_total,
                data_emissao=timezone.localdate(),
                data_vencimento=timezone.localdate(),
            )
        elif nota.tipo_operacao == TipoOperacao.COMPRA and nota.destinatario_fornecedor:
            nota.conta_pagar = service.criar_conta_pagar(
                usuario=usuario,
                fornecedor=nota.destinatario_fornecedor,
                descricao=f"NFe {nota.numero}/{nota.serie}",
                categoria=nota.categoria_financeira,
                centro_custo=nota.centro_custo,
                valor_original=nota.valor_total,
                data_emissao=timezone.localdate(),
                data_vencimento=timezone.localdate(),
            )
        nota.save(update_fields=["conta_receber", "conta_pagar", "updated_at"])

    def _calcular_imposto(self, base, aliquota):
        return (base * Decimal(str(aliquota)) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _gerar_chave_acesso(self, nota):
        cnpj = nota.emitente.cnpj.zfill(14)
        return f"{cnpj}{nota.numero:09d}{nota.serie:03d}{nota.id:018d}"[:44]
