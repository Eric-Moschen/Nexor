from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import success_response
from apps.fornecedores.serializers import FornecedorSerializer
from apps.fornecedores.permissions import CanManageFornecedores, CanViewFornecedores
from apps.fornecedores.selectors import listar_fornecedores, montar_historico_fornecedor
from apps.fornecedores.services import atualizar_fornecedor, criar_fornecedor, inativar_fornecedor


class FornecedorViewSet(ModelViewSet):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated, CanViewFornecedores]
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
    ordering_fields = ("razao_social", "created_at")

    def get_queryset(self):
        return listar_fornecedores()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dados = dict(serializer.validated_data)
        enderecos = dados.pop("enderecos", [])
        contatos = dados.pop("contatos", [])
        try:
            fornecedor = criar_fornecedor(usuario=request.user, enderecos=enderecos, contatos=contatos, **dados)
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages)
        return success_response(self.get_serializer(fornecedor).data, "Fornecedor criado com sucesso.", status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        dados = dict(serializer.validated_data)
        enderecos = dados.pop("enderecos", None)
        contatos = dados.pop("contatos", None)
        try:
            fornecedor = atualizar_fornecedor(fornecedor=instance, usuario=request.user, enderecos=enderecos, contatos=contatos, **dados)
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages)
        return success_response(self.get_serializer(fornecedor).data, "Fornecedor atualizado com sucesso.")

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        inativar_fornecedor(fornecedor=instance, usuario=request.user)
        return success_response(None, "Fornecedor inativado com sucesso.", status=204)

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            self.permission_classes = [IsAuthenticated, CanManageFornecedores]
        return super().get_permissions()

    @action(detail=True, methods=["get"])
    def historico(self, request, pk=None):
        return success_response(montar_historico_fornecedor(pk), "Historico do fornecedor carregado com sucesso.")
