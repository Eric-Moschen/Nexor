# PROMPT 05 — MÓDULO FISCAL E EMISSÃO DE NFE DO NEXOR ERP

Utilize integralmente:

- O contexto principal do projeto Nexor ERP
- A arquitetura criada no Prompt 01
- O módulo de Estoque do Prompt 02
- O módulo de Compras do Prompt 03
- O módulo Financeiro do Prompt 04

O objetivo desta etapa é implementar o MÓDULO FISCAL do ERP, preparado para emissão de NFe, controle de documentos fiscais, XML, DANFE e integração futura com SEFAZ.

Este módulo é crítico. Portanto, priorize segurança, rastreabilidade, validação fiscal e integridade dos dados.

---

# OBJETIVO

Implementar o módulo fiscal contendo:

- Cadastro fiscal da empresa
- Cadastro fiscal de clientes e fornecedores
- Natureza da operação
- CFOP
- NCM
- CST/CSOSN
- Emissão de NFe
- Controle de XML
- Geração de DANFE
- Status da NFe
- Eventos fiscais
- Cancelamento
- Inutilização futura preparada
- Integração com estoque
- Integração com financeiro
- Auditoria fiscal

---

# FUNCIONALIDADES OBRIGATÓRIAS

## 1. CADASTRO FISCAL DA EMPRESA

Campos:

- Razão social
- Nome fantasia
- CNPJ
- Inscrição estadual
- Inscrição municipal
- Regime tributário
- CNAE
- Endereço fiscal
- Certificado digital A1
- Senha do certificado protegida
- Ambiente fiscal: homologação/produção
- Status

Regras:

- Não armazenar senha em texto puro
- Certificado deve ser protegido
- Ambiente homologação deve ser padrão inicial

---

## 2. CLIENTES E FORNECEDORES — DADOS FISCAIS

Complementar estrutura de clientes/fornecedores com:

- CPF/CNPJ
- Inscrição estadual
- Indicador de IE
- Endereço fiscal completo
- Município IBGE
- UF
- CEP
- Email fiscal

---

## 3. PRODUTOS — DADOS FISCAIS

Complementar produtos com:

- NCM
- CEST
- CFOP padrão
- Unidade comercial
- Unidade tributável
- Origem da mercadoria
- CST/CSOSN
- Alíquota ICMS
- Alíquota PIS
- Alíquota COFINS
- Alíquota IPI

---

## 4. NATUREZA DA OPERAÇÃO

Campos:

- Código
- Descrição
- Tipo operação
- CFOP padrão
- Movimenta estoque
- Gera financeiro
- Status

Tipos:

- Venda
- Compra
- Devolução
- Remessa
- Retorno
- Bonificação
- Ajuste

---

## 5. NOTA FISCAL ELETRÔNICA

Campos principais:

- Número
- Série
- Chave de acesso
- Protocolo
- Ambiente
- Tipo emissão
- Tipo operação
- Natureza da operação
- Emitente
- Destinatário
- Data emissão
- Data saída/entrada
- Status
- Valor produtos
- Valor frete
- Valor desconto
- Valor total
- XML autorizado
- XML cancelamento
- DANFE PDF
- Motivo rejeição
- Usuário responsável

Status:

- Rascunho
- Validada
- Assinada
- Enviada
- Autorizada
- Rejeitada
- Cancelada
- Denegada

---

## 6. ITENS DA NFE

Campos:

- Produto
- Descrição
- CFOP
- NCM
- CST/CSOSN
- Quantidade
- Valor unitário
- Valor total
- Desconto
- Base ICMS
- Valor ICMS
- Base PIS
- Valor PIS
- Base COFINS
- Valor COFINS
- Base IPI
- Valor IPI

Regras:

- Quantidade maior que zero
- Valor unitário maior ou igual a zero
- Total deve ser calculado no backend
- Impostos calculados no backend
- Não confiar em valores fiscais enviados pelo frontend

---

## 7. EVENTOS FISCAIS

Criar histórico de eventos da NFe:

- Validação
- Assinatura
- Envio
- Autorização
- Rejeição
- Cancelamento
- Erros de comunicação
- Retorno SEFAZ

Campos:

- NFe
- Tipo evento
- Código retorno
- Mensagem
- Protocolo
- XML retorno
- Data evento
- Usuário responsável

---

# MODELAGEM

Criar DER completo contendo:

- EmpresaFiscal
- ClienteFiscal
- FornecedorFiscal
- ProdutoFiscal
- NaturezaOperacao
- NotaFiscal
- ItemNotaFiscal
- EventoFiscal
- Produto
- Cliente
- Fornecedor
- ContaReceber
- ContaPagar
- MovimentacaoEstoque
- Usuário

Aplicar:

- Constraints
- Índices
- Auditoria
- Soft delete preparado
- Integridade fiscal
- Rastreabilidade total

---

# BACKEND

Implementar no app `fiscal`:

