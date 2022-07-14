import MeCab
wakati = MeCab.Tagger('-Owakati')
#辞書を指定,neologdを使う
neowakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

word = input("文：")

wakati = wakati.parse(word).strip()
neowakati = neowakati.parse(word).strip()
print(wakati)
print(neowakati)