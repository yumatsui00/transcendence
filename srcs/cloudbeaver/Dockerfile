FROM dbeaver/cloudbeaver:latest

# 初期データベース接続設定をコピー
COPY data-sources.json /opt/cloudbeaver/workspace/GlobalConfiguration/data-sources.json

# 管理者アカウント設定をコピー
COPY server-config.json /opt/cloudbeaver/workspace/GlobalConfiguration/server-config.json
