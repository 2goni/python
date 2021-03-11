import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

with open('관세청_수입_일반수입(외화획득용)_201701_202001.json', 'r', encoding='utf8') as f :
    jsonData = json.load(f)

indexList = [i+1 for i,data in enumerate(jsonData)] #날짜 정보 그래프 X축
dateList = [data['yyyymm'] for data in jsonData] #날짜 정보 그래프 X축
wonList = [int(data['won']) for data in jsonData] 
cntList = [int(data['cnt']) for data in jsonData]

font_location = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family = font_name)
matplotlib.rcParams['axes.unicode_minus'] = False #-값 깨질때 쓴다.

plt.suptitle("관세청_수입_일반수입(외화획득용)")

plt.subplot(211)
plt.plot(indexList, wonList, 'r', label="won")
plt.xticks(indexList, dateList,rotation = 85)
plt.grid(True)
plt.legend()

plt.subplot(212)
plt.plot(indexList, cntList, 'b', label="건수")
plt.xticks(indexList, dateList,rotation = 85)
plt.legend()
plt.grid(True)

plt.show()