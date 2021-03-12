#와인의 속성을 이용해서 품질 등급 예측
#데이터분석 방법 : 기술통계, 회귀분석, t-검정
#시각화 : 히스토그램

from os import sep
import pandas as pd

red_df = pd.read_csv('winequality-red.csv', sep=';', \
    header=0, engine="python")

white_df = pd.read_csv('winequality-white.csv', sep=';', \
    header=0, engine="python")

#와인의 타입 열 추가
red_df.insert(0,column="type", value='red')
white_df.insert(0,column="type", value='white')

#와인 정보 합치기
wine = pd.concat([red_df, white_df])
print(wine.info())

wine.columns = wine.columns.str.replace(' ', '_')

#기술통계
print(sorted(wine.quality.unique())) #와인등급 중복없이 값을 나열
print(wine.quality.value_counts())
'''
wineQulity = wine.quality.value_counts().index
wineNum = wine.quality.value_counts().values
avg = sum(wineQulity*wineNum)/sum(wineNum)
print(avg)

print(wine['quality'].mean())
print(wine['quality'].std())
print(wine['quality'].agg(['mean', 'std']))
print(wine['quality'].describe())
'''

print(wine.groupby('type')['quality'].describe())

#T검정 및 선형회귀 모델 만들기
red_wine_quality  = wine.loc[wine['type']=='red', 'quality']
white_wine_quality  = wine.loc[wine['type']=='white', 'quality']

red_wine_quality = (red_wine_quality - red_wine_quality.mean())/red_wine_quality.std()
white_wine_quality  = (white_wine_quality - white_wine_quality.mean())/white_wine_quality.std()
#t검정으로 두 그룹 간의 차이를 확인한다.
from scipy import stats
from  statsmodels.formula.api import ols, glm
tResult = stats.ttest_ind(red_wine_quality, white_wine_quality, \
                            equal_var=False)
print(tResult)

#선형 회귀 분석식의 종속 변수와 독립변수를 구성한다.
#종속 변수 Quality, 독립변수 type, quality 제외 나머지 11개 속성
Rformula = "quality ~ fixed_acidity + volatile_acidity + " \
    "citric_acid + residual_sugar + chlorides + free_sulfur_dioxide + " \
    "total_sulfur_dioxide + density + pH + sulphates + alcohol"

#선형회귀 모델 ols
regression_result = ols(Rformula, data=wine).fit()
print(regression_result.summary())

#품질 등급 예측

#예측용 샘플 데이터 만들기
sample1 = wine[wine.columns.difference(['quality', 'type'])]
sample1 = sample1[0:5][:]

#품질 예측
sample1_predict = regression_result.predict(sample1)
print(sample1_predict)
print(wine[0:5]['quality'])

#새로운 데이터를 통한 품질 등급 예측
data = {"fixed_acidity" : [8.5, 8.1], "volatile_acidity" : [0.8, 0.5], "citric_acid" : [0.3, 0.4], "residual_sugar" : [6.1, 5.8], "chlorides": [0.055, 0.04], "free_sulfur_dioxide" : [30.0, 31.0], "total_sulfur_dioxide" : [98.0, 99], "density" : [0.996, 0.91], "pH" :[3.25, 3.01], "sulphates" :[0.4, 0.35], "alcohol" :[9.0, 0.88]}
sample2 = pd.DataFrame(data, columns=sample1.columns)
sample2_predict = regression_result.predict(sample2)
print(sample2_predict)

# seaborn 설치
import matplotlib.pyplot as plt
import seaborn as sns

# 스타일 테마 설정
sns.set_style('dark')

# 히스토그램 그리기
sns.displot(red_wine_quality, kde= True, color='red', label='red wine')

sns.displot(white_wine_quality, kde= True, color='blue', label='white wine')

plt.title("Quality of Wine type")
plt.legend()
plt.show()

#fixed_acidity변수가 quality에 미치는 영향력 시각화
import statsmodels.api as sm

#독립변수와 fixed_acidity 변수 제외한 나머지 변수

others = list(set(wine.columns).difference(set(["quality","fixed_acidity"])))

presids= sm.graphics.plot_partregress("quality", "fixed_acidity", others, data=wine, ret_coords=True)
plt.show()

fig = plt.figure(figsize=(8,13))
sm.graphics.plot_partregress_grid(regression_result, fig=fig)
plt.show()