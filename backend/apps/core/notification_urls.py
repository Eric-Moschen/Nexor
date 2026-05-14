from django.urls import path

from apps.core.views import NotificationViewSet

app_name = "notifications"

urlpatterns = [
    path("", NotificationViewSet.as_view({"get": "list"}), name="notification-list"),
    path("<int:pk>/", NotificationViewSet.as_view({"get": "retrieve"}), name="notification-detail"),
    path("<int:pk>/read/", NotificationViewSet.as_view({"post": "read"}), name="notification-read"),
]
