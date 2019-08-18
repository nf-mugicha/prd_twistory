from . import twitter_api
import pandas as pd
import tweepy
import csv
import seaborn as sns
sns.set(style="whitegrid")

# twitter認証情報
key = twitter_api.CONSUMER_KEY
key_secret = twitter_api.CONSUMER_SECRET_KEY
token = twitter_api.ACCESS_TOKEN
token_secret = twitter_api.ACCESS_TOKEN_SECRET

# 認証情報を設定
auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth)
