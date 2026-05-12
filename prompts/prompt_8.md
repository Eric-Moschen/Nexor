# PROMPT 08 — MÓDULO DE CLIENTES, FORNECEDORES E CRM OPERACIONAL DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- O módulo de Estoque do Prompt 02
- O módulo de Compras do Prompt 03
- O módulo Financeiro do Prompt 04
- O módulo Fiscal/NFe do Prompt 05
- O módulo de Ordens de Serviço do Prompt 06
- O módulo de Orçamentos do Prompt 07

O objetivo desta etapa é implementar os módulos de:

- Clientes
- Fornecedores
- CRM operacional
- Histórico comercial e operacional
- Contatos
- Endereços
- Interações
- Documentação empresarial

Este módulo será a BASE CENTRAL DE RELACIONAMENTO do ERP.

Toda operação futura dependerá desses dados.

Portanto:

- Não criar cadastro simples demais
- Não ignorar rastreabilidade
- Não duplicar dados
- Não misturar pessoa física/jurídica sem estratégia
- Não criar estrutura limitada

---

# OBJETIVO

Implementar os módulos de:

- Clientes
- Fornecedores
- Contatos
- Endereços
- Histórico de relacionamento
- Interações comerciais
- CRM operacional
- Classificação de clientes
- Classificação de fornecedores
- Documentos
- APIs REST
- Frontend profissional

---

# FUNCIONALIDADES OBRIGATÓRIAS

# 1. CLIENTES

Campos:

- Tipo pessoa
- Nome/Razão social
- Nome fantasia
- CPF/CNPJ
- Inscrição estadual
- Inscrição municipal
- Email principal
- Telefone principal
- WhatsApp
- Status
- Limite de crédito futuro preparado
- Observações
- Data cadastro
- Usuário responsável

Tipos:

- Pessoa Física
- Pessoa Jurídica

Status:

- Ativo
- Inativo
- Bloqueado

---

# 2. FORNECEDORES

Campos:

- Tipo pessoa
- Razão social
- Nome fantasia
- CPF/CNPJ
- Inscrição estadual
- Email
- Telefone
- WhatsApp
- Categoria fornecedor
- Status
- Observações
- Usuário responsável

Categorias:

- Matéria-prima
- Ferramentas
- Serviços
- Transporte
- Terceirizados
- Outros

---

# 3. ENDEREÇOS

Permitir múltiplos endereços.

Campos:

- CEP
- Rua
- Número
- Complemento
- Bairro
- Cidade
- UF
- Código IBGE
- Tipo endereço

Tipos:

- Comercial
- Cobrança
- Entrega
- Fiscal

---

# 4. CONTATOS

Permitir múltiplos contatos.

Campos:

- Nome
- Cargo
- Email
- Telefone
- WhatsApp
- Observação
- Principal ou não

---

# 5. CRM OPERACIONAL

Criar estrutura de interações.

Campos:

- Cliente
- Tipo interação
- Descrição
- Responsável
- Data
- Próximo contato
- Status

Tipos:

- Ligação
- WhatsApp
- Email
- Visita
- Reunião
- Suporte
- Pós-venda

Status:

- Aberto
- Em andamento
- Finalizado

---

# 6. HISTÓRICO

Registrar automaticamente:

- Criação
- Alterações
- Aprovações
- Orçamentos vinculados
- OS vinculadas
- Compras vinculadas
- NFe vinculadas
- Contatos realizados
- Alterações cadastrais

Nunca apagar histórico.

---

# 7. DOCUMENTOS

Permitir anexos futuros preparados:

- Contratos
- PDFs
- Imagens
- Certificados
- Documentos fiscais

Preparar estrutura para armazenamento desacoplado.

NÃO armazenar arquivo diretamente no banco.

---

# MODELAGEM

Criar DER completo contendo:

- Cliente
- Fornecedor
- Endereco
- Contato
- InteracaoCRM
- HistoricoRelacionamento
- DocumentoRelacionamento
- Orcamento
- OrdemServico
- PedidoCompra
- NotaFiscal
- Usuario

Aplicar:

- Constraints
- Índices
- Auditoria
- Soft delete preparado
- Integridade relacional
- Histórico completo

---

# BACKEND

Implementar:

