FROM python:3.12

ARG DB_PASS
ENV DB_PASS=${DB_PASS}

RUN apt-get update && apt-get install -y postgresql-client

#ワーキングディレクトリの設定
WORKDIR /app

#カレントディレクトリをコンテナにコピー
COPY . /app

RUN pip install --no-cache-dir -r ./tools/requirements.txt

COPY	./tools/init.sh /entrypoint.sh
RUN	chmod +x /entrypoint.sh


EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]