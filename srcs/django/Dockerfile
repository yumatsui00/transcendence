FROM python:3.12

ARG DB_PASS
ENV DB_PASS=${DB_PASS}

RUN apt-get update && apt-get install -y postgresql-client

#ワーキングディレクトリの設定
WORKDIR /app


# OpenSSL をインストール
RUN apt-get update && apt-get install -y openssl

# 自己署名証明書を作成
RUN mkdir -p /etc/ssl/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/certs/django.key \
    -out /etc/ssl/certs/django.crt \
    -subj "/CN=localhost"

#カレントディレクトリをコンテナにコピー
COPY . /app

RUN pip install --no-cache-dir -r ./tools/requirements.txt

COPY	./tools/init.sh /entrypoint.sh
RUN	chmod +x /entrypoint.sh




EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]