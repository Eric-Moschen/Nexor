# API

Base URL local:

```text
http://localhost:8000/api/v1
```

Endpoints globais:

- `/health/`
- `/health/database/`
- `/health/redis/`
- `/health/celery/`
- `/auth/login/`
- `/auth/refresh/`
- `/auth/logout/`
- `/auth/me/`
- `/accounts/users/`
- `/accounts/roles/`
- `/auditoria/logs/`
- `/core/events/`
- `/notificacoes/`

As respostas seguem o padrao:

```json
{"success": true, "message": "Operacao realizada com sucesso.", "data": {}}
```
