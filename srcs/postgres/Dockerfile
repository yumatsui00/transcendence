FROM postgres:16.4

ARG PSQL_PASS
ARG DB_NAME
ARG DB_USER
ARG DB_PASS

ENV PSQL_PASS=${PSQL_PASS}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASS=${DB_PASS}

# 動的にSQLスクリプトを生成
RUN echo "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';" > /docker-entrypoint-initdb.d/init.sql \
    && echo "CREATE DATABASE ${DB_NAME};" >> /docker-entrypoint-initdb.d/init.sql \
    && echo "ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};" >> /docker-entrypoint-initdb.d/init.sql \
    && echo "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};" >> /docker-entrypoint-initdb.d/init.sql \
    && echo "GRANT USAGE, CREATE ON SCHEMA public TO ${DB_USER};" >> /docker-entrypoint-initdb.d/init.sql

RUN cat /docker-entrypoint-initdb.d/init.sql

CMD ["postgres"]