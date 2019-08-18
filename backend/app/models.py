#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask
from settings.certification import api
import csv


def vue_app(app_name="VUE-FLASK"):
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')

    return app


def get_tweet():
    # 全ツイートを入れる空のリストを用意
    all_tweets = []
    # 直近の200ツイート分を取得しておく
    latest_tweets = api.user_timeline(count=200)
    all_tweets.extend(latest_tweets)

    # 取得するツイートがなくなるまで続ける
    while len(latest_tweets) > 0:
        latest_tweets = api.user_timeline(
            count=200, max_id=all_tweets[-1].id-1)
        all_tweets.extend(latest_tweets)

    with open('all_tweets.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ['tweet_text', '#characters', '#favorited',
                '#retweeted', 'hasImage', 'create_at']
        )
        print(writer)
        for tweet in all_tweets:
            # RTとリプライはスキップ
            if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
                continue
            else:
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
                writer.writerow(
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
            print(\n)


if __name__ == '__main__':
    get_tweet()
