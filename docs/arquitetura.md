# Arquitetura

O Nexor ERP segue arquitetura modular. Cada app concentra modelos, serializers, selectors, repositories, services, views, urls e testes do seu dominio.

Camadas principais:

- `accounts`: usuarios, JWT, RBAC e auditoria de autenticacao.
- `core`: respostas padronizadas, health checks, eventos internos, auditoria global, notificacoes e servicos compartilhados.
- `estoque`, `compras`, `financeiro`, `fiscal`, `ordens_servico`, `orcamentos`, `clientes`, `fornecedores`, `relatorios`: dominios de negocio.
- `auditoria`: consulta protegida aos logs globais.

Fluxos criticos usam service layer e `transaction.atomic()`. Integracoes entre modulos sao feitas por eventos internos e pelo `ERPIntegrationService`, preservando baixo acoplamento.
