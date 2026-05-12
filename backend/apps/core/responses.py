"""Standard API response helpers."""
from rest_framework.response import Response


def success_response(data=None, message="Operação realizada com sucesso.", status=200):
    return Response({"success": True, "message": message, "data": data or {}}, status=status)
