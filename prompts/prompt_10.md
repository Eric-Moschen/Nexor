# PROMPT 10 — AUTENTICAÇÃO, USUÁRIOS, PERMISSÕES E RBAC DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- Todos os módulos criados nos Prompts 02 a 09

O objetivo desta etapa é implementar a camada de segurança, autenticação, autorização e controle de acesso do sistema.

Este prompt é crítico. Sem ele, o ERP não é seguro nem utilizável em ambiente real.

---

# OBJETIVO

Implementar:

- Autenticação JWT
- Refresh token
- Logout seguro
- Usuários
- Perfis
- Cargos
- Permissões
- RBAC
- Controle de sessão
- Auditoria de login
- Proteção de rotas no frontend
- Interceptor Axios
- Contexto de autenticação React

---

# FUNCIONALIDADES OBRIGATÓRIAS

## 1. USUÁRIOS

Criar usuário customizado.

Campos:

- Nome completo
- Email
- Username
- Senha
- Telefone
- Cargo
- Perfil de acesso
- Status ativo/inativo
- Último login
- Data criação
- Data atualização

Regras:

- Email único
- Username único
- Senha criptografada
- Usuário inativo não pode logar
- Não expor senha em responses

---

## 2. PERFIS DE ACESSO

Criar perfis:

- Administrador
- Diretoria
- Financeiro
- Compras
- Estoque
- Fiscal
- Comercial
- Operacional
- Supervisor

---

## 3. PERMISSÕES RBAC

Permissões devem ser organizadas por módulo e ação.

Exemplos:

```txt
estoque.produto.visualizar
estoque.produto.criar
estoque.produto.editar
estoque.produto.excluir
financeiro.conta_pagar.visualizar
financeiro.conta_pagar.baixar
fiscal.nfe.emitir
os.ordem.finalizar
relatorios.dashboard.visualizar


# 4. AUTENTICAÇÃO JWT

Implementar endpoints:

POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
GET  /api/v1/auth/me/
POST /api/v1/auth/change-password/

# 5. CONTROLE DE SESSÃO

Implementar:

- Access token curto
- Refresh token mais longo
- Blacklist de refresh token no logout
- Expiração segura
- Auditoria de login/logout

# 6. AUDITORIA DE AUTENTICAÇÃO

Registrar:

- Login realizado
- Login falhou
- Logout
- Troca de senha
- Usuário
- IP
- User-Agent
- Data/hora


# BACKEND

Implementar no app accounts:

apps/accounts/
├── models.py
├── serializers.py
├── services.py
├── selectors.py
├── repositories.py
├── views.py
├── urls.py
├── permissions.py
├── validators.py
├── enums.py
└── tests/

# MODELS

Criar:

- User
- Role
- Permission
- RolePermission
- UserRole
- AuthAuditLog

# REGRAS DE NEGÓCIO

Implementar em services.py:

- Criar usuário
- Atualizar usuário
- Inativar usuário
- Alterar senha
- Validar login
- Registrar auditoria
- Verificar permissões
- Vincular perfil ao usuário
- Remover perfil do usuário

# API DE USUÁRIOS

Criar endpoints:
GET    /api/v1/accounts/users/
POST   /api/v1/accounts/users/
GET    /api/v1/accounts/users/{id}/
PUT    /api/v1/accounts/users/{id}/
POST   /api/v1/accounts/users/{id}/deactivate/
POST   /api/v1/accounts/users/{id}/activate/

#  API DE PERFIS

Criar endpoints:

GET    /api/v1/accounts/roles/
POST   /api/v1/accounts/roles/
GET    /api/v1/accounts/roles/{id}/
PUT    /api/v1/accounts/roles/{id}/
POST   /api/v1/accounts/roles/{id}/permissions/

# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Login realizado com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "Credenciais inválidas",
  "errors": {}
}

PERMISSÕES

Criar permission class reutilizável:

HasPermission("estoque.produto.criar")

Preparar uso em qualquer ViewSet/APIView.


# FRONTEND

Implementar:

# Páginas
- Login
- Esqueci minha senha preparado
- Perfil do usuário
- Gestão de usuários
- Gestão de perfis
- Acesso negado

# Componentes
- ProtectedRoute
- PermissionGuard
- LoginForm
- UserMenu
- RoleBadge
- PermissionCheckboxList

# AUTH CONTEXT

Criar contexto global:

- Usuário autenticado
- Tokens
- Login
- Logout
- Refresh automático
- Permissões carregadas
- Verificação de permissão

# AXIOS INTERCEPTOR

Implementar:

- Inserir access token automaticamente
- Renovar token ao receber 401
- Redirecionar para login se refresh falhar
- Tratar erro global


ROTAS PROTEGIDAS

Exemplo:

<ProtectedRoute permission="financeiro.conta_pagar.visualizar">
  <ContasPagarPage />
</ProtectedRoute>

# SEGURANÇA

Obrigatório:

- Senhas hashadas
- JWT seguro
- Refresh token blacklist
- Não expor tokens em logs
- Não expor senha em serializer
- Validação server-side
- Rate limit preparado
- Auditoria
- Controle por permissão real, não apenas frontend


# SEED INICIAL

Criar comando ou fixture para:

- Criar permissões padrão
- Criar perfis padrão
- Criar usuário admin inicial
- Vincular todas as permissões ao Administrador

# TESTES

Criar testes:

# Autenticação
- Login válido
- Login inválido
- Login de usuário inativo
- Refresh token
- Logout
- Me endpoint

# RBAC
- Usuário com permissão acessa
- Usuário sem permissão recebe 403
- Administrador acessa tudo
- Permissão inexistente bloqueia acesso

# Usuários
- Criar usuário
- Bloquear email duplicado
- Alterar senha
- Inativar usuário


# NÃO FAZER

- Não usar usuário padrão sem controle
- Não confiar em permissão apenas no frontend
- Não expor senha
- Não salvar token em local inseguro sem estratégia
- Não deixar endpoint crítico sem RBAC
- Não permitir usuário inativo logar
- Não hardcodar permissões nas views sem padrão reutilizável

# FORMATO DA RESPOSTA

A resposta deve conter:

1. Visão geral da segurança
2. Modelagem RBAC
3. DER completo
4. Models
5. Serializers
6. Services
7. Selectors
8. Repositories
9. Views
10. URLs
11. Permissions
12. JWT setup
13 Auditoria de login
14. Seeds iniciais
15. Testes
16. Frontend Auth Context
17. Axios interceptor
18. ProtectedRoute
19. PermissionGuard
20. Explicação técnica
21. Melhorias futuras

OBJETIVO FINAL

Criar uma camada de autenticação e autorização robusta, segura, auditável e reutilizável para todos os módulos do Nexor ERP.