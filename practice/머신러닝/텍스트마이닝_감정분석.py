#텍스트 마이닝
#텍스트 데이터에 의미있는 인사이트를 도출하기 위해
#머신러닝 고급기술을 적용하여 방전한 기술

#텍스트 단어별로 가중치를 매겨서, 백터화를 시키고 특성 백터로 머신러닝 학습을 한다.
#Word2Vec 또는 Bow

#텍스트 마이닝 분야
#감정분석 - 텍스트에서 사용자의 긍정 또는 부정의 감정을 결정 
#토픽모델링 - 문서를 구성하는 키워드 기반으로 토픽 추출

import os

from scipy.sparse.construct import random
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
print("dd")

#감성 분류 모델 구축 : 로지스틱 회귀를 이용한 이진 분류
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(random_state=0)
lr.fit(nsmc_train_tfidf, nsmc_train_df["label"])

# 로지스틱 회귀의 best 하이퍼 파라미터
from sklearn.model_selection import GridSearchCV
params = {"C": [1,3,3.5,4,4.5,5]}
lr_grid_cv = GridSearchCV(lr, param_grid=params, cv=3, scoring= "accuracy", verbose=1)

#최적 분석 모델 훈련
lr_grid_cv.fit(nsmc_train_tfidf, nsmc_train_df["label"])
print(lr_grid_cv.best_params_, round(lr_grid_cv.best_score_,4))

#최적 파라미터 저장
lr_best = lr_grid_cv.best_estimator_

#4) 분석 모델 평가
nsmc_test_tfidf = tfidf.transform(nsmc_test_df["document"])
test_predict = lr_best.predict(nsmc_test_tfidf)

from sklearn.metrics import accuracy_score
print("감성 분석 정확도 : ", round(accuracy_score(nsmc_test_df["label"], test_predict), 3))

#새로운 텍스트에대한 감성 예측

tempStr = input("감성 분석할 문장 입력 >>")
tempStr = re.compile(r'[ㄱ-ㅎ|가-힣|ㅏ-ㅣ]+').findall(tempStr)
print(tempStr)
tempStr = [" ".join(tempStr)]
print(tempStr)

#1) 입력 데이터의 피처 백터화
st_tfidf = tfidf.transform(tempStr)

#2) 최적 감정분석 모델에 적용하여 감성분석 평가
st_predict = lr_best.predict(st_tfidf)

#3) 예측값 출력하기
if st_predict == 0 :
    print(tempStr, "->>부정 감성")
else :
    print(tempStr, "->>긍정 감성")