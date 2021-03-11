import datetime
import json
import urllib.request
import matplotlib.pyplot as plt

#인증키
ServiceKey = "UONoET2Grg2f0je6CsDmMP%2BsJ%2B1fT93YXiwOrW0vSx9x%2F"\
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

def getTourismBalcList(yyyymm) : 
#함수인자로 날짜, 시이름, 구이름, 관광명소이름 
    serviceUrl = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getTourismBalcList"
    parameter = "?_type=json&serviceKey=" + ServiceKey
    parameter += "&YM=" + yyyymm

    url = serviceUrl + parameter
    retData = getRequestUrl(url)
    if retData == None :
        return None
    else :
        return json.loads(retData)


startYear = int(input("데이터를 몇 년부터 수집할까요? "))
endYear = int(input("데이터를 몇 년까지 수집할까요? "))
jsonResult = []
for year in range(startYear, endYear+1) :
    for month in range(1, 13) :
        yyyymm = "{0}{1:0>2}".format(str(year), str(month))
        jsonData = getTourismBalcList(yyyymm)
        
        if jsonData['response']['header']['resultMsg'] == 'OK' :
            item = jsonData['response']['body']['items']
            endDate = yyyymm
            if item == '' :
                break
            else :
                item = item['item']
                tb = item['tb']
                te = item['te']
                tr = item['tr']
                tePerhead = item['tePerhead']
                trPerhead = item['trPerhead']
                yyyymm = item['ym']
                jsonResult.append({'yyyymm':yyyymm, 'tb':tb, 'te':te, 'tr':tr, \
                    "tePerhead" : tePerhead, "trPerhead" : trPerhead})


with open('관광수지_%d01_%s.json' %(startYear, endDate), 'w', encoding='utf8') as outfile :
    retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print('관광수지_%d01_%s.json Saved' %(startYear, endDate))

