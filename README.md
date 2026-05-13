# Nexor ERP

Nexor ERP e a base de um sistema web profissional, modular e escalavel para gestao empresarial, inicialmente orientado a metalurgia, vidracaria, prestacao de servicos industriais e controle operacional interno.

## Objetivos

- Centralizar processos administrativos, operacionais, financeiros e fiscais.
- Preparar uma arquitetura segura para evolucao futura como SaaS multiempresa.
- Separar responsabilidades entre API, regras de negocio, persistencia e interface.
- Padronizar modulos de dominio para crescimento sem refatoracoes massivas.

## Tecnologias

- Backend: Python 3.13, Django, Django REST Framework, Simple JWT e Celery.
- Frontend: React, Vite, TailwindCSS, Axios e React Router DOM.
- Infraestrutura: PostgreSQL, Redis, Docker e Docker Compose.

## Arquitetura

O backend segue configuracao por ambiente, apps por dominio, service layer para regras de negocio, selectors para leitura, repositories quando o acesso a dados exigir isolamento e views enxutas para orquestracao HTTP. O frontend separa layouts, paginas, rotas, servicos HTTP, contexto de autenticacao e componentes reutilizaveis.

## Estrutura de Pastas

```text
backend/
  apps/
  config/
  requirements/
frontend/
  src/
    api/
    components/
    contexts/
    hooks/
    layouts/
    pages/
    routes/
    services/
    store/
    styles/
    utils/
docker-compose.yml
.env.example
```

## Como Rodar Localmente

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/local.txt
cd backend
python manage.py migrate
python manage.py runserver
```

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

## Como Rodar com Docker

```bash
cp .env.example .env
docker compose up --build
```

## Variaveis de Ambiente

As variaveis estao documentadas em `.env.example`. Chave secreta, credenciais de banco, hosts permitidos, CORS e conexoes Redis/Celery devem ser configurados por ambiente. Credenciais reais nao devem ser versionadas.

## Convencoes do Projeto

- APIs versionadas em `/api/v1/`.
- Regras de negocio em `services.py`.
- Consultas reutilizaveis em `selectors.py`.
- Serializacao e validacao de borda em `serializers.py` e `validators.py`.
- Permissoes por modulo em `permissions.py`.
- Configuracao separada em `base.py`, `local.py` e `production.py`.

## Status do Projeto

Estrutura inicial criada. Os proximos ciclos devem implementar autenticacao JWT/RBAC, modelos de dominio, testes automatizados e pipelines de CI/CD.
