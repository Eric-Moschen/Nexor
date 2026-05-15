# Banco De Dados

O projeto usa PostgreSQL com volume persistente Docker.

Ambientes:

- Desenvolvimento: `postgres_data`
- Producao: `postgres_data` no `docker-compose.prod.yml`

Boas praticas aplicadas:

- Chaves estrangeiras entre dominios.
- Constraints de valores monetarios e quantidades.
- Indices por status, datas e relacionamentos criticos.
- Soft delete preparado via `SoftDeleteModel`.
- Auditoria via `AuditModel` e `AuditLog`.
