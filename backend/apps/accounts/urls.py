from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import AuthAuditViewSet, PermissionViewSet, RoleViewSet, UserViewSet

app_name = "accounts"
router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("roles", RoleViewSet, basename="role")
router.register("permissions", PermissionViewSet, basename="permission")
router.register("auth-audit", AuthAuditViewSet, basename="auth-audit")

urlpatterns = [path("", include(router.urls))]
