#로지스틱 회귀는 분류에 사용된다.
#추세를 예측하는 선형회귀와 달리 S자 함수를 사용하여 참, 거짓을 분류한다.

#로지스틱회귀에서 많이 사용하는 S함수가 시그모이드 함수
#이진분류에 사용

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer

#1) 데이터 수집
b_cancer = load_breast_cancer()

#2) 데이터 탐색
print(b_cancer.DESCR)
b_cancer_df = pd.DataFrame(b_cancer.data, \
                        columns=b_cancer.feature_names)
b_cancer_df['diagnosis'] = b_cancer.target

#print(b_cancer_df.head())
print("유방암 진단 데이터셋 크기: ", b_cancer_df.shape)
print(b_cancer_df.info())

#데이터 정규화 (평균 0, 분산1 - 정규분포형태)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
b_cancer_scaled = scaler.fit_transform(b_cancer.data)
#print(b_cancer.data[0])
#print(b_cancer_scaled[0])

#3) 분석 모델 구축 : 로지스틱 회귀를 이용한 이진 분류 모델
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

#X,Y 설정하기 : x-환자데이터들, y-유방인지 아닌지 값
Y = b_cancer_df['diagnosis']
X = b_cancer_scaled

#훈련용 및 테스트 데이터 분할
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.3, \
                                        random_state=0)
#모델 생성
lr_b_cancer = LogisticRegression()
lr_b_cancer.fit(X_train, Y_train)

#4) 모델 평가 및 결과 분석
Y_predict = lr_b_cancer.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score, \
                            precision_score, recall_score, \
                            f1_score, roc_auc_score
#오차행렬 출력  
print(confusion_matrix(Y_test, Y_predict))

#정확도 - (예측결과와 실제값이 동일한 건수) / 전체 데이터 수
accuracy = accuracy_score(Y_test, Y_predict)

#정밀도 - 예측이 참인것 중에서, 실제 결과값이 참인 것의 비율
precision = precision_score(Y_test, Y_predict)

#재현율 = 실제값이 참인것 중에서 예측값이 참인것의 비율 
# 실제 Positive 데이터를 정확히 예측했는지 평가지표, (민감도)
recall = recall_score(Y_test, Y_predict)

#f1 score - 정밀도와 재현율을 결합한 평가지표 
f1 = f1_score(Y_test, Y_predict)

#roc auc -FPR(실제는 거짓인데 참이라 예측한 경우)이 변할 때
#TPR(실제는 참인데 참이라 예측한 경우)이 어떻게 변하는지 나타내는 곡선
# roc 곡선에서 면적을 구한 값이 roc-auc => 1에 가까울수록 성능이 좋다.
roc_auc = roc_auc_score(Y_test, Y_predict)

print("""정확도:{0:.3f}, 정밀도:{1:.3f}, 재현율:{2:.3f}, \
F1:{3:.3f}, ROC_AUC:{4:.3f}""".format(accuracy, \
    precision, recall,f1, roc_auc))


