"""
最新から過去3200ツイートまでを保管する関数
twitter-pythonライブラリを用いる。
取得したツイートはTwitter.Status型のリストをpklファイルに保存する
"""
# from settings.certification import api
# import settings.twitter_api as twitter_api
import pickle
import os


def get_3200_user_timeline(account, user_timeline_3200_raw, logger, filepath):
    logger.info("start latests' 3200 tweets scraping")
    # 3200ツイートを入れる空のリストを用意
    all_tweets = []
    # 直近200ツイートを取得
    try:
        latest_tweets = api.GetUserTimeline(
            screen_name=account,
            count=200
        )
    except:
        logger.error(
            "{} may be private account or does not exists, can not get user timeline".format(account))
        # ディレクトリを消す
        logger.error('delete directry: {}'.format(filepath))
        os.rmdir(filepath)
        raise
    # 最新のツイートid取得
    latest_id = latest_tweets[0].id
    logger.info("now's latest id: {}".format(str(latest_tweets[0].id)))
    # 直近200ツイートを格納
    all_tweets.extend(latest_tweets)
    # 取得するツイートがなくなるまで続ける
    logger.info("start 3200 tweets scraping")
    c = 1
    while len(latest_tweets) > 0:
        logger.info("count {0} max_id: {1}".format(c, all_tweets[-1].id-1))
        latest_tweets = api.GetUserTimeline(
            screen_name=account,
            count=200,
            max_id=all_tweets[-1].id-1
        )
        all_tweets.extend(latest_tweets)
        c = c+1
    max_id = all_tweets[-1].id-1
    # 取得した3200ツイート生データをファイル書き出ししておく
    with open(user_timeline_3200_raw,
              "wb") as f:
        pickle.dump(all_tweets, f)
        logger.info("save raw data of 3200 tweets: {}".format(
            user_timeline_3200_raw))
    return all_tweets, latest_id, max_id
