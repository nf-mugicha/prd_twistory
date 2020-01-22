"""
最新から過去3200ツイートまでを保管する関数
twitter-pythonライブラリを用いる。
取得したツイートはTwitter.Status型のリストをpklファイルに保存する
"""
try:
    from ..settings.certification import api
    from .connect_firestorage import upload_bucket_file
except:
    from ..settings.certification import api
    from .connect_firestorage import upload_bucket_file
import pickle
import os
import shutil
import time
from timeout_decorator import timeout, TimeoutError


@timeout(300, use_signals=False)
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
    except (ConnectionResetError) as e:
        logger.error('ConnectionResetError, do retry')
        logger.error(e)
        latest_tweets = api.GetUserTimeline(
            screen_name=account,
            count=200
        )
    except Exception as e:
        logger.error(
            "{} may be private account or does not exists, can not get user timeline".format(account))
        # ディレクトリを消す
        # logger.error('delete directry: {}'.format(filepath))
        # shutil.rmtree(filepath)
        for i in range(3 + 1):
            logger.error('retry {}'.format(i))
            sleep_sec = 3
            logger.error('sleep {} sec'.format(sleep_sec))
            time.sleep(sleep_sec)
            latest_tweets = api.GetUserTimeline(
                screen_name=account,
                count=200
            )
            if latest_tweets[0].id:
                logger.info(latest_tweets[0])
                break
    # 最新のツイートid取得
    latest_id = latest_tweets[0].id
    logger.info("now's latest id: {}".format(str(latest_tweets[0].id)))
    # 直近200ツイートを格納
    all_tweets.extend(latest_tweets)
    # 取得するツイートがなくなるまで続ける
    logger.info("start 3200 tweets scraping: {}".format(len(latest_tweets)))
    c = 1
    scraping_start_time = time.time()
    # 200ツイート以上を取得
    while len(latest_tweets) > 0:
        logger.info("count {0} max_id: {1}".format(c, all_tweets[-1].id-1))
        latest_tweets = api.GetUserTimeline(
            screen_name=account,
            count=200,
            max_id=all_tweets[-1].id-1
        )
        all_tweets.extend(latest_tweets)
        c = c+1
        # 時間を計測
        scraping_end_time = time.time() - scraping_start_time
        # 1分以上時間が掛かっていたら処理を抜ける
        if scraping_end_time > 60:
            logger.error('timeout error')
            logger.error(len(all_tweets))
            break
    max_id = all_tweets[-1].id-1
    # 取得した3200ツイート生データをファイル書き出ししておく
    with open(user_timeline_3200_raw,
              "wb") as f:
        pickle.dump(all_tweets, f)
        # fireストレージにアップロード
        upload_bucket_file(user_timeline_3200_raw, logger)
        logger.info("save raw data of 3200 tweets: {}".format(
            user_timeline_3200_raw))
    return all_tweets, latest_id, max_id
