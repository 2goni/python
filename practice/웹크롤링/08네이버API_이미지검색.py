import urllib.request 
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import json
import dload
import re

client_id = "FbRhzsAy9wRbOgSRpXRu"
client_secret = "fYyw5DbXZg"
#url 가져오기
def getRequestUrl(url) :
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id",client_id)
    req.add_header("X-Naver-Client-secret",client_secret)
    try :
        response = urllib.request.urlopen(req)
        if response.getcode() == 200 :
            print(f"[{datetime.datetime.now()}]  Url Request Success")
            return response.read().decode('UTF-8')
    except Exception as e :
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")

#검색 URL 생성해주는 함수
def getNaverSearch(type, srcText, start, display) :    
    serviceURL = "https://openapi.naver.com/v1/search"
    type = f"/{type}.json"
    parameter = "?query=%s&start=%s&display=%s"%(urllib.parse.quote(srcText),start,display)
    url = serviceURL + type + parameter

    result = getRequestUrl(url)

    if result != None :
        return json.loads(result)
    else :
        None

def getPostData(item, jsonResult, idx) :
    title = item['title']
    link = item['link']
    jsonResult.append({'idx' : idx, 'title' : title, 'link' : link}) 

type = "image"
srcTxt = input("검색어를 입력하세요")
jsonResult = []

jsonResponse = getNaverSearch(type, srcTxt, 1, 100)
total = jsonResponse["total"]
idx =  0
while(jsonResponse != None) and jsonResponse['display'] != 0 :
    for item in jsonResponse['items'] :
        idx += 1
        getPostData(item, jsonResult, idx)
    start = jsonResponse['start'] + jsonResponse['display']
    jsonResponse = getNaverSearch(type,srcTxt,start,100)

print("전체 검색 결과 %d 건" %total)
print("가져온 결과 %d건" %idx)

#json 파일로 만들기
with open("%s_naver_%s.json" %(srcTxt, type), 'w', encoding='utf-8') as outfile :
    jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(jsonFile)

print("%s_naver_%s.json Saved" %(srcTxt, type))

for image in jsonResult : 
    idx = image["idx"]
    link = image['link']
    m = re.search(r"\.(\w+)$",link)
    if m :
        fileType = m.group(1)
    else :
        fileType = "jpg"

    dload.save(link, "./image/%d.%s" % (idx, fileType))
    print("%d.%s 다운로드완료" %(idx, fileType))


#csv 파일로 만들기
newsTable = pd.DataFrame(jsonResult, columns=('idx', 'title', 'link'))
newsTable.to_csv("%s_naver_%s.csv" %(srcTxt, type), encoding='utf-8', mode='w', index=False)
