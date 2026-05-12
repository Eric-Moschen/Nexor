# CONTEXTO PRINCIPAL DO PROJETO — NEXOR ERP

## VISÃO GERAL

O Nexor ERP é um sistema ERP web profissional, moderno, escalável e modular, desenvolvido para gerenciamento completo de empresas de pequeno e médio porte, inicialmente focado em empresas dos setores:

- Metalurgia
- Vidraçaria
- Prestação de serviços industriais
- Controle operacional interno

O sistema deve ser desenvolvido com arquitetura profissional, seguindo padrões enterprise, priorizando:

1. Segurança
2. Clareza arquitetural
3. Manutenibilidade
4. Escalabilidade
5. Performance

O projeto NÃO deve ser tratado como um “sistema simples”.
A arquitetura deve permitir crescimento futuro para SaaS multiempresa.

---

# OBJETIVO DO SISTEMA

Centralizar e automatizar os processos operacionais, administrativos, financeiros e fiscais da empresa.

O sistema deve controlar:

- Estoque
- Compras
- Entradas e saídas
- Ordens de serviço
- Financeiro
- Fluxo de caixa
- Contas a pagar
- Contas a receber
- Clientes
- Fornecedores
- Emissão de NFe (Portal Nacional)
- Relatórios
- Auditoria de operações
- Controle de usuários e permissões

---

# STACK OBRIGATÓRIA

## Backend
- Python 3.13+
- Django
- Django REST Framework
- PostgreSQL

## Frontend
- React
- Vite
- TailwindCSS
- Axios
- React Router DOM

## Infraestrutura
- Docker
- Docker Compose
- Redis
- Celery

## Autenticação
- JWT Authentication
- Controle RBAC (Role Based Access Control)

---

# PADRÕES DE ARQUITETURA

O sistema deve seguir:

- SOLID
- DRY
- KISS
- Separation of Concerns
- Clean Architecture
- Service Layer Pattern
- Repository Pattern quando necessário

---

# REGRAS IMPORTANTES

## O sistema deve:

- Ser modular
- Ter baixo acoplamento
- Ter alta coesão
- Ser facilmente expansível
- Permitir novos módulos sem refatoração massiva
- Ter APIs REST padronizadas
- Ser preparado para multiempresa futuramente

---

# ESTRUTURA ESPERADA DO BACKEND

/backend
│
├── apps
│   ├── accounts
│   ├── core
│   ├── estoque
│   ├── compras
│   ├── financeiro
│   ├── fiscal
│   ├── os
│   ├── relatorios
│   ├── clientes
│   ├── fornecedores
│   └── auditoria
│
├── config
│
├── requirements
│
├── docker
│
└── manage.py

---

# ESTRUTURA ESPERADA DO FRONTEND

/frontend
│
├── src
│   ├── api
│   ├── components
│   ├── layouts
│   ├── pages
│   ├── routes
│   ├── services
│   ├── hooks
│   ├── contexts
│   ├── store
│   ├── utils
│   └── styles
│
├── public
│
└── package.json

---

# PADRÃO VISUAL

O sistema deve possuir:

- Visual moderno
- Design corporativo
- Interface limpa
- UX profissional
- Responsividade
- Componentização reutilizável

## Paleta recomendada

- Azul escuro
- Grafite
- Branco
- Roxo para destaque

---

# MÓDULOS PRINCIPAIS

# 1. AUTENTICAÇÃO E USUÁRIOS

## Funcionalidades
- Login
- Logout
- Refresh token
- Recuperação de senha
- Controle de sessão
- Permissões por perfil
- Auditoria de login

## Perfis iniciais
- Administrador
- Financeiro
- Estoque
- Compras
- Operacional
- Supervisor

---

# 2. ESTOQUE

## Funcionalidades
- Cadastro de produtos
- Controle de saldo
- Movimentações
- Entrada de materiais
- Saída de materiais
- Histórico
- Inventário
- Unidade de medida
- Controle mínimo de estoque
- Alertas de baixo estoque

---

# 3. COMPRAS

## Funcionalidades
- Solicitação de compra
- Aprovação
- Pedido de compra
- Fornecedores
- Histórico de compras
- Status do pedido

---

# 4. FINANCEIRO

## Funcionalidades
- Contas a pagar
- Contas a receber
- Fluxo de caixa
- Centro de custo
- Conciliação
- Relatórios financeiros

---

# 5. ORDENS DE SERVIÇO

## Funcionalidades
- Abertura de OS
- Status
- Prioridade
- Horas trabalhadas
- Materiais utilizados
- Responsáveis
- Histórico da OS
- Finalização

---

# 6. FISCAL

## Funcionalidades
- Emissão de NFe
- Cadastro fiscal
- Impostos
- Integração SEFAZ
- XML/PDF DANFE

---

# 7. RELATÓRIOS

## Funcionalidades
- PDF
- Excel
- Dashboards
- Indicadores
- Filtros avançados

---

# BANCO DE DADOS

O banco deve ser modelado corretamente utilizando:

- Normalização adequada
- Chaves estrangeiras
- Índices
- Constraints
- Auditoria
- Soft delete quando necessário

---

# SEGURANÇA

Obrigatório implementar:

- JWT seguro
- Refresh token
- Proteção CSRF
- Rate limit
- Validação server-side
- Sanitização
- Controle de permissões
- Logs de auditoria

---

# API

## Padrão REST

Utilizar:

- Versionamento
- Paginação
- Filtros
- Ordenação
- Responses padronizadas

## Exemplo

/api/v1/estoque/produtos/
/api/v1/financeiro/contas-pagar/
/api/v1/os/

---

# QUALIDADE

O sistema deve possuir:

- Testes automatizados
- Estrutura preparada para CI/CD
- Logs estruturados
- Tratamento de erros centralizado

---

# NÃO FAZER

- Não criar código acoplado
- Não misturar regra de negócio em views
- Não criar lógica complexa no frontend
- Não usar gambiarra
- Não ignorar validações
- Não usar arquitetura monolítica bagunçada

---

# EXPECTATIVA DAS RESPOSTAS FUTURAS

Todas as respostas futuras relacionadas ao Nexor ERP devem:

- Respeitar este contexto
- Seguir arquitetura enterprise
- Utilizar boas práticas
- Priorizar manutenibilidade
- Priorizar segurança
- Explicar decisões técnicas
- Criticar abordagens ruins
- Propor soluções profissionais
- Pensar em escalabilidade futura

---

# OBJETIVO FINAL

Criar um ERP profissional, robusto, modular e preparado para crescimento empresarial real, evitando limitações arquiteturais futuras.