# PROMPT 03 — MÓDULO DE COMPRAS DO NEXOR ERP

Utilize integralmente o contexto principal do projeto Nexor ERP, a estrutura criada no Prompt 01 e o padrão arquitetural definido no Prompt 02 para o módulo de Estoque.

O objetivo desta etapa é implementar o MÓDULO DE COMPRAS, integrado ao estoque, fornecedores e financeiro futuro.

Este módulo deve controlar o processo completo de solicitação, aprovação e acompanhamento de compras da empresa.

---

# OBJETIVO

Implementar o módulo de compras contendo:

- Solicitações de compra
- Itens da solicitação
- Aprovação/reprovação
- Pedidos de compra
- Fornecedores
- Status do processo
- Integração com estoque
- Preparação para financeiro
- Auditoria
- APIs REST
- Frontend inicial

---

# FUNCIONALIDADES OBRIGATÓRIAS

## 1. SOLICITAÇÃO DE COMPRA

Campos:

- Número da solicitação
- Solicitante
- Centro de custo
- Justificativa
- Prioridade
- Status
- Data da solicitação
- Data de aprovação
- Aprovador
- Observações

Status:

- Rascunho
- Pendente de aprovação
- Aprovada
- Reprovada
- Convertida em pedido
- Cancelada

Prioridade:

- Baixa
- Média
- Alta
- Urgente

---

## 2. ITENS DA SOLICITAÇÃO

Campos:

- Produto
- Descrição livre
- Quantidade solicitada
- Unidade de medida
- Observação
- Status do item

Regras:

- Deve permitir item vinculado a produto existente
- Deve permitir item ainda não cadastrado
- Quantidade deve ser maior que zero
- Não permitir solicitação sem itens

---

## 3. APROVAÇÃO

Implementar fluxo de aprovação:

- Apenas usuários autorizados podem aprovar
- Solicitação aprovada não pode ser editada livremente
- Solicitação reprovada deve exigir motivo
- Toda aprovação/reprovação deve gerar registro de auditoria

---

## 4. PEDIDO DE COMPRA

Campos:

- Número do pedido
- Solicitação origem
- Fornecedor
- Data do pedido
- Previsão de entrega
- Status
- Valor total
- Observações

Status:

- Aberto
- Enviado ao fornecedor
- Parcialmente recebido
- Recebido
- Cancelado

---

## 5. ITENS DO PEDIDO

Campos:

- Produto
- Descrição
- Quantidade
- Valor unitário
- Valor total
- Quantidade recebida

Regras:

- Valor total deve ser calculado
- Quantidade recebida não pode exceder quantidade comprada
- Pedido recebido deve preparar entrada no estoque

---

## 6. FORNECEDORES

Caso o módulo de fornecedores ainda não esteja implementado, criar estrutura mínima contendo:

- Razão social
- Nome fantasia
- CNPJ/CPF
- Email
- Telefone
- Status ativo/inativo

---

# MODELAGEM

Criar DER completo contendo:

- SolicitacaoCompra
- ItemSolicitacaoCompra
- PedidoCompra
- ItemPedidoCompra
- Fornecedor
- Produto
- UnidadeMedida
- Usuário

Aplicar:

- Chaves estrangeiras
- Índices
- Constraints
- Soft delete preparado
- Auditoria preparada
- Integridade relacional

---

# BACKEND

Implementar no app `compras`:

