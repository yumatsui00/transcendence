#!/bin/bash

# 証明書のディレクトリが存在しない場合、作成する
mkdir -p /etc/nginx/ssl

# # 証明書が存在しない場合のみ生成
# if [ ! -f "/etc/nginx/ssl/trascen.crt" ]; then
#     echo "Generating self-signed SSL certificate..."
#     openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#         -keyout /etc/nginx/ssl/trascen.key \
#         -out /etc/nginx/ssl/trascen.crt \
#         -subj "/C=JP/ST=Tokyo/L=Shinjuku/O=42Tokyo/OU=42Student/CN=internal-api-gateway" \
#         -addext "subjectAltName = DNS:internal-api-gateway"
#     chmod 644 /etc/nginx/ssl/trascen.*
#     mkdir -p /etc/nginx/ssl/volume
#     cp /etc/nginx/ssl/trascen.crt /etc/nginx/ssl/volume/trascen.crt
# fi

# Nginx を起動
nginx -g "daemon off;"
