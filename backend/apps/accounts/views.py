from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView

from apps.accounts.models import Role
from apps.accounts.permissions import HasPermission, IsAdministrador
from apps.accounts.selectors import list_auth_audit, list_permissions, list_roles, list_users
from apps.accounts.serializers import (
    AuthAuditLogSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    PermissionSerializer,
    RefreshSerializer,
    RolePermissionUpdateSerializer,
    RoleSerializer,
    UserSerializer,
)
from apps.accounts.services import alterar_senha, ativar_usuario, atualizar_usuario, criar_usuario, inativar_usuario, login_usuario, logout_usuario, refresh_usuario, salvar_permissoes_role
from apps.core.responses import error_response, success_response


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = login_usuario(request=request, **serializer.validated_data)
        except DjangoValidationError as exc:
            return error_response("Credenciais invalidas.", {"detail": exc.messages}, status=401)
        return success_response(
            {
                "access": result["access"],
                "refresh": result["refresh"],
                "user": UserSerializer(result["user"]).data,
            },
            "Login realizado com sucesso.",
        )


class RefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            return success_response(refresh_usuario(**serializer.validated_data), "Token renovado com sucesso.")
        except Exception:
            return error_response("Refresh token invalido.", status=401)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            logout_usuario(request=request, refresh_token=serializer.validated_data["refresh"])
        except Exception:
            return error_response("Logout nao pode ser concluido.", status=400)
        return success_response(None, "Logout realizado com sucesso.")


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success_response(UserSerializer(request.user).data, "Usuario autenticado carregado com sucesso.")


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            alterar_senha(user=request.user, request=request, **serializer.validated_data)
        except DjangoValidationError as exc:
            return error_response("Senha nao pode ser alterada.", {"detail": exc.messages}, status=400)
        return success_response(None, "Senha alterada com sucesso.")


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "accounts.usuario.visualizar"

    def get_queryset(self):
        return list_users()

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "deactivate", "activate"}:
            self.required_permission = "accounts.usuario.gerenciar"
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dados = dict(serializer.validated_data)
        password = dados.pop("password", None)
        try:
            user = criar_usuario(usuario_criador=request.user, password=password, **dados)
        except DjangoValidationError as exc:
            return error_response("Usuario nao pode ser criado.", {"detail": exc.messages}, status=400)
        return success_response(self.get_serializer(user).data, "Usuario criado com sucesso.", status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            user = atualizar_usuario(user=instance, **serializer.validated_data)
        except DjangoValidationError as exc:
            return error_response("Usuario nao pode ser atualizado.", {"detail": exc.messages}, status=400)
        return success_response(self.get_serializer(user).data, "Usuario atualizado com sucesso.")

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = inativar_usuario(user=self.get_object())
        return success_response(self.get_serializer(user).data, "Usuario inativado com sucesso.")

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        user = ativar_usuario(user=self.get_object())
        return success_response(self.get_serializer(user).data, "Usuario ativado com sucesso.")


class RoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "accounts.perfil.gerenciar"

    def get_queryset(self):
        return list_roles()

    def perform_create(self, serializer):
        serializer.save(is_system=False)

    @action(detail=True, methods=["post"])
    def permissions(self, request, pk=None):
        serializer = RolePermissionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = salvar_permissoes_role(role=self.get_object(), permission_codes=serializer.validated_data["permissions"])
        return success_response(self.get_serializer(role).data, "Permissoes do perfil atualizadas com sucesso.")


class PermissionViewSet(ReadOnlyModelViewSet):
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

    def get_queryset(self):
        return list_permissions()


class AuthAuditViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthAuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

    def get_queryset(self):
        return list_auth_audit()
