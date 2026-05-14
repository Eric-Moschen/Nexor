from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.clientes.views import InteracaoCRMViewSet

app_name = "crm"
router = DefaultRouter()
router.register("interacoes", InteracaoCRMViewSet, basename="crm-interacao")

urlpatterns = [path("", include(router.urls))]
