from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone

from apps.estoque.services import EstoqueService
from apps.financeiro.services import FinanceiroService
from apps.ordens_servico.enums import StatusOS, TipoEventoOS, TipoHoraOS
from apps.ordens_servico.models import ApontamentoHorasOS, HistoricoOS, ItemServico, MaterialUtilizadoOS, OrdemServico
from apps.ordens_servico.repositories import ApontamentoOSRepository, MaterialOSRepository, OrdemServicoRepository


class OrdemServicoService:
    status_finalizados = {StatusOS.FINALIZADA, StatusOS.CANCELADA, StatusOS.FATURADA}

    def __init__(self, ordem_repository=None, material_repository=None, apontamento_repository=None, estoque_service=None, financeiro_service=None):
        self.ordem_repository = ordem_repository or OrdemServicoRepository()
        self.material_repository = material_repository or MaterialOSRepository()
        self.apontamento_repository = apontamento_repository or ApontamentoOSRepository()
        self.estoque_service = estoque_service or EstoqueService()
        self.financeiro_service = financeiro_service or FinanceiroService()

    @transaction.atomic
    def criar_os(self, *, usuario, itens=None, **dados):
        if not dados.get("cliente"):
            raise ValidationError("OS precisa ter cliente.")
        if not dados.get("numero"):
            dados["numero"] = self._proximo_numero()
        ordem = OrdemServico.objects.create(
            usuario_criador=usuario,
            created_by=usuario,
            updated_by=usuario,
            **dados,
        )
        for item in itens or []:
            self.adicionar_item_servico(ordem_id=ordem.id, usuario=usuario, **item)
        self.registrar_historico(ordem, TipoEventoOS.CRIACAO, "Ordem de servico criada.", usuario=usuario)
        self.recalcular_totais(ordem)
        return ordem

    @transaction.atomic
    def adicionar_item_servico(self, *, ordem_id, usuario, **dados):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        self._bloquear_finalizada(ordem)
        quantidade = Decimal(str(dados["quantidade"]))
        valor_unitario = Decimal(str(dados["valor_unitario"]))
        if quantidade <= 0:
            raise ValidationError("Quantidade do servico deve ser maior que zero.")
        if valor_unitario < 0:
            raise ValidationError("Valor unitario nao pode ser negativo.")
        item = ItemServico.objects.create(
            ordem_servico=ordem,
            descricao=dados["descricao"],
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=(quantidade * valor_unitario).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            observacao=dados.get("observacao", ""),
        )
        ordem.updated_by = usuario
        ordem.save(update_fields=["updated_by", "updated_at"])
        self.recalcular_totais(ordem)
        return item

    @transaction.atomic
    def enviar_aprovacao(self, *, ordem_id, usuario):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status not in {StatusOS.RASCUNHO, StatusOS.ABERTA}:
            raise ValidationError("Apenas OS em rascunho ou aberta pode ser enviada para aprovacao.")
        return self._alterar_status(ordem, StatusOS.EM_APROVACAO, TipoEventoOS.ENVIO_APROVACAO, "OS enviada para aprovacao.", usuario)

    @transaction.atomic
    def aprovar(self, *, ordem_id, usuario):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status != StatusOS.EM_APROVACAO:
            raise ValidationError("Apenas OS em aprovacao pode ser aprovada.")
        return self._alterar_status(ordem, StatusOS.APROVADA, TipoEventoOS.APROVACAO, "OS aprovada.", usuario)

    @transaction.atomic
    def iniciar(self, *, ordem_id, usuario):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status not in {StatusOS.APROVADA, StatusOS.PAUSADA}:
            raise ValidationError("Apenas OS aprovada ou pausada pode iniciar execucao.")
        if not ordem.data_inicio:
            ordem.data_inicio = timezone.now()
        ordem = self._alterar_status(ordem, StatusOS.EM_EXECUCAO, TipoEventoOS.INICIO, "Execucao iniciada.", usuario, save=False)
        ordem.save(update_fields=["status", "data_inicio", "updated_by", "updated_at"])
        return ordem

    @transaction.atomic
    def pausar(self, *, ordem_id, usuario):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status != StatusOS.EM_EXECUCAO:
            raise ValidationError("Apenas OS em execucao pode ser pausada.")
        return self._alterar_status(ordem, StatusOS.PAUSADA, TipoEventoOS.PAUSA, "OS pausada.", usuario)

    @transaction.atomic
    def retomar(self, *, ordem_id, usuario):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status != StatusOS.PAUSADA:
            raise ValidationError("Apenas OS pausada pode ser retomada.")
        return self._alterar_status(ordem, StatusOS.EM_EXECUCAO, TipoEventoOS.RETOMADA, "OS retomada.", usuario)

    @transaction.atomic
    def finalizar(self, *, ordem_id, usuario):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status not in {StatusOS.APROVADA, StatusOS.EM_EXECUCAO, StatusOS.PAUSADA}:
            raise ValidationError("OS precisa estar aprovada, em execucao ou pausada para finalizar.")
        ordem.data_finalizacao = timezone.now()
        ordem = self._alterar_status(ordem, StatusOS.FINALIZADA, TipoEventoOS.FINALIZACAO, "OS finalizada.", usuario, save=False)
        ordem.save(update_fields=["status", "data_finalizacao", "updated_by", "updated_at"])
        return ordem

    @transaction.atomic
    def cancelar(self, *, ordem_id, usuario, motivo=""):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status == StatusOS.FATURADA:
            raise ValidationError("OS faturada nao pode ser cancelada sem regra especifica de estorno.")
        if ordem.status == StatusOS.CANCELADA:
            raise ValidationError("OS ja esta cancelada.")
        return self._alterar_status(ordem, StatusOS.CANCELADA, TipoEventoOS.CANCELAMENTO, motivo or "OS cancelada.", usuario)

    @transaction.atomic
    def faturar(self, *, ordem_id, usuario, data_vencimento=None, categoria=None, centro_custo=None):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        if ordem.status == StatusOS.CANCELADA:
            raise ValidationError("OS cancelada nao pode gerar financeiro.")
        if ordem.conta_receber_id:
            raise ValidationError("OS ja possui faturamento vinculado.")
        if ordem.status not in {StatusOS.FINALIZADA, StatusOS.APROVADA}:
            raise ValidationError("OS precisa estar aprovada ou finalizada para faturar.")
        categoria = categoria or ordem.categoria_financeira
        centro_custo = centro_custo or ordem.centro_custo
        data_vencimento = data_vencimento or timezone.localdate()
        if not categoria or not centro_custo:
            raise ValidationError("Categoria financeira e centro de custo sao obrigatorios para faturar OS.")
        valor = ordem.valor_final or ordem.valor_estimado
        if valor <= 0:
            raise ValidationError("OS sem valor nao pode ser faturada.")
        conta = self.financeiro_service.criar_conta_receber(
            usuario=usuario,
            cliente=ordem.cliente,
            descricao=f"OS {ordem.numero} - {ordem.titulo}",
            categoria=categoria,
            centro_custo=centro_custo,
            valor_original=valor,
            data_emissao=timezone.localdate(),
            data_vencimento=data_vencimento,
        )
        ordem.conta_receber = conta
        ordem.status = StatusOS.FATURADA
        ordem.updated_by = usuario
        ordem.save(update_fields=["conta_receber", "status", "updated_by", "updated_at"])
        self.registrar_historico(ordem, TipoEventoOS.FATURAMENTO, "OS faturada e conta a receber gerada.", usuario=usuario, dados={"conta_receber": conta.id})
        return ordem

    @transaction.atomic
    def adicionar_material(self, *, ordem_id, produto, quantidade, usuario, custo_unitario=None):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        self._bloquear_finalizada(ordem, permite_finalizada=False)
        if ordem.status == StatusOS.CANCELADA:
            raise ValidationError("OS cancelada nao pode receber material.")
        if not produto.is_active:
            raise ValidationError("Produto precisa estar ativo.")
        quantidade = Decimal(str(quantidade))
        if quantidade <= 0:
            raise ValidationError("Quantidade de material deve ser maior que zero.")
        custo_unitario = Decimal(str(custo_unitario if custo_unitario is not None else produto.custo_medio))
        if custo_unitario < 0:
            raise ValidationError("Custo unitario nao pode ser negativo.")
        self.estoque_service.registrar_saida(produto_id=produto.id, quantidade=quantidade, usuario=usuario, observacao=f"OS {ordem.numero}")
        material = MaterialUtilizadoOS.objects.create(
            ordem_servico=ordem,
            produto=produto,
            quantidade=quantidade,
            custo_unitario=custo_unitario,
            custo_total=(quantidade * custo_unitario).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            usuario_responsavel=usuario,
        )
        self.recalcular_totais(ordem)
        self.registrar_historico(ordem, TipoEventoOS.MATERIAL, f"Material utilizado: {produto.nome}", usuario=usuario, dados={"produto": produto.id, "quantidade": str(quantidade)})
        return material

    @transaction.atomic
    def remover_material(self, *, material_id, usuario):
        material = self.material_repository.get_for_update(material_id)
        ordem = material.ordem_servico
        self._bloquear_finalizada(ordem)
        self.estoque_service.registrar_entrada(produto_id=material.produto_id, quantidade=material.quantidade, usuario=usuario, observacao=f"Estorno OS {ordem.numero}")
        self.registrar_historico(ordem, TipoEventoOS.ESTORNO_MATERIAL, f"Material estornado: {material.produto.nome}", usuario=usuario, dados={"material": material.id})
        material.delete()
        self.recalcular_totais(ordem)

    @transaction.atomic
    def registrar_apontamento(self, *, ordem_id, colaborador, data, hora_inicio, hora_fim, usuario, tipo_hora=TipoHoraOS.NORMAL, custo_hora=Decimal("0.00"), observacao=""):
        ordem = self.ordem_repository.get_for_update(ordem_id)
        self._bloquear_finalizada(ordem, permite_finalizada=False)
        if ordem.status == StatusOS.CANCELADA:
            raise ValidationError("OS cancelada nao pode receber apontamento.")
        total_horas = self._calcular_total_horas(data, hora_inicio, hora_fim)
        self._validar_sobreposicao(colaborador=colaborador, data=data, hora_inicio=hora_inicio, hora_fim=hora_fim)
        custo_total = self._calcular_custo_horas(total_horas, Decimal(str(custo_hora)), tipo_hora)
        apontamento = ApontamentoHorasOS.objects.create(
            ordem_servico=ordem,
            colaborador=colaborador,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            total_horas=total_horas,
            tipo_hora=tipo_hora,
            custo_hora=custo_hora,
            custo_total=custo_total,
            observacao=observacao,
        )
        self.recalcular_totais(ordem)
        self.registrar_historico(ordem, TipoEventoOS.APONTAMENTO, "Apontamento de horas registrado.", usuario=usuario, dados={"apontamento": apontamento.id, "horas": str(total_horas)})
        return apontamento

    @transaction.atomic
    def atualizar_apontamento(self, *, apontamento_id, usuario, **dados):
        apontamento = self.apontamento_repository.get_for_update(apontamento_id)
        ordem = apontamento.ordem_servico
        self._bloquear_finalizada(ordem)
        data = dados.get("data", apontamento.data)
        hora_inicio = dados.get("hora_inicio", apontamento.hora_inicio)
        hora_fim = dados.get("hora_fim", apontamento.hora_fim)
        colaborador = dados.get("colaborador", apontamento.colaborador)
        tipo_hora = dados.get("tipo_hora", apontamento.tipo_hora)
        custo_hora = Decimal(str(dados.get("custo_hora", apontamento.custo_hora)))
        total_horas = self._calcular_total_horas(data, hora_inicio, hora_fim)
        self._validar_sobreposicao(colaborador=colaborador, data=data, hora_inicio=hora_inicio, hora_fim=hora_fim, exclude_id=apontamento.id)
        apontamento.colaborador = colaborador
        apontamento.data = data
        apontamento.hora_inicio = hora_inicio
        apontamento.hora_fim = hora_fim
        apontamento.tipo_hora = tipo_hora
        apontamento.custo_hora = custo_hora
        apontamento.total_horas = total_horas
        apontamento.custo_total = self._calcular_custo_horas(total_horas, custo_hora, tipo_hora)
        apontamento.observacao = dados.get("observacao", apontamento.observacao)
        apontamento.save()
        self.recalcular_totais(ordem)
        self.registrar_historico(ordem, TipoEventoOS.APONTAMENTO, "Apontamento de horas atualizado.", usuario=usuario, dados={"apontamento": apontamento.id})
        return apontamento

    @transaction.atomic
    def remover_apontamento(self, *, apontamento_id, usuario):
        apontamento = self.apontamento_repository.get_for_update(apontamento_id)
        ordem = apontamento.ordem_servico
        self._bloquear_finalizada(ordem)
        self.registrar_historico(ordem, TipoEventoOS.APONTAMENTO, "Apontamento de horas removido.", usuario=usuario, dados={"apontamento": apontamento.id})
        apontamento.delete()
        self.recalcular_totais(ordem)

    def recalcular_totais(self, ordem):
        ordem.refresh_from_db()
        valor_itens = ordem.itens.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
        custo_materiais = ordem.materiais.aggregate(total=Sum("custo_total"))["total"] or Decimal("0.00")
        custo_mao_obra = ordem.apontamentos.aggregate(total=Sum("custo_total"))["total"] or Decimal("0.00")
        ordem.valor_final = valor_itens if valor_itens > 0 else ordem.valor_estimado
        ordem.custo_materiais = custo_materiais
        ordem.custo_mao_obra = custo_mao_obra
        ordem.custo_total = custo_materiais + custo_mao_obra
        ordem.save(update_fields=["valor_final", "custo_materiais", "custo_mao_obra", "custo_total", "updated_at"])
        return ordem

    def registrar_historico(self, ordem, tipo_evento, descricao, usuario=None, status_anterior="", status_novo="", dados=None):
        return HistoricoOS.objects.create(
            ordem_servico=ordem,
            tipo_evento=tipo_evento,
            descricao=descricao,
            status_anterior=status_anterior,
            status_novo=status_novo,
            usuario_responsavel=usuario if getattr(usuario, "is_authenticated", False) else None,
            dados_extras=dados or {},
        )

    def _alterar_status(self, ordem, novo_status, evento, descricao, usuario, save=True):
        status_anterior = ordem.status
        ordem.status = novo_status
        ordem.updated_by = usuario
        if save:
            ordem.save(update_fields=["status", "updated_by", "updated_at"])
        self.registrar_historico(ordem, evento, descricao, usuario=usuario, status_anterior=status_anterior, status_novo=novo_status)
        return ordem

    def _bloquear_finalizada(self, ordem, permite_finalizada=False):
        bloqueados = {StatusOS.CANCELADA, StatusOS.FATURADA}
        if not permite_finalizada:
            bloqueados.add(StatusOS.FINALIZADA)
        if ordem.status in bloqueados:
            raise ValidationError("OS neste status nao pode ser alterada livremente.")

    def _calcular_total_horas(self, data, hora_inicio, hora_fim):
        inicio = datetime.combine(data, hora_inicio)
        fim = datetime.combine(data, hora_fim)
        if fim <= inicio:
            raise ValidationError("Hora fim deve ser maior que hora inicio.")
        horas = Decimal(str((fim - inicio).total_seconds())) / Decimal("3600")
        return horas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _validar_sobreposicao(self, *, colaborador, data, hora_inicio, hora_fim, exclude_id=None):
        queryset = ApontamentoHorasOS.objects.filter(colaborador=colaborador, data=data).filter(Q(hora_inicio__lt=hora_fim) & Q(hora_fim__gt=hora_inicio))
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        if queryset.exists():
            raise ValidationError("Existe sobreposicao de horario para este colaborador.")

    def _calcular_custo_horas(self, total_horas, custo_hora, tipo_hora):
        multiplicador = Decimal("1.00")
        if tipo_hora == TipoHoraOS.EXTRA_50:
            multiplicador = Decimal("1.50")
        elif tipo_hora == TipoHoraOS.EXTRA_100:
            multiplicador = Decimal("2.00")
        return (total_horas * custo_hora * multiplicador).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _proximo_numero(self):
        hoje = timezone.localdate().strftime("%Y%m%d")
        sequencial = OrdemServico.objects.filter(numero__startswith=f"OS-{hoje}").count() + 1
        return f"OS-{hoje}-{sequencial:04d}"
