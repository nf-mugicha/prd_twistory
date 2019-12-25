import json
from requests_oauthlib import OAuth1Session

from .settings import twitter_api


class TweetPost(object):
    """
    生成されたツイートをツイッターに投稿するクラス
    ツイートデータを画面から受け取り、ツイートする。
    """

    def __init__(self, account, generated_text, logger):
        """
        params
            account: str アカウント名
            generated_text: json 生成されたテキスト
            logger: ロガー
        """
        self.account = account
        self.generated_text = generated_text
        self.logger = logger

    def create_oath_session(self, access_token, secret_token):
        twitter_oath = OAuth1Session(
            twitter_api.CONSUMER_KEY,
            twitter_api.CONSUMER_SECRET_KEY,
            access_token,
            secret_token
        )

        return twitter_oath

    def tweet_posting(self, twitter_oath):
        """
        ツイート投稿する
        """
        url = "https://api.twitter.com/1.1/statuses/update.json"
        generated_text = self.generated_text
        params = {'status': generated_text +
                  str(' #ついじぇね\n「自分っぽい」ツイートを作ってみよう https://aitter_twigene.me')}
        req = twitter_oath.post(url, params)

        if req.status_code == 200:
            self.logger.info('tweet success')
            self.logger.info("{ 'account': {0}, 'generated_tweet: {1}' }".format(
                self.account, self.generated_text))
        else:
            self.logger.error('tweet faild')
            self.logger.error(req.text)


if __name__ == '__main__':
    from settings.logging import logging_setting
    logger = logging_setting('TweetPostTest')
    account = 'テスト'
    generated_text = '投稿'
    tweet_post = TweetPost(account, generated_text, logger)
    twitter_oath = tweet_post.create_oath_session()
    tweet_post.tweet_posting(twitter_oath)
