from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.compras.models import (
    HistoricoAprovacaoCompra,
    ItemPedidoCompra,
    ItemSolicitacaoCompra,
    PedidoCompra,
    SolicitacaoCompra,
)
from apps.compras.repositories import PedidoCompraRepository, SolicitacaoCompraRepository
from apps.estoque.services import EstoqueService
from apps.fornecedores.models import Fornecedor


class ComprasService:
    def __init__(self, solicitacao_repository=None, pedido_repository=None, estoque_service=None):
        self.solicitacao_repository = solicitacao_repository or SolicitacaoCompraRepository()
        self.pedido_repository = pedido_repository or PedidoCompraRepository()
        self.estoque_service = estoque_service or EstoqueService()

    @transaction.atomic
    def criar_solicitacao(self, *, solicitante, centro_custo, justificativa, prioridade, observacoes="", itens=None):
        itens = itens or []
        if not itens:
            raise ValidationError("A solicitacao precisa ter pelo menos um item.")

        solicitacao = SolicitacaoCompra.objects.create(
            numero=self._proximo_numero("SC", SolicitacaoCompra),
            solicitante=solicitante,
            centro_custo=centro_custo,
            justificativa=justificativa,
            prioridade=prioridade,
            observacoes=observacoes,
            created_by=solicitante,
            updated_by=solicitante,
        )

        for item in itens:
            self._criar_item_solicitacao(solicitacao, item)

        return solicitacao

    @transaction.atomic
    def enviar_para_aprovacao(self, *, solicitacao_id, usuario):
        solicitacao = self.solicitacao_repository.get_for_update(solicitacao_id)
        if solicitacao.status != SolicitacaoCompra.Status.RASCUNHO:
            raise ValidationError("Apenas solicitacoes em rascunho podem ser enviadas para aprovacao.")
        if not solicitacao.itens.exists():
            raise ValidationError("A solicitacao precisa ter pelo menos um item.")
        return self._alterar_status(
            solicitacao=solicitacao,
            novo_status=SolicitacaoCompra.Status.PENDENTE,
            usuario=usuario,
            acao=HistoricoAprovacaoCompra.Acao.ENVIAR,
        )

    @transaction.atomic
    def aprovar_solicitacao(self, *, solicitacao_id, usuario):
        solicitacao = self.solicitacao_repository.get_for_update(solicitacao_id)
        if solicitacao.status != SolicitacaoCompra.Status.PENDENTE:
            raise ValidationError("Apenas solicitacoes pendentes podem ser aprovadas.")
        solicitacao.data_aprovacao = timezone.now()
        solicitacao.aprovador = usuario
        return self._alterar_status(
            solicitacao=solicitacao,
            novo_status=SolicitacaoCompra.Status.APROVADA,
            usuario=usuario,
            acao=HistoricoAprovacaoCompra.Acao.APROVAR,
        )

    @transaction.atomic
    def reprovar_solicitacao(self, *, solicitacao_id, usuario, motivo):
        if not motivo or not motivo.strip():
            raise ValidationError("Reprovacao exige motivo.")
        solicitacao = self.solicitacao_repository.get_for_update(solicitacao_id)
        if solicitacao.status != SolicitacaoCompra.Status.PENDENTE:
            raise ValidationError("Apenas solicitacoes pendentes podem ser reprovadas.")
        solicitacao.data_aprovacao = timezone.now()
        solicitacao.aprovador = usuario
        return self._alterar_status(
            solicitacao=solicitacao,
            novo_status=SolicitacaoCompra.Status.REPROVADA,
            usuario=usuario,
            acao=HistoricoAprovacaoCompra.Acao.REPROVAR,
            motivo=motivo,
        )

    @transaction.atomic
    def cancelar_solicitacao(self, *, solicitacao_id, usuario, motivo=""):
        solicitacao = self.solicitacao_repository.get_for_update(solicitacao_id)
        if solicitacao.status in {SolicitacaoCompra.Status.CONVERTIDA, SolicitacaoCompra.Status.CANCELADA}:
            raise ValidationError("Solicitacao nao pode ser cancelada neste status.")
        return self._alterar_status(
            solicitacao=solicitacao,
            novo_status=SolicitacaoCompra.Status.CANCELADA,
            usuario=usuario,
            acao=HistoricoAprovacaoCompra.Acao.CANCELAR,
            motivo=motivo,
        )

    @transaction.atomic
    def converter_solicitacao_em_pedido(self, *, solicitacao_id, fornecedor_id, usuario, previsao_entrega=None, observacoes=""):
        solicitacao = self.solicitacao_repository.get_for_update(solicitacao_id)
        if solicitacao.status != SolicitacaoCompra.Status.APROVADA:
            raise ValidationError("Apenas solicitacao aprovada pode virar pedido.")
        fornecedor = Fornecedor.objects.get(id=fornecedor_id, is_active=True)
        pedido = PedidoCompra.objects.create(
            numero=self._proximo_numero("PC", PedidoCompra),
            solicitacao_origem=solicitacao,
            fornecedor=fornecedor,
            previsao_entrega=previsao_entrega,
            observacoes=observacoes,
            created_by=usuario,
            updated_by=usuario,
        )
        for item in solicitacao.itens.all():
            ItemPedidoCompra.objects.create(
                pedido=pedido,
                produto=item.produto,
                descricao=item.descricao_livre or item.produto.nome,
                quantidade=item.quantidade_solicitada,
                unidade_medida=item.unidade_medida,
                valor_unitario=Decimal("0.00"),
                valor_total=Decimal("0.00"),
            )
            item.status = ItemSolicitacaoCompra.Status.CONVERTIDO
            item.save(update_fields=["status", "updated_at"])
        self._recalcular_valor_total(pedido)
        self._alterar_status(
            solicitacao=solicitacao,
            novo_status=SolicitacaoCompra.Status.CONVERTIDA,
            usuario=usuario,
            acao=HistoricoAprovacaoCompra.Acao.CONVERTER,
        )
        return pedido

    @transaction.atomic
    def criar_pedido(self, *, fornecedor, usuario, itens, solicitacao_origem=None, previsao_entrega=None, observacoes=""):
        if not fornecedor:
            raise ValidationError("Fornecedor obrigatorio para pedido.")
        if not itens:
            raise ValidationError("O pedido precisa ter pelo menos um item.")
        pedido = PedidoCompra.objects.create(
            numero=self._proximo_numero("PC", PedidoCompra),
            solicitacao_origem=solicitacao_origem,
            fornecedor=fornecedor,
            previsao_entrega=previsao_entrega,
            observacoes=observacoes,
            created_by=usuario,
            updated_by=usuario,
        )
        for item in itens:
            quantidade = Decimal(str(item["quantidade"]))
            valor_unitario = Decimal(str(item["valor_unitario"]))
            if quantidade <= 0:
                raise ValidationError("Quantidade deve ser maior que zero.")
            if valor_unitario < 0:
                raise ValidationError("Valor unitario nao pode ser negativo.")
            ItemPedidoCompra.objects.create(
                pedido=pedido,
                produto=item.get("produto"),
                descricao=item["descricao"],
                quantidade=quantidade,
                unidade_medida=item["unidade_medida"],
                valor_unitario=valor_unitario,
                valor_total=quantidade * valor_unitario,
            )
        self._recalcular_valor_total(pedido)
        return pedido

    @transaction.atomic
    def registrar_recebimento_parcial(self, *, pedido_id, usuario, itens, observacao=""):
        pedido = self.pedido_repository.get_for_update(pedido_id)
        if pedido.status == PedidoCompra.Status.CANCELADO:
            raise ValidationError("Pedido cancelado nao pode receber itens.")
        for recebimento in itens:
            item = pedido.itens.select_for_update().get(id=recebimento["item"])
            quantidade = Decimal(str(recebimento["quantidade"]))
            nova_quantidade = item.quantidade_recebida + quantidade
            if nova_quantidade > item.quantidade:
                raise ValidationError("Quantidade recebida nao pode exceder a quantidade comprada.")
            item.quantidade_recebida = nova_quantidade
            item.save(update_fields=["quantidade_recebida", "updated_at"])
            if item.produto:
                self.estoque_service.registrar_entrada(
                    produto_id=item.produto_id,
                    quantidade=quantidade,
                    usuario=usuario,
                    observacao=observacao or f"Recebimento do pedido {pedido.numero}",
                )
        self._atualizar_status_recebimento(pedido)
        from apps.core.events.base import InternalEvent, PEDIDO_RECEBIDO
        from apps.core.events.dispatcher import EventDispatcher

        EventDispatcher().publish(InternalEvent(
            name=PEDIDO_RECEBIDO,
            module="compras",
            aggregate_type="compras.PedidoCompra",
            aggregate_id=str(pedido.id),
            payload={"title": "Pedido recebido", "message": f"Pedido {pedido.numero} recebido e integrado ao estoque.", "status": pedido.status},
            user=usuario,
        ))
        return pedido

    @transaction.atomic
    def registrar_recebimento_total(self, *, pedido_id, usuario, observacao=""):
        pedido = self.pedido_repository.get_for_update(pedido_id)
        itens = []
        for item in pedido.itens.all():
            restante = item.quantidade - item.quantidade_recebida
            if restante > 0:
                itens.append({"item": item.id, "quantidade": restante})
        if not itens:
            raise ValidationError("Pedido ja esta totalmente recebido.")
        return self.registrar_recebimento_parcial(pedido_id=pedido.id, usuario=usuario, itens=itens, observacao=observacao)

    @transaction.atomic
    def cancelar_pedido(self, *, pedido_id, usuario):
        pedido = self.pedido_repository.get_for_update(pedido_id)
        if pedido.status == PedidoCompra.Status.RECEBIDO:
            raise ValidationError("Pedido recebido nao pode ser cancelado.")
        pedido.status = PedidoCompra.Status.CANCELADO
        pedido.updated_by = usuario
        pedido.save(update_fields=["status", "updated_by", "updated_at"])
        return pedido

    def _criar_item_solicitacao(self, solicitacao, item):
        if not item.get("produto") and not item.get("descricao_livre", "").strip():
            raise ValidationError("Informe produto ou descricao livre.")
        quantidade = Decimal(str(item["quantidade_solicitada"]))
        if quantidade <= 0:
            raise ValidationError("Quantidade deve ser maior que zero.")
        return ItemSolicitacaoCompra.objects.create(solicitacao=solicitacao, **item)

    def _alterar_status(self, *, solicitacao, novo_status, usuario, acao, motivo=""):
        status_anterior = solicitacao.status
        solicitacao.status = novo_status
        solicitacao.updated_by = usuario
        solicitacao.save(update_fields=["status", "data_aprovacao", "aprovador", "updated_by", "updated_at"])
        HistoricoAprovacaoCompra.objects.create(
            solicitacao=solicitacao,
            usuario=usuario,
            acao=acao,
            status_anterior=status_anterior,
            status_posterior=novo_status,
            motivo=motivo,
        )
        return solicitacao

    def _recalcular_valor_total(self, pedido):
        total = sum((item.valor_total for item in pedido.itens.all()), Decimal("0.00"))
        pedido.valor_total = total
        pedido.save(update_fields=["valor_total", "updated_at"])

    def _atualizar_status_recebimento(self, pedido):
        itens = list(pedido.itens.all())
        if all(item.quantidade_recebida >= item.quantidade for item in itens):
            pedido.status = PedidoCompra.Status.RECEBIDO
        elif any(item.quantidade_recebida > 0 for item in itens):
            pedido.status = PedidoCompra.Status.PARCIAL
        pedido.save(update_fields=["status", "updated_at"])

    def _proximo_numero(self, prefixo, model):
        hoje = timezone.localdate().strftime("%Y%m%d")
        sequencial = model.objects.filter(numero__startswith=f"{prefixo}-{hoje}").count() + 1
        return f"{prefixo}-{hoje}-{sequencial:04d}"
