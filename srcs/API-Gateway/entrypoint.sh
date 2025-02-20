#!/bin/bash

set -e

export PYTHONPATH="/app"
exec "$@"


echo "✅connection between 2FA-DB established"
echo "Migrating..."

# python manage.py makemigrations --noinput
# python manage.py migrate --noinput

echo "✅ Starting 2FA-service with HTTPS..."
exec gunicorn \
    --certfile=/etc/ssl/certs/api-gateway/api-gateway.crt \
    --keyfile=/etc/ssl/certs/api-gateway/api-gateway.key \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    API_Gateway.wsgi:application --chdir /app