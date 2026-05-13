from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.financeiro.views import FinanceiroRecordViewSet

app_name = "financeiro"
router = DefaultRouter()
router.register("registros", FinanceiroRecordViewSet, basename="financeiro-record")
urlpatterns = [path("", include(router.urls))]
