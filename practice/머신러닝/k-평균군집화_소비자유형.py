#군집분석 : 타켓마케팅을 위한 K-평균 군집화

#영국 온라인 소매 플랫폼 2010.12.01~ 2021.12.09까지 발생한 실제
#거래데이터 541,909개

#군집화는 대표적인 비지도학습을 데이터 안에 숨겨진 패턴을 찾아,
#타깃값을 만들어야 한다. 

#군집 분석 대표적인 알고리즘 - k-평균, 계층적 군집
#k-평균 알고리즘 - k개의 클러스터를 구성하기 위한것

#적절한 K값을 찾는 방법
#1) 엘보방법 : 클러스터의 중심점과 클러스터내의 데이터 거리 차이의 제곱합
#을 왜곡이라고 한다. 왜곡을 활용하여 최적의 K를 찾는다.
#클러스터의 개수 k의 변화에 따른 왜괵의 변화를 그래프로 그려보면
#그래프가 꺽이는 지점인 엘보가 나타나는데, 그 지점의 K를 최적의 K로 선택함.

#2)실루엣 분석 : 클러스터 내에 있는 데이터가 얼마나 조밀하게 모여있는지
#측정하는 그래프도구로서 클러스터와 데이터가 얼마나 가까운가를 나타내는
#응집력 a(i)와 데이터가 다른 클러스터 내의 데이터와 얼마나 떨어져있는가를
#나타내는 클러스터 분리도 b(i)를 이용한 실루엣 계수 s(i)를 계산한다.
#실루엣 계수는 -1~1사이의 값을 가지며 1에 가까울수록 좋은 군집화 의미

import pandas as pd
import math

#1) 데이터 수집
retail_df = pd.read_csv("./머신러닝/OnlineRetail.csv", header=0, \
            engine="python")
#print(retail_df.head())
#print(retail_df.info())

#오류 데이터 정제
#print(retail_df.isnull().sum())
retail_df = retail_df[retail_df['CustomerID'].notnull()]
retail_df = retail_df[retail_df['Quantity'] > 0]
retail_df = retail_df[retail_df['UnitPrice'] > 0]
retail_df['CustomerID'] = retail_df["CustomerID"].astype(int)

# print(retail_df.isnull().sum())
# print(retail_df.shape)
# print(retail_df.info())

#중복 레코드 제거
retail_df.drop_duplicates(inplace=True)
#제품수, 거래건수, 고객수 탐색
print(pd.DataFrame([{'Product':len(retail_df["StockCode"].value_counts()), \
                    'Transaction':len(retail_df["InvoiceNo"].value_counts()), \
                    'Customer':len(retail_df["CustomerID"].value_counts())}], \
                     columns=["Product", "Transaction", "Customer" ], \
                     index=['counts']))
print(retail_df['Country'].value_counts())

#주문금액 컬럼 추가
retail_df["SaleAmount"] = retail_df["UnitPrice"] * retail_df["Quantity"]
print(retail_df.head())

#고객의 마지막 주문후 경과일, 주문횟수, 주문총액 구하기
aggressions = { \
    'InvoiceNo' : 'count', \
    'SaleAmount' : 'sum', \
    'InvoiceDate' : 'max' \
}
customer_df = retail_df.groupby("CustomerID").agg(aggressions)
customer_df = customer_df.reset_index()
#print(customer_df.head())
import datetime
customer_df["InvoiceDate"]  = pd.to_datetime(customer_df["InvoiceDate"])
customer_df["InvoiceDate"] = datetime.datetime(2011,12,10) - \
                            customer_df['InvoiceDate']
customer_df["InvoiceDate"] = customer_df["InvoiceDate"].apply(\
                            lambda x: x.days+1)
#print(customer_df.head())
customer_df =  customer_df.rename(columns={"InvoiceNo":"Freq", \
                                "InvoiceDate" : "ElapsedDays"})
#print(customer_df.head())

#현재 데이터의 분포 확인
import matplotlib.pyplot as plt
import seaborn as sns
'''
fig, ax = plt.subplots()
ax.boxplot([customer_df["Freq"], customer_df["SaleAmount"], \
    customer_df["ElapsedDays"]], sym="bo")
plt.xticks([1,2,3], ['Freq', 'SaleAmount', 'ElapsedDays'])
plt.show()
'''
#데이터 값의 왜곡을 줄이기 위한 로그 함수로 분포 조정
import numpy as np
customer_df['Freq_log'] = np.log1p(customer_df["Freq"])
customer_df['SaleAmount_log'] = np.log1p(customer_df["SaleAmount"])
customer_df['ElapsedDays_log'] = np.log1p(customer_df["ElapsedDays"])
print(customer_df.head())

#조정된 데이터 분포를 다시 박스플롯으로 확인
'''
fig, ax = plt.subplots()
ax.boxplot([customer_df["Freq_log"], customer_df["SaleAmount_log"], \
    customer_df["ElapsedDays_log"]], sym="bo")
plt.xticks([1,2,3], ['Freq_log', 'SaleAmount_log', 'ElapsedDays_log'])
plt.show()
'''
#3) 모델 구축 : K-평균 군집화 모델
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

