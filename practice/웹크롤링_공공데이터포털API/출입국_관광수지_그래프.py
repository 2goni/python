import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

with open('관광수지_201701_202001.json', 'r', encoding='utf8') as f :
    jsonData = json.load(f)

indexList = [i+1 for i,data in enumerate(jsonData)] #날짜 정보 그래프 X축
dateList = [data['yyyymm'] for data in jsonData] #날짜 정보 그래프 X축
tourbList = [int(data['tb']) for data in jsonData] #관광 수지
tourExpenseList = [int(data['te']) for data in jsonData] #관광 지출
tourIncomeList = [int(data['tr']) for data in jsonData] #관광 수입
font_location = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family = font_name)
matplotlib.rcParams['axes.unicode_minus'] = False #-값 깨질때 쓴다.
plt.plot(indexList, tourbList, 'y--', label="관광수지")
plt.plot(indexList, tourExpenseList, 'r', label="관광지출")
plt.plot(indexList, tourIncomeList, 'b', label="관광수입")
plt.xlabel("방문월")
plt.ylabel("원")
plt.title("관광 지출 및 수입")
plt.legend()
plt.grid(True)
plt.xticks(indexList, dateList,rotation = 85)
plt.show()