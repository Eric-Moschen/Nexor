from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import error_response, success_response
from apps.financeiro.permissions import CanManageFinanceiro, CanViewFinanceiro
from apps.financeiro.serializers import (
    BaixaFinanceiraSerializer,
    BaixaInputSerializer,
    CategoriaFinanceiraSerializer,
    CentroCustoSerializer,
    ContaPagarSerializer,
    ContaReceberSerializer,
)
from apps.financeiro.selectors import dashboard_financeiro, fluxo_caixa_resumo, listar_categorias, listar_centros_custo, listar_contas_pagar, listar_contas_receber
from apps.financeiro.services import FinanceiroService
from apps.financeiro.models import CategoriaFinanceira, CentroCusto


class CentroCustoViewSet(ModelViewSet):
    serializer_class = CentroCustoSerializer
    permission_classes = [IsAuthenticated, CanManageFinanceiro]

    def get_queryset(self):
        return listar_centros_custo()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CategoriaFinanceiraViewSet(ModelViewSet):
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated, CanManageFinanceiro]

    def get_queryset(self):
        return listar_categorias()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ContaPagarViewSet(ModelViewSet):
    serializer_class = ContaPagarSerializer
    permission_classes = [IsAuthenticated, CanViewFinanceiro]
    filterset_fields = ("status", "fornecedor", "categoria", "centro_custo")
    search_fields = ("numero_lancamento", "descricao", "fornecedor__razao_social")
    ordering_fields = ("data_vencimento", "valor_atual", "status")

    def get_queryset(self):
        return listar_contas_pagar()

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "baixar", "cancelar"}:
            return [IsAuthenticated(), CanManageFinanceiro()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            conta = FinanceiroService().criar_conta_pagar(usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Conta a pagar nao pode ser criada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(conta).data, "Conta a pagar criada com sucesso.", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="baixar")
    def baixar(self, request, pk=None):
        serializer = BaixaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            baixa = FinanceiroService().baixar_conta_pagar(conta_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Pagamento nao pode ser registrado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(BaixaFinanceiraSerializer(baixa).data, "Pagamento registrado com sucesso.", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        try:
            conta = FinanceiroService().cancelar_conta_pagar(conta_id=pk, usuario=request.user)
        except ValidationError as exc:
            return error_response("Conta a pagar nao pode ser cancelada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(conta).data, "Conta a pagar cancelada com sucesso.")


class ContaReceberViewSet(ModelViewSet):
    serializer_class = ContaReceberSerializer
    permission_classes = [IsAuthenticated, CanViewFinanceiro]
    filterset_fields = ("status", "cliente", "categoria", "centro_custo")
    search_fields = ("numero_lancamento", "descricao", "cliente__razao_social")
    ordering_fields = ("data_vencimento", "valor_atual", "status")

    def get_queryset(self):
        return listar_contas_receber()

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "baixar", "cancelar"}:
            return [IsAuthenticated(), CanManageFinanceiro()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            conta = FinanceiroService().criar_conta_receber(usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Conta a receber nao pode ser criada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(conta).data, "Conta a receber criada com sucesso.", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="baixar")
    def baixar(self, request, pk=None):
        serializer = BaixaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            baixa = FinanceiroService().baixar_conta_receber(conta_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Recebimento nao pode ser registrado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(BaixaFinanceiraSerializer(baixa).data, "Recebimento registrado com sucesso.", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        try:
            conta = FinanceiroService().cancelar_conta_receber(conta_id=pk, usuario=request.user)
        except ValidationError as exc:
            return error_response("Conta a receber nao pode ser cancelada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(conta).data, "Conta a receber cancelada com sucesso.")


class FluxoCaixaView(APIView):
    permission_classes = [IsAuthenticated, CanViewFinanceiro]

    def get(self, request):
        return success_response(fluxo_caixa_resumo(), "Fluxo de caixa consolidado com sucesso.")


class DashboardFinanceiroView(APIView):
    permission_classes = [IsAuthenticated, CanViewFinanceiro]

    def get(self, request):
        return success_response(dashboard_financeiro(), "Dashboard financeiro carregado com sucesso.")
