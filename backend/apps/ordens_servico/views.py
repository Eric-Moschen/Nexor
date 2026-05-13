from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.ordens_servico.serializers import OrdensServicoRecordSerializer
from apps.ordens_servico.selectors import list_records


class OrdensServicoRecordViewSet(ModelViewSet):
    serializer_class = OrdensServicoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return list_records()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
