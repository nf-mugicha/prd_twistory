import MeCab

"""
MeCabを使ってテキストを形態素解析する関数
"""

mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def mecab_tagger(text):
    mecab.parse('')  # 文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    # 一単語分の辞書
    morpho_dic = {}
    while node:
        # 単語を取得
        word = node.surface
        # 品詞を取得
        pos = node.feature.split(",")
        print("{0}, {1}".format(word, pos))
        # 辞書に登録
        morpho_dic[word] = pos
        # 次の単語へ
        node = node.next
        # 単語と形態素解析の連想配列のリストが一文リストに入る
        morpho_list.append(morpho_dic)
        morpho_dic = {}
    print(morpho_list)


if __name__ == "__main__":
    texts = ["そういえばビームシールドが切れたから買いたいんだけど、水色のビームシールド買うにはFAGすちれっとセット買わないといけなくて、青い槍とかスナイパーライフルとかウィングバインダーとかいらないものがどんどん増える。",
             "雷怖い。おもにPCとかPS4死なないか怖い。", "少数精鋭で敵の中枢を破壊するが基本戦術になってるDestinyの世界はやばい。", "ビームシールドのセットが買いたいなあ"]
    # 形態素解析した一文を入れるリスト
    morpho_list = []
    for text in texts:
        mecab_tagger(text)
