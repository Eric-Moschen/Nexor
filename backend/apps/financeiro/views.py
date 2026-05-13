from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.financeiro.serializers import FinanceiroRecordSerializer
from apps.financeiro.selectors import list_records


class FinanceiroRecordViewSet(ModelViewSet):
    serializer_class = FinanceiroRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return list_records()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
