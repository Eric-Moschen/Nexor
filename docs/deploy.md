# Deploy

## Local empresarial

Use `docker-compose.yml` com `.env` local. Esse modo usa Vite dev server e Django runserver.

## Producao

Use `docker-compose.prod.yml`.

Variaveis obrigatorias:

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `CORS_ALLOWED_ORIGINS`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

Comando:

```powershell
docker compose -f docker-compose.prod.yml up --build -d
```

O backend roda com Gunicorn e o Nginx publica frontend, API, admin, static e media.
