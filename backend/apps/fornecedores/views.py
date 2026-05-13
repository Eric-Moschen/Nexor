from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.fornecedores.serializers import FornecedoresRecordSerializer
from apps.fornecedores.selectors import list_records


class FornecedoresRecordViewSet(ModelViewSet):
    serializer_class = FornecedoresRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return list_records()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
