#텍스트 마이닝
#텍스트 데이터에 의미있는 인사이트를 도출하기 위해
#머신러닝 고급기술을 적용하여 방전한 기술

#텍스트 단어별로 가중치를 매겨서, 백터화를 시키고 특성 백터로 머신러닝 학습을 한다.
#Word2Vec 또는 Bow

#텍스트 마이닝 분야
#감정분석 - 텍스트에서 사용자의 긍정 또는 부정의 감정을 결정 
#토픽모델링 - 문서를 구성하는 키워드 기반으로 토픽 추출

import os
os.environ["PYTHONENCODING"] = "utf-8"
import warnings
warnings.filterwarnings(action= 'ignore')

#(1)데이터수집
#깃허브에서 데이터 파일 다운로드 : https://github.com/e9t/nsmc

import pandas as pd
nsmc_train_df = pd.read_csv("./머신러닝/ratings_train.txt", encoding="utf-8", sep='\t', engine='python')
print(nsmc_train_df.head())
print(nsmc_train_df.info())

nsmc_train_df = nsmc_train_df[nsmc_train_df["document"].notnull()]
print(nsmc_train_df['label'].value_counts())

#한글 이외의 문자는 공백으로 변환
import re
nsmc_train_df["document"].apply(lambda x: re.sub(r'[^ㄱ-ㅎ|가-힣]+', " ", x))
print(nsmc_train_df.head())

#평가용 데이터 준비
nsmc_test_df = pd.read_csv("./머신러닝/ratings_train.txt", encoding="utf-8", sep='\t', engine='python')
nsmc_test_df = nsmc_test_df[nsmc_test_df["document"].notnull()]
nsmc_test_df["document"].apply(lambda x: re.sub(r'[^ㄱ-ㅎ|가-힣|ㅏ-ㅣ]+', " ", x))

print(nsmc_test_df.head())

from konlpy.tag import Okt
okt = Okt()

def okt_tokenizer(text) :
    tokens = okt.morphs(text) #형태소 기반으로 분리를 해준다
    return tokens

# TF-IDF 기반 피처 백터 생성
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(tokenizer = okt_tokenizer, ngram_range=(1,2), min_df=3, max_df= 0.9)
tfidf.fit(nsmc_train_df['document'])
nsmc_train_tfidf = tfidf.transform(nsmc_train_df["document"])