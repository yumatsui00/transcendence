#!/bin/bash

#エラー時にスクリプトを停止
set -e



# Djangoプロジェクトがあるか確認。あったらスキップ
if [ ! -f "/app/manage.py" ]; then
	echo "Creating Django Project..."
	django-admin startproject app /app
fi

#データベースの起動を待つ
echo "Waiting for PSQL to be established..."
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1;" 2>&1; do
	echo "📌 PostgreSQL が起動していません。再試行中..."
	# echo "🔍 for debugging: PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c"
	sleep 2
done

echo "✅connection established"
echo "Migrating..."
python manage.py migrate


echo "🦄starting Django with Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 app.wsgi:application