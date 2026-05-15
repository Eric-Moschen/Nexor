#!/usr/bin/env sh
set -eu

if [ "${1:-}" = "" ]; then
  echo "Uso: restore.sh /backups/arquivo.sql.gz"
  exit 1
fi

export PGPASSWORD="${POSTGRES_PASSWORD}"
gzip -dc "$1" | psql -h "${POSTGRES_HOST:-postgres}" -U "${POSTGRES_USER}" "${POSTGRES_DB}"
echo "Restore concluido a partir de $1"
