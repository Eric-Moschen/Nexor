from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.permissions import has_permission
from apps.core.models import EventLog, Notification
from apps.core.responses import success_response
from apps.core.serializers import EventLogSerializer, NotificationSerializer
from apps.core.notifications.services import NotificationService


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return success_response({"status": "ok"}, message="Nexor ERP API operacional.")


class EventLogViewSet(ReadOnlyModelViewSet):
    serializer_class = EventLogSerializer
    permission_classes = [has_permission("core.evento.visualizar")]
    filterset_fields = ("event_name", "module", "status")
    search_fields = ("event_name", "aggregate_type", "aggregate_id")
    ordering_fields = ("created_at", "processed_at")

    def get_queryset(self):
        return EventLog.objects.select_related("user").all()


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [has_permission("notificacoes.notificacao.visualizar")]
    filterset_fields = ("level", "category", "is_read")
    search_fields = ("title", "message", "category")
    ordering_fields = ("created_at", "read_at")

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.select_related("recipient", "event")
        return queryset.filter(recipient=user) | queryset.filter(recipient__isnull=True)

    @action(detail=True, methods=["post"], url_path="read", permission_classes=[has_permission("notificacoes.notificacao.visualizar")])
    def read(self, request, pk=None):
        notification = self.get_object()
        NotificationService.mark_read(notification, user=request.user)
        return success_response(self.get_serializer(notification).data, message="Notificacao marcada como lida.")
