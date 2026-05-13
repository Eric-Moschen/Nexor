from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.orcamentos.enums import StatusOrcamento, TipoEventoOrcamento
from apps.orcamentos.models import HistoricoOrcamento, ItemProdutoOrcamento, ItemServicoOrcamento, Orcamento
from apps.orcamentos.pdf.orcamento_pdf import OrcamentoPdfGenerator
from apps.orcamentos.repositories import OrcamentoRepository
from apps.ordens_servico.services import OrdemServicoService


class OrcamentoService:
    status_bloqueados_edicao = {StatusOrcamento.APROVADO, StatusOrcamento.CONVERTIDO_OS, StatusOrcamento.CANCELADO}

    def __init__(self, repository=None, pdf_generator=None, os_service=None):
        self.repository = repository or OrcamentoRepository()
        self.pdf_generator = pdf_generator or OrcamentoPdfGenerator()
        self.os_service = os_service or OrdemServicoService()

    @transaction.atomic
    def criar_orcamento(self, *, usuario, itens_produto=None, itens_servico=None, **dados):
        if not dados.get("cliente"):
            raise ValidationError("Orcamento precisa ter cliente.")
        if not itens_produto and not itens_servico:
            raise ValidationError("Orcamento precisa ter ao menos um item.")
        if dados["data_validade"] < timezone.localdate():
            raise ValidationError("Data de validade nao pode ser anterior a data atual.")
        if not dados.get("numero"):
            dados["numero"] = self._proximo_numero()
        orcamento = Orcamento.objects.create(usuario_responsavel=usuario, created_by=usuario, updated_by=usuario, **dados)
        for item in itens_produto or []:
            self._criar_item_produto(orcamento, item)
        for item in itens_servico or []:
            self._criar_item_servico(orcamento, item)
        self.recalcular_totais(orcamento)
        self.registrar_historico(orcamento, TipoEventoOrcamento.CRIACAO, "Orcamento criado.", usuario=usuario)
        return orcamento

    @transaction.atomic
    def atualizar_orcamento(self, *, orcamento_id, usuario, **dados):
        orcamento = self.repository.get_for_update(orcamento_id)
        self._bloquear_edicao(orcamento)
        if "data_validade" in dados and dados["data_validade"] < timezone.localdate():
            raise ValidationError("Data de validade nao pode ser anterior a data atual.")
        for field, value in dados.items():
            setattr(orcamento, field, value)
        orcamento.updated_by = usuario
        orcamento.save()
        self.recalcular_totais(orcamento)
        self.registrar_historico(orcamento, TipoEventoOrcamento.ALTERACAO, "Orcamento atualizado.", usuario=usuario)
        return orcamento

    @transaction.atomic
    def enviar(self, *, orcamento_id, usuario):
        orcamento = self.repository.get_for_update(orcamento_id)
        if orcamento.status not in {StatusOrcamento.RASCUNHO, StatusOrcamento.EM_ANALISE}:
            raise ValidationError("Apenas orcamento em rascunho ou analise pode ser enviado.")
        if not self._possui_itens(orcamento):
            raise ValidationError("Orcamento precisa ter ao menos um item.")
        return self._alterar_status(orcamento, StatusOrcamento.ENVIADO, TipoEventoOrcamento.ENVIO, "Orcamento enviado ao cliente.", usuario)

    @transaction.atomic
    def aprovar(self, *, orcamento_id, usuario):
        orcamento = self.repository.get_for_update(orcamento_id)
        if orcamento.status == StatusOrcamento.CANCELADO:
            raise ValidationError("Orcamento cancelado nao pode ser aprovado.")
        if orcamento.status == StatusOrcamento.EXPIRADO or orcamento.data_validade < timezone.localdate():
            raise ValidationError("Orcamento expirado nao pode ser aprovado sem revalidacao.")
        if orcamento.status not in {StatusOrcamento.ENVIADO, StatusOrcamento.EM_ANALISE, StatusOrcamento.RASCUNHO}:
            raise ValidationError("Orcamento nao esta em status permitido para aprovacao.")
        return self._alterar_status(orcamento, StatusOrcamento.APROVADO, TipoEventoOrcamento.APROVACAO, "Orcamento aprovado pelo cliente.", usuario)

    @transaction.atomic
    def reprovar(self, *, orcamento_id, usuario, motivo):
        if not motivo or not motivo.strip():
            raise ValidationError("Reprovacao exige motivo.")
        orcamento = self.repository.get_for_update(orcamento_id)
        if orcamento.status in {StatusOrcamento.CANCELADO, StatusOrcamento.CONVERTIDO_OS}:
            raise ValidationError("Orcamento neste status nao pode ser reprovado.")
        orcamento.motivo_reprovacao = motivo
        orcamento.save(update_fields=["motivo_reprovacao", "updated_at"])
        return self._alterar_status(orcamento, StatusOrcamento.REPROVADO, TipoEventoOrcamento.REPROVACAO, motivo, usuario)

    @transaction.atomic
    def cancelar(self, *, orcamento_id, usuario, motivo=""):
        orcamento = self.repository.get_for_update(orcamento_id)
        if orcamento.status == StatusOrcamento.CONVERTIDO_OS:
            raise ValidationError("Orcamento convertido em OS nao pode ser cancelado sem regra especifica.")
        return self._alterar_status(orcamento, StatusOrcamento.CANCELADO, TipoEventoOrcamento.CANCELAMENTO, motivo or "Orcamento cancelado.", usuario)

    @transaction.atomic
    def expirar(self, *, orcamento_id, usuario=None):
        orcamento = self.repository.get_for_update(orcamento_id)
        if orcamento.status in {StatusOrcamento.APROVADO, StatusOrcamento.CONVERTIDO_OS, StatusOrcamento.CANCELADO}:
            raise ValidationError("Orcamento neste status nao pode expirar.")
        return self._alterar_status(orcamento, StatusOrcamento.EXPIRADO, TipoEventoOrcamento.EXPIRACAO, "Orcamento expirado.", usuario)

    @transaction.atomic
    def converter_em_os(self, *, orcamento_id, usuario):
        orcamento = self.repository.get_for_update(orcamento_id)
        if orcamento.status != StatusOrcamento.APROVADO:
            raise ValidationError("Apenas orcamento aprovado pode virar OS.")
        if orcamento.ordem_servico_id:
            raise ValidationError("Orcamento ja foi convertido em OS.")
        itens_os = [
            {"descricao": item.descricao, "quantidade": item.quantidade, "valor_unitario": item.valor_unitario, "observacao": item.observacao}
            for item in orcamento.itens_servico.all()
        ]
        if not itens_os:
            itens_os = [{"descricao": orcamento.titulo, "quantidade": Decimal("1.0000"), "valor_unitario": orcamento.valor_total, "observacao": "OS gerada a partir de orcamento."}]
        ordem = self.os_service.criar_os(
            usuario=usuario,
            cliente=orcamento.cliente,
            titulo=orcamento.titulo,
            descricao_servico=orcamento.descricao or orcamento.titulo,
            tipo_servico="Orcamento aprovado",
            valor_estimado=orcamento.valor_total,
            itens=itens_os,
        )
        orcamento.ordem_servico = ordem
        orcamento.status = StatusOrcamento.CONVERTIDO_OS
        orcamento.updated_by = usuario
        orcamento.save(update_fields=["ordem_servico", "status", "updated_by", "updated_at"])
        self.registrar_historico(orcamento, TipoEventoOrcamento.CONVERSAO_OS, "Orcamento convertido em OS.", usuario=usuario, status_novo=StatusOrcamento.CONVERTIDO_OS, dados={"ordem_servico": ordem.id})
        return orcamento

    @transaction.atomic
    def gerar_pdf(self, *, orcamento_id, usuario):
        orcamento = self.repository.get_active(orcamento_id)
        arquivo = self.pdf_generator.generate(orcamento)
        orcamento.pdf_gerado.save(arquivo.name, arquivo, save=True)
        self.registrar_historico(orcamento, TipoEventoOrcamento.PDF, "PDF do orcamento gerado.", usuario=usuario)
        return orcamento.pdf_gerado

    def recalcular_totais(self, orcamento):
        orcamento.refresh_from_db()
        valor_produtos = orcamento.itens_produto.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
        valor_servicos = orcamento.itens_servico.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
        custo_produtos = orcamento.itens_produto.aggregate(total=Sum("custo_total"))["total"] or Decimal("0.00")
        custo_servicos = orcamento.itens_servico.aggregate(total=Sum("custo_estimado"))["total"] or Decimal("0.00")
        total_bruto = valor_produtos + valor_servicos
        desconto = min(orcamento.valor_desconto, total_bruto)
        total = total_bruto - desconto
        custo_total = custo_produtos + custo_servicos
        margem = Decimal("0.00")
        if total > 0:
            margem = ((total - custo_total) / total * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        orcamento.valor_produtos = valor_produtos
        orcamento.valor_servicos = valor_servicos
        orcamento.valor_total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        orcamento.custo_total = custo_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        orcamento.margem_estimada = margem
        orcamento.save(update_fields=["valor_produtos", "valor_servicos", "valor_total", "custo_total", "margem_estimada", "updated_at"])
        return orcamento

    def registrar_historico(self, orcamento, tipo_evento, descricao, usuario=None, status_anterior="", status_novo="", dados=None):
        return HistoricoOrcamento.objects.create(
            orcamento=orcamento,
            tipo_evento=tipo_evento,
            descricao=descricao,
            status_anterior=status_anterior,
            status_novo=status_novo,
            usuario_responsavel=usuario if getattr(usuario, "is_authenticated", False) else None,
            dados_extras=dados or {},
        )

    def _criar_item_produto(self, orcamento, item):
        produto = item["produto"]
        if not produto.is_active:
            raise ValidationError("Produto precisa estar ativo.")
        quantidade = Decimal(str(item["quantidade"]))
        custo_unitario = Decimal(str(item.get("custo_unitario", produto.custo_medio)))
        valor_unitario = Decimal(str(item["valor_unitario"]))
        desconto = Decimal(str(item.get("desconto", 0)))
        self._validar_item(quantidade, custo_unitario, valor_unitario, desconto)
        total = (quantidade * valor_unitario - desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        custo_total = (quantidade * custo_unitario).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return ItemProdutoOrcamento.objects.create(
            orcamento=orcamento,
            produto=produto,
            descricao=item.get("descricao") or produto.nome,
            quantidade=quantidade,
            custo_unitario=custo_unitario,
            valor_unitario=valor_unitario,
            desconto=desconto,
            valor_total=max(total, Decimal("0.00")),
            custo_total=custo_total,
        )

    def _criar_item_servico(self, orcamento, item):
        quantidade = Decimal(str(item["quantidade"]))
        custo_estimado = Decimal(str(item.get("custo_estimado", 0)))
        valor_unitario = Decimal(str(item["valor_unitario"]))
        desconto = Decimal(str(item.get("desconto", 0)))
        self._validar_item(quantidade, custo_estimado, valor_unitario, desconto)
        total = (quantidade * valor_unitario - desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return ItemServicoOrcamento.objects.create(
            orcamento=orcamento,
            descricao=item["descricao"],
            quantidade=quantidade,
            custo_estimado=custo_estimado,
            valor_unitario=valor_unitario,
            desconto=desconto,
            valor_total=max(total, Decimal("0.00")),
            observacao=item.get("observacao", ""),
        )

    def _validar_item(self, quantidade, custo, valor_unitario, desconto):
        if quantidade <= 0:
            raise ValidationError("Quantidade deve ser maior que zero.")
        if custo < 0 or valor_unitario < 0 or desconto < 0:
            raise ValidationError("Valores monetarios nao podem ser negativos.")

    def _alterar_status(self, orcamento, novo_status, evento, descricao, usuario):
        status_anterior = orcamento.status
        orcamento.status = novo_status
        orcamento.updated_by = usuario
        orcamento.save(update_fields=["status", "updated_by", "updated_at"])
        self.registrar_historico(orcamento, evento, descricao, usuario=usuario, status_anterior=status_anterior, status_novo=novo_status)
        return orcamento

    def _bloquear_edicao(self, orcamento):
        if orcamento.status in self.status_bloqueados_edicao:
            raise ValidationError("Orcamento aprovado, convertido ou cancelado nao pode ser editado livremente.")

    def _possui_itens(self, orcamento):
        return orcamento.itens_produto.exists() or orcamento.itens_servico.exists()

    def _proximo_numero(self):
        hoje = timezone.localdate().strftime("%Y%m%d")
        sequencial = Orcamento.objects.filter(numero__startswith=f"ORC-{hoje}").count() + 1
        return f"ORC-{hoje}-{sequencial:04d}"
