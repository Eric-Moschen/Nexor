from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.core.views import EventLogViewSet, HealthCheckView, NotificationViewSet

app_name = "core"
router = DefaultRouter()
router.register("events", EventLogViewSet, basename="event-log")
router.register("notificacoes", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
    path("", include(router.urls)),
]
