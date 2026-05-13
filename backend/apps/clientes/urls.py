from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.clientes.views import ClientesRecordViewSet

app_name = "clientes"
router = DefaultRouter()
router.register("registros", ClientesRecordViewSet, basename="clientes-record")
urlpatterns = [path("", include(router.urls))]
