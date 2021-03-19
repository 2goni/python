import numpy as np
import pandas as pd

data_df = pd.read_csv("./머신러닝/auto-mpg.csv", header=0, \
            engine="python")

data_df = data_df.drop(['car_name', 'origin', 'horsepower'], axis=1, \
                        inplace=False)

from  statsmodels.formula.api import ols, glm
Rformula = "mpg ~ cylinders + displacement + weight + acceleration + model_year"

regression_result = ols(Rformula, data=data_df).fit()
print(regression_result.summary())

#회귀 분석 결과 산점도 + 선형회귀 그래프로 시각화
import matplotlib.pyplot as plt
import statsmodels.api as sm

fig = plt.figure(figsize=(16,16))
sm.graphics.plot_partregress_grid(regression_result, fig=fig)
plt.show()

# 새로운 데이터를 통한 연비 예측하기
data = {"cylinders" : [8], "displacement" : [310], "weight" : [3000], "acceleration" : [11], "model_year": [85]}
sample_predict = regression_result.predict(data)
print("이 자동차의 예상 연비(mpg)는 %.2f입니다." %sample_predict)

