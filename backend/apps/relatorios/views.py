from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import error_response, success_response
from apps.relatorios.enums import FormatoExportacao, TipoDashboard, TipoRelatorio
from apps.relatorios.permissions import CanManageRelatorios, CanViewAnalytics, CanViewCommercialAnalytics, CanViewFinancialAnalytics, CanViewOperationalAnalytics
from apps.relatorios.selectors import listar_exportacoes
from apps.relatorios.serializers import ExportacaoArquivoSerializer, RelatoriosRecordSerializer
from apps.relatorios.services import DashboardService, RelatorioService
from apps.relatorios.validators import normalizar_filtros


class RelatoriosRecordViewSet(ModelViewSet):
    serializer_class = RelatoriosRecordSerializer
    permission_classes = [IsAuthenticated, CanManageRelatorios]

    def get_queryset(self):
        from apps.relatorios.selectors import list_records

        return list_records()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, CanViewAnalytics]
    tipo_dashboard = None

    def get_permissions(self):
        permission_by_dashboard = {
            TipoDashboard.FINANCEIRO: CanViewFinancialAnalytics,
            TipoDashboard.COMERCIAL: CanViewCommercialAnalytics,
            TipoDashboard.OPERACIONAL: CanViewOperationalAnalytics,
        }
        permission_class = permission_by_dashboard.get(self.tipo_dashboard, CanViewAnalytics)
        return [IsAuthenticated(), permission_class()]

    def get(self, request):
        try:
            filtros = normalizar_filtros(request.query_params)
            payload = DashboardService().consolidar(tipo_dashboard=self.tipo_dashboard, filtros=filtros, usuario=request.user)
        except ValidationError as exc:
            return error_response("Dashboard nao pode ser consolidado.", {"detail": exc.messages}, status=400)
        return success_response(payload, "Dashboard carregado com sucesso.")


class RelatorioAPIView(APIView):
    permission_classes = [IsAuthenticated, CanViewAnalytics]
    tipo_relatorio = None

    def get_permissions(self):
        permission_by_report = {
            TipoRelatorio.FINANCEIRO: CanViewFinancialAnalytics,
            TipoRelatorio.COMERCIAL: CanViewCommercialAnalytics,
            TipoRelatorio.OS: CanViewOperationalAnalytics,
        }
        permission_class = permission_by_report.get(self.tipo_relatorio, CanViewAnalytics)
        return [IsAuthenticated(), permission_class()]

    def get(self, request):
        try:
            filtros = normalizar_filtros(request.query_params)
            relatorio = RelatorioService().gerar_relatorio(tipo_relatorio=self.tipo_relatorio, filtros=filtros, usuario=request.user)
        except ValidationError as exc:
            return error_response("Falha ao gerar relatorio.", {"detail": exc.messages}, status=400)
        return success_response(relatorio.payload, "Relatorio gerado com sucesso.")


class ExportarRelatorioAPIView(APIView):
    permission_classes = [IsAuthenticated, CanManageRelatorios]
    formato = None

    def post(self, request):
        try:
            filtros = normalizar_filtros(request.data)
            tipo_relatorio = request.data.get("tipo_relatorio", TipoRelatorio.FINANCEIRO)
            exportacao = RelatorioService().solicitar_exportacao(tipo_relatorio=tipo_relatorio, formato=self.formato, filtros=filtros, usuario=request.user)
        except ValidationError as exc:
            return error_response("Falha ao gerar relatorio.", {"detail": exc.messages}, status=400)
        serializer = ExportacaoArquivoSerializer(exportacao, context={"request": request})
        return success_response(serializer.data, "Exportacao registrada com sucesso.", status=201)


class ExportacaoListAPIView(APIView):
    permission_classes = [IsAuthenticated, CanViewAnalytics]

    def get(self, request):
        serializer = ExportacaoArquivoSerializer(listar_exportacoes(request.user), many=True, context={"request": request})
        return success_response(serializer.data, "Exportacoes carregadas com sucesso.")


class DashboardExecutivoView(DashboardAPIView):
    tipo_dashboard = TipoDashboard.EXECUTIVO


class DashboardFinanceiroView(DashboardAPIView):
    tipo_dashboard = TipoDashboard.FINANCEIRO


class DashboardEstoqueView(DashboardAPIView):
    tipo_dashboard = TipoDashboard.ESTOQUE


class DashboardComercialView(DashboardAPIView):
    tipo_dashboard = TipoDashboard.COMERCIAL


class DashboardOperacionalView(DashboardAPIView):
    tipo_dashboard = TipoDashboard.OPERACIONAL


class RelatorioFinanceiroView(RelatorioAPIView):
    tipo_relatorio = TipoRelatorio.FINANCEIRO


class RelatorioEstoqueView(RelatorioAPIView):
    tipo_relatorio = TipoRelatorio.ESTOQUE


class RelatorioComercialView(RelatorioAPIView):
    tipo_relatorio = TipoRelatorio.COMERCIAL


class RelatorioOSView(RelatorioAPIView):
    tipo_relatorio = TipoRelatorio.OS


class RelatorioComprasView(RelatorioAPIView):
    tipo_relatorio = TipoRelatorio.COMPRAS


class ExportarPDFView(ExportarRelatorioAPIView):
    formato = FormatoExportacao.PDF


class ExportarExcelView(ExportarRelatorioAPIView):
    formato = FormatoExportacao.EXCEL


class ExportarCSVView(ExportarRelatorioAPIView):
    formato = FormatoExportacao.CSV
