#numpy 벡터 및 행렬 계산할때 쓰는 라이브러리
#numpy 라이브러리는 고성능 수치계산할때
#numpy 딥러닝 행렬 처리할때 많이 쓰인다.

import numpy as np

a = np.arange(15).reshape(3,5) #3X5 행렬
print(a)
print(a.shape)  # 배열 각 축의 크기
print(a.ndim)   # 축의 개수
print(a.size)   # 전체요소의 개수 

b = np.array([0.5,1.5,2.5])
print(b)

c = np.array([[0,1,2],[3,4,5]])
print(c)

print(np.empty((2,3))) #빈값 쓰레기값
print(np.zeros((2,3))) #0으로 채움
print(np.ones((2,3,4))) #1로 채움
print(np.arange(10,30,5)) #범위값으로 벡터만듬
print(np.linspace(10,30,3)) #요소 3개 등간격  

a = np.array([[0,1,4,9], [16,25,36,49]])
print(a.sum()) #모든 요소의 합
print(a.min()) #요소 중 최솟값
print(a.max()) #요소 중 최댓값
print(a.argmax()) #인덱스 중 최댓값

print(a.sum(axis=0)) #행 별로 더한값
print(a.sum(axis=1)) #열 별로 더한 값

print(a.ravel()) #행렬을 1차원 배열 만들어 준다.
print(a.T) #전치행렬 행과 열을 바꾼 행렬로 만들어준다.

print(np.arange(4) + 2)

a = np.arange(3).reshape((3,1)) * np.arange(3)
print(a)


