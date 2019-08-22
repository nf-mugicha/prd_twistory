"""
最新から過去3200ツイートまでを保管する関数
twitter-pythonライブラリを用いる。
取得したツイートはTwitter.Status型のリストをpklファイルに保存する
"""
from settings.certification import api
import settings.twitter_api as twitter_api
import pickle


def get_3200_user_timeline(account, user_timeline_3200_raw):
        # 3200ツイートを入れる空のリストを用意
    all_tweets = []
    # 直近200ツイートを取得
    latest_tweets = api.GetUserTimeline(
        screen_name=account,
        count=200
    )
    # 直近200ツイートを格納
    all_tweets.extend(latest_tweets)
    # 取得するツイートがなくなるまで続ける
    while len(latest_tweets) > 0:
        # while True:
        # while True:
        latest_tweets = api.GetUserTimeline(
            screen_name=account,
            count=200,
            max_id=all_tweets[-1].id-1
        )
        all_tweets.extend(latest_tweets)
        print(str(all_tweets[-1].id-1))
    # 取得した3200ツイート生データをファイル書き出ししておく
    with open(user_timeline_3200_raw,
              "wb") as f:
        pickle.dump(all_tweets, f)
        # for tweet in all_tweets:
        #     # json形式のstr型ファイルとして格納
        #     # json.dump(dict, tweet, indent=2)
        #     f.wtite(str(tweet) + "\n")
    return all_tweets
