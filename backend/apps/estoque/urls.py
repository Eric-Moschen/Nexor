from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.estoque.views import EstoqueRecordViewSet

app_name = "estoque"
router = DefaultRouter()
router.register("registros", EstoqueRecordViewSet, basename="estoque-record")
urlpatterns = [path("", include(router.urls))]
