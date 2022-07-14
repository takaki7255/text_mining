# mecab導入（辞書使用含めて）覚書<br>
* mecabインストール<br>
* 辞書をgithubなどからクローンする<br>
    * 参考:https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md<br>
* ?mecab -Dで色々確認できる<br>
* クローンしたものを-dで指定する<br>
    * neo_wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')<br>