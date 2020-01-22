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
from backend.app.TweetPost import TweetPost

from backend.app.functions.connect_firestorage import upload_bucket_file

from flask import Flask
import os  # for nonce
import pickle
import csv
import traceback
import time
import shutil
from requests_oauthlib import OAuth1Session
import slackweb

app = vue_app()
logger, logging_file = logging_setting('TweetGeneratorLogging')
slack = slackweb.Slack(url=twitter_api.SLACK_ERROR)


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/tweet', methods=["POST"])
def tweet_post():
    logger.info('start tweet posting')
    try:
        account_info = request.json
        logger.info('tweet data: {}'.format(account_info))
        if type(account_info) == dict:
            account = account_info['account']
            generated_text = account_info['generated_text']
            access_token = account_info['accessToken']
            secret_token = account_info['secretToken']
            display_name = account_info['displayName']
            tweet_post = TweetPost(
                account, generated_text, logger, display_name
            )
            twitter_oath = tweet_post.create_oath_session(
                access_token, secret_token
            )
            response_message = tweet_post.tweet_posting(twitter_oath)
            logger.info('Tweet message: {}'.format(response_message))
            # fireストレージにアップロード
            # upload_bucket_file(logging_file, logger)
            return response_message
    except Exception as e:
        slack.notify(text=str(traceback.format_exc()), username=account)
        logger.error(traceback.format_exc())
        # fireストレージにアップロード
        # upload_bucket_file(logging_file, logger)
        response_data = {
            "res_text": "ツイート失敗しました。twitter投稿画面を開きます", "status": 401}
        return response_data


@app.route('/generate', methods=["POST"])
def tweet_generate():
    start = time.time()
    logger.info('start generate tweet')
    try:
        logger.info(request)
        account_info = request.json
        logger.info('POST data: {}'.format(account_info))
    except Exception as e:
        logger.error(traceback.format_exc())
        result_text = "リクエスト取得に失敗しました。もう一度やってみてください。\nまた、鍵アカウントはツイート生成できません。"
        logger.error(result_text)
        slack.notify(text=str(result_text) +
                     str(traceback.format_exc()), username=account)
        elapsed_time = time.time() - start
        logger.error('error finish time: {} [sec.]'.format(elapsed_time))
        return result_text
    try:
        if type(account_info) == dict:
            account = account_info['account']
        else:
            account = ""
            result_text = "アカウント取得に失敗しました。お手数ですが、ログインし直してもう一度お試しお願いします。また、鍵アカウントはツイート生成できません。"
            return result_text
        logger.info('account name: {}'.format(account))
        filepath = "get_tweets_assets/{0}".format(account)
        tweets_generater = TweetsGenerater(account, logger)
        # 最新の3200ツイートを取得
        latest_id, account, filename_3200 = tweets_generater.get_tweet()
        if latest_id is None:
            result_text = "twitterAPI制限により現在ツイート取得ができません。約15分後に再度アクセスして下さい\nまた、鍵アカウントはツイート生成できません"
            slack.notify(text=result_text, username=account)
            return result_text
        # 今保存されているものより新しいツイートを取得し、tsvファイルに上書きする
        tweets_generater.get_latest_tweets(
            latest_id, account, filename_3200)
        # ツイート生成
        result_text = tweets_generater.generate_tweets()
        elapsed_time = time.time() - start
        # ローカルファイルを消す
        logger.info('finish time: {} [sec.]'.format(elapsed_time))
        # fireストレージにアップロード
        # upload_bucket_file(logging_file, logger)
        # ローカルのファイルを削除
        if os.path.exists(filepath):
            logger.info("delete local file: {}".format(filepath))
            shutil.rmtree(filepath)
        return result_text
    except Exception as e:
        logger.error(traceback.format_exc())
        result_text = "ツイート生成に失敗しました。もう一度やってみてください。\nまた、鍵アカウントはツイート生成できません。"
        logger.error(result_text)
        slack.notify(text=str(result_text) +
                     str(traceback.format_exc()), username=account)
        elapsed_time = time.time() - start
        logger.error('error finish time: {} [sec.]'.format(elapsed_time))
        # fireストレージにアップロード
        # upload_bucket_file(logging_file, logger)
        # ローカルのファイルを削除
        if os.path.exists(filepath):
            logger.error("delete local file: {}".format(filepath))
            shutil.rmtree(filepath)
        return result_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    logger.info('run.py is running')
