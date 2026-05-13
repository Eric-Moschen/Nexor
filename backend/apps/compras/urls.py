from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.compras.views import ComprasRecordViewSet

app_name = "compras"
router = DefaultRouter()
router.register("registros", ComprasRecordViewSet, basename="compras-record")
urlpatterns = [path("", include(router.urls))]
