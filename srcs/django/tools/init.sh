#!/bin/bash

#エラー時にスクリプトを停止
set -e

export PYTHONPATH="/app"

#データベースの起動を待つ
echo "Waiting for PSQL to be established..."
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\q" 2>&1; do
	echo "📌 PostgreSQL が起動していません。再試行中..."
	# echo "🔍 for debugging: PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c"
	sleep 2
done

echo "✅connection established"
echo "Migrating..."

# 🔹 すべてのアプリのマイグレーションを適用
# python manage.py migrate --noinput  # すべてのマイグレーションを適用

# 🔹 `app` のマイグレーションを適用
python manage.py makemigrations api
python manage.py migrate --noinput 


echo "🦄starting Django with Gunicorn..."
exec gunicorn --certfile=/etc/ssl/certs/django.crt --keyfile=/etc/ssl/certs/django.key \
    --bind 0.0.0.0:8000 --forwarded-allow-ips="*" backend.wsgi:application
