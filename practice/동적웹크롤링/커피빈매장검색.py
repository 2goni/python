
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

url = "https://www.coffeebeankorea.com/store/store.asp"
wd = webdriver.Chrome("chromedriver.exe")

#커피빈 매장 홈페이지 열기
wd.get(url)
StoreList = []
for i in range(1, 368) :
    wd.execute_script(f"storePop2('{i}')")
    time.sleep(1)

html = wd.page_source
soup = BeautifulSoup(html, "html.parser")
allStore = soup.find_all("div", attrs={"class" : "matizCoverLayerContent"})
resultList = []
#태그분석
for store in allStore : 
    try :
        name = store.select("div.store_txt > h2")[0].string
        rtime = store.select("table.store_table > tbody > tr > td")[0].string
        address = store.select("table.store_table > tbody > tr > td")[2].text
        phone = store.select("table.store_table > tbody > tr > td")[3].string
    #파싱한 정보 storeList에 저장    
        storeInfoDic = {}
        storeInfoDic['name'] = name
        storeInfoDic['time'] = rtime
        storeInfoDic['address'] = address
        storeInfoDic['phone'] = phone
        resultList.append(storeInfoDic)
    except : 
        continue
    
    #storeList json 파일로 저장
with open(f"Coffebean.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)

#matizCoverLayer3Content > div > div > div.store_txt > table > tbody:nth-child(1) > tr:nth-child(3) > td