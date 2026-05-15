# Troubleshooting

## Docker nao reconhecido

Instale e abra o Docker Desktop. Aguarde o engine iniciar.

## Tabela `django_session` nao existe

Rode:

```powershell
docker compose exec backend python manage.py migrate
```

## Frontend nao mostra dados

Verifique:

- Backend em `http://localhost:8000/api/v1/health/`
- `VITE_API_BASE_URL`
- Login JWT valido
- Permissoes RBAC do usuario

## Nginx nao sobe em producao

Confira se a porta `80` esta livre e se `docker/nginx/nginx.conf` esta montado corretamente.