#데이터 정규 분포로 스케일링
from sklearn.preprocessing import StandardScaler
X_features = customer_df[['Freq_log', 'SaleAmount_log', 'ElapsedDays_log']]
X_features_scaled = StandardScaler().fit_transform(X_features)

#최적의 K값 찾기
#(1) 엘보우 방법 - 클러스터 개수 1~10까지 반복하면서 왜곡 값을 리스트에 저장
distortions = []
for i in range(1, 11) :
    kmeans_i  = KMeans(n_clusters=i, random_state=0)  #모델 생성
    kmeans_i.fit(X_features_scaled) #모델 훈련
    distortions.append(kmeans_i.inertia_)

plt.plot(range(1,11), distortions, marker='o')
plt.xlabel("Number of clusters")
plt.ylabel("Distortion")
plt.show()


#엘보방법을 통한 최적의 K값 - 3~5
kmeans = KMeans(n_clusters=3, random_state=0)
Y_labels = kmeans.fit_predict(X_features_scaled)
customer_df["ClusterLabel"] =  Y_labels
print(customer_df.head())


#실루엣 계수에 따른 각 클러스터의 비중 시각화 함수 정의
from matplotlib import cm

def silhouetteViz(n_cluster, X_features): 
    
    kmeans = KMeans(n_clusters=n_cluster, random_state=0)
    Y_labels = kmeans.fit_predict(X_features)
    
    silhouette_values = silhouette_samples(X_features, Y_labels, metric='euclidean')

    y_ax_lower, y_ax_upper = 0, 0
    y_ticks = []

    for c in range(n_cluster):
        c_silhouettes = silhouette_values[Y_labels == c]
        c_silhouettes.sort()
        y_ax_upper += len(c_silhouettes)
        color = cm.jet(float(c) / n_cluster)
        plt.barh(range(y_ax_lower, y_ax_upper), c_silhouettes,
                 height=1.0, edgecolor='none', color=color)
        y_ticks.append((y_ax_lower + y_ax_upper) / 2.)
        y_ax_lower += len(c_silhouettes)
    
    silhouette_avg = np.mean(silhouette_values)
    plt.axvline(silhouette_avg, color='red', linestyle='--')
    plt.title('Number of Cluster : '+ str(n_cluster)+'\n' \
              + 'Silhouette Score : '+ str(round(silhouette_avg,3)))
    plt.yticks(y_ticks, range(n_cluster))   
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.ylabel('Cluster')
    plt.xlabel('Silhouette coefficient')
    plt.tight_layout()
    plt.show()

#클러스터 수에 따른 클러스터 데이터 분포의 시각화 함수 정의
def clusterScatter(n_cluster, X_features): 
    c_colors = []
    kmeans = KMeans(n_clusters=n_cluster, random_state=0)
    Y_labels = kmeans.fit_predict(X_features)

    for i in range(n_cluster):
        c_color = cm.jet(float(i) / n_cluster) #클러스터의 색상 설정
        c_colors.append(c_color)
        #클러스터의 데이터 분포를 동그라미로 시각화
        plt.scatter(X_features[Y_labels == i,0], X_features[Y_labels == i,1],
                     marker='o', color=c_color, edgecolor='black', s=50, 
                     label='cluster '+ str(i))       
    
    #각 클러스터의 중심점을 삼각형으로 표시
    for i in range(n_cluster):
        plt.scatter(kmeans.cluster_centers_[i,0], kmeans.cluster_centers_[i,1], 
                    marker='^', color=c_colors[i], edgecolor='w', s=200)
        
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

#클러스터 3인 경우의 실루엣 score 및 클러스터 비중 시각화
#silhouetteViz(2, X_features_scaled) #0.4
#silhouetteViz(3, X_features_scaled) #0.303
#silhouetteViz(4, X_features_scaled) #0.309
#silhouetteViz(5, X_features_scaled) #0.278
#silhouetteViz(6, X_features_scaled) #0.274

#결정된 K를 적용하여 최적의 K-means 모델 완성
best_cluster = 4

kmeans = KMeans(n_clusters=best_cluster, random_state=0)
Y_labels = kmeans.fit_predict(X_features_scaled)
customer_df["ClusterLabel"] = Y_labels
print(customer_df.head())
customer_df.to_csv("./머신러닝/OnlineRetail_Cluster.csv")
clusterScatter(4, X_features_scaled)

#클러스터 분석하기

#1) 각 클러스터별 고객수
print(customer_df.groupby("ClusterLabel")["CustomerID"].count())

#2) 주문 1회당 평균 구매금액
customer_df["SaleAmountAvg"] = customer_df["SaleAmount"]/ \
                                customer_df["Freq"]

customer_cluster_df = customer_df.drop(['Freq_log', \
                    'SaleAmount_log', 'ElapsedDays_log'], \
                    axis=1, inplace=False)
#print(customer_cluster_df.head())

print(customer_cluster_df.drop(['CustomerID'], axis=1, \
    inplace=False).groupby("ClusterLabel").mean())

