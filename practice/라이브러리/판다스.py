#판다는 DB처럼 테이블 형식의 데이터를 다룰때 쉽게 처리해준다.

import pandas as pd
import numpy as np

s1 = pd.Series([1,2,3,4,6,9,10,np.nan])
print(s1)

s2 = pd.Series([1,3,5,np.nan,6,8], index=np.arange(3,9))
print(s2)

dates = pd.date_range('20210301', periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6,4), index=dates, \
    columns=list("ABCD"))

print(df)


#시리즈
data1 = [10,20,30,40,50]
data2 = ["1반","2반","3반","4반","5반"]

sr1 = pd.Series(data1)
sr2 = pd.Series(data2)
sr3 = pd.Series(data1, index=data2)

print(sr1[2])
print(sr2[3])
print(sr3['1반'])

print(sr3.index)
print(sr3.values)
print(sr3.items())

data1 = [10,20,30,40,50]
data2 = [100,100,100,100,100]

sr1 = pd.Series(data1)
sr2 = pd.Series(data2)

print(sr1+sr2)
print(sr1*sr2)
print(sr1/sr2)
print(sr1*3)

df = pd.DataFrame(np.random.randn(6,4), index=dates, \
    columns=list("ABCD"))

print(df.head(1))
print(df.tail(1))
print(df.index)
print(df.columns)
print(df.values)

print(df['A'])
print(df['C'])
print(df[0:3])
print(df['20210302':'20210305'])
print(df['A']['20210302'])
print(df.loc['20210301'])

df.to_csv("FrameText.csv", header=None, encoding="utf-8")
df2 = pd.read_csv("FrameText.csv", header=None, encoding="utf-8", \
    index_col=0, engine="python")

    






