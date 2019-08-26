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

from functions.get_3200_user_timeline import get_3200_user_timeline
from functions.get_all_user_timeline import get_all_user_timeline
from functions.save_tsv_3200_tweets import save_tsv_3200_tweets
from functions.save_tsv_all_tweets import save_tsv_all_tweets

from functions.PrepareChain import PrepareChain
from functions.GenerateText import GenerateText

from settings.logging import logging_setting

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

    def get_tweet(self):
        # 既に3200件のデータを取り終えていたらやらない
        if not os.path.exists(self.user_timeline_3200_raw):
            # 3200件のツイートデータ取得・保存
            all_tweets, latest_id = get_3200_user_timeline(
                self.account, self.user_timeline_3200_raw, logger)
        # tsvファイルもあればそれを開く
        if os.path.exists(self.filename_3200):
            logger.info('already done all tweets scraping')
            logger.info("open file of 3200 tweets data: {}".format(
                self.filename_3200))
            all_tweets = []
            with open(self.filename_3200, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_tweets.append(row)
                max_id = all_tweets[-1]["max_id"]-1
        else:
            # 保存したpklファイルを開く
            with open(self.user_timeline_3200_raw, 'rb') as f:
                all_tweets = pickle.load(f)
                # 3200ツイート取得・tsvファイルに保存
                all_tweets, max_id = save_tsv_3200_tweets(
                    all_tweets, self.filename_3200, logger)
                logger.debug('save 3200tweets: {}'.format(self.filename_3200))
                logger.debug("latest id: {0}".format(max_id))
        # 全データ保存ファイルが既に存在したら取ってくる
        if os.path.exists(self.user_timeline_all_raw):
            logger.info('already done all tweets scraping')
            with open(self.user_timeline_all_raw, 'rb') as f:
                logger.info("open file of all tweets data: {}".format(
                    self.user_timeline_all_raw))
                # 全てのツイートデータのファイルをロード
                all_tweets_pkl = pickle.load(f)
            save_tsv_all_tweets(all_tweets_pkl, self.filename_all, logger)
        # ファイルがなかったら新しく取得
        else:
            get_all_user_timeline(
                self.account,
                max_id,
                self.user_timeline_all_raw,
                self.filename_all,
                logger
            )

    def generate_tweets(self):
        # ツイートテキストだけを抽出する
        tweet_text_list = []
        with open(self.filename_3200, newline='') as f:
            logger.debug("open: {}".format(self.filename_3200))
            # with open(self.filename_all, newline='') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                tweet_text_list.append(row['tweet_text'])
        # 。で繋げて１つのテキストにする
        text = "。".join(tweet_text_list[:-1])
        logger.debug("joined tweets text:\n{}\n".format(text))
        # tsvファイルが存在したらgeneratorを立ち上げる
        if os.path.exists(self.triplet_freqs_tsv):
            logger.info("{} exists".format(self.triplet_freqs_tsv))
            # tsvファイルからツイート生成
            generator = GenerateText(logger)
            logger.debug(generator.generate_from_tsv(self.triplet_freqs_tsv))
        else:
            # 3gramsを作る準備
            chain = PrepareChain(text, logger)
            # 三つ組のテキストと出現回数を保存
            triplet_freqs = chain.make_triplet_freqs()
            # tsvファイルに保存
            chain.save_tsv(triplet_freqs=triplet_freqs,
                           file_triplet_freqs=self.triplet_freqs_tsv, init=True)
            # tsvファイルからツイート生成
            generator = GenerateText(logger)
            logger.debug(generator.generate_from_tsv(self.triplet_freqs_tsv))


if __name__ == '__main__':
    logger.debug('start main thread')
    try:
        account = "MuggyTeaa"
        logger.info('account name: {}'.format(account))
        tweets_generater = TweetsGenerater(account)
        tweets_generater.get_tweet()
        tweets_generater.generate_tweets()
    except:
        logger.error(traceback.format_exc())
