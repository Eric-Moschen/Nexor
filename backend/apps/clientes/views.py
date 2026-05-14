from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.clientes.permissions import CanManageClientes, CanManageRelacionamento, CanViewRelacionamento
from apps.clientes.serializers import ClienteSerializer, InteracaoCRMSerializer
from apps.clientes.selectors import listar_clientes, listar_interacoes_cliente, listar_interacoes_crm, montar_historico_cliente
from apps.clientes.services import atualizar_cliente, atualizar_interacao, criar_cliente, finalizar_interacao, inativar_cliente, registrar_interacao
from apps.core.responses import error_response, success_response


def _raise_drf_validation(error):
    if isinstance(error, DjangoValidationError):
        raise ValidationError(error.message_dict if hasattr(error, "message_dict") else error.messages)
    raise error


class ClienteViewSet(ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, CanViewRelacionamento]
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
    ordering_fields = ("razao_social", "created_at")

    def get_queryset(self):
        return listar_clientes()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dados = dict(serializer.validated_data)
        enderecos = dados.pop("enderecos", [])
        contatos = dados.pop("contatos", [])
        try:
            cliente = criar_cliente(usuario=request.user, enderecos=enderecos, contatos=contatos, **dados)
        except DjangoValidationError as exc:
            _raise_drf_validation(exc)
        return success_response(self.get_serializer(cliente).data, "Cliente criado com sucesso.", status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        dados = dict(serializer.validated_data)
        enderecos = dados.pop("enderecos", None)
        contatos = dados.pop("contatos", None)
        try:
            cliente = atualizar_cliente(cliente=instance, usuario=request.user, enderecos=enderecos, contatos=contatos, **dados)
        except DjangoValidationError as exc:
            _raise_drf_validation(exc)
        return success_response(self.get_serializer(cliente).data, "Cliente atualizado com sucesso.")

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        inativar_cliente(cliente=instance, usuario=request.user)
        return success_response(None, "Cliente inativado com sucesso.", status=204)

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy", "interacoes"} and self.request.method != "GET":
            self.permission_classes = [IsAuthenticated, CanManageClientes]
        return super().get_permissions()

    @action(detail=True, methods=["get"])
    def historico(self, request, pk=None):
        return success_response(montar_historico_cliente(pk), "Historico do cliente carregado com sucesso.")

    @action(detail=True, methods=["get", "post"])
    def interacoes(self, request, pk=None):
        cliente = self.get_object()
        if request.method == "GET":
            serializer = InteracaoCRMSerializer(listar_interacoes_cliente(cliente.id), many=True)
            return success_response(serializer.data, "Interacoes do cliente carregadas com sucesso.")
        serializer = InteracaoCRMSerializer(data={**request.data, "cliente": cliente.id, "responsavel": request.data.get("responsavel") or request.user.id})
        serializer.is_valid(raise_exception=True)
        try:
            interacao = registrar_interacao(cliente=cliente, usuario=request.user, **serializer.validated_data)
        except DjangoValidationError as exc:
            _raise_drf_validation(exc)
        return success_response(InteracaoCRMSerializer(interacao).data, "Interacao registrada com sucesso.", status=201)


class InteracaoCRMViewSet(ModelViewSet):
    serializer_class = InteracaoCRMSerializer
    permission_classes = [IsAuthenticated, CanViewRelacionamento]
    http_method_names = ["get", "post", "put", "patch", "head", "options"]

    def get_queryset(self):
        return listar_interacoes_crm()

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "finalizar"}:
            self.permission_classes = [IsAuthenticated, CanManageRelacionamento]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, "responsavel": request.data.get("responsavel") or request.user.id})
        serializer.is_valid(raise_exception=True)
        cliente = serializer.validated_data["cliente"]
        try:
            interacao = registrar_interacao(cliente=cliente, usuario=request.user, **serializer.validated_data)
        except DjangoValidationError as exc:
            _raise_drf_validation(exc)
        return success_response(self.get_serializer(interacao).data, "Interacao registrada com sucesso.", status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            interacao = atualizar_interacao(interacao=instance, usuario=request.user, **serializer.validated_data)
        except DjangoValidationError as exc:
            _raise_drf_validation(exc)
        return success_response(self.get_serializer(interacao).data, "Interacao atualizada com sucesso.")

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return error_response("Interacoes CRM nao podem ser excluidas fisicamente.", status=405)

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        interacao = finalizar_interacao(interacao=self.get_object(), usuario=request.user)
        return success_response(self.get_serializer(interacao).data, "Interacao finalizada com sucesso.")
