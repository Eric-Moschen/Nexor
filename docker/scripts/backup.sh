#!/usr/bin/env sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-/backups}"
STAMP="$(date +%Y%m%d-%H%M%S)"
FILE="${BACKUP_DIR}/nexor-${POSTGRES_DB}-${STAMP}.sql.gz"

mkdir -p "${BACKUP_DIR}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
pg_dump -h "${POSTGRES_HOST:-postgres}" -U "${POSTGRES_USER}" "${POSTGRES_DB}" | gzip > "${FILE}"
echo "Backup criado em ${FILE}"
