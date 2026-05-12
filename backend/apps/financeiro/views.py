"""API views for this domain."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.responses import success_response


class DomainStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success_response({"module": request.resolver_match.namespace or "domain"})
