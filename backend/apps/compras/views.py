from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.compras.models import PedidoCompra, SolicitacaoCompra
from apps.compras.permissions import CanApproveCompras, CanManageCompras, CanReceiveCompras, CanViewCompras
from apps.compras.serializers import (
    ConverterPedidoSerializer,
    PedidoCompraSerializer,
    RecebimentoParcialSerializer,
    ReprovacaoSerializer,
    SolicitacaoCompraSerializer,
)
from apps.compras.selectors import listar_pedidos, listar_solicitacoes
from apps.compras.services import ComprasService
from apps.core.responses import error_response, success_response


class SolicitacaoCompraViewSet(ModelViewSet):
    serializer_class = SolicitacaoCompraSerializer
    permission_classes = [IsAuthenticated, CanViewCompras]
    filterset_fields = ("status", "prioridade", "centro_custo")
    search_fields = ("numero", "centro_custo", "justificativa")
    ordering_fields = ("data_solicitacao", "prioridade", "status")

    def get_queryset(self):
        return listar_solicitacoes()

    def get_permissions(self):
        if self.action in {"aprovar", "reprovar"}:
            return [IsAuthenticated(), CanApproveCompras()]
        if self.action in {"create", "update", "partial_update", "destroy", "enviar_aprovacao", "cancelar", "converter_pedido"}:
            return [IsAuthenticated(), CanManageCompras()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            solicitacao = ComprasService().criar_solicitacao(solicitante=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Solicitacao nao pode ser criada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(solicitacao).data, "Solicitacao criada com sucesso.", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != SolicitacaoCompra.Status.RASCUNHO:
            return error_response("Solicitacao aprovada ou em fluxo nao pode ser editada livremente.", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop("partial", False))
        serializer.is_valid(raise_exception=True)
        itens = serializer.validated_data.pop("itens", None)
        for field, value in serializer.validated_data.items():
            setattr(instance, field, value)
        instance.updated_by = request.user
        instance.save()
        if itens is not None:
            instance.itens.all().delete()
            for item in itens:
                instance.itens.create(**item)
        return success_response(self.get_serializer(instance).data, "Solicitacao atualizada com sucesso.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            ComprasService().cancelar_solicitacao(solicitacao_id=instance.id, usuario=request.user)
        except ValidationError as exc:
            return error_response("Solicitacao nao pode ser cancelada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(None, "Solicitacao cancelada com sucesso.", status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="enviar-aprovacao")
    def enviar_aprovacao(self, request, pk=None):
        return self._executar_acao(lambda: ComprasService().enviar_para_aprovacao(solicitacao_id=pk, usuario=request.user), "Solicitacao enviada para aprovacao.")

    @action(detail=True, methods=["post"], url_path="aprovar")
    def aprovar(self, request, pk=None):
        return self._executar_acao(lambda: ComprasService().aprovar_solicitacao(solicitacao_id=pk, usuario=request.user), "Solicitacao aprovada com sucesso.")

    @action(detail=True, methods=["post"], url_path="reprovar")
    def reprovar(self, request, pk=None):
        serializer = ReprovacaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._executar_acao(
            lambda: ComprasService().reprovar_solicitacao(solicitacao_id=pk, usuario=request.user, motivo=serializer.validated_data["motivo"]),
            "Solicitacao reprovada com sucesso.",
        )

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        return self._executar_acao(lambda: ComprasService().cancelar_solicitacao(solicitacao_id=pk, usuario=request.user), "Solicitacao cancelada com sucesso.")

    @action(detail=True, methods=["post"], url_path="converter-pedido")
    def converter_pedido(self, request, pk=None):
        serializer = ConverterPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pedido = ComprasService().converter_solicitacao_em_pedido(solicitacao_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Solicitacao nao pode ser convertida em pedido.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(PedidoCompraSerializer(pedido).data, "Pedido criado com sucesso.", status=status.HTTP_201_CREATED)

    def _executar_acao(self, func, message):
        try:
            solicitacao = func()
        except ValidationError as exc:
            return error_response("Acao nao permitida.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(solicitacao).data, message)


class PedidoCompraViewSet(ModelViewSet):
    serializer_class = PedidoCompraSerializer
    permission_classes = [IsAuthenticated, CanViewCompras]
    filterset_fields = ("status", "fornecedor")
    search_fields = ("numero", "fornecedor__razao_social", "fornecedor__documento")
    ordering_fields = ("data_pedido", "previsao_entrega", "valor_total", "status")

    def get_queryset(self):
        return listar_pedidos()

    def get_permissions(self):
        if self.action in {"recebimento_parcial", "recebimento_total"}:
            return [IsAuthenticated(), CanReceiveCompras()]
        if self.action in {"create", "update", "partial_update", "destroy", "cancelar"}:
            return [IsAuthenticated(), CanManageCompras()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pedido = ComprasService().criar_pedido(usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Pedido nao pode ser criado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(pedido).data, "Pedido criado com sucesso.", status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        return self.cancelar(request, pk=self.get_object().id)

    @action(detail=True, methods=["post"], url_path="recebimento-parcial")
    def recebimento_parcial(self, request, pk=None):
        serializer = RecebimentoParcialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pedido = ComprasService().registrar_recebimento_parcial(pedido_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Recebimento nao pode ser registrado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(pedido).data, "Recebimento parcial registrado com sucesso.")

    @action(detail=True, methods=["post"], url_path="recebimento-total")
    def recebimento_total(self, request, pk=None):
        try:
            pedido = ComprasService().registrar_recebimento_total(pedido_id=pk, usuario=request.user, observacao=request.data.get("observacao", ""))
        except ValidationError as exc:
            return error_response("Recebimento nao pode ser registrado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(pedido).data, "Recebimento total registrado com sucesso.")

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        try:
            pedido = ComprasService().cancelar_pedido(pedido_id=pk, usuario=request.user)
        except ValidationError as exc:
            return error_response("Pedido nao pode ser cancelado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(pedido).data, "Pedido cancelado com sucesso.")
