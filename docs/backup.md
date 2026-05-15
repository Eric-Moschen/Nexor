# Backup E Restore

Scripts:

- `docker/scripts/backup.sh`
- `docker/scripts/restore.sh`
- `docker/scripts/cleanup.sh`

Estrategia:

- Backup diario do PostgreSQL.
- Retencao configuravel por `BACKUP_RETENTION_DAYS`.
- Restore testado periodicamente em ambiente isolado.
- Manter copia fora do servidor principal.

Exemplo Linux:

```sh
docker compose -f docker-compose.prod.yml exec postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > backups/nexor.sql.gz
```
