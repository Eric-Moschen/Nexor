from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.clientes.serializers import ClienteSerializer
from apps.clientes.selectors import listar_clientes
from apps.core.responses import success_response


class ClienteViewSet(ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
    ordering_fields = ("razao_social", "created_at")

    def get_queryset(self):
        return listar_clientes()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)
        return success_response(serializer.data, "Cliente criado com sucesso.", status=201)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return success_response(None, "Cliente inativado com sucesso.", status=204)
