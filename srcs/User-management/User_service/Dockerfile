FROM python:3.12

#ping for debug
RUN apt-get update && apt-get install -y postgresql-client iputils-ping

#ワーキングディレクトリの設定
WORKDIR /app

#カレントディレクトリをコンテナにコピー
COPY . /app

# OpenSSL をインストール
# RUN apt-get update && apt-get install -y openssl

# 自己署名証明書を作成
# RUN mkdir -p /etc/ssl/django && \
#     openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#     -keyout /etc/ssl/django/django.key \
#     -out /etc/ssl/django/django.crt \
#     -subj "/CN=User-Service"

RUN pip install --no-cache-dir -r ./requirements.txt

COPY	./entrypoint.sh /entrypoint.sh
RUN	chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]