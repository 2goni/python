import urllib.request 
import datetime
from bs4 import BeautifulSoup
import pandas as pd


def getRequestUrl(url) :
    req = urllib.request.Request(url)
    try :
        response = urllib.request.urlopen(req)
        if response.getcode() == 200 :
            print(f"[{datetime.datetime.now()}]  Url Request Success")
            return response.read().decode('UTF-8')
    except Exception as e :
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")

maxPage = 2
storeList = []
for i in range(1,maxPage +1) :
    pageNo = i
    url = f"http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page={pageNo}"

    html = getRequestUrl(url)
    soup = BeautifulSoup(html, 'html.parser')
    tag_tbody = soup.find('tbody')

    for storeInfo in tag_tbody.find_all('tr') :
        #매장 정보가 없으면 반목문 나가기
        if len(storeInfo) < 4 :
            break
        tag_td = storeInfo.find_all('td')
        storeDic = {}
        storeDic["name"] = tag_td[1].string #매장이름
        storeDic["region"] = tag_td[0].string #지역정보
        storeDic["address"] = tag_td[2].string #주소
        storeDic["phone"] = tag_td[3].string #전화번호
        storeList.append(storeDic)

print("매장개수 : " + str(len(storeList)))
for store in storeList : 
    print(store)

store_table = pd.DataFrame(storeList, columns=('name', 'region', 'address', 'phone'))

store_table.to_csv("처갓집.csv", encoding="UTF-8", mode="w", index=True)
