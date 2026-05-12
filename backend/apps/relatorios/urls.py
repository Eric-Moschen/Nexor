"""URL routes for this domain."""
from django.urls import path

from .views import DomainStatusView

app_name = "domain"

urlpatterns = [
    path("", DomainStatusView.as_view(), name="status"),
]
