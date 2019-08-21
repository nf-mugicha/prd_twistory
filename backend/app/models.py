#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask
from settings.certification import api, api_header
import csv
import settings.twitter_api as twitter_api
from urllib.parse import urlencode, quote, quote_plus
import hashlib
import hmac
import base64
from operator import itemgetter
import time
import requests
import os  # for nonce
import json
import pickle


def vue_app(app_name="VUE-FLASK"):
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')

    return app


# def get_tweet(account):
#     # 全ツイートを入れる空のリストを用意
#     all_tweets = []
#     # 直近の200ツイート分を取得しておく
#     latest_tweets = api.user_timeline(screen_name=account, count=200)
#     all_tweets.extend(latest_tweets)
#     # 取得するツイートがなくなるまで続ける
#     while len(latest_tweets) > 0:
#         # while True:
#         latest_tweets = api.user_timeline(
#             screen_name=account,
#             count=200, max_id=all_tweets[-1].id-1)
#         all_tweets.extend(latest_tweets)
#         print(str(all_tweets[-1].id-1))
#     # デバッグのためファイル書き出ししてみる
#     with open("alltweets_raw_data.json", "w", newline="") as f:
#         all_tweets_raw_data = f.write(all_tweets)
#     return all_tweets_raw_data, all_tweets


# def set_tsv(all_tweets_raw_data):
#     """
#     抽出したデータをファイルに書き込む関数
#     """
#     with open(filename, 'w', newline="") as f:
#         writer = csv.writer(f, delimiter='\t')
#         writer.writerow(
#             ['tweet_text', '#characters', '#favorited',
#                 '#retweeted', 'hasImage', 'create_at',
#                 "image_1st", "image_2nd", "image_3rd", "image_4th"
#              ])
#         print(writer)
#         for tweet in all_tweets:
#             # RTとリプライはスキップ
#             # if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
#             #     continue
#             # else:
#             # 画像付きのツイートか
#             has_image = 0
#             # ブログリンク付きのツイートか
#             # has_bloglink = 0
#             # ツイート文字列
#             tweet_characters = tweet.text
#             # if 'media' in tweet.entities:
#             #     # urlは文字数としてカウントしない
#             #     tweet_characters = tweet_characters.strip(
#             #         tweet.entities['urls'][0]['url']
#             #     ).strip()
#             writecsv.writerow(
#                 [tweet.text,
#                     len(tweet_characters),
#                     tweet.favorite_count,
#                     tweet.retweet_count,
#                     has_image,
#                     tweet.created_at]
#             )
#         print([tweet.text,
#                len(tweet_characters),
#                tweet.favorite_count,
#                tweet.retweet_count,
#                has_image,
#                tweet.created_at]
#               )


def get_3200_user_timeline(account):
        # 3200ツイートを入れる空のリストを用意
    all_tweets = []
    # 直近200ツイートを取得
    latest_tweets = api.GetUserTimeline(
        screen_name=account,
        count=200
    )
    # 直近200ツイートを格納
    all_tweets.extend(latest_tweets)

    # for s in statuse:
    # print(s.text)

    # 取得するツイートがなくなるまで続ける
    while len(latest_tweets) > 0:
        # while True:
        # while True:
        latest_tweets = api.GetUserTimeline(
            screen_name=account,
            count=200,
            max_id=all_tweets[-1].id-1
        )
        all_tweets.extend(latest_tweets)
        print(str(all_tweets[-1].id-1))
    # 取得した3200ツイート生データをファイル書き出ししておく
    with open(user_timeline_3200_raw,
              "wb") as f:
        pickle.dump(all_tweets, f)
        # for tweet in all_tweets:
        #     # json形式のstr型ファイルとして格納
        #     # json.dump(dict, tweet, indent=2)
        #     f.wtite(str(tweet) + "\n")
    return all_tweets


def set_tsv(all_tweets):
    with open(filename_3200, 'w', newline='') as f:
        # ファイル出力準備
        writecsv = csv.DictWriter(
            f,
            [
                'id', 'tweet_text', 'favorite_count',
                'retweet_count', 'hasImage', 'created_at',
                "image_0", "image_1", "image_2", "image_3"
            ],
            delimiter='\t'
        )
        writecsv.writeheader()
        tweet_excerpt = {}
        for tweet in all_tweets:
            # 連想配列に格納
            tweet_excerpt['id'] = tweet.id
            tweet_excerpt["tweet_text"] = tweet.text
            tweet_excerpt["favorite_count"] = tweet.favorite_count
            tweet_excerpt["retweet_count"] = tweet.retweet_count
            tweet_excerpt["created_at"] = tweet.created_at
            tweet_excerpt["hasImage"] = False
            # 画像つきのツイートだったら画像URLを格納
            if tweet.media:
                tweet_excerpt["hasImage"] = True
                for i, m in enumerate(tweet.media):
                    tweet_excerpt["image_{}".format(i)] = m.media_url_https
            # ファイル出力
            writecsv.writerow(tweet_excerpt)
            # 辞書を初期化
            tweet_excerpt = {}
    max_id = all_tweets[-1].id-1
    # 3200ツイート分のリストと、最後のmax_idを返す
    return all_tweets, max_id


