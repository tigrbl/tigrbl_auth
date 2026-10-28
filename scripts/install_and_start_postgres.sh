#!/usr/bin/env bash
set -euo pipefail

POSTGRES_DB="${POSTGRES_DB:-tba_auth_ci}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-postgres}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"

if ! command -v psql >/dev/null 2>&1; then
  echo "[postgres-setup] Installing PostgreSQL packages..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y postgresql postgresql-contrib
fi

CLUSTER_VERSION="$(ls /etc/postgresql 2>/dev/null | sort -V | tail -n1 || true)"
if [[ -z "${CLUSTER_VERSION}" ]]; then
  echo "[postgres-setup] No PostgreSQL cluster version directory found under /etc/postgresql." >&2
  exit 1
fi

if ! pg_lsclusters | awk '{print $1 " " $2 " " $4}' | grep -q "^${CLUSTER_VERSION} main online$"; then
  echo "[postgres-setup] Starting PostgreSQL cluster ${CLUSTER_VERSION}/main..."
  pg_ctlcluster "${CLUSTER_VERSION}" main start
fi

CONFIG_FILE="/etc/postgresql/${CLUSTER_VERSION}/main/postgresql.conf"
HBA_FILE="/etc/postgresql/${CLUSTER_VERSION}/main/pg_hba.conf"

if ! grep -q "^listen_addresses = '\*'" "${CONFIG_FILE}"; then
  sed -i "s|^#\?listen_addresses\s*=.*|listen_addresses = '*'|" "${CONFIG_FILE}"
fi
if ! grep -q "^port = ${POSTGRES_PORT}$" "${CONFIG_FILE}"; then
  sed -i "s/^#\?port\s*=.*/port = ${POSTGRES_PORT}/" "${CONFIG_FILE}"
fi
if ! grep -q "^host\s\+all\s\+all\s\+127\.0\.0\.1/32\s\+scram-sha-256" "${HBA_FILE}"; then
  echo "host all all 127.0.0.1/32 scram-sha-256" >> "${HBA_FILE}"
fi

pg_ctlcluster "${CLUSTER_VERSION}" main restart

if command -v sudo >/dev/null 2>&1; then
  PSQL_AS_POSTGRES=(sudo -u postgres psql -v ON_ERROR_STOP=1)
  PSQL_QUERY_AS_POSTGRES=(sudo -u postgres psql -tAc)
  CREATEDB_AS_POSTGRES=(sudo -u postgres createdb)
else
  PSQL_AS_POSTGRES=(runuser -u postgres -- psql -v ON_ERROR_STOP=1)
  PSQL_QUERY_AS_POSTGRES=(runuser -u postgres -- psql -tAc)
  CREATEDB_AS_POSTGRES=(runuser -u postgres -- createdb)
fi

"${PSQL_AS_POSTGRES[@]}" <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${POSTGRES_USER}') THEN
    CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASSWORD}';
  ELSE
    ALTER ROLE ${POSTGRES_USER} WITH LOGIN PASSWORD '${POSTGRES_PASSWORD}';
  END IF;
END
\$\$;
SQL

if ! "${PSQL_QUERY_AS_POSTGRES[@]}" "SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DB}'" | grep -q 1; then
  "${CREATEDB_AS_POSTGRES[@]}" -O "${POSTGRES_USER}" "${POSTGRES_DB}"
fi

echo "[postgres-setup] PostgreSQL is ready."
echo "[postgres-setup] POSTGRES_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:${POSTGRES_PORT}/${POSTGRES_DB}"
