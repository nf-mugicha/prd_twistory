#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask
import os  # for nonce
import pickle
from functions.get_3200_user_timeline import get_3200_user_timeline
from functions.get_all_user_timeline import get_all_user_timeline
from functions.save_tsv_3200_tweets import save_tsv_3200_tweets
from functions.save_tsv_all_tweets import save_tsv_all_tweets


def vue_app(app_name="VUE-FLASK"):
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')

    return app


def get_tweet(account):
    filepath = "get_tweets_assets/{0}".format(account)
    # ユーザーごとにフォルダを分ける
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filename_3200 = "{0}/tweets_3200_{1}.tsv".format(
        filepath, account)
    filename_all = "{0}/tweets_all_{1}.tsv".format(
        filepath, account)
    user_timeline_3200_raw = "{0}/tweets_3200_raw_{1}.pkl".format(
        filepath, account)
    user_timeline_all_raw = "{0}/tweets_all_raw_{1}.pkl".format(
        filepath, account)
    # 既に3200件のデータを取り終えていたらやらない
    if not os.path.exists(user_timeline_3200_raw):
        # 3200件のツイートデータ取得・保存
        all_tweets = get_3200_user_timeline(
            account, user_timeline_3200_raw)
    # 保存したpklファイルを開く
    with open(user_timeline_3200_raw, 'rb') as f:
        print(f)
        all_tweets = pickle.load(f)
        # 3200ツイート取得・tsvファイルに保存
        # all_tweets, max_id = set_tsv(all_tweets)
        all_tweets, max_id = save_tsv_3200_tweets(all_tweets, filename_3200)
    # max_id = 1154384366694359041
    # 全データ保存
    if os.path.exists(user_timeline_all_raw):
        print('all data exists')
        with open(user_timeline_all_raw, 'rb') as f:
            print(f)
            all_tweets_pkl = pickle.load(f)
        save_tsv_all_tweets(all_tweets_pkl, filename_all)
    else:
        get_all_user_timeline(
            account, max_id, user_timeline_all_raw, filename_all)


if __name__ == '__main__':
    print('start tweet scraping')
    account = ""
    get_tweet(account)
