from settings.certification import api
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
from .preprocess import clean_tweet_text

"""
ユーザータイムラインを3200件以上取得する。
twitterAPI仕様
・一度に取得できるツイート数は50件
・コール制限　1500回/15分間

一度に7万5000ツイート取得可能
理論上は全ツイート取得が可能。

取得したツイートの連想配列のリストをpklファイルに保存する
"""


def get_all_user_timeline(
        account, max_id, user_timeline_all_raw, filename_all, logger):
    logger.debug("start scraping more {}s' timeline".format(account))
    logger.debug("scraping from {}".format(max_id))
    consumer_key = twitter_api.CONSUMER_KEY
    consumer_secret = twitter_api.CONSUMER_SECRET_KEY
    access_token = twitter_api.ACCESS_TOKEN
    access_token_secret = twitter_api.ACCESS_TOKEN_SECRET
    req_method = "GET"

    # Creating key
    key = "&".join([consumer_secret, access_token_secret])
    key = key.encode("utf-8")
    logger.info("Key: {}".format(key))

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
            logger.info("connect twitterAPI counter: {}".format(a))
            req_url = twitter_api.TWITTER_API_URL
            params_a = {
                "q": "from:{0}\tmax_id:{1}".format(account, max_id),
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
            logger.info("req_params: {}".format(req_params))

            enc_req_method = quote(req_method, safe="")
            enc_req_url = quote(req_url, safe="")
            signature_data = "&".join(
                [enc_req_method, enc_req_url, req_params])
            signature_data = signature_data.encode("utf-8")

            digester = hmac.new(key, signature_data, hashlib.sha1)
            _hash = digester.digest()

            signature = base64.b64encode(_hash)
            logger.info("signature: {}".format(signature))
            # params_c["oauth_signature"] = signature
            params_c["oauth_signature"] = signature

            # give me idea to rewrite dict into "key=value, key=value,..."
            oauth_params = urlencode(params_c)
            oauth_params = oauth_params.replace("&", ",")
            logger.info("oauth_params: {}".format(oauth_params))

            headers = {
                "Authorization": "OAuth " + oauth_params
            }

            req_url += '?' + urlencode(params_a)
            logger.info("request URL: {}".format(req_url))
            # print('\n')

            res = requests.get(req_url, headers=headers)
            datas = res.json()  # API response
            if len(datas) < 2:
                logger.info('error response')
                logger.info(datas)
                # 取得した生データをファイル書き出ししておく
                with open(user_timeline_all_raw,
                          "wb") as f:
                    pickle.dump(all_tweets, f)
                    logger.info("save file until this time: {}".format(
                        user_timeline_all_raw))
                break
            elif len(datas["modules"]) == 0:
                logger.info('finish tweet scraping')
                logger.info(datas)
                # 取得した生データをファイル書き出ししておく
                with open(user_timeline_all_raw,
                          "wb") as f:
                    pickle.dump(all_tweets, f)
                    logger.info("save file: {}".format(
                        user_timeline_all_raw))
                break
            else:
                # データを格納する
                for i, data in enumerate(datas["modules"]):
                    data = [data["status"]['data']]
                    all_tweets.extend(data)
                    # RTは除外
                    if data[0]["text"].startswith('RT'):
                        continue
                    # ツイートテキスト前処理
                    tweet_text = clean_tweet_text(data[0]["text"], logger)
                    # 連想配列に格納
                    tweet_excerpt["id"] = data[0]["id"]
                    tweet_excerpt["tweet_text"] = tweet_text
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
                    logger.info("tweet: {}".format(tweet_excerpt))
                    # 辞書を初期化
                    tweet_excerpt = {}
                # print(data[0]["id"])
                max_id = data[0]["id"]-1
                a = a+1
                logger.debug('oldest_max_id: {}'.format(max_id))
