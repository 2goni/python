import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

with open('한  국_국민해외관광객_201701_202012.json', 'r', encoding='utf8') as f :
    jsonData1 = json.load(f)
with open('중  국_방한외래관광객_201701_202012.json', 'r', encoding='utf8') as f :
    jsonData2 = json.load(f)

natName1 = jsonData1[0]["natName"]
natName2 = jsonData2[0]["natName"]
indexList = [i+1 for i,data in enumerate(jsonData1)] #날짜 정보 그래프 X축
dateList = [data['yyyymm'] for data in jsonData1] #날짜 정보 그래프 X축
NumList1 = [int(data['num']) for data in jsonData1] #한국인 출국자 수 
NumList2 = [int(data['num']) for data in jsonData2] #중국인 입국자 수

font_location = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family = font_name)
plt.plot(indexList, NumList1, 'r--', label=natName1)
plt.plot(indexList, NumList2, 'b', label=natName2)
plt.xlabel("방문월")
plt.ylabel("방문객수")
plt.title(natName1 + " 및 " + natName2 + " 관광객수")
plt.legend()
plt.grid(True)
plt.xticks(indexList, dateList,rotation = 85)
plt.show()