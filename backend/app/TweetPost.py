import json
from requests_oauthlib import OAuth1Session
import slackweb
import traceback
from datetime import datetime

from .settings import twitter_api
from .settings.firebase import db


class TweetPost(object):
    """
    生成されたツイートをツイッターに投稿するクラス
    ツイートデータを画面から受け取り、ツイートする。
    """

    def __init__(self, account, generated_text, logger, display_name):
        """
        params
            account: str アカウント名
            generated_text: json 生成されたテキスト
            logger: ロガー
        """
        self.account = account
        self.generated_text = generated_text
        self.logger = logger
        self.display_name = display_name

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
        # params = {'status': generated_text +
        #           str('\n #ついじぇね\n') + str(self.display_name) + " ボットがツイートしました" + str('\n https://aitter-twigene.me')}
        # params = {'status': generated_text +
        #           str('\n\n #ついじぇね #') + str(self.display_name) + "ボットのツイート" + "\n自分っぽいツイートを自動生成してみよう！" + str('\n https://aitter-twigene.me')}
        params = {'status': generated_text +
                  str('\n\n #ついじぇね #自分bot') + str('\n https://aitter-twigene.me')}
        req = twitter_oath.post(url, params)
        self.logger.info(req)
        doc_ref = db.collection('UsersTweets')
        doc_ref.add({
            'account': self.account,
            'generated_text': generated_text,
            'created_at': datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
        })

        slack = slackweb.Slack(url=twitter_api.SLACK_TWEET)
        if req.status_code == 200:
            self.logger.info('tweet success')
            try:
                slack.notify(text=generated_text, username=self.account)
                response_data = {"res_text": "ツイートしました！",
                                 "status": 200}
                return response_data
            except Exception:
                self.logger.error("could not connect to slack")
                self.logger.error(traceback.format_exc())
                response_data = {"res_text": "ツイートしました！",
                                 "status": 200}
                return response_data
        elif req.status_code == 403:
            self.logger.error(req.text)
            slack.notify(text=str(req.text) + str(generated_text), username=self.account)
            response_data = {
                "res_text": "ツイートが重複しているかtwitter投稿API上限に達しました。\n twitter投稿画面を開きます", "status": 403}
            return response_data
        else:
            self.logger.error('tweet faild')
            slack.notify(text=str(req.text) + str(generated_text), username=self.account)
            self.logger.error(req.text)
            response_data = {
                "res_text": "ツイート失敗しました。twitter投稿画面を開きます", "status": 401}
            return response_data


if __name__ == '__main__':
    from settings.logging import logging_setting
    logger = logging_setting('TweetPostTest')
    account = 'テスト'
    generated_text = '投稿'
    tweet_post = TweetPost(account, generated_text, logger)
    twitter_oath = tweet_post.create_oath_session()
    tweet_post.tweet_posting(twitter_oath)
