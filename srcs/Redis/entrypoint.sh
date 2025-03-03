#!/bin/bash

set -e

echo "✅ Starting redis ..."

certfile="/etc/ssl/certs/redis/redis.crt"
keyfile="/etc/ssl/certs/redis/redis.key"

# 証明書ファイルとキーが存在するまで待機
until [ -f "$certfile" ] && [ -f "$keyfile" ]; do
  echo "Waiting for $certfile and $keyfile to be created..."
  sleep 1
done
# 環境変数からパスワードを取得
REDIS_PASSWORD=${REDIS_PASSWORD:-defaultpassword}

# redis.confファイルにパスワードを設定
sed -i "s/^requirepass .*/requirepass $REDIS_PASSWORD/" /etc/redis/redis.conf

exec redis-server /etc/redis/redis.conf