from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import success_response
from apps.fornecedores.serializers import FornecedorSerializer
from apps.fornecedores.selectors import listar_fornecedores


class FornecedorViewSet(ModelViewSet):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
    ordering_fields = ("razao_social", "created_at")

    def get_queryset(self):
        return listar_fornecedores()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(serializer.data, "Fornecedor criado com sucesso.", status=201)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return success_response(None, "Fornecedor inativado com sucesso.", status=204)