```txt
apps/compras/
├── models.py
├── serializers.py
├── services.py
├── selectors.py
├── repositories.py
├── views.py
├── urls.py
├── permissions.py
├── validators.py
└── tests/

# REGRAS DE NEGÓCIO

Implementar em services.py:

# Solicitação

- Criar solicitação com itens
- Enviar para aprovação
- Aprovar solicitação
- Reprovar solicitação
- Cancelar solicitação
- Converter solicitação em pedido

# Pedido

- Criar pedido a partir de solicitação aprovada
- Atualizar status
- Registrar recebimento parcial
- Registrar recebimento total
- Preparar integração com entrada de estoque

# API

Criar endpoints REST:

# Solicitações

GET    /api/v1/compras/solicitacoes/
POST   /api/v1/compras/solicitacoes/
GET    /api/v1/compras/solicitacoes/{id}/
PUT    /api/v1/compras/solicitacoes/{id}/
DELETE /api/v1/compras/solicitacoes/{id}/
POST   /api/v1/compras/solicitacoes/{id}/enviar-aprovacao/
POST   /api/v1/compras/solicitacoes/{id}/aprovar/
POST   /api/v1/compras/solicitacoes/{id}/reprovar/
POST   /api/v1/compras/solicitacoes/{id}/cancelar/
POST   /api/v1/compras/solicitacoes/{id}/converter-pedido/

# Pedidos

GET    /api/v1/compras/pedidos/
POST   /api/v1/compras/pedidos/
GET    /api/v1/compras/pedidos/{id}/
PUT    /api/v1/compras/pedidos/{id}/
POST   /api/v1/compras/pedidos/{id}/recebimento-parcial/
POST   /api/v1/compras/pedidos/{id}/recebimento-total/
POST   /api/v1/compras/pedidos/{id}/cancelar/


# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Solicitação criada com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "Solicitação não pode ser aprovada",
  "errors": {}
}

# VALIDAÇÕES

Implementar:

- Solicitação precisa ter pelo menos 1 item
- Quantidade maior que zero
- Reprovação exige motivo
- Apenas solicitação pendente pode ser aprovada
- Apenas solicitação aprovada pode virar pedido
- Pedido cancelado não pode receber itens
- Quantidade recebida não pode passar da quantidade comprada
- Fornecedor obrigatório para pedido
- Valor unitário não pode ser negativo


# PERMISSÕES

Preparar RBAC:

- Administrador: acesso total
- Compras: criar e gerenciar pedidos
- Supervisor: aprovar/reprovar solicitações
- Estoque: visualizar pedidos e registrar recebimento
- Financeiro: visualizar dados de compra para contas a pagar


# INTEGRAÇÃO COM ESTOQUE

Preparar integração com o módulo de estoque:

- Pedido recebido deve gerar entrada de estoque
- Recebimento parcial deve movimentar apenas quantidade recebida
- Histórico deve registrar origem da compra
- Não atualizar estoque diretamente fora do service

Obrigatório usar:

transaction.atomic()

# FRONTEND

Criar telas:

- Lista de solicitações de compra
- Nova solicitação
- Detalhes da solicitação
- Aprovação de solicitação
- Lista de pedidos de compra
- Detalhes do pedido
- Registro de recebimento

Componentes:

- Tabela de solicitações
- Formulário de solicitação
- Formulário de itens
- Badge de status
- Modal de aprovação/reprovação
- Modal de recebimento
- Toast de feedback

# UX

Implementar:

- Loading states
- Empty states
- Mensagens de erro claras
- Confirmação antes de cancelar
- Bloqueio visual para ações não permitidas
- Filtros por status, fornecedor e período


# TESTES

Criar testes para:

Solicitações
- Criar solicitação válida
- Bloquear solicitação sem itens
- Enviar para aprovação
- Aprovar solicitação
- Reprovar com motivo
- Bloquear reprovação sem motivo
- Converter solicitação aprovada em pedido

Pedidos
- Criar pedido válido
- Registrar recebimento parcial
- Registrar recebimento total
- Bloquear recebimento acima da quantidade
- Cancelar pedido

# NÃO FAZER

- Não colocar regra de aprovação na view
- Não atualizar estoque diretamente no controller/view
- Não permitir pedido sem fornecedor
- Não permitir solicitação aprovada ser editada sem regra clara
- Não criar status soltos como string sem enum/choices
- Não ignorar auditoria
- Não criar fluxo financeiro ainda, apenas preparar integração


FORMATO DA RESPOSTA

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
11. Validações
12. Endpoints
13. Fluxo de aprovação
14. Fluxo de pedido
15. Integração com estoque
16. Testes
17. Estrutura frontend
18. Componentes React
19. Explicação técnica
20. Melhorias futuras

# OBJETIVO FINAL

Criar um módulo de compras profissional, auditável, seguro e integrado ao estoque, servindo como base para os módulos financeiro e fiscal do Nexor ERP.