from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import error_response, success_response
from apps.financeiro.models import CategoriaFinanceira, CentroCusto
from apps.ordens_servico.enums import StatusOS
from apps.ordens_servico.permissions import CanApproveOrdensServico, CanBillOrdensServico, CanManageOrdensServico, CanViewOrdensServico
from apps.ordens_servico.serializers import (
    ApontamentoHorasOSSerializer,
    CancelarOSSerializer,
    FaturarOSSerializer,
    HistoricoOSSerializer,
    MaterialUtilizadoOSSerializer,
    OrdemServicoSerializer,
)
from apps.ordens_servico.selectors import listar_apontamentos_os, listar_historico_os, listar_materiais_os, listar_ordens_servico
from apps.ordens_servico.services import OrdemServicoService


class OrdemServicoViewSet(ModelViewSet):
    serializer_class = OrdemServicoSerializer
    permission_classes = [IsAuthenticated, CanViewOrdensServico]
    filterset_fields = ("status", "prioridade", "cliente", "responsavel_tecnico")
    search_fields = ("numero", "titulo", "descricao_servico", "cliente__razao_social")
    ordering_fields = ("data_abertura", "data_prevista", "prioridade", "status", "valor_final")

    def get_queryset(self):
        return listar_ordens_servico()

    def get_permissions(self):
        if self.action in {"aprovar", "pausar", "retomar", "finalizar", "cancelar"}:
            return [IsAuthenticated(), CanApproveOrdensServico()]
        if self.action == "faturar":
            return [IsAuthenticated(), CanBillOrdensServico()]
        if self.action in {"create", "update", "partial_update", "destroy", "enviar_aprovacao", "iniciar", "materiais", "remover_material", "apontamentos", "apontamento_detail"}:
            return [IsAuthenticated(), CanManageOrdensServico()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        itens = serializer.validated_data.pop("itens", [])
        try:
            ordem = OrdemServicoService().criar_os(usuario=request.user, itens=itens, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("OS nao pode ser criada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(ordem).data, "Ordem de servico criada com sucesso.", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        ordem = self.get_object()
        if ordem.status in {StatusOS.FINALIZADA, StatusOS.CANCELADA, StatusOS.FATURADA}:
            return error_response("OS finalizada, cancelada ou faturada nao pode ser editada livremente.", status=status.HTTP_400_BAD_REQUEST)
        if "itens" in request.data:
            return error_response("Itens de servico devem ser alterados pelo fluxo dedicado de OS.", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(ordem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        OrdemServicoService().recalcular_totais(ordem)
        return success_response(self.get_serializer(ordem).data, "OS atualizada com sucesso.")

    def destroy(self, request, *args, **kwargs):
        ordem = self.get_object()
        if ordem.status in {StatusOS.FINALIZADA, StatusOS.FATURADA}:
            return error_response("OS finalizada ou faturada nao pode ser removida.", status=status.HTTP_400_BAD_REQUEST)
        ordem.is_active = False
        ordem.deleted_at = timezone.now()
        ordem.updated_by = request.user
        ordem.save(update_fields=["is_active", "deleted_at", "updated_by", "updated_at"])
        return success_response(message="OS removida com sucesso.")

    @action(detail=True, methods=["post"], url_path="enviar-aprovacao")
    def enviar_aprovacao(self, request, pk=None):
        return self._executar_acao(pk, "enviar_aprovacao", "OS enviada para aprovacao com sucesso.")

    @action(detail=True, methods=["post"], url_path="aprovar")
    def aprovar(self, request, pk=None):
        return self._executar_acao(pk, "aprovar", "OS aprovada com sucesso.")

    @action(detail=True, methods=["post"], url_path="iniciar")
    def iniciar(self, request, pk=None):
        return self._executar_acao(pk, "iniciar", "Execucao da OS iniciada com sucesso.")

    @action(detail=True, methods=["post"], url_path="pausar")
    def pausar(self, request, pk=None):
        return self._executar_acao(pk, "pausar", "OS pausada com sucesso.")

    @action(detail=True, methods=["post"], url_path="retomar")
    def retomar(self, request, pk=None):
        return self._executar_acao(pk, "retomar", "OS retomada com sucesso.")

    @action(detail=True, methods=["post"], url_path="finalizar")
    def finalizar(self, request, pk=None):
        return self._executar_acao(pk, "finalizar", "OS finalizada com sucesso.")

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        serializer = CancelarOSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ordem = OrdemServicoService().cancelar(ordem_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("OS nao pode ser cancelada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(ordem).data, "OS cancelada com sucesso.")

    @action(detail=True, methods=["post"], url_path="faturar")
    def faturar(self, request, pk=None):
        serializer = FaturarOSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        categoria = CategoriaFinanceira.objects.filter(id=serializer.validated_data.get("categoria")).first() if serializer.validated_data.get("categoria") else None
        centro = CentroCusto.objects.filter(id=serializer.validated_data.get("centro_custo")).first() if serializer.validated_data.get("centro_custo") else None
        if serializer.validated_data.get("categoria") and not categoria:
            return error_response("Categoria financeira nao encontrada.", status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data.get("centro_custo") and not centro:
            return error_response("Centro de custo nao encontrado.", status=status.HTTP_400_BAD_REQUEST)
        try:
            ordem = OrdemServicoService().faturar(
                ordem_id=pk,
                usuario=request.user,
                data_vencimento=serializer.validated_data.get("data_vencimento"),
                categoria=categoria,
                centro_custo=centro,
            )
        except ValidationError as exc:
            return error_response("OS nao pode ser faturada.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(ordem).data, "OS faturada com sucesso.")

    @action(detail=True, methods=["get", "post"], url_path="materiais")
    def materiais(self, request, pk=None):
        if request.method == "GET":
            return success_response(MaterialUtilizadoOSSerializer(listar_materiais_os(pk), many=True).data, "Materiais carregados com sucesso.")
        serializer = MaterialUtilizadoOSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            material = OrdemServicoService().adicionar_material(ordem_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Material nao pode ser utilizado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(MaterialUtilizadoOSSerializer(material).data, "Material registrado com sucesso.", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path=r"materiais/(?P<material_id>[^/.]+)")
    def remover_material(self, request, pk=None, material_id=None):
        try:
            OrdemServicoService().remover_material(material_id=material_id, usuario=request.user)
        except ValidationError as exc:
            return error_response("Material nao pode ser removido.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(message="Material removido e estoque estornado com sucesso.")

    @action(detail=True, methods=["get", "post"], url_path="apontamentos")
    def apontamentos(self, request, pk=None):
        if request.method == "GET":
            return success_response(ApontamentoHorasOSSerializer(listar_apontamentos_os(pk), many=True).data, "Apontamentos carregados com sucesso.")
        serializer = ApontamentoHorasOSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            apontamento = OrdemServicoService().registrar_apontamento(ordem_id=pk, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Apontamento nao pode ser registrado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(ApontamentoHorasOSSerializer(apontamento).data, "Apontamento registrado com sucesso.", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["put", "delete"], url_path=r"apontamentos/(?P<apontamento_id>[^/.]+)")
    def apontamento_detail(self, request, pk=None, apontamento_id=None):
        service = OrdemServicoService()
        if request.method == "DELETE":
            try:
                service.remover_apontamento(apontamento_id=apontamento_id, usuario=request.user)
            except ValidationError as exc:
                return error_response("Apontamento nao pode ser removido.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
            return success_response(message="Apontamento removido com sucesso.")
        serializer = ApontamentoHorasOSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            apontamento = service.atualizar_apontamento(apontamento_id=apontamento_id, usuario=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return error_response("Apontamento nao pode ser atualizado.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(ApontamentoHorasOSSerializer(apontamento).data, "Apontamento atualizado com sucesso.")

    @action(detail=True, methods=["get"], url_path="historico")
    def historico(self, request, pk=None):
        return success_response(HistoricoOSSerializer(listar_historico_os(pk), many=True).data, "Historico carregado com sucesso.")

    def _executar_acao(self, ordem_id, metodo, mensagem):
        try:
            ordem = getattr(OrdemServicoService(), metodo)(ordem_id=ordem_id, usuario=self.request.user)
        except ValidationError as exc:
            return error_response("Operacao de OS nao pode ser concluida.", {"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return success_response(self.get_serializer(ordem).data, mensagem)
