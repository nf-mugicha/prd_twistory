"""
全ツイートのpklファイルからtsvを生成する関数
"""
import csv
from .preprocess import clean_tweet_text


def save_tsv_all_tweets(all_tweets_pkl, filename_all, logger):
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
        for i, data in enumerate(all_tweets_pkl):
            # RTは除外
            if data["text"].startswith('RT'):
                continue
            # ツイートテキスト前処理
            tweet_text = clean_tweet_text(data["text"], logger)
            # 連想配列に格納
            tweet_excerpt["id"] = data["id"]
            tweet_excerpt["tweet_text"] = tweet_text
            tweet_excerpt["favorite_count"] = data["favorite_count"]
            tweet_excerpt["retweet_count"] = data["retweet_count"]
            tweet_excerpt["created_at"] = data["created_at"]
            tweet_excerpt["hasImage"] = False
            # 画像つきのツイートだったら画像URLを格納
            if "extended_entities" in data:
                if "media" in data["extended_entities"]:
                    tweet_excerpt["hasImage"] = True
                    for i, m in enumerate(data["extended_entities"]['media']):
                        tweet_excerpt["image_{}".format(
                            i)] = m["media_url_https"]
            # ファイル出力
            writecsv.writerow(tweet_excerpt)
            # 辞書を初期化
            tweet_excerpt = {}
