from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.fiscal.views import FiscalRecordViewSet

app_name = "fiscal"
router = DefaultRouter()
router.register("registros", FiscalRecordViewSet, basename="fiscal-record")
urlpatterns = [path("", include(router.urls))]
