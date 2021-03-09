import urllib.request 
import datetime
import time
import json

#url끌고오기 (기본)
def getRequestUrl(url) :
    req = urllib.request.Request(url)
    try :
        response = urllib.request.urlopen(req)
        if response.getcode() == 200 :
            print(f"[{datetime.datetime.now()}] Url Request Success")
            return response.read().decode('UTF-8')
    except Exception as e :
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")


print("<< 네이버 연관 검색어> >")
searchText = input("검색어를 입력하세요")
ServiceUrl = "https://ac.search.naver.com/nx/ac?q="
parameter = urllib.parse.quote(searchText)
parameter += "&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&enc=UTF-8&st=100&"
url = ServiceUrl + parameter
print(getRequestUrl(url))

jsonResult = json.loads(getRequestUrl(url))

result = []
for item in jsonResult["items"][0] :
    result.append(item[0])

for item in result :
    print(item)
