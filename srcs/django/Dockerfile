FROM python:3.12


RUN apt-get update && apt-get install -y postgresql-client

#ワーキングディレクトリの設定
WORKDIR /app

#カレントディレクトリをコンテナにコピー
COPY . /app

# OpenSSL をインストール
RUN apt-get update && apt-get install -y openssl

# 自己署名証明書を作成
RUN mkdir -p /etc/ssl/django && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/django/django.key \
    -out /etc/ssl/django/django.crt \
    -subj "/CN=localhost"



RUN pip install --no-cache-dir -r ./tools/requirements.txt

COPY	./tools/init.sh /entrypoint.sh
RUN	chmod +x /entrypoint.sh



EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]