from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.auditoria.serializers import AuditoriaRecordSerializer
from apps.auditoria.selectors import list_records


class AuditoriaRecordViewSet(ModelViewSet):
    serializer_class = AuditoriaRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return list_records()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
