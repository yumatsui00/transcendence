FROM ubuntu:latest

RUN apt-get update && apt-get install -y redis-server

RUN mkdir -p /etc/redis

COPY ./redis.conf /etc/redis/redis.conf

# Redisサーバーを起動
CMD ["redis-server", "/etc/redis/redis.conf"]