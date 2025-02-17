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
python manage.py makemigrations api --noinput
python manage.py migrate --noinput 
python manage.py collectstatic --noinput #static内のファイルをstaticfilesにコピー



# echo "🦄starting Django with Gunicorn..."
# exec gunicorn \
#     --certfile=/etc/ssl/django/django.crt \
#     --keyfile=/etc/ssl/django/django.key \
#     --bind 0.0.0.0:8000 \
#     --workers 4 \
#     --access-logfile - \
#     --error-logfile - \
#     --timeout 120 \
#     backend.wsgi:application
#dpahneに変更
echo "🦄starting Django with Daphne..."
exec daphne -e ssl:442:privateKey=/etc/ssl/django/django.key:certKey=/etc/ssl/django/django.crt -b 0.0.0.0 backend.asgi:application