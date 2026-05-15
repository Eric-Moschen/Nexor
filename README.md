# Nexor ERP

ERP web modular para operacao corporativa de pequenas e medias empresas, com backend Django REST, frontend React/Vite, PostgreSQL, Redis, Celery, Docker e RBAC.

## Tecnologias

- Python 3.13, Django, Django REST Framework
- PostgreSQL 17
- Redis 7
- Celery e Celery Beat
- React, Vite, TailwindCSS, Axios, React Router
- Docker, Docker Compose, Gunicorn e Nginx

## Arquitetura

O backend fica em `backend/apps`, separado por modulos de negocio: contas, estoque, compras, financeiro, fiscal, ordens de servico, orcamentos, clientes, fornecedores, relatorios, auditoria e core. O `core` concentra eventos internos, auditoria global, notificacoes, health checks e servicos compartilhados.

O frontend fica em `frontend/src`, com services Axios, rotas protegidas, layout corporativo, paginas modulares e centro operacional integrado.

## Como Rodar Localmente

```powershell
copy .env.example .env
docker compose up --build -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_initial_data
```

URLs:

- Frontend: `http://localhost:5173`
- API: `http://localhost:8000/api/v1/`
- Admin Django: `http://localhost:8000/admin/`

Usuario inicial padrao:

- Usuario: `admin`
- Senha: `Admin@12345`

## Deploy De Producao

Edite `.env` com `DJANGO_SETTINGS_MODULE=config.settings.production`, `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY` forte, hosts reais e origens confiaveis.

```powershell
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml exec backend python manage.py seed_initial_data
```

Em producao, o Nginx atende na porta `80`, serve o frontend estatico, encaminha `/api/` e `/admin/` para o Django, e serve `/static/` e `/media/`.

## Comandos Uteis

```powershell
docker compose logs -f backend
docker compose logs -f celery
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py seed_rbac
docker compose exec backend python manage.py seed_initial_data
docker compose exec backend python manage.py test
```

## Backups

```powershell
docker compose -f docker-compose.prod.yml exec postgres sh /scripts/backup.sh
```

Alternativa recomendada em servidor: montar `docker/scripts` no container ou executar `pg_dump` a partir do host com as variaveis do `.env`.

## Health Checks

- `GET /api/v1/health/`
- `GET /api/v1/health/database/`
- `GET /api/v1/health/redis/`
- `GET /api/v1/health/celery/`

## Segurança

O projeto usa JWT, RBAC, rate limit DRF, CORS por ambiente, CSRF preparado, cookies seguros em producao, logs protegidos, auditoria global e variaveis de ambiente para segredos.

## Troubleshooting

Se o Docker nao iniciar, abra o Docker Desktop e aguarde o engine ficar ativo. Se as tabelas Django nao existirem, rode `docker compose exec backend python manage.py migrate`. Se o frontend nao refletir dados, confira `VITE_API_BASE_URL` e se o backend esta saudavel em `/api/v1/health/`.
