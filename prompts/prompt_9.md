# PROMPT 09 — MÓDULO DE DASHBOARD, RELATÓRIOS E BUSINESS INTELLIGENCE DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- O módulo de Estoque do Prompt 02
- O módulo de Compras do Prompt 03
- O módulo Financeiro do Prompt 04
- O módulo Fiscal/NFe do Prompt 05
- O módulo de Ordens de Serviço do Prompt 06
- O módulo de Orçamentos do Prompt 07
- O módulo de Clientes/CRM do Prompt 08

O objetivo desta etapa é implementar o módulo de:

- Dashboards
- Indicadores
- KPIs
- Relatórios gerenciais
- Relatórios operacionais
- Business Intelligence operacional
- Analytics internos
- Exportações
- Gráficos
- Monitoramento de performance empresarial

Este módulo será o CENTRO DE INTELIGÊNCIA DO ERP.

Portanto:

- Não criar dashboards genéricos
- Não fazer queries pesadas diretamente nas views
- Não gerar relatórios sem otimização
- Não misturar regra operacional com camada analítica
- Não criar gráficos sem estrutura de dados adequada

---

# OBJETIVO

Implementar o módulo de dashboards e relatórios contendo:

- Dashboard executivo
- Dashboard operacional
- Dashboard financeiro
- Dashboard comercial
- Dashboard estoque
- Indicadores em tempo real
- Relatórios PDF
- Relatórios Excel
- Exportações CSV
- Gráficos
- Filtros avançados
- Consolidação de dados
- Cache preparado
- APIs analíticas

---

# FUNCIONALIDADES OBRIGATÓRIAS

# 1. DASHBOARD EXECUTIVO

Exibir:

- Total faturado
- Total recebido
- Total em aberto
- Total de OS abertas
- Total de orçamentos pendentes
- Total de compras pendentes
- Produtos com baixo estoque
- Fluxo financeiro resumido
- Indicadores mensais

---

# 2. DASHBOARD FINANCEIRO

Exibir:

- Contas a pagar
- Contas a receber
- Inadimplência
- Fluxo de caixa
- Projeção financeira
- Receita mensal
- Despesa mensal
- Margem operacional
- Evolução financeira

---

# 3. DASHBOARD ESTOQUE

Exibir:

- Produtos sem estoque
- Produtos abaixo do mínimo
- Produtos mais movimentados
- Entradas e saídas
- Giro de estoque
- Custo de estoque
- Produtos parados

---

# 4. DASHBOARD COMERCIAL

Exibir:

- Orçamentos enviados
- Taxa de aprovação
- Taxa de conversão
- Clientes ativos
- Clientes inativos
- Ticket médio
- OS faturadas
- Receita por cliente

---

# 5. DASHBOARD OPERACIONAL

Exibir:

- OS em execução
- OS atrasadas
- Horas apontadas
- Produtividade
- Custos operacionais
- Serviços mais executados
- Colaboradores mais ativos

---

# 6. RELATÓRIOS

Implementar relatórios:

## Financeiros

- Fluxo de caixa
- Contas vencidas
- Contas pagas
- Contas recebidas
- Resultado mensal

## Estoque

- Inventário
- Movimentações
- Giro de estoque
- Produtos críticos

## Compras

- Compras por fornecedor
- Pedidos pendentes
- Histórico de compras

## OS

- OS por status
- Custos por OS
- Horas por colaborador
- Materiais utilizados

## Comercial

- Orçamentos
- Conversões
- Clientes ativos
- Receita por cliente

---

# 7. EXPORTAÇÕES

Implementar:

- PDF
- Excel
- CSV

Preparar geração assíncrona via Celery.

---

# 8. FILTROS AVANÇADOS

Implementar filtros:

- Data inicial/final
- Cliente
- Fornecedor
- Status
- Centro de custo
- Categoria
- Responsável
- Tipo de operação

---

# MODELAGEM

Criar DER contendo:

- DashboardCache
- RelatorioGerado
- ExportacaoArquivo
- Usuario
- Integrações com módulos existentes

Aplicar:

- Auditoria
- Controle de geração
- Histórico de exportações
- Controle de permissões

---

# BACKEND

Implementar no app `relatorios`:

