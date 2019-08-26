"""
ツイートテキストの前処理を行う関数
改行・スペース・URLを除く
リプライ・ハッシュタグも覗く
"""

import pandas as pd
import re
import unicodedata

reply_pattern_bf = '@[\w]+'
url_pattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
hash_tag_pattern = '#[\w]+'


def clean_tweet_text(tweets_text, logger):
    logger.debug(tweets_text)
    # リプライの場合は@アカウントのみを取り除く
    tweets_text_clean = re.sub(
        reply_pattern_bf, '', tweets_text)
    # URLを取り除く
    tweets_text_clean = re.sub(url_pattern, '', tweets_text_clean)
    # ハッシュタグを取り除く
    tweets_text_clean = re.sub(hash_tag_pattern, '', tweets_text_clean)
    # スペース・タブ・改行を取り除く
    tweets_text_clean = ''.join(tweets_text_clean.split())
    # 半角カタカナ、全角英数、ローマ数字・丸数字、異体字を正規化
    tweets_text_clean = unicodedata.normalize("NFKC", tweets_text_clean)

    logger.debug(tweets_text_clean)
    # 正規化した文字列を返す
    return tweets_text_clean
