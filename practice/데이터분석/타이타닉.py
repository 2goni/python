#타이타닉호 승객 변수를 분석항 생존율과 상관관계를 찾는다.

#상관분석을 통해 어떤 변수가 생존율에 연관이 있는지 알아낸다.

#성별별 생존률 파이차트 그리기
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from seaborn.palettes import color_palette

titanic = sns.load_dataset("titanic")

#데이터 결측치 확인
#print(titanic.isnull().sum())

#age 결측치 중앙값으로 치환하기
titanic['age'] = titanic['age'].fillna(titanic['age'].median())

#embarked 결측치 최빈치로 치환하기
#print(titanic['embarked'].value_counts())
titanic['embarked'] = titanic['embarked'].fillna("S")

#embarked_town 결측치 최빈치로 치환하기
#print(titanic['embark_town'].value_counts())
titanic['embark_town'] = titanic['embark_town'].fillna("Southampton")

#deck 결측치 최빈치로 치환하기
#print(titanic['deck'].value_counts())
titanic['deck'] = titanic['deck'].fillna("C")

#print(titanic.isnull().sum())
titanic.to_csv("titinic.csv", index=False)

print(titanic.info())
print(titanic.survived.value_counts())

'''
#캔버스 및 프레임생성
f, ax = plt.subplots(1,2, figsize=(10,5))

#남자 생존자 파이차트
titanic['survived'][titanic['sex']=='male'].value_counts().\
    plot.pie(explode=[0, 0.1], autopct='%1.1f%%', \
        ax=ax[0], shadow = True)

#여자 생존자 파이차트
titanic['survived'][titanic['sex']=='female'].value_counts().\
    plot.pie(explode=[0, 0.1], autopct='%1.1f%%', \
        ax=ax[1], shadow = True)

ax[0].set_title('Survived (Male)')
ax[1].set_title('Survived (Female)')
plt.show()
'''

#등급별 생존자수 막대차트로 시각화
# sns.countplot(x='pclass', hue='survived', data=titanic)
# plt.title('Pclass Vs Survived')
# plt.show()

#데이터분석 : 상관분석 모델링

titanic_corr = titanic.corr(method='pearson')
print(titanic_corr)

# #산점도로 상관분석 시각화
# sns.pairplot(titanic, hue='survived')
# plt.show()

#두 변수간의 상관관계 시각화
sns.catplot(x='pclass', y='survived', hue='sex', \
    data = titanic, kind='point')
plt.show()

#상관계수 히트맵으로 시각화
def category_age(x) :
    if x < 10 :
        return 0
    elif x < 20 :
        return 1
    elif x < 30 :
        return 2
    elif x < 40 :
        return 3
    elif x < 50 :
        return 4
    elif x < 60 :
        return 5
    elif x < 70 :
        return 6
    else :
        return 7

titanic['age2'] = titanic['age'].apply(category_age)
titanic['sex'] = titanic['sex'].map({'male':1, 'female':0})
titanic['family'] = titanic['sibsp'] + titanic['parch'] + 1

heatmap_data = titanic[['survived', 'sex', 'age2', 'family', \
                        'pclass', 'fare']]

#히트맵에 사용할 색상맵 지정
color_map = plt.cm.RdBu

sns.heatmap(heatmap_data.astype(float).corr(), \
    linewidths=0.1, vmax=1.0, square=True, cmap=color_map, \
        linecolor='white', annot=True, annot_kws={'size':10})
plt.show()

