import os
import time

try:
    from ..settings.firebase import bucket
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    from settings.firebase import bucket


def upload_bucket_file(filename, logger):
    logger.info('File {0} uploaded to {1}'.format(filename, filename))
    try:
        blob = bucket.blob(filename)
        blob.upload_from_filename(filename)
    except:
        for i in range(3 + 1):
            logger.error('storage upload retry {}'.format(i))
            sleep_sec = 3
            logger.error('sleep {} sec'.format(sleep_sec))
            time.sleep(sleep_sec)
            blob = bucket.blob(filename)
            blob.upload_from_filename(filename)
            if blob:
                logger.info("uploaded success")
                break


def download_bucket_file(filename, logger):
    blob = bucket.blob(filename)
    try:
        logger.info(
            'Blob {0} downloaded to {1}'.format(filename, filename))
        blob.download_to_filename(filename)
    except:  # firebaseにファイルが存在しない場合（初めてのユーザー）
        logger.info('{} does not exist'.format(filename))
        if os.path.exists(filename):
            # ローカルのディレクトリを削除する
            os.remove(filename)
        return


if __name__ == '__main__':
    from settings.logging import logging_setting
    logger = logging_setting('TweetGeneratorModelTextLogging')
    filename = "get_tweets_assets/aquirax_k/tweets_3200_raw_aquirax_k.pkl"
    upload_bucket_file(filename, logger)

