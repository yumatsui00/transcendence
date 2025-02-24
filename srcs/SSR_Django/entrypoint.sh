#!/bin/bash

set -e

export PYTHONPATH="/app"

echo "✅ Starting SSR-Django with HTTPS..."
exec gunicorn \
    --certfile=/etc/ssl/certs/ssr-django/ssr-django.crt \
    --keyfile=/etc/ssl/certs/ssr-django/ssr-django.key  \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    SSR_DjangoProject.wsgi:application --chdir /app
