# Seguranca

Controles implementados:

- JWT com refresh token e blacklist.
- RBAC por permissao granular.
- Rate limit DRF.
- CORS e CSRF configuraveis por ambiente.
- `DEBUG=False` em producao.
- Cookies seguros em producao.
- `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS` e `Referrer-Policy`.
- Auditoria global e logs rotacionados.
- Segredos via `.env`.

Checklist antes de producao:

- Trocar `DJANGO_SECRET_KEY`.
- Usar senha forte do PostgreSQL.
- Configurar hosts e origens reais.
- Ativar HTTPS no proxy ou load balancer.
- Restringir acesso ao banco e Redis.
