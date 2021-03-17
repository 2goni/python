import numpy as np
import pandas as pd

# 1) 데이터 수집
data_df = pd.read_csv("./머신러닝/auto-mpg.csv", header=0, \
            engine="python")

# 2) 데이터 탐색
#print("데이터 셋 크기 :", data_df.shape)
#print(data_df.head())

#분석하지 않을 변수 제외하기
data_df = data_df.drop(['car_name', 'origin', 'horsepower'], axis=1, \
                        inplace=False)
#print(data_df.head())
#print(data_df.info())

# 3) 분석 모델 구축
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

#X, Y 분할하기 - Y는 연비, X는 배기량, 연식....
Y = data_df['mpg']
X = data_df.drop(['mpg'], axis=1, inplace=False)

#훈련용 데이터와 평가용 데이터 분할
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,\
                                test_size=0.3, random_state=0)

#선형회귀모델 생성
lr = LinearRegression()
lr.fit(X_train, Y_train)

#모델 평가
Y_predict = lr.predict(X_test)

#4) 모델 평가 및 결과 분석 시각화
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

#회귀 분석 결과 산점도 + 선형회귀 그래프로 시각화
import matplotlib.pyplot as plt
import seaborn as sns

fig, axs = plt.subplots(figsize=(16,16), ncols=3, nrows=2)
x_features = list(X_train.columns)
plot_color = ['r', 'b', 'y', 'g', 'r']

for i, feature in enumerate(x_features) :
    row = int(i/3)
    col = i%3
    sns.regplot(x=feature, y="mpg", data=data_df, ax=axs[row][col], \
        color=plot_color[i])
plt.show()

# 새로운 데이터를 통한 연비 예측하기
cylinders_1 = int(input("cylinders : "))
displacement_1 = int(input("displacement : "))
weight_1 = int(input("weight : "))
acceration_1 = int(input("acceration : "))
model_year_1 = int(input("model_year : "))

mpg_predict = lr.predict([[cylinders_1, displacement_1, \
                        weight_1, acceration_1, model_year_1]])

print("이 자동차의 예상 연비(mpg)는 %.2f입니다." %mpg_predict)

