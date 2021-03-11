import datetime
import json
import urllib.request
import matplotlib.pyplot as plt

#인증키
ServiceKey = "UONoET2Grg2f0je6CsDmMP%2BsJ%2B1fT93YXiwOrW0vSx9x%2F" \
            "GmRf%2BJkVpL%2BTtntfYLXec8mro6YEsU5OI94WOfr7w%3D%3D" 
                								
def getRequestUrl(url):
    req = urllib.request.Request(url)						
    try:						
        response = urllib.request.urlopen(req)						
        if response.getcode() == 200:						
            print("[%s] Url Request Success" % datetime.datetime.now())						
            return response.read().decode('utf-8')						
    except Exception as e:						
        print(e)						
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))						
        return None	

def getTourVisitorInfo(yyyymm, sido, gungu, resnm) : 
#함수인자로 날짜, 시이름, 구이름, 관광명소이름 
    serviceUrl = "http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList"
    parameter = "?_type=json&serviceKey=" + ServiceKey
    parameter += "&YM=" + yyyymm
    parameter += "&SIDO=" + urllib.parse.quote(sido)
    parameter += "&GUNGU=" + urllib.parse.quote(gungu)
    parameter += "&RES_NM=" + urllib.parse.quote(resnm)

    url = serviceUrl + parameter
    retData = getRequestUrl(url)
    if retData == None :
        return None
    else :
        return json.loads(retData)

sido = "서울특별시"
gungu = "종로구"
resname = "경복궁"
yyyymm = "201601"

#제공해주는 API는 한달치 정보만 가져오므로, 시작년도와 끝년도를 입력받아 모든 정보 가져오기
startYear = 2016
endYear = 2019

jsonResult = []
for year in range(startYear, endYear+1) :
    for month in range(1, 13) :
        yyyymm = "{0}{1:0>2}".format(str(year), str(month))
        jsonData = getTourVisitorInfo(yyyymm, sido, gungu, resname)
        
        if jsonData['response']['header']['resultMsg'] == 'OK' :
            item = jsonData['response']['body']['items']
            endDate = yyyymm
            if item == '' :
                break
            else :
                item = item['item']
                addrCd = item['addrCd']
                gungu = item['gungu']
                sido = item['sido']
                resNm = item['resNm']
                forNum = item['csForCnt']
                natNum = item['csNatCnt']
                yyyymm = item['ym']
                jsonResult.append({'yyyymm':yyyymm, 'addrCd':addrCd, 'sido':sido, \
                                'gungu':gungu, 'resNm':resNm , 'forNum':forNum, 'natNum':natNum})

with open('%s_관광지입장정보_%d01_%s.json' %(sido, startYear, endDate), 'w', encoding='utf8') as outfile :
    retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print('%s_관광지입장정보_%d01_%s.json Saved' %(sido, startYear, yyyymm))

#jsonResult는 List 이다. Value => Dic
dateList = [data['yyyymm'] for data in jsonResult] #날짜 정보 그래프 X축
forNumList = [data['forNum'] for data in jsonResult] #외국인 수 Y1 값
natNumList = [data['natNum'] for data in jsonResult] #내국인 수 Y2 값

plt.plot(dateList, forNumList, 'r--', label="외국인")
plt.plot(dateList, natNumList, 'b', label="내국인")
plt.xlabel("방문월")
plt.ylabel("방문객수")
plt.title(resname + " 관광객 방문객수")
plt.legend()
plt.grid(True)
plt.show()