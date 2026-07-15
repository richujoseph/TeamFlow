#!/bin/bash
# =============================================================================
# TeamFlow EPMS — Backend Entrypoint
# =============================================================================
# Runs before the main command (gunicorn or runserver).
#
# 1. Waits for PostgreSQL to be ready
# 2. Runs migrations in development mode only
# 3. Collects static files
# 4. Executes the main command
# =============================================================================

set -e

echo "TeamFlow Backend — Starting up..."

# ---------------------------------------------------------------------------
# Wait for PostgreSQL to accept connections
# ---------------------------------------------------------------------------
echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-postgres}:${POSTGRES_PORT:-5432}..."

python << 'END'
import os
import socket
import sys
import time

host = os.environ.get("POSTGRES_HOST", "postgres")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        print(f"PostgreSQL is ready at {host}:{port}")
        sys.exit(0)
    except OSError:
        retry_count += 1
        print(f"  Attempt {retry_count}/{max_retries} — waiting...")
        time.sleep(1)

print(f"ERROR: Could not connect to PostgreSQL at {host}:{port} after {max_retries} attempts.")
sys.exit(1)
END

# ---------------------------------------------------------------------------
# Run migrations (development only)
# ---------------------------------------------------------------------------
if [ "${DJANGO_ENV}" = "development" ]; then
    echo "Running migrations (development mode)..."
    python manage.py migrate --noinput
    echo "Migrations complete."
else
    echo "Skipping auto-migration (production mode). Run 'manage.py migrate' explicitly."
fi

# ---------------------------------------------------------------------------
# Collect static files
# ---------------------------------------------------------------------------
echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

# ---------------------------------------------------------------------------
# Execute main command
# ---------------------------------------------------------------------------
echo "Starting application..."
exec "$@"
