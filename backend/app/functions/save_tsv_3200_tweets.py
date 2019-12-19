"""
取得した3200件分のツイートをtsvファイルに保管する関数
取得するものは以下
・ツイートid
・ツイートテキスト
・ふぁぼ数
・RT数
・画像付きツイートか否か
・ツイート日時
・画像URL
"""
import csv
from .preprocess import clean_tweet_text
from .connect_firestorage import upload_bucket_file


def save_tsv_3200_tweets(all_tweets, filename_3200, logger):
    with open(filename_3200, 'w', newline='') as f:
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
        tweet_excerpt = {}
        tweet_id = []
        for tweet in all_tweets:
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
            tweet_id.append(int(tweet.id))
            # 辞書を初期化
            tweet_excerpt = {}
    # fireストレージにアップロード
    upload_bucket_file(filename_3200, logger)
    max_id = min(tweet_id)
    latest_id = max(tweet_id)
    # 3200ツイート分のリストと、最後のmax_idを返す
    return all_tweets, max_id, latest_id
