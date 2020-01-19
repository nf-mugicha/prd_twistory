#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask
from flask_cors import CORS
import os
import pickle
import csv
import traceback
import time
import shutil
import slackweb
import inspect

try:
    from .functions.get_3200_user_timeline import get_3200_user_timeline
    from .functions.get_all_user_timeline import get_all_user_timeline
    from .functions.save_tsv_3200_tweets import save_tsv_3200_tweets
    from .functions.save_tsv_all_tweets import save_tsv_all_tweets
    from .functions.preprocess import clean_tweet_text

    from .functions.PrepareChain import PrepareChain
    from .functions.GenerateText import GenerateText

    from .functions.connect_firestorage import upload_bucket_file, download_bucket_file

    from .settings.certification import api
    from .settings import twitter_api
    # from .settings.firebase import bucket
except:
    from functions.get_3200_user_timeline import get_3200_user_timeline
    from functions.get_all_user_timeline import get_all_user_timeline
    from functions.save_tsv_3200_tweets import save_tsv_3200_tweets
    from functions.save_tsv_all_tweets import save_tsv_all_tweets
    from functions.preprocess import clean_tweet_text

    from functions.PrepareChain import PrepareChain
    from functions.GenerateText import GenerateText

    from functions.connect_firestorage import upload_bucket_file, download_bucket_file

    from settings.certification import api
    from settings import twitter_api
    # from settings.firebase import bucket


def vue_app(app_name="VUE-FLASK"):
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')
    CORS(app, resources={'/*': {"origins": "*"}})
    return app


