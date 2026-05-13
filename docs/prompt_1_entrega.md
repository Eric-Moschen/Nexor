# Prompt 01 - Entrega da Estrutura Inicial do Nexor ERP

## 1. Visao Geral da Arquitetura

O Nexor ERP foi estruturado como uma aplicacao web modular, com backend Django REST Framework, frontend React/Vite, PostgreSQL como banco transacional, Redis como broker/cache operacional e Celery para processamento assincrono. A organizacao inicial prioriza separacao de responsabilidades, baixo acoplamento e evolucao futura para um modelo SaaS multiempresa.

## 2. Estrutura Completa de Diretorios

```text
backend/
  apps/
    accounts/
    core/
    estoque/
    compras/
    financeiro/
    fiscal/
    ordens_servico/
    clientes/
    fornecedores/
    relatorios/
    auditoria/
  config/
    settings/
  requirements/
frontend/
  src/
    api/
    assets/
    components/
    constants/
    contexts/
    hooks/
    layouts/
    pages/
    routes/
    services/
    store/
    styles/
    utils/
```

## 3. Comandos de Criacao

```bash
cp .env.example .env
docker compose up --build
```

Para execucao local sem Docker:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/local.txt
cd backend
python manage.py migrate
python manage.py runserver
```

```bash
cd frontend
npm install
npm run dev
```

## 4. Configuracao Backend

O backend possui configuracao separada em `base.py`, `local.py` e `production.py`, com variaveis de ambiente para segredo, debug, hosts, CORS, PostgreSQL e Redis/Celery. A API esta versionada em `/api/v1/` e preparada com JWT, paginacao, filtros, ordenacao e tratamento global de excecoes.

## 5. Configuracao Frontend

O frontend utiliza React, Vite, TailwindCSS, Axios e React Router DOM. A estrutura separa cliente HTTP, rotas, layouts, paginas, componentes, contexto de autenticacao, hooks e servicos.

## 6. Configuracao PostgreSQL

O PostgreSQL e obrigatorio e esta configurado no Django via variaveis de ambiente. O `docker-compose.yml` inclui healthcheck, volume persistente e credenciais de desenvolvimento em `.env.example`.

## 7. Configuracao Docker

O Docker Compose sobe `backend`, `frontend`, `postgres`, `redis`, `celery` e `celery-beat`, permitindo o comando padrao `docker compose up --build`.

## 8. Configuracao Redis

O Redis esta configurado como servico dedicado, com healthcheck e URLs expostas por `REDIS_URL`, `CELERY_BROKER_URL` e `CELERY_RESULT_BACKEND`.

## 9. Configuracao Celery

O Celery foi inicializado em `backend/config/celery.py`, com autodiscovery de tasks e workers separados no Compose. A estrutura ja comporta rotinas futuras de NFe, relatorios, emails e integracoes externas.

## 10. Arquivos Iniciais

Foram criados arquivos principais de backend, frontend, Docker, variaveis de ambiente, requirements, README, gitignore, dockerignore e documentacao da entrega.

## 11. README Inicial

O `README.md` documenta nome do projeto, objetivos, tecnologias, arquitetura, estrutura, execucao local, execucao com Docker, variaveis de ambiente, convencoes e status.

## 12. Explicacao Tecnica das Decisoes

A base utiliza apps por dominio para permitir crescimento modular. Views ficam enxutas, regras de negocio devem evoluir em services, consultas reutilizaveis em selectors e acesso especializado a dados em repositories quando necessario. A configuracao por ambiente evita credenciais fixas e reduz risco operacional. A separacao do frontend evita concentrar regra de negocio na interface e facilita evolucao para gerenciamento de estado mais robusto no futuro.

## 13. Proximos Passos Recomendados

1. Criar migrations iniciais e testes automatizados para `accounts` e modulos principais.
2. Implementar login, refresh token, logout e auditoria real de login.
3. Definir modelo multiempresa antes dos cadastros produtivos.
4. Implementar RBAC com permissoes por perfil e por modulo.
5. Adicionar CI com validacao de backend, frontend e Docker.
