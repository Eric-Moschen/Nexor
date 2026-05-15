from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.core.views import CeleryHealthView, DatabaseHealthView, EventLogViewSet, HealthCheckView, NotificationViewSet, RedisHealthView

app_name = "core"
router = DefaultRouter()
router.register("events", EventLogViewSet, basename="event-log")
router.register("notificacoes", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
    path("database/", DatabaseHealthView.as_view(), name="health-database"),
    path("redis/", RedisHealthView.as_view(), name="health-redis"),
    path("celery/", CeleryHealthView.as_view(), name="health-celery"),
    path("", include(router.urls)),
]