class TweetsGenerater(object):
    """
    ツイート生成クラス
    twitterAPIを使用して任意のアカウントのツイートを取得する。
    形態素解析した単語の三つ組を作り、tsvファイルに保存する
    マルコフ連鎖でツイート生成する。
    """

    def __init__(self, account, logger):
        """
        初期化メソッド
        @param account アカウント名
        """
        self.account = account
        self.logger = logger
        self.filepath = "get_tweets_assets/{0}".format(account)
        # ユーザーごとにフォルダを分ける
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
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

    def location(depth=0):
        frame = inspect.currentframe().f_back
        return os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno

    def get_latest_tweets(self, since_id, account, filename_3200):
        """
        最新から過去3200ツイートまでを保管する関数
        twitter-pythonライブラリを用いる。
        取得したツイートはTwitter.Status型のリストをpklファイルに保存する
        """
        self.logger.info(
            "start latests' 200 tweets scraping since_id: {}".format(since_id))
        # 3200ツイートを入れる空のリストを用意
        all_tweets = []
        # since_idを探すための箱
        search_id_list = []
        slack = slackweb.Slack(url=twitter_api.SLACK_ERROR)
        # location = location()
        # 直近200ツイートを取得
        try:
            latest_tweets = api.GetUserTimeline(
                screen_name=account,
                count=200,
                since_id=since_id
            )
        except Exception as e:
            self.logger.error(
                "{} could not get latest tweets".format(account))
            # ディレクトリを消す
            self.logger.error(e)
            # 最新ツイート取得できなかったら、空のリストを返す（既に3200ツイートは取得し終えているのでそれで賄う）
            latest_tweets = []
        # もし取得するツイートがなかったらそのまま返す
        if len(latest_tweets) == 0:
            self.logger.info("Nothing of latest tweets")
            return all_tweets, since_id
        # 取得ツイートが200以下だったらいっぺんに格納する
        if len(latest_tweets) < 200:
            all_tweets.extend(latest_tweets)
            # since_idから遡った200件の、最も新しいid（200件以上新作があった時に使う）
            latest_id = int(all_tweets[0].id)
            max_id = int(all_tweets[-1].id)-1
        # 200ツイート取得しているということは、最新ツイートが200ツイート以上ある可能性が高いので、更に取得する
        elif len(latest_tweets) >= 200:
            # とりあえず全件格納する
            all_tweets.extend(latest_tweets)
            self.logger.info("start 200 more tweets scraping")
            # since_idから遡った200件の、最も新しいid（200件以上新作があった時に使う）
            latest_id = int(latest_tweets[0].id)
            max_id = int(latest_tweets[-1].id)-1
            c = 1
            since_id_flag = True
            latest_id = int(all_tweets[0].id)
            max_id = int(all_tweets[-1].id)
            while since_id_flag:
                max_id = int(all_tweets[-1].id)
                # latest_id = int(all_tweets[-1].id)
                try:
                    scraping_start_time = time.time()
                    latest_tweets = api.GetUserTimeline(
                        screen_name=account,
                        count=200,
                        max_id=int(all_tweets[-1].id)-1
                    )
                    # 時間を計測
                    scraping_end_time = time.time() - scraping_start_time
                    # 1分以上時間が掛かっていたら処理を抜ける
                    if scraping_end_time > 60:
                        self.logger.error('timeout error')
                        self.logger.error(len(all_tweets))
                        since_id_flag = False
                        break
                except Exception as e:
                    self.logger.error('something wrong {}'.format(e))
                    self.logger.error(traceback.format_exc())
                    break
                    # since_idに到達したら終わり
                for l in latest_tweets:
                    # リストに追加する
                    all_tweets.append(l)
                if int(all_tweets[-1].id) == max_id:
                    since_id_flag = False
                    break
                c = c+1
                self.logger.info(
                    "count {0} all_tweets[-1].id: {1}".format(c, all_tweets[-1].id))
                self.logger.info("count {0} max_id: {1}".format(c, max_id))
            max_id = int(all_tweets[-1].id)-1
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
                # 保存するツイートが重複しないように
                if tweet.id < since_id:
                    break
                # RTは除外
                if tweet.text.startswith('RT'):
                    continue
                # ツイートテキストを前処理
                tweet_text = clean_tweet_text(tweet.text, self.logger)
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
            # logger.info("writing count: {0}".format(c))
            # fireストレージにアップロード
            upload_bucket_file(filename_3200, self.logger)
            latest_id = all_tweets[0].id-1
            self.logger.info("{0} new tweets, latest id: {1}".format(
                len(all_tweets), all_tweets[0].id))
        return all_tweets, latest_id

    def get_tweet(self):
        # ストレージからダウンロード
        download_bucket_file(self.user_timeline_3200_raw, self.logger)
        download_bucket_file(self.filename_3200, self.logger)
        slack = slackweb.Slack(url=twitter_api.SLACK_TWEET)
        # 既に3200件のデータを取り終えていたらやらない
        if not os.path.exists(self.user_timeline_3200_raw):
            slack.notify(text="new user", username=self.account)
            # 3200件のツイートデータ取得・保存

            all_tweets, latest_id, max_id = get_3200_user_timeline(
                self.account,
                self.user_timeline_3200_raw,
                self.logger,
                self.filepath
            )
            # API制限でツイート取得できてない
            if len(all_tweets) == 0:
                return
        # tsvファイルもあればそれを開く
        if os.path.exists(self.filename_3200):
            self.logger.info('already done all tweets scraping')
            self.logger.info("open file of 3200 tweets data: {}".format(
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
                self.logger.info('max_id: {}'.format(max_id))
                self.logger.info('latest_id: {}'.format(latest_id))

        else:
            # 保存したpklファイルを開く
            with open(self.user_timeline_3200_raw, 'rb') as f:
                all_tweets = pickle.load(f)
                # 3200ツイート取得・tsvファイルに保存
                all_tweets, max_id, latest_id = save_tsv_3200_tweets(
                    all_tweets, self.filename_3200, self.logger)
                self.logger.info(
                    'save 3200tweets: {}'.format(self.filename_3200))
                self.logger.info('max_id: {}'.format(max_id))
                self.logger.info('latest_id: {}'.format(latest_id))
        return latest_id, self.account, self.filename_3200
        # 今保存されているものより新しいツイートを取得し、tsvファイルに上書きする
        # all_tweets, latest_id = self.get_latest_tweets(
        #     latest_id, self.account, self.filename_3200)
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
            self.logger.debug("open: {}".format(self.filename_3200))
            # with open(self.filename_all, newline='') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                tweet_text_list.append(row['tweet_text'])
        self.logger.info(
            "{} tweets in this list now".format(len(tweet_text_list)))
        # 。で繋げて１つのテキストにする
        text = "。".join(tweet_text_list[:-1])
        self.logger.debug("joined tweets text:\n{}\n".format(text))
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
        self.logger.info('start make 3grams')
        # 3gramsを作る準備
        chain = PrepareChain(text, self.logger)
        # 三つ組のテキストと出現回数を保存
        triplet_freqs = chain.make_triplet_freqs()
        # tsvファイルに保存
        chain.save_tsv(triplet_freqs=triplet_freqs,
                       file_triplet_freqs=self.triplet_freqs_tsv, init=True)
        self.logger.info('finished make 3grams')
        # tsvファイルからツイート生成
        self.logger.info('start generate tweets')
        generator = GenerateText(self.logger)
        result_text = generator.generate_from_tsv(self.triplet_freqs_tsv)
        self.logger.info('finish generate tweets')

        return result_text


if __name__ == '__main__':
    from settings.logging import logging_setting
    logger = logging_setting('TweetGeneratorModelTextLogging')
    start = time.time()
    logger.info('start generate tweet')
    try:
        account = "Ann_NH"
        logger.info('account name: {}'.format(account))
        tweets_generater = TweetsGenerater(account, logger)
        # 最新の3200ツイートを取得
        latest_id, account, filename_3200 = tweets_generater.get_tweet()
        # 今保存されているものより新しいツイートを取得し、tsvファイルに上書きする
        tweets_generater.get_latest_tweets(
            latest_id, account, filename_3200)
        # ツイート生成
        tweets_generater.generate_tweets()
        elapsed_time = time.time() - start
        logger.info('finish time: {} [sec.]'.format(elapsed_time))
    except:
        logger.error(traceback.format_exc())
