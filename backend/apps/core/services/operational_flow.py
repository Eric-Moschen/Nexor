from django.core.exceptions import ValidationError
from django.db import transaction

from apps.clientes.enums import StatusRelacionamento
from apps.core.audit.services import AuditService
from apps.core.events.base import (
    InternalEvent,
    MATERIAL_OS_UTILIZADO,
    NFE_AUTORIZADA,
    ORCAMENTO_APROVADO,
    OS_FATURADA,
    OS_FINALIZADA,
    PEDIDO_RECEBIDO,
)
from apps.core.events.dispatcher import EventDispatcher
from apps.core.models import AuditLog


class ERPIntegrationService:
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or EventDispatcher()

    @transaction.atomic
    def comercial_para_os(self, *, orcamento_id, usuario):
        from apps.orcamentos.services import OrcamentoService

        service = OrcamentoService()
        orcamento = service.aprovar(orcamento_id=orcamento_id, usuario=usuario)
        self._validar_cliente(orcamento.cliente)
        orcamento = service.converter_em_os(orcamento_id=orcamento.id, usuario=usuario)
        self.dispatcher.publish(InternalEvent(
            name=ORCAMENTO_APROVADO,
            module="orcamentos",
            aggregate_type="orcamentos.Orcamento",
            aggregate_id=str(orcamento.id),
            payload={
                "title": "Orcamento aprovado e convertido",
                "message": f"Orcamento {orcamento.numero} convertido na OS {orcamento.ordem_servico.numero}.",
                "ordem_servico": orcamento.ordem_servico_id,
            },
            user=usuario,
        ))
        AuditService.register(user=usuario, action=AuditLog.Action.APPROVE, module="orcamentos", record=orcamento)
        return orcamento

    @transaction.atomic
    def finalizar_os(self, *, ordem_id, usuario):
        from apps.ordens_servico.services import OrdemServicoService

        ordem = OrdemServicoService().finalizar(ordem_id=ordem_id, usuario=usuario)
        self.dispatcher.publish(InternalEvent(
            name=OS_FINALIZADA,
            module="ordens_servico",
            aggregate_type="ordens_servico.OrdemServico",
            aggregate_id=str(ordem.id),
            payload={"title": "OS finalizada", "message": f"OS {ordem.numero} finalizada para faturamento."},
            user=usuario,
        ))
        return ordem

    @transaction.atomic
    def faturar_os(self, *, ordem_id, usuario, data_vencimento=None, categoria=None, centro_custo=None):
        from apps.ordens_servico.services import OrdemServicoService

        ordem = OrdemServicoService().faturar(
            ordem_id=ordem_id,
            usuario=usuario,
            data_vencimento=data_vencimento,
            categoria=categoria,
            centro_custo=centro_custo,
        )
        self.dispatcher.publish(InternalEvent(
            name=OS_FATURADA,
            module="financeiro",
            aggregate_type="ordens_servico.OrdemServico",
            aggregate_id=str(ordem.id),
            payload={"title": "OS faturada", "message": f"Conta a receber gerada para a OS {ordem.numero}.", "conta_receber": ordem.conta_receber_id},
            user=usuario,
        ))
        return ordem

    @transaction.atomic
    def registrar_material_os(self, *, ordem_id, produto, quantidade, usuario, custo_unitario=None):
        from apps.ordens_servico.services import OrdemServicoService

        material = OrdemServicoService().adicionar_material(
            ordem_id=ordem_id,
            produto=produto,
            quantidade=quantidade,
            usuario=usuario,
            custo_unitario=custo_unitario,
        )
        self.dispatcher.publish(InternalEvent(
            name=MATERIAL_OS_UTILIZADO,
            module="estoque",
            aggregate_type="ordens_servico.MaterialUtilizadoOS",
            aggregate_id=str(material.id),
            payload={"produto": material.produto_id, "quantidade": str(material.quantidade), "ordem_servico": material.ordem_servico_id},
            user=usuario,
        ))
        return material

    @transaction.atomic
    def receber_pedido_e_gerar_financeiro(self, *, pedido_id, usuario, categoria=None, centro_custo=None, data_vencimento=None, itens=None):
        from apps.compras.services import ComprasService
        from apps.financeiro.services import FinanceiroService

        pedido = ComprasService().registrar_recebimento_parcial(pedido_id=pedido_id, usuario=usuario, itens=itens, observacao="Recebimento integrado") if itens else ComprasService().registrar_recebimento_total(pedido_id=pedido_id, usuario=usuario, observacao="Recebimento integrado")
        conta = None
        if categoria and centro_custo and data_vencimento:
            conta = FinanceiroService().gerar_conta_pagar_de_pedido(
                pedido_id=pedido.id,
                categoria=categoria,
                centro_custo=centro_custo,
                data_vencimento=data_vencimento,
                usuario=usuario,
            )
        self.dispatcher.publish(InternalEvent(
            name=PEDIDO_RECEBIDO,
            module="compras",
            aggregate_type="compras.PedidoCompra",
            aggregate_id=str(pedido.id),
            payload={"title": "Pedido recebido", "message": f"Pedido {pedido.numero} integrado ao estoque.", "conta_pagar": getattr(conta, "id", None)},
            user=usuario,
        ))
        return pedido

    @transaction.atomic
    def nfe_autorizada_para_financeiro(self, *, nota, usuario):
        if getattr(nota, "status", "") != "autorizada":
            raise ValidationError("NFe precisa estar autorizada para integrar financeiro.")
        self.dispatcher.publish(InternalEvent(
            name=NFE_AUTORIZADA,
            module="fiscal",
            aggregate_type="fiscal.NotaFiscal",
            aggregate_id=str(nota.id),
            payload={"title": "NFe autorizada", "message": f"NFe {nota.numero}/{nota.serie} autorizada e integrada.", "valor_total": str(nota.valor_total)},
            user=usuario,
        ))
        return nota

    def _validar_cliente(self, cliente):
        if not cliente.is_active or cliente.status == StatusRelacionamento.BLOQUEADO:
            raise ValidationError("Cliente bloqueado ou inativo nao pode seguir no fluxo operacional.")