```txt
apps/fiscal/
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
├── integrations/
│   ├── sefaz_client.py
│   ├── xml_builder.py
│   ├── danfe_generator.py
│   └── certificate_manager.py
└── tests/


# REGRAS DE NEGÓCIO

Implementar em services.py.

# NFe
- Criar NFe em rascunho
- Adicionar itens
- Validar dados fiscais obrigatórios
- Calcular totais
- Calcular impostos
- Assinar XML
- Enviar para SEFAZ
- Registrar retorno
- Cancelar NFe
- Gerar DANFE

# Integração Estoque
- Se natureza movimenta estoque, movimentar estoque somente após autorização
- NFe rejeitada não pode movimentar estoque
- Cancelamento deve preparar reversão de estoque conforme regra fiscal

# Integração Financeiro
- Se natureza gera financeiro, criar conta a receber ou pagar após autorização
- NFe rejeitada não pode gerar financeiro
- Cancelamento deve preparar estorno financeiro conforme regra


# API

Criar endpoints:

# Configurações fiscais

GET    /api/v1/fiscal/empresa/
POST   /api/v1/fiscal/empresa/
PUT    /api/v1/fiscal/empresa/{id}/

# Naturezas de operação

GET    /api/v1/fiscal/naturezas-operacao/
POST   /api/v1/fiscal/naturezas-operacao/
GET    /api/v1/fiscal/naturezas-operacao/{id}/
PUT    /api/v1/fiscal/naturezas-operacao/{id}/

#  NFe

GET    /api/v1/fiscal/nfe/
POST   /api/v1/fiscal/nfe/
GET    /api/v1/fiscal/nfe/{id}/
PUT    /api/v1/fiscal/nfe/{id}/
POST   /api/v1/fiscal/nfe/{id}/validar/
POST   /api/v1/fiscal/nfe/{id}/assinar/
POST   /api/v1/fiscal/nfe/{id}/enviar/
POST   /api/v1/fiscal/nfe/{id}/cancelar/
GET    /api/v1/fiscal/nfe/{id}/danfe/
GET    /api/v1/fiscal/nfe/{id}/xml/


# RESPONSE PADRONIZADA

Sucesso 
{
  "success": true,
  "message": "NFe autorizada com sucesso",
  "data": {}
}

Erro
{
  "success": false,
  "message": "NFe rejeitada pela SEFAZ",
  "errors": {}
}


# VALIDAÇÕES

Implementar:

- CNPJ válido
- CPF válido
- IE conforme UF
- CEP válido
- Município IBGE obrigatório
- NCM obrigatório
- CFOP obrigatório
- Natureza da operação obrigatória
- Produto fiscal completo
- Cliente fiscal completo
- Certificado digital válido
- Ambiente fiscal definido
- NFe sem item não pode ser enviada
- NFe rejeitada não movimenta estoque
- NFe rejeitada não gera financeiro
- NFe autorizada não pode ser editada

# PERMISSÕES

Preparar RBAC:

- Administrador: acesso total
- Fiscal: emitir, validar, cancelar
- Financeiro: visualizar impacto financeiro
- Estoque: visualizar impacto de estoque
- Operacional: visualizar notas autorizadas


# INTEGRAÇÃO COM SEFAZ

Preparar abstração em:

integrations/sefaz_client.py

A integração deve ser desacoplada.

Não acoplar lógica SEFAZ diretamente em views ou serializers.

Criar camada responsável por:

- Montar XML
- Assinar XML
- Enviar XML
- Consultar retorno
- Tratar rejeições
- Registrar eventos

# SEGURANÇA FISCAL

Obrigatório:

- Certificado A1 protegido
- Senha do certificado criptografada
- Logs sem exposição de senha
- XML armazenado com controle de acesso
- Auditoria completa
- JWT obrigatório
- Controle de permissões

# CELERY

Usar Celery para tarefas futuras:

- Envio assíncrono de NFe
- Consulta de autorização
- Geração de DANFE
- Envio de XML por email
- Processamento de eventos fiscais


# FRONTEND

Criar telas:

- Configuração fiscal da empresa
- Cadastro de natureza da operação
- Lista de NFe
- Nova NFe
- Detalhes da NFe
- Eventos da NFe
- Visualização DANFE
- Download XML


# COMPONENTES

Criar:

- Formulário fiscal
- Tabela de notas fiscais
- Badge de status fiscal
- Timeline de eventos fiscais
- Modal de cancelamento
- Card de totais da NFe
- Validador visual de dados fiscais


# UX

Implementar:

- Alertas de homologação/produção
- Bloqueio visual para NFe autorizada
- Feedback claro para rejeições
- Loading durante envio
- Histórico de eventos visível
- Confirmação antes de cancelar


# TESTES

Criar testes:

# NFe
- Criar NFe válida
- Bloquear NFe sem item
- Bloquear NFe sem destinatário fiscal
- Calcular totais
- Calcular impostos
- Validar mudança de status
- Bloquear edição após autorização
- Registrar rejeição
- Registrar autorização

# Integrações
- Mock SEFAZ
- Mock assinatura XML
- Mock geração DANFE

# Estoque/Financeiro
- NFe autorizada movimenta estoque
- NFe rejeitada não movimenta estoque
- NFe autorizada gera financeiro
- NFe rejeitada não gera financeiro



# NÃO FAZER

- Não implementar regra fiscal no frontend
- Não confiar em cálculo vindo do frontend
- Não expor senha do certificado
- Não acoplar SEFAZ nas views
- Não movimentar estoque antes da autorização
- Não gerar financeiro antes da autorização
- Não permitir editar NFe autorizada
- Não usar float para valores fiscais
- Não ignorar eventos fiscais

# IMPORTANTE

Utilizar obrigatoriamente:

Decimal
transaction.atomic()
Celery

Valores fiscais nunca devem usar float.

# FORMATO DA RESPOSTA

A resposta deve conter:

1. Visão geral do módulo fiscal
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
12. Validações fiscais
13. Integração SEFAZ desacoplada
14. XML builder
15. DANFE generator
16. Certificate manager
17. Fluxo de emissão de NFe
18. Fluxo de cancelamento
19. Integração com estoque
20. Integração com financeiro
21. Testes
22. Estrutura frontend
23. Componentes React
24. Explicação técnica
25. Melhorias futuras


# OBJETIVO FINAL

Criar um módulo fiscal profissional, seguro, auditável e preparado para emissão real de NFe, sem comprometer a arquitetura do Nexor ERP.