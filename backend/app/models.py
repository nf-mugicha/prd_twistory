#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask
import os  # for nonce
import pickle
import csv
import traceback
import time

from functions.get_3200_user_timeline import get_3200_user_timeline
from functions.get_all_user_timeline import get_all_user_timeline
from functions.save_tsv_3200_tweets import save_tsv_3200_tweets
from functions.save_tsv_all_tweets import save_tsv_all_tweets
from functions.preprocess import clean_tweet_text

from functions.PrepareChain import PrepareChain
from functions.GenerateText import GenerateText

from settings.logging import logging_setting

from settings.certification import api
import settings.twitter_api as twitter_api

logger = logging_setting('TweetGeneratorLogging')


def vue_app(app_name="VUE-FLASK"):
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')

    return app


class TweetsGenerater(object):
    """
    ツイート生成クラス
    twitterAPIを使用して任意のアカウントのツイートを取得する。
    形態素解析した単語の三つ組を作り、tsvファイルに保存する
    マルコフ連鎖でツイート生成する。
    """

    def __init__(self, account):
        """
        初期化メソッド
        @param account アカウント名
        """
        self.account = account
        self.filepath = "get_tweets_assets/{0}".format(account)
        # ユーザーごとにフォルダを分ける
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)
        # 取得したツイートツイート保存先
        self.filename_3200 = "{0}/tweets_3200_{1}.tsv".format(
            self.filepath, account)
        self.filename_all = "{0}/tweets_all_{1}.tsv".format(
            self.filepath, account)
        self.user_timeline_3200_raw = "{0}/tweets_3200_raw_{1}.pkl".format(
            self.filepath, account)
        self.user_timeline_all_raw = "{0}/tweets_all_raw_{1}.pkl".format(
            self.filepath, account)
        # 3grams保存先
        self.triplet_freqs_tsv = "{0}/triplet_freqs_3200_{1}.tsv".format(
            self.filepath, account)

    def _get_latest_tweets(self, since_id, account, filename_3200):
        """
        最新から過去3200ツイートまでを保管する関数
        twitter-pythonライブラリを用いる。
        取得したツイートはTwitter.Status型のリストをpklファイルに保存する
        """
        logger.info(
            "start latests' 200 tweets scraping since_id: {}".format(since_id))
        # 3200ツイートを入れる空のリストを用意
        all_tweets = []
        # 直近200ツイートを取得
        try:
            latest_tweets = api.GetUserTimeline(
                screen_name=account,
                count=200,
                since_id=since_id
            )
        except:
            logger.error(
                "{} may be private account or does not exists, can not get user timeline".format(account))
            raise
        # もし取得するツイートがなかったらそのまま返す
        if len(latest_tweets) == 0:
            logger.info("Nothing of latest tweets")
            return all_tweets, since_id
        # since_idから遡った200件の、最も新しいid（200件以上新作があった時に使う）
        latest_id = latest_tweets[0].id
        logger.info("now's latest id: {}".format(str(latest_tweets[0].id)))
        # 直近200ツイートを格納
        all_tweets.extend(latest_tweets)
        # 取得するツイートがなくなるまで続ける
        logger.info("start tweets scraping more")
        c = 1
        while len(latest_tweets) > 0:
            logger.info("count {0} max_id: {1}".format(c, all_tweets[-1].id-1))
            latest_tweets = api.GetUserTimeline(
                screen_name=account,
                count=200,
                since_id=latest_id
            )
            all_tweets.extend(latest_tweets)
            c = c+1
        logger.info("latest tweets {} counts".format(len(all_tweets)))
        # 取得した3200ツイート生データをファイル書き出ししておく
        with open(filename_3200, "a", newline="") as f:
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
            tweet_excerpt = {}
            c = 0
            for tweet in all_tweets:
                c = c+1
                logger.info("count: {0}, {1}".format(c, tweet.id))
                if tweet.id == since_id:
                    break
                # RTは除外
                if tweet.text.startswith('RT'):
                    continue
                # ツイートテキストを前処理
                tweet_text = clean_tweet_text(tweet.text, logger)
                # 連想配列に格納
                tweet_excerpt['id'] = tweet.id
                tweet_excerpt["tweet_text"] = tweet_text
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
            latest_id = all_tweets[0].id-1
        return all_tweets, latest_id

    def get_tweet(self):
        # 既に3200件のデータを取り終えていたらやらない
        if not os.path.exists(self.user_timeline_3200_raw):
            # 3200件のツイートデータ取得・保存
            all_tweets, latest_id, max_id = get_3200_user_timeline(
                self.account, self.user_timeline_3200_raw, logger)
        # tsvファイルもあればそれを開く
        if os.path.exists(self.filename_3200):
            logger.info('already done all tweets scraping')
            logger.info("open file of 3200 tweets data: {}".format(
                self.filename_3200))
            all_tweets = []
            all_tweets_id = []
            with open(self.filename_3200, 'r') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    all_tweets.append(row)
                    all_tweets_id.append(int(row["id"]))
                max_id = int(min(all_tweets_id))-1
                latest_id = int(max(all_tweets_id))
                logger.info('max_id: {}'.format(max_id))
                logger.info('latest_id: {}'.format(latest_id))

        else:
            # 保存したpklファイルを開く
            with open(self.user_timeline_3200_raw, 'rb') as f:
                all_tweets = pickle.load(f)
                # 3200ツイート取得・tsvファイルに保存
                all_tweets, max_id, latest_id = save_tsv_3200_tweets(
                    all_tweets, self.filename_3200, logger)
                logger.info('save 3200tweets: {}'.format(self.filename_3200))
                logger.info('max_id: {}'.format(max_id))
                logger.info('latest_id: {}'.format(latest_id))
        # 今保存されているものより新しいツイートを取得し、tsvファイルに上書きする
        all_tweets, latest_id = self._get_latest_tweets(
            latest_id, self.account, self.filename_3200)
        # todo 全データ取得APIを作るか不明なので一旦コメントアウト
        # 全データ保存ファイルが既に存在したら取ってくる
        # if os.path.exists(self.user_timeline_all_raw):
        #     logger.info('already done all tweets scraping')
        #     with open(self.user_timeline_all_raw, 'rb') as f:
        #         logger.info("open file of all tweets data: {}".format(
        #             self.user_timeline_all_raw))
        #         # 全てのツイートデータのファイルをロード
        #         all_tweets_pkl = pickle.load(f)
        #     save_tsv_all_tweets(all_tweets_pkl, self.filename_all, logger)
        # # ファイルがなかったら新しく取得
        # else:
        #     get_all_user_timeline(
        #         self.account,
        #         max_id,
        #         self.user_timeline_all_raw,
        #         self.filename_all,
        #         logger
        #     )

    def generate_tweets(self):
        # ツイートテキストだけを抽出する
        tweet_text_list = []
        with open(self.filename_3200, newline='') as f:
            logger.debug("open: {}".format(self.filename_3200))
            # with open(self.filename_all, newline='') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                tweet_text_list.append(row['tweet_text'])
        logger.info("{} tweets in this list now".format(len(tweet_text_list)))
        # 。で繋げて１つのテキストにする
        text = "。".join(tweet_text_list[:-1])
        logger.debug("joined tweets text:\n{}\n".format(text))
        # 3gramsのtsvファイルが存在したらgeneratorを立ち上げる
        # if os.path.exists(self.triplet_freqs_tsv):
        #     logger.info("{} exists".format(self.triplet_freqs_tsv))
        #     # tsvファイルからツイート生成
        #     logger.info('start generate tweets')
        #     generator = GenerateText(logger)
        #     generator.generate_from_tsv(self.triplet_freqs_tsv)
        #     logger.info('finish generate tweets')
        # else:
        # 毎回最新ツイートを取得するため、毎回tsvファイルを読み込む
        logger.info('start make 3grams')
        # 3gramsを作る準備
        chain = PrepareChain(text, logger)
        # 三つ組のテキストと出現回数を保存
        triplet_freqs = chain.make_triplet_freqs()
        # tsvファイルに保存
        chain.save_tsv(triplet_freqs=triplet_freqs,
                       file_triplet_freqs=self.triplet_freqs_tsv, init=True)
        logger.info('finished make 3grams')
        # tsvファイルからツイート生成
        logger.info('start generate tweets')
        generator = GenerateText(logger)
        generator.generate_from_tsv(self.triplet_freqs_tsv)
        logger.info('finish generate tweets')


if __name__ == '__main__':
    start = time.time()
    logger.info('start generate tweet')
    try:
        account = "Pxilicon"
        logger.info('account name: {}'.format(account))
        tweets_generater = TweetsGenerater(account)
        tweets_generater.get_tweet()
        tweets_generater.generate_tweets()
        elapsed_time = time.time() - start
        logger.info('finish time: {} [sec.]'.format(elapsed_time))
    except:
        logger.error(traceback.format_exc())