```txt
apps/clientes/
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

apps/fornecedores/
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


# REGRAS DE NEGÓCIO

Implementar em services.py.

# Clientes
- Criar cliente
- Atualizar cliente
- Bloquear cliente
- Inativar cliente
- Validar CPF/CNPJ
- Validar IE
- Registrar histórico

# Fornecedores
- Criar fornecedor
- Atualizar fornecedor
- Inativar fornecedor
- Validar documentos
- Registrar histórico

# CRM
- Registrar interação
- Atualizar interação
- Finalizar interação
- Gerar lembrete futuro preparado


# API

Criar endpoints:

# Clientes

GET    /api/v1/clientes/
POST   /api/v1/clientes/
GET    /api/v1/clientes/{id}/
PUT    /api/v1/clientes/{id}/
DELETE /api/v1/clientes/{id}/
GET    /api/v1/clientes/{id}/historico/
GET    /api/v1/clientes/{id}/interacoes/
POST   /api/v1/clientes/{id}/interacoes/

# Fornecedores

GET    /api/v1/fornecedores/
POST   /api/v1/fornecedores/
GET    /api/v1/fornecedores/{id}/
PUT    /api/v1/fornecedores/{id}/
DELETE /api/v1/fornecedores/{id}/
GET    /api/v1/fornecedores/{id}/historico/

# CRM

GET    /api/v1/crm/interacoes/
POST   /api/v1/crm/interacoes/
PUT    /api/v1/crm/interacoes/{id}/
POST   /api/v1/crm/interacoes/{id}/finalizar/

# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Cliente criado com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "CNPJ inválido",
  "errors": {}
}

# VALIDAÇÕES

Implementar:

- CPF válido
- CNPJ válido
- IE válida conforme UF
- Email válido
- CEP válido
- Cliente precisa possuir nome
- Fornecedor precisa possuir razão social
- Não permitir duplicidade de CPF/CNPJ ativo
- Não permitir interação sem responsável
- Não permitir exclusão física de cliente/fornecedor

# PERMISSÕES

Preparar RBAC:

- Administrador
- Comercial
- Compras
- Financeiro
- Operacional
- Supervisor

# INTEGRAÇÃO COM ORÇAMENTOS

Obrigatório:

- Orçamento deve utilizar cliente
- Histórico deve mostrar orçamentos vinculados


# INTEGRAÇÃO COM OS

Obrigatório:

- OS deve utilizar cliente
- Histórico operacional deve aparecer no cliente

# INTEGRAÇÃO COM FINANCEIRO

Obrigatório:

- Cliente vinculado a contas a receber
- Fornecedor vinculado a contas a pagar

# INTEGRAÇÃO COM FISCAL

Obrigatório:

- Dados fiscais centralizados
- Não duplicar cadastro fiscal em outros módulos
- Serviços fiscais devem consultar módulo de clientes/fornecedores

# FRONTEND

Criar telas:

- Lista de clientes
- Cadastro de cliente
- Detalhes do cliente
- Lista de fornecedores
- Cadastro de fornecedor
- CRM operacional
- Histórico
- Interações
- Contatos
- Endereços


# COMPONENTES

Criar:

- Tabela de clientes
- Tabela de fornecedores
- Card de informações
- Timeline de histórico
- Modal de interação
- Formulário reutilizável
- Badge de status
- Badge de categoria
- Tabs de navegação

# UX

Implementar:

- Busca rápida
- Filtros avançados
- Loading states
- Empty states
- Timeline de relacionamento
- Histórico visual
- Alertas de bloqueio
- Feedback claro

# TESTES

Criar testes:

# Clientes
- Criar cliente válido
- Bloquear CPF inválido
- Bloquear CNPJ inválido
- Bloquear duplicidade
- Inativar cliente

# Fornecedores
- Criar fornecedor válido
- Validar IE
- Inativar fornecedor

# CRM
- Registrar interação
- Finalizar interação
- Validar responsável

# SEGURANÇA

Implementar:

- JWT obrigatório
- Auditoria completa
- Logs de alteração
- Controle de permissões
- Soft delete
- Validação server-side

# PERFORMANCE

Preparar:

- Índices por CPF/CNPJ
- Índices por status
- Índices por nome
- Paginação
- select_related
- prefetch_related
- Queries otimizadas

# NÃO FAZER

- Não duplicar cadastro fiscal
- Não apagar cliente fisicamente
- Não armazenar arquivos no banco
- Não misturar lógica CRM nas views
- Não confiar em validação frontend
- Não usar estrutura procedural bagunçada
- Não ignorar histórico

IMPORTANTE

Utilizar obrigatoriamente:

transaction.atomic()

Preparar estrutura para crescimento futuro:

- Multiempresa
- CRM avançado
- Pipeline comercial
- SLA
- Tickets
- Portal do cliente


# FORMATO DA RESPOSTA

A resposta deve conter:

1. Visão geral do módulo
2. DER completo
3. Models
4. Serializers
5. Services
6. Selectors
7. Repositories
8. Views
9. URLs
10. Permissions
11. Enums
12. Validações
13. Fluxo CRM
14. Histórico de relacionamento
15. Integração com orçamento
16. Integração com OS
17. Integração com financeiro
18. Integração com fiscal
19. Testes
20. Estrutura frontend
21. Componentes React
22. Explicação técnica
23. Melhorias futuras

# OBJETIVO FINAL

Criar um módulo centralizado de Clientes, Fornecedores e CRM operacional profissional, seguro e auditável, servindo como núcleo de relacionamento empresarial do Nexor ERP.