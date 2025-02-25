FROM dbeaver/cloudbeaver:latest

# 初期データベース接続設定をコピー
COPY data-sources.json /opt/cloudbeaver/workspace/GlobalConfiguration/.dbeaver/data-sources.json
COPY .cloudbeaver.auto.conf /opt/cloudbeaver/conf/.cloudbeaver.auto.conf

COPY server-config.json /opt/cloudbeaver/workspace/GlobalConfiguration/.dbeaver/server-config.json