def get_all_user_timeline(account, max_id):
    consumer_key = twitter_api.CONSUMER_KEY
    consumer_secret = twitter_api.CONSUMER_SECRET_KEY
    access_token = twitter_api.ACCESS_TOKEN
    access_token_secret = twitter_api.ACCESS_TOKEN_SECRET
    req_method = "GET"

    # Creating key
    key = "&".join([consumer_secret, access_token_secret])
    key = key.encode("utf-8")
    print("[+] Key:\n\n", key)

    # For authentication
    timestamp = time.time()
    nonce = os.urandom(10).hex()

    params_b = {
        "oauth_token": access_token,
        "oauth_consumer_key": consumer_key,
        "oauth_signature_method": 'HMAC-SHA1',
        "oauth_timestamp": timestamp,
        "oauth_nonce": nonce,
        "oauth_version": "1.0",
    }
    with open(filename_all, 'w', newline='') as f:
        # ファイル出力準備
        writecsv = csv.DictWriter(
            f,
            [
                'id', 'tweet_text', 'favorite_count',
                'retweet_count', 'hasImage', 'created_at',
                "image_0", "image_1", "image_2", "image_3"
            ],
            delimiter='\t'
        )
        writecsv.writeheader()
        # counter
        a = 0
        # ファイル書き出しようの連想配列
        tweet_excerpt = {}
        # 取得したツイートを格納する
        all_tweets = []
        while True:
            print(a)
            # print(type(max_id))
            # print(max_id)
            req_url = twitter_api.TWITTER_API_URL
            params_a = {
                "q": "from:{0}\tmax_id:{1}".format(account, max_id),
                # "q": "from:"+str(account),
                # "q": "from:{}\suntil:2019-08-19".format(account),
                "modules": "status",
                "count": 50
            }

            # Marge params
            params_c = dict(params_a)
            params_c.update(params_b)

            req_params = sorted(params_c.items(), key=itemgetter(0))
            req_params = urlencode(req_params)
            # By default, quote() do not quote "/".
            req_params = quote(req_params, safe="")
            # print("[+] req_params:\n\n", req_params)

            enc_req_method = quote(req_method, safe="")
            enc_req_url = quote(req_url, safe="")
            signature_data = "&".join(
                [enc_req_method, enc_req_url, req_params])
            signature_data = signature_data.encode("utf-8")

            digester = hmac.new(key, signature_data, hashlib.sha1)
            _hash = digester.digest()

            signature = base64.b64encode(_hash)
            # print("[+] signature:\n\n", signature)
            # params_c["oauth_signature"] = signature
            params_c["oauth_signature"] = signature

            # give me idea to rewrite dict into "key=value, key=value,..."
            oauth_params = urlencode(params_c)
            oauth_params = oauth_params.replace("&", ",")
            # print("[+] oauth_params:\n\n", oauth_params)

            headers = {
                "Authorization": "OAuth " + oauth_params
            }

            req_url += '?' + urlencode(params_a)
            # print(req_url)
            # print('\n')

            res = requests.get(req_url, headers=headers)
            datas = res.json()  # API response
            if len(datas) < 2:
                print('error response')
                print(datas)
                # 取得した3200ツイート生データをファイル書き出ししておく
                with open(user_timeline_all_raw,
                          "wb") as f:
                    pickle.dump(all_tweets, f)
                break
            elif len(datas["modules"]) == 0:
                print(datas)
                print('finish tweet scraping')
                # 取得した生データをファイル書き出ししておく
                with open(user_timeline_all_raw,
                          "wb") as f:
                    pickle.dump(all_tweets, f)
                break
            else:
                # データを格納する
                for i, data in enumerate(datas["modules"]):
                    data = [data["status"]['data']]
                    all_tweets.extend(data)
                    # 連想配列に格納
                    tweet_excerpt["id"] = data[0]["id"]
                    tweet_excerpt["tweet_text"] = data[0]["text"]
                    tweet_excerpt["favorite_count"] = data[0]["favorite_count"]
                    tweet_excerpt["retweet_count"] = data[0]["retweet_count"]
                    tweet_excerpt["created_at"] = data[0]["created_at"]
                    tweet_excerpt["hasImage"] = False
                    # 画像つきのツイートだったら画像URLを格納
                    if "extended_entities" in data[0]:
                        if "media" in data[0]["extended_entities"]:
                            tweet_excerpt["hasImage"] = True
                            for i, m in enumerate(data[0]["extended_entities"]['media']):
                                tweet_excerpt["image_{}".format(
                                    i)] = m["media_url_https"]
                    # ファイル出力
                    writecsv.writerow(tweet_excerpt)
                    # 辞書を初期化
                    tweet_excerpt = {}
                # print(data[0]["id"])
                max_id = data[0]["id"]-1
                a = a+1
                print('oldest_max_id: {}'.format(max_id))


if __name__ == '__main__':
    print('start tweet scraping')
    account = "Pxilicon"
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
        all_tweets = get_3200_user_timeline(account)
    # 保存したファイルを開く
    with open(user_timeline_3200_raw, 'rb') as f:
        print(f)
        all_tweets = pickle.load(f)
        all_tweets, max_id = set_tsv(all_tweets)
    # max_id = 1154384366694359041
    get_all_user_timeline(account, max_id)
