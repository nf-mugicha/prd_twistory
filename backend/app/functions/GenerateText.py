# -*- coding: utf-8 -*-

"""
マルコフ連鎖を用いて適当な文章を自動生成するファイル
"""

import os.path
import sqlite3
import random
import csv
from .PrepareChain import PrepareChain


class GenerateText(object):
    """
    文章生成用クラス
    """

    def __init__(self, logger):
        """
        初期化メソッド
        @param n いくつの文章を生成するか
        @param logger ログオブジェクト
        """
        # self.n = n
        self.logger = logger

    def generate_from_tsv(self, triplet_freqs_tsv):
        """
        実際に生成する
        @return 生成された文章
        """
        # DBが存在しないときは例外をあげる
        if not os.path.exists(triplet_freqs_tsv):
            self.logger.error(
                "tsv file does not exist: {]".format(triplet_freqs_tsv))
            raise IOError("tsvファイルが存在しません")

        text_3grams_list = []
        # tsvファイルオープン
        with open(triplet_freqs_tsv, newline='') as f:
            reader = csv.DictReader(f, delimiter='\t')
            self.logger.info("open file: {}".format(triplet_freqs_tsv))
            for row in reader:
                text_3grams_list.append(row)

        # 最終的にできる文章
        generated_text = ""

        # 指定の数だけ作成する
        while True:
            text = self._generate_sentence(text_3grams_list)
            # 生成したテキストが30文字以上だったらやり直し
            if len(text) < 10 or len(text) > 45:
                self.logger.info("not output for 10 < text < 45")
                self.logger.info("text length: {}".format(len(text)))
                self.logger.info(text)
                continue
            else:
                generated_text += text
                self.logger.info("text length:{}".format(len(generated_text)))
                self.logger.info(generated_text)
                break

        return generated_text

    def _get_chain_from_tsv(self, text_3grams_list, prefixes):
        """
        チェーンの情報をtsvファイルから取得する
        @param text_3grams_list 3gramsの辞書型配列が格納されたリスト
        @param prefixes チェーンを取得するprefixの条件 tupleかlist
        @return チェーンの情報の配列
        """

        # 結果
        result = []
        self.logger.debug("prefixes: {}".format(prefixes))
        # prefixが含まれるもののみを配列に格納する
        for row in text_3grams_list:
            # prefixが２の場合はどちらも一致するものを配列に格納する
            if len(prefixes) == 2:
                if (prefixes[0] in row['prefix1']) and (prefixes[1] in row['prefix2']):
                    self.logger.debug("make sentence: {}".format(row))
                    self.logger.debug(
                        "prefix[0] in row['prefix1'] and (prefixes[1] in row['prefix2']) is {}".format(
                            (prefixes[0] in row['prefix1']) and (
                                prefixes[1] in row['prefix2'])
                        )
                    )
                    result.append(row)
            elif prefixes[0] in row['prefix1']:
                self.logger.debug(
                    "it may be BEGIN SENTENCE: {}".format(row))
                result.append(row)
            else:
                self.logger.debug(
                    "it may not use to make sentence: {}".format(row))
                continue

        return result

    def _generate_sentence(self, text_3grams_list):
        """
        ランダムに一文を生成する
        @param con DBコネクション
        @return 生成された1つの文章
        """
        # 生成文章のリスト
        morphemes = []

        # はじまりを取得
        first_triplet = self._get_first_triplet(text_3grams_list)
        self.logger.debug("first triplet {}".format(first_triplet))
        morphemes.append(first_triplet['prefix2'])
        morphemes.append(first_triplet['suffix'])

        # 文章を紡いでいく
        while morphemes[-1] != PrepareChain.END:
            prefix1 = morphemes[-2]
            prefix2 = morphemes[-1]
            triplet = self._get_triplet(text_3grams_list, prefix1, prefix2)
            morphemes.append(triplet['suffix'])
        self.logger.debug(morphemes)
        # 連結
        result = "".join(morphemes[:-1])

        return result

    def _get_first_triplet(self, text_3grams_list):
        """
        文章のはじまりの3つ組をランダムに取得する
        @param text_3grams_list 文章の三つ組と確立が格納されたdictのリスト
        @return 文章のはじまりの3つ組のdict
        """
        # BEGINをprefix1としてチェーンを取得
        prefixes = (PrepareChain.BEGIN,)

        # チェーン情報を取得
        chains = self._get_chain_from_tsv(text_3grams_list, prefixes)

        # 取得したチェーンから、確率的に1つ選ぶ
        first_triplet = self._get_probable_triplet(chains)

        return first_triplet

    def _get_triplet(self, text_3grams_list, prefix1, prefix2):
        """
        prefix1とprefix2からsuffixをランダムに取得する
        @param text_3grams_list 文章を3gramsに分けた辞書型配列のリスト
        @param prefix1 1つ目のprefix
        @param prefix2 2つ目のprefix
        @return 3つ組のタプル
        """
        # BEGINをprefix1としてチェーンを取得
        prefixes = (prefix1, prefix2)

        # チェーン情報を取得
        chains = self._get_chain_from_tsv(text_3grams_list, prefixes)

        # 取得したチェーンから、確率的に1つ選ぶ
        triplet = self._get_probable_triplet(chains)

        return triplet

    def _get_probable_triplet(self, chains):
        """
        チェーンの配列の中から確率的に1つを返す
        @param chains チェーンの配列
        @return 確率的に選んだ3つ組
        """
        # 確率配列
        probability = []

        # 確率に合うように、インデックスを入れる
        for (index, chain) in enumerate(chains):
            for j in range(int(chain["freq"])):
                probability.append(index)

        # ランダムに1つを選ぶ
        chain_index = random.choice(probability)

        return chains[chain_index]


if __name__ == '__main__':
    generator = GenerateText()
    # print(generator.generate())
    print(generator.generate_from_tsv())
