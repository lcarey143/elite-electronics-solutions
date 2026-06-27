#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8080}"

log() {
  echo "[start] $*"
}

log "Starting gunicorn on 0.0.0.0:${PORT} (healthcheck can probe while setup runs)..."
gunicorn ees_project.wsgi \
  --bind "0.0.0.0:${PORT}" \
  --timeout 120 \
  --graceful-timeout 30 \
  --workers 2 &
GUNICORN_PID=$!

sleep 2

log "Running migrations..."
for attempt in 1 2 3 4 5 6 7 8 9 10; do
  if python manage.py migrate --noinput; then
    log "Migrations complete."
    break
  fi
  if [ "$attempt" -eq 10 ]; then
    log "Migrations failed after 10 attempts."
    kill "$GUNICORN_PID" 2>/dev/null || true
    exit 1
  fi
  log "Migrate attempt ${attempt} failed, retrying in 3s..."
  sleep 3
done

log "Seeding site data..."
python manage.py seed_data

log "Ensuring admin user..."
python manage.py ensure_admin

log "Collecting static files..."
python manage.py collectstatic --noinput

log "Email configuration:"
python manage.py check_email_config || true

log "Reloading gunicorn workers after setup..."
kill -HUP "$GUNICORN_PID"

log "Ready."
wait "$GUNICORN_PID"
