from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import UserViewSet

app_name = "accounts"
router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
urlpatterns = [path("", include(router.urls))]
