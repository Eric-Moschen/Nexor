# PROMPT 07 — MÓDULO DE ORÇAMENTOS DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- O módulo de Estoque do Prompt 02
- O módulo de Compras do Prompt 03
- O módulo Financeiro do Prompt 04
- O módulo Fiscal/NFe do Prompt 05
- O módulo de Ordens de Serviço do Prompt 06

O objetivo desta etapa é implementar o MÓDULO DE ORÇAMENTOS, integrado a clientes, produtos, serviços, estoque, ordens de serviço, financeiro e fiscal.

Este módulo deve controlar propostas comerciais, formação de preço, aprovação do cliente, conversão em OS/venda e rastreabilidade comercial.

---

# OBJETIVO

Implementar o módulo de Orçamentos contendo:

- Cadastro de orçamento
- Itens de produtos
- Itens de serviços
- Cálculo de custos
- Cálculo de margem
- Cálculo de preço de venda
- Descontos
- Validade da proposta
- Status comercial
- Aprovação/reprovação do cliente
- Conversão em Ordem de Serviço
- Conversão futura em venda/NFe
- Geração de PDF
- Envio por email preparado
- APIs REST
- Frontend inicial

---

# FUNCIONALIDADES OBRIGATÓRIAS

## 1. ORÇAMENTO

Campos:

- Número do orçamento
- Cliente
- Título
- Descrição
- Data de criação
- Data de validade
- Status
- Condição de pagamento
- Prazo de entrega
- Observações internas
- Observações para o cliente
- Valor de produtos
- Valor de serviços
- Valor de desconto
- Valor total
- Margem estimada
- Usuário responsável

Status:

- Rascunho
- Em análise
- Enviado
- Aprovado
- Reprovado
- Expirado
- Convertido em OS
- Cancelado

---

## 2. ITENS DE PRODUTO

Campos:

- Orçamento
- Produto
- Descrição
- Quantidade
- Custo unitário
- Valor unitário
- Desconto
- Valor total

Regras:

- Produto precisa estar ativo
- Quantidade maior que zero
- Valor total calculado no backend
- Não confiar em cálculo do frontend
- Não baixar estoque no orçamento

---

## 3. ITENS DE SERVIÇO

Campos:

- Orçamento
- Descrição do serviço
- Quantidade
- Custo estimado
- Valor unitário
- Desconto
- Valor total
- Observação

Regras:

- Quantidade maior que zero
- Valores calculados no backend
- Serviço pode virar item de OS depois

---

## 4. APROVAÇÃO DO CLIENTE

Implementar fluxo:

- Marcar orçamento como enviado
- Aprovar orçamento
- Reprovar orçamento com motivo
- Cancelar orçamento
- Expirar orçamento automaticamente futuramente preparado

Regras:

- Orçamento aprovado não pode ser editado livremente
- Orçamento reprovado deve registrar motivo
- Orçamento expirado não pode ser aprovado sem revalidação
- Toda mudança de status deve gerar histórico

---

## 5. HISTÓRICO DO ORÇAMENTO

Registrar eventos:

- Criação
- Alteração
- Envio
- Aprovação
- Reprovação
- Cancelamento
- Expiração
- Conversão em OS
- Geração de PDF

---

## 6. CONVERSÃO EM ORDEM DE SERVIÇO

Implementar:

- Converter orçamento aprovado em OS
- Criar OS vinculada ao orçamento
- Levar itens de serviço para OS
- Preparar materiais previstos
- Evitar conversão duplicada

---

# MODELAGEM

Criar DER completo contendo:

- Orcamento
- ItemProdutoOrcamento
- ItemServicoOrcamento
- HistoricoOrcamento
- Cliente
- Produto
- OrdemServico
- Usuario

Aplicar:

- Constraints
- Índices
- Auditoria
- Soft delete preparado
- Integridade relacional
- Rastreabilidade completa

---

# BACKEND

Implementar no app `orcamentos`:

