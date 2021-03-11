import datetime
import json
import urllib.request
import matplotlib.pyplot as plt

'''
종류별 코드 - 수출
A	일반수출
B	보세공장으로부터 수출
C	관세자유지역으로부터 수출
D	자유무역지역으로 부터 수출
E	종합보세구역으로부터 수출
F	공해상에서 체포한 수산물의 현지수출(원양어업협회 통보분)
G	보세판매장으로부터 수출
L	선상신고
P	우편수출(국제우체국 면허분)

종류별 코드 - 수입
11	일반수입(외화획득용)
12	외국으로부터 수출할 목적으로 보세공장에 반입되는 물품
13	보세공장으로부터 수입(제품과세)
14	외국자유무역지역 반입물품(원재료)
15	자유무역지역 제조가공물품통관
16	해외진출기업 제작물품 수입(외화획득용)
17	보세건설장반입물품 수리전사용승인 물품
18	보세판매장 반입물품(보세공장,수출자유지역반입)
19	해외진출기업 제작물품 수입(내수용)
20	보세건설장반입물품 수리전사용승인물품(분할신고)
21	일반수입(내수용)
22	수리전반출승인수입(외화획득용)
23	수리전반출승인수입(내수용)
24	면세품 판매장 수입(반입)
25	면세품 판매장의 잉여품 수입(반입)
26	우편물품(국제우체국 면허분)
27	종합보세구역에 반입, 자유무역지역에 반입
28	보세공장물품,자유무역지역 잉여품통관
29	보세공장으로부터 수입(원료과세)
30	보세판매장 반입물품(외국에서 직수입)
31	외국으로부터 수입을 목적으로 보세공장에 반입되는 물품
32	종합보세구역으로부터 수입
33	보세판매장 반입물품(기타 환급대상물품반입)
34	보세공장,자유무역지역,종합보세구역에서 잉여품수입-외화획득용
35	외국자유무역지역 반입물품(시설재)
36	종합보세구역(보세공장기능) 원료과세 / 종합보세구역 원료과세
37	외국자유무역지역 반입물품(GDC 물품)
'''

#인증키
ServiceKey = "zCpyrUPHh3%2FV6PjnkzwsOASmkhpbKCFXTlyM4xzRoA0W%2F"\
    "xLuS3FK142RF3Ksbae%2FHgrHGp3QNk7ze29sNcq2ag%3D%3D" 
                								
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

def getkindtradeList(searchBgnDe, searchEndDe, searchClCd, searchGbn) : 
#함수인자로 날짜, 시이름, 구이름, 관광명소이름 
    serviceUrl = "http://openapi.customs.go.kr/openapi/service/newTradestatistics/getkindtradeList"
    parameter = "?_type=json&serviceKey=" + ServiceKey
    parameter += "&searchBgnDe=" + searchBgnDe
    parameter += "&searchEndDe=" + searchEndDe
    parameter += "&searchClCd=" + searchClCd
    parameter += "&searchGbn=" + searchGbn

    url = serviceUrl + parameter
    retData = getRequestUrl(url)
    if retData == None :
        return None
    else :
        return json.loads(retData)
startYearMon = input("데이터를 몇년몇월부터 수집할까요? ")
endYearMon = input("데이터를 몇년몇월까지 수집할까요? ")
searchClCd = input("11:일반수입, A:일반수출 중 선택하여 입력하세요.")
searchGbn = "2" if searchClCd=='11' else "1" 

jsonData = getkindtradeList(startYearMon, endYearMon, searchClCd, searchGbn)
jsonResult = []
if jsonData['response']['header']['resultCode'] == '00' :
    item = jsonData['response']['body']['items']
    if item == '' :
        print("가져온 결과가 없습니다.")
    else :
        itemList = jsonData['response']['body']['items']['item']
        for item in itemList[:-2] :
            yyyymm = item['year']
            codeName = item['statCdCntnKor1']
            statCd = item['statCd']
            cnt = item['cnt']
            won = item['won']
            type = item['impexp']
            jsonResult.append({'yyyymm':yyyymm, 'codeName':codeName, 'statCd':statCd, \
                    "cnt" : cnt, "won" : won, "type":type})
    
with open('관세청_%s_%s_%s_%s.json' %(type, codeName,startYearMon,endYearMon ), 'w', encoding='utf8') as outfile :
    retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print('관세청_%s_%s_%s_%s.json' %(type, codeName,startYearMon,endYearMon ))
