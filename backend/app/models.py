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


def vue_app(app_name="VUE-FLASK"):
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')

    return app


def get_tweet(account):
    # 全ツイートを入れる空のリストを用意
    all_tweets = []
    # 直近の200ツイート分を取得しておく
    latest_tweets = api.user_timeline(screen_name=account, count=200)
    all_tweets.extend(latest_tweets)

    # 取得するツイートがなくなるまで続ける
    while len(latest_tweets) > 0:
        # while True:
        latest_tweets = api.user_timeline(
            screen_name=account,
            count=200, max_id=all_tweets[-1].id-1)
        all_tweets.extend(latest_tweets)
        print(str(all_tweets[-1].id-1))

    with open('all_tweets_nobodytrurai_1.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ['tweet_text', '#characters', '#favorited',
                '#retweeted', 'hasImage', 'create_at']
        )
        print(writer)
        for tweet in all_tweets:
            # RTとリプライはスキップ
            # if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
            #     continue
            # else:
            # 画像付きのツイートか
            has_image = 0
            # ブログリンク付きのツイートか
            # has_bloglink = 0
            # ツイート文字列
            tweet_characters = tweet.text
            # if 'media' in tweet.entities:
            #     # urlは文字数としてカウントしない
            #     tweet_characters = tweet_characters.strip(
            #         tweet.entities['urls'][0]['url']
            #     ).strip()
            writecsv.writerow(
                [tweet.text,
                    len(tweet_characters),
                    tweet.favorite_count,
                    tweet.retweet_count,
                    has_image,
                    tweet.created_at]
            )
        print([tweet.text,
               len(tweet_characters),
               tweet.favorite_count,
               tweet.retweet_count,
               has_image,
               tweet.created_at]
              )


def get_user_timeline(account):
    # 全ツイートを入れる空のリストを用意
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
    with open(filename, 'w', newline='') as f:
        writecsv = csv.writer(f)
        writecsv.writerow([
            'tweet_text', '#characters', '#favorited',
            '#retweeted', 'hasImage', 'create_at']
        )
        for tweet in all_tweets:
                # RTとリプライはスキップ
                # if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
                #     continue
                # else:
                # 画像付きのツイートか
            has_image = 0
            # ファイル出力
            writecsv.writerow([
                tweet.text,
                tweet.favorite_count,
                tweet.retweet_count,
                has_image,
                tweet.created_at]
            )
        # writer.writerow([tweet])
        # print([tweet.text,
        #        tweet.favorite_count,
        #        tweet.retweet_count,
        #        has_image,
        #        tweet.created_at]
        #       )
    max_id = all_tweets[-1].id-1
    # 3200ツイート分のリストと、最後のmax_idを返す
    return all_tweets, max_id


def get_user_tweets_more(account, max_id, all_tweets):
    consumer_key = twitter_api.CONSUMER_KEY
    consumer_secret = twitter_api.CONSUMER_SECRET_KEY
    access_token = twitter_api.ACCESS_TOKEN
    access_token_secret = twitter_api.ACCESS_TOKEN_SECRET
    req_method = "GET"

    # req_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    # For api
    # params_a = {
    #     "screen_name": "73_spica",
    #     "count": 200
    # }

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
    with open(filename_2, 'w', newline='') as f:
        writecsv = csv.writer(f)
        writecsv.writerow([
            'tweet_text', '#characters', '#favorited',
            '#retweeted', 'hasImage', 'create_at']
        )
        # writecsv = csv.writer(f)
        a = 0
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
                continue
            elif len(datas['modules']) == 0:
                print('finish tweet scraping')
                break
            else:
                # データを格納する
                for i, data in enumerate(datas["modules"]):
                    data = [data["status"]['data']]
                    all_tweets.extend(data)
                    # print(all_tweets[-1]['text'])
                    # print(all_tweets[-1]["id"])
                    # 画像付きのツイートか
                    has_image = 0
                    # ファイル出力
                    tweet_list = [data[0]["text"],
                                  data[0]["favorite_count"],
                                  data[0]["retweet_count"],
                                  has_image,
                                  data[0]["created_at"]
                                  ]
                    writecsv.writerow(tweet_list)
                    # print(type(list))
                    # print(list)
                # print(data[0]["id"])
                max_id = data[0]["id"]-1
                a = a+1
                print('oldest_max_id: {}'.format(max_id))


if __name__ == '__main__':
    print('start')
    account = "hinodeeeeee"
    filename = "tweet_data_{}.csv".format(account)
    filename_2 = "tweet_data_{}_2.csv".format(account)
    # get_tweet('nobody_tsurai')
    all_tweets, max_id = get_user_timeline(account)
    # これが3200ツイート目
    # max_id = 1140264711226662911
    # max_id = 1148956601585291263
    # これが最初のmax_id
    # max_id = 1159413593881939967
    # get_user_tweets("nobody_tsurai", max_id)
    # all_tweets = []
    # max_id = 1139674341669400575
    # all_tweets = []
    # max_id = 486369808967929858
    get_user_tweets_more(account, max_id, all_tweets)
