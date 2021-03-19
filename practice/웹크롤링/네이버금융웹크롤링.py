import urllib.request 
import datetime
from bs4 import BeautifulSoup
import json

def getRequestUrl(url) :
    req = urllib.request.Request(url)
    try :
        response = urllib.request.urlopen(req)
        if response.getcode() == 200 :
            print(f"[{datetime.datetime.now()}]  Url Request Success")
            return response.read()
    except Exception as e :
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")

resultList = []
i = 32
while True :
    try:
        url = f"https://finance.naver.com/sise/sise_market_sum.nhn?&page={i}"
        html = getRequestUrl(url)
        soup = BeautifulSoup(html, 'html.parser')
        tag_tbody = soup.find('table',attrs={'class' : 'type_2' })
        for storeInfo in tag_tbody.find_all('tr')[2:] :
            try :
                tag_td = storeInfo.find_all('td')
                resultDic = {}
                resultDic["순위"] = tag_td[0].string 
                resultDic["종목명"] = tag_td[1].string 
                resultDic["현재가"] = tag_td[2].string
                resultDic["시가총액"] = tag_td[6].string 
                resultDic["외국인비율"] = tag_td[8].string 
                resultDic["PER"] = tag_td[10].string 
                resultDic["ROE"] = tag_td[11].string 
                resultList.append(resultDic)
            except : 
                continue
        i-=1
    except :
        break
with open(f"네이버금융.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)

