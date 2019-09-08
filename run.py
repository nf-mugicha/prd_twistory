#!/usr/bin/env python
# -*- coding: utf-8 -*
from backend.app.models import vue_app
from backend.app.functions.get_3200_user_timeline import get_3200_user_timeline
from backend.app.functions.get_all_user_timeline import get_all_user_timeline
from backend.app.functions.save_tsv_3200_tweets import save_tsv_3200_tweets
from backend.app.functions.save_tsv_all_tweets import save_tsv_all_tweets
from backend.app.functions.preprocess import clean_tweet_text

from backend.app.functions.PrepareChain import PrepareChain
from backend.app.functions.GenerateText import GenerateText
from backend.app.models import TweetsGenerater

from backend.app.settings.certification import api
import backend.app.settings.twitter_api as twitter_api

from flask import render_template, request, make_response
from backend.app.settings.logging import logging_setting

from flask import Flask
import os  # for nonce
import pickle
import csv
import traceback
import time

app = vue_app()
logger = logging_setting('TweetGeneratorLogging')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=["GET", "POST"])
def tweet_generate():
    start = time.time()
    logger.info('start generate tweet')
    try:
        account_info = request.json
        logger.info('POST data: {}'.format(account_info))
        # account = "Pxilicon"
        account = account_info['account']
        logger.info('account name: {}'.format(account))
        tweets_generater = TweetsGenerater(account, logger)
        # 最新の3200ツイートを取得
        latest_id, account, filename_3200 = tweets_generater.get_tweet()
        # 今保存されているものより新しいツイートを取得し、tsvファイルに上書きする
        tweets_generater.get_latest_tweets(
            latest_id, account, filename_3200)
        # ツイート生成
        result_text = tweets_generater.generate_tweets()
        elapsed_time = time.time() - start
        logger.info('finish time: {} [sec.]'.format(elapsed_time))
        return result_text
    except:
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    app.run()
