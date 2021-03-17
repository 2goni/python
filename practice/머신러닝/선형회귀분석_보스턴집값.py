#회귀분석 입력 데이터를 기반으로 결과를 예측

#머신러닝 기본 프로세스
#데이터수집 -> 데이터전치리 및 탐색 -> 
#훈련데이터/테스트데이터 분할 -> 모델 구축 및 학습 -> 모델평가 ->
#모델 예측

#머신러닝 - 지도학습, 비지도학습
#지도학습 - 선형회귀분석(예측), 로지스틱회귀분석(분류), 결정트리모델(다중분류)
#비지도학습- k-means 군집 (비슷한데이터들끼리 군집화 시켜준다)
#텍스트마이닝 - 감성분석, 토픽분류

#pip install sklearn
#사이킷 라이브러리 제공 데이터 
#보스턴집값, 붓꽃(아리리스), 당뇨병 환자데이터
#숫자 0~9까지 필기체 흑백데이터, 와인 화학 성분데이터

#1) 데이터 수집
import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
boston = load_boston()

#2) 데이터 준비 및 탐색
#print(boston.DESCR)

boston_df = pd.DataFrame(boston.data, columns=boston.feature_names)
boston_df["PRICE"] = boston.target
#print(boston_df.head())
#print('보스턴 주택 가격 데이터셋 크기 : ', boston_df.shape)
#print(boston_df.info())

#3) 분석 모델 구축 - 선형회귀분석
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

#X, Y분할하기 X독립변수(원인)-CRIM, NOX.., Y는 종속변수(결과)-가격
Y = boston_df["PRICE"]
X = boston_df.drop(["PRICE"], axis=1, inplace=False)

#훈련용 데이터와 평가용 데이터 분할
X_train, X_test, Y_train, Y_test = train_test_split(X, \
    Y, test_size=0.3, random_state=156)

#선형회귀분석 : 모델생성
lr = LinearRegression()

#모델훈련
lr.fit(X_train, Y_train)

#평가데이터에 대한 예측 수행 -> 예측 결과 Y_predict 구하기
Y_predict = lr.predict(X_test)

#4) 모델 성능평가 및 결과분석 시각화
mse = mean_squared_error(Y_test, Y_predict)
rmse = np.sqrt(mse)

print("MSE : {0:.3f}, RSME : {1:.3f}".format(mse,rmse))
print("R^2(Variance score) : {0:.3f}".format(\
    r2_score(Y_test, Y_predict)))

print("Y 절편 값 :", lr.intercept_)
print("회귀 계수 값 :", np.round(lr.coef_, 1))

coef  = pd.Series(data=np.round(lr.coef_, 2), \
    index=X.columns)
coef.sort_values(ascending=False)

#회귀 분석 결과 산점도, 선형 회귀 그래프로 시각화
import matplotlib.pyplot as plt
import seaborn as sns

fig, axs = plt.subplots(figsize=(16,16), ncols=3,\
                        nrows=5)
x_features =  list(X_train.columns)
for i, feature in enumerate(x_features) :
    row = int(i/3)
    col = i%3
    sns.regplot(x=feature, y="PRICE", data=boston_df, ax=axs[row][col])
plt.subplots_adjust(hspace=0.4)
plt.show()












