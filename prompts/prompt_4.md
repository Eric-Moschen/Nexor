# PROMPT 04 — MÓDULO FINANCEIRO DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- O padrão estrutural do Prompt 02 (Estoque)
- O padrão de fluxo operacional do Prompt 03 (Compras)

O objetivo desta etapa é implementar o MÓDULO FINANCEIRO do ERP de forma profissional, segura, auditável e preparada para crescimento empresarial real.

O módulo financeiro será um dos núcleos mais críticos do sistema.

Portanto:

- Não simplificar modelagem
- Não misturar responsabilidades
- Não criar lógica financeira procedural bagunçada
- Não ignorar rastreabilidade
- Não ignorar integridade financeira

---

# OBJETIVO

Implementar o módulo financeiro contendo:

- Contas a pagar
- Contas a receber
- Fluxo de caixa
- Centros de custo
- Categorias financeiras
- Baixas financeiras
- Parcelamentos
- Conciliação futura preparada
- Auditoria financeira
- Dashboard financeiro
- Integração com compras
- Integração futura com fiscal/NFe

---

# FUNCIONALIDADES OBRIGATÓRIAS

# 1. CONTAS A PAGAR

Campos:

- Número do lançamento
- Fornecedor
- Descrição
- Categoria financeira
- Centro de custo
- Valor original
- Valor atual
- Data emissão
- Data vencimento
- Status
- Tipo pagamento
- Observação
- Pedido de compra origem (opcional)
- Usuário responsável

Status:

- Pendente
- Parcialmente pago
- Pago
- Vencido
- Cancelado

---

# 2. CONTAS A RECEBER

Campos:

- Número do lançamento
- Cliente
- Descrição
- Categoria financeira
- Centro de custo
- Valor original
- Valor atual
- Data emissão
- Data vencimento
- Status
- Forma recebimento
- Observação
- Usuário responsável

Status:

- Pendente
- Parcialmente recebido
- Recebido
- Vencido
- Cancelado

---

# 3. BAIXAS FINANCEIRAS

Implementar estrutura de baixa financeira separada.

NÃO atualizar pagamento diretamente no lançamento principal.

Campos:

- Conta relacionada
- Tipo (pagamento/recebimento)
- Valor pago
- Data pagamento
- Multa
- Juros
- Desconto
- Observação
- Usuário responsável

Regras:

- Permitir pagamento parcial
- Permitir múltiplas baixas
- Atualizar saldo restante corretamente
- Atualizar status automaticamente

---

# 4. CENTRO DE CUSTO

Campos:

- Código
- Nome
- Descrição
- Status

Exemplos:

- Produção
- Administrativo
- Compras
- Manutenção
- Operacional

---

# 5. CATEGORIAS FINANCEIRAS

Campos:

- Nome
- Tipo
- Descrição
- Status

Tipos:

- Receita
- Despesa

---

# 6. FLUXO DE CAIXA

Implementar cálculo baseado em:

- Contas pagas
- Contas recebidas

Dashboard inicial contendo:

- Total a pagar
- Total a receber
- Fluxo mensal
- Contas vencidas
- Saldo projetado

---

# 7. PARCELAMENTO

Implementar parcelamento financeiro.

Exemplo:

- 12x
- vencimentos mensais automáticos

Regras:

- Gerar parcelas automaticamente
- Cada parcela deve possuir rastreabilidade
- Não duplicar informações manualmente

---

# MODELAGEM

Criar DER completo contendo:

- ContaPagar
- ContaReceber
- BaixaFinanceira
- CategoriaFinanceira
- CentroCusto
- Parcelamento
- Fornecedor
- Cliente
- Usuário

Aplicar:

- Constraints
- Índices
- Auditoria
- Soft delete preparado
- Integridade financeira
- Histórico preservado

---

# BACKEND

Implementar:

