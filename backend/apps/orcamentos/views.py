from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import error_response, success_response
from apps.orcamentos.enums import StatusOrcamento
from apps.orcamentos.permissions import CanApproveOrcamento, CanManageOrcamento, CanViewOrcamento
from apps.orcamentos.serializers import CancelarOrcamentoSerializer, HistoricoOrcamentoSerializer, OrcamentoSerializer, ReprovarOrcamentoSerializer
from apps.orcamentos.selectors import listar_historico_orcamento, listar_orcamentos
from apps.orcamentos.services import OrcamentoService


class OrcamentoViewSet(ModelViewSet):
    serializer_class = OrcamentoSerializer
    permission_classes = [IsAuthenticated, CanViewOrcamento]
    filterset_fields = ("status", "cliente")
    search_fields = ("numero", "titulo", "descricao", "cliente__razao_social")
    ordering_fields = ("data_criacao", "data_validade", "valor_total", "status")

    def get_queryset(self):
        return listar_orcamentos()

    def get_permissions(self):
        if self.action in {"aprovar", "reprovar"}:
            return [IsAuthenticated(), CanApproveOrcamento()]
        if self.action in {"create", "update", "partial_update", "destroy", "enviar", "cancelar", "converter_os", "pdf"}:
            return [IsAuthenticated(), CanManageOrcamento()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        itens_produto = serializer.validated_data.pop("itens_produto", [])
        itens_servico = serializer.validated_data.pop("itens_servico", [])
        try:
            orcamento = OrcamentoService().criar_orcamento(usuario=request.user, itens_produto=itens_produto, itens_servico=itens_servico, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Orcamento nao pode ser criado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(orcamento).data, "Orcamento criado com sucesso.", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        orcamento = self.get_object()
        if orcamento.status in {StatusOrcamento.APROVADO, StatusOrcamento.CONVERTIDO_OS, StatusOrcamento.CANCELADO}:
            return error_response("Orcamento aprovado, convertido ou cancelado nao pode ser editado livremente.", status=status.HTTP_400_BAD_REQUEST)
        if "itens_produto" in request.data or "itens_servico" in request.data:
            return error_response("Itens do orcamento devem ser recalculados por fluxo dedicado.", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(orcamento, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            orcamento = OrcamentoService().atualizar_orcamento(orcamento_id=orcamento.id, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Orcamento nao pode ser atualizado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(orcamento).data, "Orcamento atualizado com sucesso.")

    def destroy(self, request, *args, **kwargs):
        orcamento = self.get_object()
        if orcamento.status == StatusOrcamento.CONVERTIDO_OS:
            return error_response("Orcamento convertido em OS nao pode ser removido.", status=status.HTTP_400_BAD_REQUEST)
        orcamento.is_active = False
        orcamento.deleted_at = timezone.now()
        orcamento.updated_by = request.user
        orcamento.save(update_fields=["is_active", "deleted_at", "updated_by", "updated_at"])
        return success_response(message="Orcamento removido com sucesso.")

    @action(detail=True, methods=["post"], url_path="enviar")
    def enviar(self, request, pk=None):
        return self._executar_acao(pk, "enviar", "Orcamento enviado com sucesso.")

    @action(detail=True, methods=["post"], url_path="aprovar")
    def aprovar(self, request, pk=None):
        return self._executar_acao(pk, "aprovar", "Orcamento aprovado com sucesso.")

    @action(detail=True, methods=["post"], url_path="reprovar")
    def reprovar(self, request, pk=None):
        serializer = ReprovarOrcamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            orcamento = OrcamentoService().reprovar(orcamento_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Orcamento nao pode ser reprovado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(orcamento).data, "Orcamento reprovado com sucesso.")

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        serializer = CancelarOrcamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            orcamento = OrcamentoService().cancelar(orcamento_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Orcamento nao pode ser cancelado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(orcamento).data, "Orcamento cancelado com sucesso.")

    @action(detail=True, methods=["post"], url_path="converter-os")
    def converter_os(self, request, pk=None):
        return self._executar_acao(pk, "converter_em_os", "Orcamento convertido em OS com sucesso.")

    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(self, request, pk=None):
        try:
            arquivo = OrcamentoService().gerar_pdf(orcamento_id=pk, usuario=request.user)
        except ValidationError as exc:
            return error_response("PDF nao pode ser gerado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return FileResponse(arquivo.open("rb"), as_attachment=True, filename=arquivo.name.split("/")[-1])

    @action(detail=True, methods=["get"], url_path="historico")
    def historico(self, request, pk=None):
        return success_response(HistoricoOrcamentoSerializer(listar_historico_orcamento(pk), many=True).data, "Historico carregado com sucesso.")

    def _executar_acao(self, orcamento_id, metodo, mensagem):
        try:
            orcamento = getattr(OrcamentoService(), metodo)(orcamento_id=orcamento_id, usuario=self.request.user)
        except ValidationError as exc:
            return error_response("Operacao de orcamento nao pode ser concluida.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(orcamento).data, mensagem)
