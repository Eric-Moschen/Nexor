from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.responses import error_response, success_response
from apps.estoque.models import MovimentacaoEstoque
from apps.estoque.permissions import CanManageEstoque
from apps.estoque.serializers import (
    CategoriaProdutoSerializer,
    EstoqueMovimentacaoInputSerializer,
    MovimentacaoEstoqueSerializer,
    ProdutoSerializer,
    UnidadeMedidaSerializer,
)
from apps.estoque.selectors import listar_categorias, listar_movimentacoes, listar_produtos, listar_unidades_medida
from apps.estoque.services import EstoqueService


class StandardResponseMixin:
    success_create_message = "Registro criado com sucesso."
    success_update_message = "Registro atualizado com sucesso."
    success_delete_message = "Registro removido com sucesso."

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(serializer.data, self.success_create_message, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(serializer.data, self.success_update_message)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return success_response(None, self.success_delete_message, status=status.HTTP_204_NO_CONTENT)


class CategoriaProdutoViewSet(StandardResponseMixin, ModelViewSet):
    serializer_class = CategoriaProdutoSerializer
    permission_classes = [IsAuthenticated, CanManageEstoque]

    def get_queryset(self):
        return listar_categorias()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class UnidadeMedidaViewSet(StandardResponseMixin, ModelViewSet):
    serializer_class = UnidadeMedidaSerializer
    permission_classes = [IsAuthenticated, CanManageEstoque]

    def get_queryset(self):
        return listar_unidades_medida()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProdutoViewSet(StandardResponseMixin, ModelViewSet):
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated, CanManageEstoque]
    filterset_fields = ("categoria", "unidade_medida", "is_active")
    search_fields = ("codigo_interno", "sku", "codigo_barras", "nome", "marca")
    ordering_fields = ("nome", "sku", "estoque_atual", "created_at")
    success_create_message = "Produto criado com sucesso."
    success_update_message = "Produto atualizado com sucesso."
    success_delete_message = "Produto inativado com sucesso."

    def get_queryset(self):
        return listar_produtos()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MovimentacaoEstoqueViewSet(ReadOnlyModelViewSet):
    serializer_class = MovimentacaoEstoqueSerializer
    permission_classes = [IsAuthenticated, CanManageEstoque]
    filterset_fields = ("produto", "tipo")
    search_fields = ("produto__codigo_interno", "produto__sku", "produto__nome", "observacao")
    ordering_fields = ("data_movimentacao", "quantidade")

    def get_queryset(self):
        return listar_movimentacoes()

    def _registrar(self, request, tipo):
        serializer = EstoqueMovimentacaoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = EstoqueService()
        payload = {
            "produto_id": serializer.validated_data["produto"].id,
            "quantidade": serializer.validated_data["quantidade"],
            "observacao": serializer.validated_data.get("observacao", ""),
        }
        try:
            if tipo == MovimentacaoEstoque.Tipo.ENTRADA:
                movimentacao = service.registrar_entrada(usuario=request.user, **payload)
                message = "Entrada registrada com sucesso."
            elif tipo == MovimentacaoEstoque.Tipo.SAIDA:
                movimentacao = service.registrar_saida(usuario=request.user, **payload)
                message = "Saida registrada com sucesso."
            else:
                movimentacao = service.registrar_ajuste(usuario=request.user, **payload)
                message = "Ajuste registrado com sucesso."
        except ValidationError as exc:
            detail = exc.message if hasattr(exc, "message") else exc.messages
            return error_response("Movimentacao rejeitada.", {"detail": detail}, status=status.HTTP_400_BAD_REQUEST)

        output = MovimentacaoEstoqueSerializer(movimentacao)
        return success_response(output.data, message, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="entrada")
    def entrada(self, request):
        return self._registrar(request, MovimentacaoEstoque.Tipo.ENTRADA)

    @action(detail=False, methods=["post"], url_path="saida")
    def saida(self, request):
        return self._registrar(request, MovimentacaoEstoque.Tipo.SAIDA)

    @action(detail=False, methods=["post"], url_path="ajuste")
    def ajuste(self, request):
        return self._registrar(request, MovimentacaoEstoque.Tipo.AJUSTE)
