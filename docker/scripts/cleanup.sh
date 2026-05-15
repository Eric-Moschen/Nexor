#!/usr/bin/env sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"

find "${BACKUP_DIR}" -type f -name "nexor-*.sql.gz" -mtime +"${RETENTION_DAYS}" -delete
echo "Backups antigos removidos de ${BACKUP_DIR}"
