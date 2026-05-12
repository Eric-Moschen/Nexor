# Nexor ERP

Nexor ERP é uma base inicial profissional para um sistema ERP web modular, escalável e preparado para evolução SaaS multiempresa. O projeto nasce com foco em empresas de metalurgia, vidraçaria, serviços industriais e controle operacional interno.

## Objetivos

- Centralizar processos operacionais, administrativos, financeiros e fiscais.
- Manter separação clara entre domínios, camadas e responsabilidades.
- Preparar autenticação JWT, RBAC, auditoria, soft delete e multiempresa futura.
- Oferecer uma base segura para evolução incremental com APIs REST versionadas.

## Tecnologias

### Backend

- Python 3.13+
- Django
- Django REST Framework
- Simple JWT
- PostgreSQL
- Celery
- Redis
- django-cors-headers
- python-decouple

### Frontend

- React
- Vite
- TailwindCSS
- Axios
- React Router DOM

### Infraestrutura

- Docker
- Docker Compose
- PostgreSQL
- Redis
- Celery worker
- Celery beat preparado via profile `scheduler`

## Arquitetura

A solução utiliza uma Clean Architecture simplificada com modularização por domínio. Cada app Django é um bounded context com pontos dedicados para:

- `models.py`: entidades persistentes.
- `serializers.py`: contratos de entrada/saída da API.
- `views.py`: camada HTTP enxuta.
- `services.py`: regras de negócio.
- `selectors.py`: consultas e leituras complexas.
- `repositories.py`: abstrações de persistência quando necessárias.
- `permissions.py`: autorização e expansão RBAC.
- `validators.py`: validações de domínio.

O frontend separa layout, páginas, serviços HTTP, hooks, contexto de autenticação e constantes para manter baixo acoplamento e facilitar a troca futura por Zustand ou Redux.

## Estrutura de pastas

```text
backend/
├── apps/
│   ├── accounts/
│   ├── core/
│   ├── estoque/
│   ├── compras/
│   ├── financeiro/
│   ├── fiscal/
│   ├── ordens_servico/
│   ├── clientes/
│   ├── fornecedores/
│   ├── relatorios/
│   └── auditoria/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── celery.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/
├── docker/
├── .env.example
├── manage.py
└── Dockerfile

frontend/
├── src/
│   ├── api/
│   ├── assets/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   ├── routes/
│   ├── services/
│   ├── hooks/
│   ├── contexts/
│   ├── store/
│   ├── utils/
│   ├── styles/
│   └── constants/
├── public/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── Dockerfile
```

## Comandos de criação utilizados como referência

```bash
mkdir -p backend/apps/{accounts,core,estoque,compras,financeiro,fiscal,ordens_servico,clientes,fornecedores,relatorios,auditoria}
mkdir -p backend/config/settings backend/requirements backend/docker
mkdir -p frontend/src/{api,assets,components,layouts,pages,routes,services,hooks,contexts,store,utils,styles,constants} frontend/public
```

Em uma evolução com ferramentas instaladas localmente, os comandos equivalentes seriam:

```bash
python -m venv .venv
pip install -r backend/requirements/local.txt
django-admin startproject config backend
npm create vite@latest frontend -- --template react
```

## Como rodar localmente sem Docker

1. Copie as variáveis de ambiente:

   ```bash
   cp backend/.env.example backend/.env
   ```

2. Crie um banco PostgreSQL e ajuste `POSTGRES_*` no arquivo `.env`.

3. Suba o backend:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements/local.txt
   python manage.py migrate
   python manage.py runserver
   ```

4. Suba o frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Como rodar com Docker

1. Copie o arquivo de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Execute:

   ```bash
   docker compose up --build
   ```

3. Acesse:

   - Frontend: <http://localhost:5173>
   - Backend health check: <http://localhost:8000/api/v1/health/>
   - Admin Django: <http://localhost:8000/admin/>

## Variáveis de ambiente

As principais variáveis estão documentadas em `.env.example` e `backend/.env.example`:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `VITE_API_BASE_URL`

Nenhuma credencial real deve ser versionada.

## Convenções do projeto

- APIs sob o prefixo `/api/v1/`.
- Views devem permanecer finas e delegar regras para services/selectors.
- Domínios devem evitar dependência direta entre apps; prefira contratos explícitos.
- Use variáveis de ambiente para segredos e configurações por ambiente.
- Preserve nomes e camadas dos módulos para facilitar expansão futura.
- Use PostgreSQL em todos os ambientes de desenvolvimento integrado; não use SQLite.

## Decisões técnicas

- **Configuração por ambiente:** `base.py`, `local.py` e `production.py` reduzem risco de misturar ajustes de desenvolvimento e produção.
- **PostgreSQL obrigatório:** evita divergências de comportamento com SQLite e prepara o projeto para constraints, índices e integridade transacional.
- **Celery + Redis:** deixa a base preparada para emissão de NFe, relatórios, emails, integrações e rotinas automáticas.
- **JWT:** estabelece uma base stateless para APIs REST e clientes web modernos.
- **RBAC preparado:** permissões foram isoladas para permitir perfis como Administrador, Financeiro, Estoque, Compras, Operacional e Supervisor.
- **Frontend modular:** rotas, layouts, services e contexts evitam acoplamento e facilitam crescimento da interface.

## Próximos passos recomendados

1. Criar modelo customizado de usuário e grupos/perfis RBAC.
2. Definir entidade de empresa/tenant e aplicá-la aos modelos de domínio.
3. Implementar auditoria de login e trilhas de operação.
4. Modelar os cadastros iniciais de clientes, fornecedores e produtos.
5. Adicionar testes automatizados com pytest-django e testes de frontend.
6. Configurar CI/CD com lint, testes, build Docker e análise de segurança.
7. Adicionar observabilidade com métricas, tracing e logs estruturados em JSON.

## Status do projeto

Base inicial criada. O projeto está preparado para evolução dos domínios, mas ainda não contém regras de negócio completas de ERP.
