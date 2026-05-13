from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import error_response, success_response
from apps.fiscal.enums import StatusNFe
from apps.fiscal.models import ClienteFiscal, EmpresaFiscal, FornecedorFiscal, NaturezaOperacao, ProdutoFiscal
from apps.fiscal.permissions import CanManageFiscal, CanViewFiscal
from apps.fiscal.serializers import (
    CancelamentoNFeSerializer,
    ClienteFiscalSerializer,
    EmpresaFiscalSerializer,
    FornecedorFiscalSerializer,
    NaturezaOperacaoSerializer,
    NotaFiscalSerializer,
    ProdutoFiscalSerializer,
)
from apps.fiscal.selectors import listar_clientes_fiscais, listar_empresas, listar_fornecedores_fiscais, listar_naturezas_operacao, listar_notas_fiscais, listar_produtos_fiscais
from apps.fiscal.services import FiscalService


class EmpresaFiscalViewSet(ModelViewSet):
    serializer_class = EmpresaFiscalSerializer
    permission_classes = [IsAuthenticated, CanManageFiscal]

    def get_queryset(self):
        return listar_empresas()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        senha = serializer.validated_data.pop("senha_certificado", "")
        try:
            empresa = FiscalService().salvar_empresa(usuario=request.user, senha_certificado=senha, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Empresa fiscal nao pode ser criada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(empresa).data, "Empresa fiscal criada com sucesso.", status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        senha = serializer.validated_data.pop("senha_certificado", "")
        empresa = serializer.save(updated_by=self.request.user)
        if senha:
            empresa.certificado_senha_protegida = FiscalService().certificate_manager.protect_password(senha)
            empresa.save(update_fields=["certificado_senha_protegida", "updated_at"])


class ClienteFiscalViewSet(ModelViewSet):
    serializer_class = ClienteFiscalSerializer
    permission_classes = [IsAuthenticated, CanManageFiscal]

    def get_queryset(self):
        return listar_clientes_fiscais()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class FornecedorFiscalViewSet(ModelViewSet):
    serializer_class = FornecedorFiscalSerializer
    permission_classes = [IsAuthenticated, CanManageFiscal]

    def get_queryset(self):
        return listar_fornecedores_fiscais()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProdutoFiscalViewSet(ModelViewSet):
    serializer_class = ProdutoFiscalSerializer
    permission_classes = [IsAuthenticated, CanManageFiscal]

    def get_queryset(self):
        return listar_produtos_fiscais()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class NaturezaOperacaoViewSet(ModelViewSet):
    serializer_class = NaturezaOperacaoSerializer
    permission_classes = [IsAuthenticated, CanManageFiscal]

    def get_queryset(self):
        return listar_naturezas_operacao()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class NotaFiscalViewSet(ModelViewSet):
    serializer_class = NotaFiscalSerializer
    permission_classes = [IsAuthenticated, CanViewFiscal]
    filterset_fields = ("status", "tipo_operacao", "ambiente", "emitente")
    search_fields = ("numero", "chave_acesso", "protocolo", "emitente__razao_social")
    ordering_fields = ("data_emissao", "valor_total", "status")

    def get_queryset(self):
        return listar_notas_fiscais()

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "validar", "assinar", "enviar", "cancelar"}:
            return [IsAuthenticated(), CanManageFiscal()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        itens = serializer.validated_data.pop("itens")
        try:
            nota = FiscalService().criar_nfe(usuario=request.user, itens=itens, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("NFe nao pode ser criada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(nota).data, "NFe criada com sucesso.", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        nota = self.get_object()
        if nota.status in {StatusNFe.AUTORIZADA, StatusNFe.CANCELADA, StatusNFe.DENEGADA}:
            return error_response("NFe finalizada nao pode ser editada.", status=status.HTTP_400_BAD_REQUEST)
        if "itens" in request.data:
            return error_response("Itens da NFe devem ser recalculados por fluxo fiscal dedicado.", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(nota, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        FiscalService().recalcular_totais(nota)
        return success_response(self.get_serializer(nota).data, "NFe atualizada com sucesso.")

    @action(detail=True, methods=["post"], url_path="validar")
    def validar(self, request, pk=None):
        return self._executar_acao(pk, "validar_nfe", "NFe validada com sucesso.")

    @action(detail=True, methods=["post"], url_path="assinar")
    def assinar(self, request, pk=None):
        return self._executar_acao(pk, "assinar_nfe", "NFe assinada com sucesso.")

    @action(detail=True, methods=["post"], url_path="enviar")
    def enviar(self, request, pk=None):
        return self._executar_acao(pk, "enviar_nfe", "NFe enviada para autorizacao.")

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        serializer = CancelamentoNFeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            nota = FiscalService().cancelar_nfe(nota_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("NFe nao pode ser cancelada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(nota).data, "NFe cancelada com sucesso.")

    @action(detail=True, methods=["get"], url_path="danfe")
    def danfe(self, request, pk=None):
        try:
            arquivo = FiscalService().gerar_danfe(nota_id=pk)
        except ValidationError as exc:
            return error_response("DANFE nao pode ser gerado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return FileResponse(arquivo.open("rb"), as_attachment=True, filename=arquivo.name.split("/")[-1])

    @action(detail=True, methods=["get"], url_path="xml")
    def xml(self, request, pk=None):
        nota = self.get_object()
        if not nota.xml_autorizado:
            return error_response("XML ainda nao disponivel para esta NFe.", status=status.HTTP_404_NOT_FOUND)
        response = HttpResponse(nota.xml_autorizado, content_type="application/xml")
        response["Content-Disposition"] = f'attachment; filename="nfe-{nota.numero}-{nota.serie}.xml"'
        return response

    def _executar_acao(self, nota_id, metodo, mensagem):
        try:
            nota = getattr(FiscalService(), metodo)(nota_id=nota_id, usuario=self.request.user)
        except ValidationError as exc:
            return error_response("Operacao fiscal nao pode ser concluida.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(nota).data, mensagem)
