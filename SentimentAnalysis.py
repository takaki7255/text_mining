import MeCab
import re
import functools

from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation


class SentimentAnalysis:
    def __init__(self):
        """
        コンストラクタ
        """
        pass

    def split_text(self,text):
        """
        文章を文に分割する
        """
        split_punc2 = functools.partial(split_punctuation, punctuations=r"。!?")
        concat_tail_te = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(て)$", remove_former_matched=False)
        segmenter = make_pipeline(normalize, split_newline, concat_tail_te, split_punc2)
        return list(segmenter(text))

    def MorphologicalAnalysis(self,text):
        """
        形態素解析
        """
        sa = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        cha = sa.parse(text)
        return cha

    def sentiment_analysis(self,text):
        """
        感情分析
        """
        # return self.nlp(self.document if text is None else text)
        pass
        

def main():
    sa = SentimentAnalysis()
    text = input('文を入力してください: ')
    print(sa.split_text(text))
    sentences = sa.split_text(text)
    for sentence in sentences:
        print(sa.MorphologicalAnalysis(sentence))
    
if __name__ == '__main__':
    main()


        