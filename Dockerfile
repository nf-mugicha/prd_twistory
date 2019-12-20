# ベースイメージ
FROM python:3.7

RUN mkdir -p /var/www/
# workdirの指定
WORKDIR /var/www/

# 依存Pythonライブラリ一覧コピー
COPY requirements.txt ./

# 依存Pythonライブラリインストール
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt


CMD ["uwsgi","--ini","/var/www/uwsgi.ini"]
