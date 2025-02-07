FROM postgres:16.4

# 動的にSQLスクリプトを生成
RUN echo "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';" > /docker-entrypoint-initdb.d/init.sql \
    && echo "CREATE DATABASE ${POSTGRES_DB};" >> /docker-entrypoint-initdb.d/init.sql \
    && echo "ALTER DATABASE ${POSTGRES_DB} OWNER TO ${POSTGRES_USER};" >> /docker-entrypoint-initdb.d/init.sql \
    && echo "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};" >> /docker-entrypoint-initdb.d/init.sql \
    && echo "GRANT USAGE, CREATE ON SCHEMA public TO ${POSTGRES_USER};" >> /docker-entrypoint-initdb.d/init.sql

RUN cat /docker-entrypoint-initdb.d/init.sql

CMD ["postgres"]