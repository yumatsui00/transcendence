FROM python:3.12

ARG DB_PASS
ENV DB_PASS=${DB_PASS}

RUN apt-get update && apt-get install -y

#ワーキングディレクトリの設定
WORKDIR /app

#カレントディレクトリをコンテナにコピー
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD bash /app/tools/init.sh