```txt
apps/relatorios/
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
├── exports/
│   ├── pdf_exporter.py
│   ├── excel_exporter.py
│   └── csv_exporter.py
├── dashboards/
│   ├── financeiro_dashboard.py
│   ├── estoque_dashboard.py
│   ├── operacional_dashboard.py
│   └── comercial_dashboard.py
└── tests/

# REGRAS DE NEGÓCIO

Implementar em services.py.

# Dashboard
- Consolidar dados
- Calcular indicadores
- Aplicar filtros
- Utilizar cache
- Evitar queries pesadas repetidas

# Relatórios
- Gerar relatório
- Registrar histórico
- Exportar arquivo
- Permitir download seguro

# Exportações
- Gerar PDF
- Gerar Excel
- Gerar CSV
- Executar tarefas pesadas via Celery

# API

Criar endpoints:

# Dashboards

GET /api/v1/dashboard/executivo/
GET /api/v1/dashboard/financeiro/
GET /api/v1/dashboard/estoque/
GET /api/v1/dashboard/comercial/
GET /api/v1/dashboard/operacional/

# Relatórios

GET /api/v1/relatorios/financeiro/
GET /api/v1/relatorios/estoque/
GET /api/v1/relatorios/comercial/
GET /api/v1/relatorios/os/
GET /api/v1/relatorios/compras/

# Exportações

POST /api/v1/relatorios/exportar/pdf/
POST /api/v1/relatorios/exportar/excel/
POST /api/v1/relatorios/exportar/csv/
GET  /api/v1/relatorios/exportacoes/

# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Relatório gerado com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "Falha ao gerar relatório",
  "errors": {}
}

# VALIDAÇÕES

Implementar:

- Intervalo de datas válido
- Usuário autorizado
- Limite de exportações simultâneas preparado
- Filtros válidos
- Não permitir acesso a dados sem permissão

# PERMISSÕES

Preparar RBAC:

- Administrador
- Diretoria
- Financeiro
- Comercial
- Operacional
- Supervisor

Cada dashboard deve respeitar permissões de acesso.


# PERFORMANCE

OBRIGATÓRIO:

- select_related
- prefetch_related
- annotate
- aggregate
- paginação
- cache
- queries otimizadas
- evitar N+1 queries

Preparar:

- Redis cache
- Celery async tasks

# CELERY

Utilizar Celery para:

- Geração de PDF
- Geração de Excel
- Exportações pesadas
- Consolidação de indicadores
- Atualização de cache

# FRONTEND

Criar telas:

- Dashboard executivo
- Dashboard financeiro
- Dashboard operacional
- Dashboard comercial
- Dashboard estoque
- Central de relatórios
- Histórico de exportações

# COMPONENTES

Criar:

- Cards KPI
- Gráficos
- Tabelas analíticas
- Filtros avançados
- Calendário de período
- Export buttons
- Loading analytics
- Empty analytics
- Indicadores visuais
- Timeline financeira


# GRÁFICOS

Implementar:

- Barras
- Linha
- Pizza
- Área
- Evolução temporal

Utilizar biblioteca madura e estável.

Sugestão:

- Recharts

# UX

Implementar:

- Dashboard responsivo
- Atualização dinâmica
- Skeleton loading
- Feedback visual
- Exportação visual
- Alertas críticos
- Indicadores coloridos
- Experiência corporativa


# TESTES

Criar testes:

# Dashboards
- Consolidar indicadores
- Aplicar filtros
- Validar permissões

# Relatórios
- Gerar relatório válido
- Exportar PDF
- Exportar Excel
- Exportar CSV

# Performance
- Garantir queries otimizadas
- Evitar N+1


# SEGURANÇA

Implementar:

- JWT obrigatório
- Controle RBAC
- Auditoria de exportação
- Controle de acesso aos relatórios
- Download seguro
- Logs de geração
- Validação server-side

# NÃO FAZER

- Não gerar dashboard com query pesada na view
- Não calcular KPI no frontend
- Não gerar exportação síncrona pesada
- Não ignorar cache
- Não ignorar permissões
- Não usar gráficos improvisados
- Não expor arquivos publicamente sem controle
- Não usar lógica procedural bagunçada


# IMPORTANTE

Utilizar obrigatoriamente:

Celery
Redis Cache
transaction.atomic()

Preparar estrutura para:

- BI avançado
- Data warehouse futuro
- Indicadores multiempresa
- Metas
- SLA
- KPIs customizados


# FORMATO DA RESPOSTA

A resposta deve conter:

1. Visão geral do módulo
2. Arquitetura analítica
3. DER completo
4. Models
5. Serializers
6. Services
7. Selectors
8. Repositories
9. Views
10. URLs
11. Permissions
12. Enums
13. Estrutura de dashboards
14. Estrutura de relatórios
15. Exportadores PDF/Excel/CSV
16. Integração com módulos existentes
17. Estratégia de cache
18. Estratégia Celery
19. Testes
20. Estrutura frontend
21. Componentes React
22. Estrutura de gráficos
23. Explicação técnica
24. Melhorias futuras

OBJETIVO FINAL

Criar um módulo de Dashboard, Relatórios e Business Intelligence profissional, escalável e performático, servindo como centro analítico do Nexor ERP.
