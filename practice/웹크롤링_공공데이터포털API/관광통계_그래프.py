import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

with open('서울특별시_관광지입장정보_201601_201901.json', 'r', encoding='utf8') as f :
    jsonData = json.load(f)

indexList = [i+1 for i,data in enumerate(jsonData)] #날짜 정보 그래프 X축
dateList = [data['yyyymm'] for data in jsonData] #날짜 정보 그래프 X축
forNumList = [int(data['forNum']) for data in jsonData] #외국인 수 Y1 값
natNumList = [int(data['natNum']) for data in jsonData] #내국인 수 Y2 값
font_location = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family = font_name)
plt.plot(indexList, forNumList, 'r--', label="외국인")
plt.plot(indexList, natNumList, 'b', label="내국인")
plt.xlabel("방문월")
plt.ylabel("방문객수")
plt.title("경복궁 관광객 방문객수")
plt.legend()
plt.grid(True)
plt.xticks(indexList, dateList,rotation = 85)
plt.show()