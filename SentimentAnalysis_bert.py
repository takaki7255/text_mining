from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer
import codecs
 
class SentimentAnalysis:
    def __init__(self):
        """
        コンストラクタ
        """
        model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
        tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
        self.nlp = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)
        self.document = None
 
    def analyze(self,text = None):
        '''
        感情分析
        '''
        return self.nlp(self.document if text is None else text)
 
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

def main():
    sa = SentimentAnalysis()
    while True:
        text = input('文を入力してください: ')
        if text == 'exit':
            break
        print(sa.analyze(text))

if __name__ == '__main__':
    main()