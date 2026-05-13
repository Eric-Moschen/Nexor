from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.clientes.views import ClienteViewSet

app_name = "clientes"
router = DefaultRouter()
router.register("clientes", ClienteViewSet, basename="cliente")
urlpatterns = [path("", include(router.urls))]
