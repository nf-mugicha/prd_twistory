from . import twitter_api
import pandas as pd
import tweepy
import csv
import seaborn as sns
import twitter
sns.set(style="whitegrid")

# twitter認証情報
key = twitter_api.CONSUMER_KEY
key_secret = twitter_api.CONSUMER_SECRET_KEY
token = twitter_api.ACCESS_TOKEN
token_secret = twitter_api.ACCESS_TOKEN_SECRET

api_header = {
    key: key_secret,
    token: token_secret
}

# 認証情報を設定
# auth = tweepy.OAuthHandler(key, key_secret)
# auth.set_access_token(token, token_secret)
# api = tweepy.API(auth)

# 認証情報を設定
api = twitter.Api(
    consumer_key=key,
    consumer_secret=key_secret,
    access_token_key=token,
    access_token_secret=token_secret
)