```txt
apps/financeiro/
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

Implementar em services.py

# Contas
- Criar conta
- Cancelar conta
- Atualizar status
- Validar vencimentos
- Calcular saldo restante

# Baixas
- Registrar baixa
- Registrar pagamento parcial
- Aplicar juros/multa/desconto
- Atualizar status automaticamente

# Parcelamento
- Gerar parcelas automáticas
- Calcular vencimentos
- Vincular parcelas à origem

# Fluxo de caixa
- Consolidar movimentações
- Calcular saldo diário/mensal
- Preparar dashboard

# API

Criar endpoints:

# Contas a pagar

GET    /api/v1/financeiro/contas-pagar/
POST   /api/v1/financeiro/contas-pagar/
GET    /api/v1/financeiro/contas-pagar/{id}/
PUT    /api/v1/financeiro/contas-pagar/{id}/
POST   /api/v1/financeiro/contas-pagar/{id}/baixar/
POST   /api/v1/financeiro/contas-pagar/{id}/cancelar/

# Contas a receber

GET    /api/v1/financeiro/contas-receber/
POST   /api/v1/financeiro/contas-receber/
GET    /api/v1/financeiro/contas-receber/{id}/
PUT    /api/v1/financeiro/contas-receber/{id}/
POST   /api/v1/financeiro/contas-receber/{id}/baixar/
POST   /api/v1/financeiro/contas-receber/{id}/cancelar/

# Fluxo de caixa

GET /api/v1/financeiro/fluxo-caixa/
GET /api/v1/financeiro/dashboard/


# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Pagamento registrado com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "Valor da baixa excede saldo pendente",
  "errors": {}
}


# VALIDAÇÕES

Implementar:

- Não permitir baixa maior que saldo
- Não permitir valor negativo
- Não permitir conta sem categoria
- Não permitir conta sem centro de custo
- Não permitir cancelamento após quitação total sem regra
- Não permitir parcela inválida
- Não permitir data vencimento inválida
- Não permitir conta sem responsável

# PERMISSÕES

Preparar RBAC:

- Administrador
- Financeiro
- Supervisor
- Compras (visualização parcial)
- Diretoria futura preparada

# INTEGRAÇÃO COM COMPRAS

Implementar integração:

- Pedido de compra aprovado pode gerar conta a pagar
- Histórico financeiro deve registrar origem
- Não duplicar contas automaticamente sem controle


# INTEGRAÇÃO FUTURA COM FISCAL

Preparar estrutura para:

- NFe entrada
- NFe saída
- Impostos
- XML
- Conciliação bancária futura

NÃO implementar ainda.


# FRONTEND

Criar telas:

- Dashboard financeiro
- Contas a pagar
- Contas a receber
- Cadastro financeiro
- Registro de baixa
- Fluxo de caixa
- Parcelamentos
- Categorias financeiras
- Centros de custo


# COMPONENTES

Criar:

- Cards financeiros
- Tabelas financeiras
- Badge de status
- Modal de baixa
- Modal de parcelamento
- Filtros avançados
- Gráficos financeiros
- Indicadores


# UX

Implementar:

- Dashboard corporativo
- Indicadores visuais
- Alertas de vencimento
- Alertas de inadimplência
- Loading states
- Empty states
- Confirmações críticas


# TESTES

Criar testes:

# Contas
- Criar conta válida
- Bloquear conta inválida
- Cancelar conta
- Atualizar status

# Baixas
- Pagamento parcial
- Pagamento total
- Múltiplas baixas
- Bloquear baixa inválida
- Aplicar juros/multa/desconto

# Parcelamentos
- Gerar parcelas
- Validar vencimentos
- Validar cálculos

# Fluxo
- Consolidar entradas
- Consolidar saídas
- Calcular saldo

# SEGURANÇA

Implementar:

- JWT obrigatório
- Auditoria financeira
- Logs financeiros
- Rastreabilidade
- transaction.atomic()
- Controle de permissões
- Validação server-side

# PERFORMANCE

Preparar:

- Índices financeiros
- Paginação
- select_related
- prefetch_related
- Queries otimizadas

# NÃO FAZER

- Não atualizar saldo manualmente sem service
- Não misturar pagamento com conta principal
- Não usar float para dinheiro
- Não ignorar auditoria
- Não criar cálculo financeiro no frontend
- Não ignorar transações do banco
- Não usar lógica procedural bagunçada


# IMPORTANTE

Utilizar obrigatoriamente:

Decimal
transaction.atomic()

Nunca utilizar float para valores financeiros.

# FORMATO DA RESPOSTA

A resposta deve conter:

1. Arquitetura financeira
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
13. Fluxo financeiro
14. Fluxo de baixas
15. Fluxo de parcelamento
16. Integração com compras
17. Dashboard financeiro
18. Testes
19. Estrutura frontend
20. Componentes React
21. Explicação técnica
22. Melhorias futuras


# OBJETIVO FINAL

Criar um módulo financeiro enterprise, auditável, seguro, desacoplado e preparado para operação empresarial real dentro do Nexor ERP.