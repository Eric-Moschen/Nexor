# PROMPT 06 — MÓDULO DE ORDENS DE SERVIÇO DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- O módulo de Estoque do Prompt 02
- O módulo de Compras do Prompt 03
- O módulo Financeiro do Prompt 04
- O módulo Fiscal/NFe do Prompt 05

O objetivo desta etapa é implementar o MÓDULO DE ORDENS DE SERVIÇO, integrado a clientes, estoque, financeiro e fiscal.

Este módulo deve controlar serviços prestados pela empresa, desde orçamento/aprovação até execução, uso de materiais, apontamento de horas, finalização e geração financeira/fiscal.

---

# OBJETIVO

Implementar o módulo de Ordens de Serviço contendo:

- Cadastro de OS
- Itens de serviço
- Materiais utilizados
- Apontamento de horas
- Status da OS
- Responsáveis
- Prioridade
- Cliente
- Orçamento vinculado
- Cálculo de custo
- Cálculo de preço
- Histórico da OS
- Integração com estoque
- Integração com financeiro
- Integração futura com NFe
- APIs REST
- Frontend inicial

---

# FUNCIONALIDADES OBRIGATÓRIAS

## 1. ORDEM DE SERVIÇO

Campos:

- Número da OS
- Cliente
- Título
- Descrição do serviço
- Tipo de serviço
- Prioridade
- Status
- Data de abertura
- Data prevista
- Data de início
- Data de finalização
- Responsável técnico
- Observações
- Valor estimado
- Valor final
- Usuário criador

Status:

- Rascunho
- Aberta
- Em aprovação
- Aprovada
- Em execução
- Pausada
- Finalizada
- Cancelada
- Faturada

Prioridade:

- Baixa
- Média
- Alta
- Urgente

---

## 2. ITENS DE SERVIÇO

Campos:

- Ordem de serviço
- Descrição
- Quantidade
- Valor unitário
- Valor total
- Observação

Regras:

- Quantidade maior que zero
- Valor calculado no backend
- Não usar `float`
- Serviço finalizado não pode ser alterado livremente

---

## 3. MATERIAIS UTILIZADOS

Campos:

- Ordem de serviço
- Produto
- Quantidade
- Custo unitário
- Custo total
- Data de utilização
- Usuário responsável

Regras:

- Produto precisa estar ativo
- Quantidade maior que zero
- Não permitir uso sem saldo suficiente
- Saída de estoque deve ser registrada via service do estoque
- Toda baixa de material deve gerar histórico

---

## 4. APONTAMENTO DE HORAS

Campos:

- Ordem de serviço
- Colaborador/usuário
- Data
- Hora início
- Hora fim
- Total de horas
- Tipo de hora
- Observação

Tipos:

- Normal
- Extra 50%
- Extra 100%

Regras:

- Hora fim maior que hora início
- Não permitir apontamento em OS finalizada/cancelada
- Não permitir sobreposição de horário para o mesmo colaborador
- Total deve ser calculado no backend

---

## 5. HISTÓRICO DA OS

Registrar eventos:

- Criação
- Aprovação
- Início
- Pausa
- Retomada
- Uso de material
- Apontamento de horas
- Alteração de status
- Finalização
- Cancelamento
- Faturamento

---

# MODELAGEM

Criar DER completo contendo:

- OrdemServico
- ItemServico
- MaterialUtilizadoOS
- ApontamentoHorasOS
- HistoricoOS
- Cliente
- Produto
- MovimentacaoEstoque
- ContaReceber
- NotaFiscal
- Usuário

Aplicar:

- Constraints
- Índices
- Auditoria
- Soft delete preparado
- Integridade relacional
- Rastreabilidade completa

---

# BACKEND

Implementar no app `ordens_servico`:

