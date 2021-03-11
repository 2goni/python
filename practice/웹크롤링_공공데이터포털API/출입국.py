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

def getEdrcntTourismStatsList(yyyymm, natCd, edCd) : 
#함수인자로 날짜, 시이름, 구이름, 관광명소이름 
    serviceUrl = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameter = "?_type=json&serviceKey=" + ServiceKey
    parameter += "&YM=" + yyyymm
    parameter += "&NAT_CD=" + natCd
    parameter += "&ED_CD=" + edCd

    url = serviceUrl + parameter
    retData = getRequestUrl(url)
    if retData == None :
        return None
    else :
        return json.loads(retData)

print("<< 국내 입국한 외국인 및 출국한 내국인의 통계 데이터를 수집합니다. >>")
nat_cd = input("국가 코드를 입력하세요. (ex 한국:100 / 중국: 112/ 일본:130 / 미국: 275) : ")
startYear = int(input("데이터를 몇 년부터 수집할까요? "))
endYear = int(input("데이터를 몇 년까지 수집할까요? "))
ed_cd = input("E: 방한외래관광객, D: 해외출국 코드 선택하세요. ")

jsonResult = []
for year in range(startYear, endYear+1) :
    for month in range(1, 13) :
        yyyymm = "{0}{1:0>2}".format(str(year), str(month))
        jsonData = getEdrcntTourismStatsList(yyyymm, nat_cd, ed_cd)
        
        if jsonData['response']['header']['resultMsg'] == 'OK' :
            item = jsonData['response']['body']['items']
            endDate = yyyymm
            if item == '' :
                break
            else :
                item = item['item']
                natName = item['natKorNm']
                num = item['num']
                ed = item['ed']
                yyyymm = item['ym']
                jsonResult.append({'yyyymm':yyyymm, 'natName':natName, 'num':num, 'ed':ed})


with open('%s_%s_%d01_%s.json' %(natName, ed, startYear, endDate), 'w', encoding='utf8') as outfile :
    retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print('%s_%s_%d01_%s.json Saved' %(natName, ed, startYear, endDate))

