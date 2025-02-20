FROM python:3.12

#ワーキングディレクトリの設定
WORKDIR /app

#カレントディレクトリをコンテナにコピー
COPY . /app

# OpenSSL をインストール
RUN apt-get update && apt-get install -y openssl && apt-get clean

# 自己署名証明書を作成
RUN mkdir -p /etc/ssl/django && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/django/django.key \
    -out /etc/ssl/django/django.crt \
    -subj "/CN=localhost"
# 自己証明書を.pemとして作成
RUN cat /etc/ssl/django/django.crt /etc/ssl/django/django.key > /etc/ssl/django/django.pem
RUN pip install --no-cache-dir -r ./requirements.txt

COPY	./entrypoint.sh /entrypoint.sh
RUN	chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]