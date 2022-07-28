import MeCab
import re
import functools
import pandas as pd
import codecs
import kuzukiri

from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation

from transformers import pipeline 
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import BertJapaneseTokenizer


class SentimentAnalysis:
    def __init__(self):
        """
        コンストラクタ
        """
        pass

    def read_file(self,filename,encoding='utf-8'):
        '''
        ファイルの読み込み
 
        Parameters:
        --------
            filename : str   TF-IDFしたい文書が書かれたファイル名 
        '''
        with codecs.open(filename,'r',encoding,'ignore') as f:
            self.read_text(f.read())
 
    def read_text(self,text):
        '''
        テキストの読み込み
 
        Parameters:
        --------
            text : str   TF-IDFしたい文書
        '''
        # 形態素解析を用いて名詞のリストを作成
        self.document = text

    def split_text(self,text):
        """
        文章を文に分割する
        """
        split_punc2 = functools.partial(split_punctuation, punctuations=r"。.!?")
        concat_tail_te = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(て)$", remove_former_matched=False)
        segmenter = make_pipeline(normalize, split_newline, concat_tail_te, split_punc2)
        return list(segmenter(text))

    def split_text_2(self,text):
        """
        文章を文に分割する
        """
        segmenter = kuzukiri.Segmenter()
        sentences = segmenter.split(text)
        return list(sentences)
        

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
        # 極性辞書をデータフレームで読み込み
        df_dic = pd.read_csv('pn_ja.dic', sep=':', names=("Word", "読み", "品詞", "Score"), encoding='shift-jis')
        keys = df_dic["Word"].tolist()
        values = df_dic["Score"].tolist()
        dic = dict(zip(keys, values))

        # 形態素解析
        sa = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        nouns = [line for line in sa.parse(text).splitlines() if "名詞" in line.split()[-1]]
        # cha = sa.parse(text)
        # # 感情分析
        # # 形態素解析結果を行ごとに分割
        # cha_list = cha.split('\n')
        # # 形態素解析結果を名詞のみ抽出
        # cha_list_nouns = [re.sub(r'\t.*', '', cha_list[i]) for i in range(len(cha_list)) if re.sub(r'\t.*', '', cha_list[i]) != '']
        # # 形態素解析結果を名詞のみ抽出
        # # cha_list_noun_score = [dic[cha_list_noun[i]] for i in range(len(cha_list_noun))]
        # # 感情分析結果を合計
        # # score = sum(cha_list_noun_score)
        # #return score
        return nouns #途中で放棄した　未完成

    def sentiment_analysis_2(self,text):
        model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
        tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking') 
        nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        return nlp(text)
        
        
        

def main():
    sa = SentimentAnalysis()
    result_list = []
    while True:
        text = input(">> ")
        if text == "exit":
            break
        sentences = sa.split_text_2(text)
        for sentence in sentences:
            result = sa.sentiment_analysis_2(sentence)
            # result_list.append([sentence,result[0]['label'],result[0]['score']])
            if result[0]['label'] == 'ポジティブ':
                if result[0]['score'] > 0.85:
                    # result_list.append([sentence,result[0]['label'],result[0]['score']])
                    print(sentence +" :この文は嫌味を言われている可能性があります。")
        # print(result_list)

def analysis_sentences(text):
    sa = SentimentAnalysis()
    sentences = sa.split_text_2(text)
    message_list = []
    for sentence in sentences:
        result = sa.sentiment_analysis_2(sentence)
        if result[0]['label'] == 'ポジティブ':
            if result[0]['score'] > 0.85:
                message = sentence +" <-- この文は嫌味を言われている可能性があります。"
                message_list.append(message)
    return message_list

def analysis_text(text):
    sa = SentimentAnalysis()
    result = sa.sentiment_analysis_2(text)
    if result[0]['label'] == 'ポジティブ':
        if result[0]['score'] > 0.85:
            message = text +" <-- この文は嫌味を言われている可能性があります。"
            return message
    return None
    
if __name__ == '__main__':
    main()


        