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

exec redis-server /etc/redis/redis.conf