```txt
apps/ordens_servico/
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



#REGRAS DE NEGÓCIO

Implementar em services.py.

# OS
- Criar OS
- Enviar para aprovação
- - Aprovar OS
- Iniciar execução
- Pausar OS
- Retomar OS
- Finalizar OS
- Cancelar OS
- Faturar OS

# Materiais
- Adicionar material
- Validar estoque
- Registrar saída de estoque
- Calcular custo total de material

# Horas
- Registrar apontamento
- Validar sobreposição
- Calcular horas
- Calcular custo de mão de obra

# Financeiro
- Gerar conta a receber ao faturar OS
- Não gerar financeiro em OS cancelada
- Não permitir faturamento duplicado

# Fiscal
- Preparar emissão de NFe vinculada à OS
- Não emitir NFe antes de faturar/aprovar conforme regra definida


# API

Criar endpoints:

# Ordens de Serviço

GET    /api/v1/os/
POST   /api/v1/os/
GET    /api/v1/os/{id}/
PUT    /api/v1/os/{id}/
DELETE /api/v1/os/{id}/
POST   /api/v1/os/{id}/enviar-aprovacao/
POST   /api/v1/os/{id}/aprovar/
POST   /api/v1/os/{id}/iniciar/
POST   /api/v1/os/{id}/pausar/
POST   /api/v1/os/{id}/retomar/
POST   /api/v1/os/{id}/finalizar/
POST   /api/v1/os/{id}/cancelar/
POST   /api/v1/os/{id}/faturar/

# Materiais da OS

GET    /api/v1/os/{id}/materiais/
POST   /api/v1/os/{id}/materiais/
DELETE /api/v1/os/{id}/materiais/{material_id}/

# Apontamentos de Horas

GET    /api/v1/os/{id}/apontamentos/
POST   /api/v1/os/{id}/apontamentos/
PUT    /api/v1/os/{id}/apontamentos/{apontamento_id}/
DELETE /api/v1/os/{id}/apontamentos/{apontamento_id}/

# Histórico

GET /api/v1/os/{id}/historico/


# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Ordem de serviço finalizada com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "Não é possível utilizar material sem saldo suficiente",
  "errors": {}
}


# VALIDAÇÕES

Implementar:

- OS precisa ter cliente
- OS finalizada não pode ser editada livremente
- OS cancelada não pode receber material
- OS cancelada não pode receber apontamento
- Material precisa ter estoque disponível
- Quantidade de material deve ser maior que zero
- Hora fim deve ser maior que hora início
- Não permitir sobreposição de horário
- Não permitir faturamento duplicado
- Não permitir cancelar OS faturada sem regra específica
- Não permitir apagar histórico

# PERMISSÕES

Preparar RBAC:

- Administrador: acesso total
- Operacional: criar e atualizar OS
- Supervisor: aprovar, pausar, finalizar e cancelar
- Estoque: visualizar materiais e validar movimentações
- Financeiro: visualizar faturamento e valores
- Fiscal: visualizar dados para emissão fiscal

# INTEGRAÇÃO COM ESTOQUE

Obrigatório:

- Material utilizado gera saída de estoque
- Usar service do módulo de estoque
- Registrar origem como OS
- Não atualizar produto diretamente
- Usar transaction.atomic()

# INTEGRAÇÃO COM FINANCEIRO

Obrigatório:

- OS faturada gera conta a receber
- Conta deve conter origem vinculada à OS
- Não duplicar conta a receber
- Usar service financeiro

# INTEGRAÇÃO COM FISCAL

Preparar:

- OS faturada pode gerar NFe
- NFe deve referenciar OS origem
- Não implementar regra fiscal complexa novamente
- Usar service fiscal quando necessário

# FRONTEND

Criar telas:

- Lista de ordens de serviço
- Nova OS
- Detalhes da OS
- Aprovação da OS
- Execução da OS
- Materiais utilizados
- Apontamento de horas
- Histórico da OS
- Faturamento da OS

# COMPONENTES

Criar:

- Tabela de OS
- Formulário de OS
- Badge de status
- Badge de prioridade
- Timeline de histórico
- Modal de material
- Modal de apontamento de horas
- Modal de finalização
- Modal de cancelamento
- Card de custos
- Card de faturamento

# UX

Implementar:

- Loading states
- Empty states
- Confirmações críticas
- Bloqueio visual para ações não permitidas
- Feedback claro para erro de estoque
- Linha do tempo da OS
- Filtros por cliente, status, prioridade e período


# TESTES

Criar testes:

# OS
- Criar OS válida
- Aprovar OS
- Iniciar OS
- Pausar OS
- Retomar OS
- Finalizar OS
- Cancelar OS
- Bloquear edição de OS finalizada
- Bloquear faturamento duplicado

# Materiais
- Adicionar material com saldo
- Bloquear material sem saldo
- Registrar saída de estoque

# Horas
- Registrar apontamento válido
- Bloquear hora fim menor que início
- Bloquear sobreposição de horários

# Financeiro
- Faturar OS gera conta a receber
- OS cancelada não gera financeiro

# SEGURANÇA

Implementar:

- JWT obrigatório
- Auditoria completa
- Logs de eventos da OS
- Validação server-side
- Controle de permissões
- transaction.atomic()
- Nunca confiar nos cálculos do frontend

# PERFORMANCE

Preparar:

- Índices por status
- Índices por cliente
- Índices por data
- Paginação
- select_related
- prefetch_related
- Queries otimizadas

# NÃO FAZER

- Não colocar regra de negócio na view
- Não atualizar estoque diretamente
- Não gerar financeiro direto na view
- Não usar float para dinheiro
- Não permitir OS sem cliente
- Não apagar histórico
- Não ignorar transações
- Não duplicar lógica de estoque/financeiro/fiscal

IMPORTANTE

Utilizar obrigatoriamente:

Decimal
transaction.atomic()

Valores monetários nunca devem usar float.


# FORMATO DA RESPOSTA

A resposta deve conter:

1. Visão geral do módulo de OS
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
13. Fluxo da OS
14. Fluxo de materiais
15. Fluxo de apontamento de horas
16. Integração com estoque
17. Integração com financeiro
18. Integração com fiscal
19. Testes
20. Estrutura frontend
21. Componentes React
22. Explicação técnica
23. Melhorias futuras 


# OBJETIVO FINAL

Criar um módulo de Ordens de Serviço robusto, auditável, seguro e integrado aos módulos principais do Nexor ERP, servindo como base operacional para empresas de serviços, metalurgia e vidraçaria.