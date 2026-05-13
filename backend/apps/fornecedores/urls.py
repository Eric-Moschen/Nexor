from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.fornecedores.views import FornecedoresRecordViewSet

app_name = "fornecedores"
router = DefaultRouter()
router.register("registros", FornecedoresRecordViewSet, basename="fornecedores-record")
urlpatterns = [path("", include(router.urls))]