```txt
apps/orcamentos/
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
├── pdf/
│   └── orcamento_pdf.py
└── tests/


Caso o app orcamentos ainda não exista, criar e registrar no projeto.



# REGRAS DE NEGÓCIO

Implementar em services.py.

# Orçamento
- Criar orçamento
- Atualizar orçamento
- Calcular totais
- Aplicar descontos
- Calcular margem
- Enviar orçamento
- Aprovar orçamento
- Reprovar orçamento
- Cancelar orçamento
- Expirar orçamento
- Converter orçamento em OS

# PDF
- Gerar PDF do orçamento
- Registrar evento no histórico
- Preparar envio por email futuro

# API

Criar endpoints:

# Orçamentos

GET    /api/v1/orcamentos/
POST   /api/v1/orcamentos/
GET    /api/v1/orcamentos/{id}/
PUT    /api/v1/orcamentos/{id}/
DELETE /api/v1/orcamentos/{id}/
POST   /api/v1/orcamentos/{id}/enviar/
POST   /api/v1/orcamentos/{id}/aprovar/
POST   /api/v1/orcamentos/{id}/reprovar/
POST   /api/v1/orcamentos/{id}/cancelar/
POST   /api/v1/orcamentos/{id}/converter-os/
GET    /api/v1/orcamentos/{id}/pdf/
GET    /api/v1/orcamentos/{id}/historico/


# RESPONSE PADRONIZADA

Sucesso
{
  "success": true,
  "message": "Orçamento aprovado com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "Orçamento expirado não pode ser aprovado sem revalidação",
  "errors": {}
}

# VALIDAÇÕES

Implementar:

- Orçamento precisa ter cliente
- Orçamento precisa ter ao menos um item
- Quantidade deve ser maior que zero
- Valores monetários não podem ser negativos
- Data de validade não pode ser anterior à data de criação
- Orçamento aprovado não pode ser editado livremente
- Orçamento reprovado exige motivo
- Orçamento convertido não pode ser convertido novamente
- Orçamento cancelado não pode ser aprovado
- Orçamento expirado não pode ser aprovado sem revalidação


# PERMISSÕES

Preparar RBAC:

- Administrador: acesso total
- Comercial: criar, editar e enviar orçamento
- Supervisor: aprovar descontos acima do limite
- Financeiro: visualizar valores e condições
- Operacional: visualizar orçamento convertido em OS

# INTEGRAÇÃO COM ESTOQUE

Obrigatório:

- Orçamento não movimenta estoque
- Deve consultar produto e custo atual
- Deve preparar reserva futura sem implementar reserva ainda
- Não atualizar saldo de produto

# INTEGRAÇÃO COM ORDENS DE SERVIÇO

Obrigatório:

- Orçamento aprovado pode virar OS
- OS deve manter referência ao orçamento
- Não permitir conversão duplicada
- Usar service do módulo de OS

# INTEGRAÇÃO COM FINANCEIRO

Preparar:

- Condições de pagamento
- Parcelamento futuro
- Conta a receber futura após faturamento
- Não gerar financeiro no orçamento

# INTEGRAÇÃO COM FISCAL

Preparar:

- NFe futura após venda/faturamento
- Não emitir NFe no orçamento
- Não duplicar regras fiscais

# FRONTEND

Criar telas:

- Lista de orçamentos
- Novo orçamento
- Detalhes do orçamento
- Itens do orçamento
- Aprovação/reprovação
- Geração de PDF
- Conversão em OS

# COMPONENTES

Criar:

- Tabela de orçamentos
- Formulário de orçamento
- Formulário de item de produto
- Formulário de item de serviço
- Card de totais
- Badge de status
- Modal de aprovação
- Modal de reprovação
- Modal de conversão em OS
- Preview de PDF

# UX

Implementar:

- Loading states
- Empty states
- Confirmações críticas
- Bloqueio visual para ações não permitidas
- Feedback claro para orçamento expirado
- Cálculo visual de totais
- Filtros por cliente, status e período


# TESTES

Criar testes:

# Orçamento
- Criar orçamento válido
- Bloquear orçamento sem cliente
- Bloquear orçamento sem itens
- Calcular totais corretamente
- Aplicar desconto
- Aprovar orçamento
- Reprovar orçamento com motivo
- Bloquear reprovação sem motivo
- Cancelar orçamento
- Bloquear edição após aprovação
- Converter orçamento aprovado em OS
- Bloquear conversão duplicada

# PDF
- Gerar PDF válido
- Registrar evento de geração

# SEGURANÇA

Implementar:

- JWT obrigatório
- Auditoria completa
- Controle de permissões
- Validação server-side
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

- Não movimentar estoque no orçamento
- Não gerar financeiro no orçamento
- Não emitir NFe no orçamento
- Não usar float para dinheiro
- Não calcular valores finais no frontend
- Não permitir conversão duplicada em OS
- Não colocar regra de negócio na view
- Não apagar histórico

IMPORTANTE

Utilizar obrigatoriamente:

Decimal
transaction.atomic()

Valores monetários nunca devem usar float.



# FORMATO DA RESPOSTA

A resposta deve conter:

1. Visão geral do módulo de orçamentos
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
13. Fluxo do orçamento
14. Fluxo de aprovação/reprovação
15. Fluxo de conversão em OS
16. Geração de PDF
17. Integração com estoque
18. Integração com OS
19. Integração com financeiro
20. Integração com fiscal
21. Testes
22. Estrutura frontend
23. Componentes React
24. Explicação técnica
25. Melhorias futuras

# OBJETIVO FINAL

Criar um módulo de Orçamentos profissional, seguro, auditável e integrado ao fluxo operacional do Nexor ERP, permitindo transformar propostas comerciais em ordens de serviço ou vendas futuras com rastreabilidade completa.

