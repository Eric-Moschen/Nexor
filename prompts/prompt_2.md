# PROMPT 02 — MODELAGEM E IMPLEMENTAÇÃO DO PRIMEIRO MÓDULO DO NEXOR ERP

Utilize integralmente o contexto principal do projeto Nexor ERP e toda a estrutura criada no Prompt 01.

O objetivo desta etapa é implementar o PRIMEIRO MÓDULO REAL DO ERP utilizando arquitetura enterprise, modelagem correta, separação de responsabilidades e estrutura preparada para crescimento futuro.

O módulo escolhido para esta etapa será:

# MÓDULO DE ESTOQUE

Este módulo será a base operacional do ERP e impactará diretamente:

- Compras
- Financeiro
- Ordens de Serviço
- Fiscal
- Inventário
- Movimentações
- Custos
- Relatórios

Portanto, a modelagem deve ser feita corretamente desde o início.

---

# OBJETIVO

Implementar o módulo completo de estoque contendo:

- Modelagem de banco profissional
- APIs REST
- Regras de negócio desacopladas
- Controle de movimentações
- Controle de saldo
- Histórico
- Validações
- Estrutura frontend inicial
- Preparação para auditoria
- Preparação para multiempresa futura

---

# FUNCIONALIDADES OBRIGATÓRIAS

# 1. PRODUTOS

Implementar cadastro de produtos contendo:

- Código interno
- Código SKU
- Código de barras
- Nome
- Descrição
- Categoria
- Unidade de medida
- Marca
- Custo médio
- Preço de venda
- Estoque mínimo
- Estoque atual
- Status ativo/inativo
- Data de criação
- Data de atualização

---

# 2. CATEGORIAS

Implementar categorias de produtos contendo:

- Nome
- Descrição
- Status

---

# 3. UNIDADES DE MEDIDA

Implementar unidades:

Exemplos:

- UN
- KG
- MT
- CX
- PC

---

# 4. MOVIMENTAÇÕES DE ESTOQUE

Implementar movimentações contendo:

- Entrada
- Saída
- Ajuste
- Transferência futura preparada

Campos:

- Produto
- Tipo movimentação
- Quantidade
- Saldo anterior
- Saldo posterior
- Usuário responsável
- Observação
- Data movimentação

---

# 5. REGRAS DE NEGÓCIO

Implementar regras obrigatórias:

## Entrada

- Soma saldo corretamente

## Saída

- Não permitir estoque negativo
- Validar saldo antes

## Ajuste

- Registrar histórico
- Atualizar saldo corretamente

## Auditoria

Toda movimentação deve ficar registrada.

Nunca apagar histórico.

---

# MODELAGEM

Criar modelagem profissional.

## Criar DER completo contendo:

- Produto
- Categoria
- UnidadeMedida
- MovimentacaoEstoque

## Relacionamentos corretos

## Índices

## Constraints

## Soft delete preparado

## Auditoria preparada

---

# BACKEND

Implementar:

## Models

## Serializers

## Services

Toda regra de negócio deve ficar em services.

## Selectors

Separar consultas complexas.

## Repositories

Preparar abstração de persistência.

## Views

Views enxutas.

## URLs

Separadas por módulo.

## Permissions

Preparar RBAC.

---

# API

Criar endpoints REST:

# Produtos

```txt
GET    /api/v1/estoque/produtos/
POST   /api/v1/estoque/produtos/
GET    /api/v1/estoque/produtos/{id}/
PUT    /api/v1/estoque/produtos/{id}/
DELETE /api/v1/estoque/produtos/{id}/

# Categorias

GET    /api/v1/estoque/categorias/
POST   /api/v1/estoque/categorias/


# Movimentações

POST   /api/v1/estoque/movimentacoes/entrada/
POST   /api/v1/estoque/movimentacoes/saida/
POST   /api/v1/estoque/movimentacoes/ajuste/
GET    /api/v1/estoque/movimentacoes/

# RESPONSE PADRONIZADA

Padronizar responses:

Sucesso

{
  "success": true,
  "message": "Produto criado com sucesso",
  "data": {}
}

Erro

{
  "success": false,
  "message": "Saldo insuficiente",
  "errors": {}
}

# VALIDAÇÕES

Implementar:

- SKU único
- Código interno único
- Estoque mínimo >= 0
- Quantidade movimentação > 0
- Produto ativo
- Não permitir saída sem saldo

# FRONTEND

Criar estrutura inicial React do módulo.

Implementar:

# Páginas
- Listagem de produtos
- Cadastro de produto
- Movimentação estoque
- Histórico movimentações

# Componentes
- Tabela reutilizável
- Formulário reutilizável
- Modal
- Toast
- Inputs padronizados

# UX
- Loading states
- Empty states
- Mensagens de erro
- Validação frontend

# TAILWIND

Criar layout profissional:

- Dashboard corporativo
- Sidebar
- Header
- Cards
- Tabelas modernas
- Formulários limpos
- Responsividade

# SEGURANÇA

Implementar:

- JWT obrigatório
- Permissões por perfil
- Auditoria
- Validação server-side
- Sanitização
- Logs preparados

# TESTES

Criar:

# Testes unitários

- Regras de estoque
- Entrada
- Saída
- Ajuste

# Testes de API

- CRUD produto
- Movimentações

QUALIDADE

Aplicar:

- SOLID
- DRY
- KISS
- Clean Code
- Separation of Concerns

# NÃO FAZER

- Não colocar regra de negócio na view
- Não atualizar estoque diretamente na model sem service
- Não criar código duplicado
- Não criar endpoint sem validação
- Não usar lógica procedural bagunçada
- Não ignorar transações do banco


IMPORTANTE

Utilizar:

- transaction.atomic()
- services.py
- serializers separados
- selectors para queries
- repositories para persistência complexa

# PERFORMANCE

Preparar:

- select_related
- prefetch_related
- índices corretos
- paginação

# FORMATO DA RESPOSTA

A resposta deve conter:

1. Arquitetura do módulo
2. DER completo
3. Models completas
4. Serializers
5. Services
6. Selectors
7. Repositories
8. Views
9. URLs
10. Permissions
11. Validações
12. Endpoints
13. Fluxo de movimentação
14. Testes
15. Estrutura frontend
16. Componentes React
17. Integração Axios
18. Explicação técnica
19. Melhorias futuras

# OBJETIVO FINAL

Criar um módulo de estoque profissional, robusto e escalável, servindo como padrão arquitetural para os próximos módulos do Nexor ERP.