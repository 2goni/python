import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import re





area = "강남구"
url = f"https://m.land.naver.com/search/result/{area}"
wd = webdriver.Chrome("chromedriver.exe")
wd.get(url)
time.sleep(1)
html = wd.page_source
soup = BeautifulSoup(html, "html.parser")
allbuttons = soup.find_all("div", attrs={"class" : "marker_circle _marker _markerEnv"})
resultList = []
for i,button in enumerate(allbuttons) : 
    key = button['key']
    lgeo = button['lgeo']
    rletTpCd= "APT"
    tradTpCd= "A1%3AB1%3AB2"
    elem = wd.find_element_by_xpath(f'//*[@key="{key}"]')
    elem.click()
    time.sleep(3)
    ihtml = wd.page_source
    soup = BeautifulSoup(html, "html.parser")
    lat = re.search(r"lat: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
    lon = re.search(r"lon: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
    z = re.search(r"z: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
    cortarNo = re.search(r"cortarNo: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)

    time.sleep(3)
    while True :
        url = f"https://m.land.naver.com/cluster/ajax/articleList?itemId={key}&lgeo={lgeo}&srletTpCd=APT&tradTpCd=A1%3AB1%3AB2&z={z}&lat={lat}&lon={lon}&cortarNo={cortarNo}&sort=rank&page={i+1}"
        res = requests.get(url).text
        print(res)
        time.sleep(3)
        name = re.search(r'atclNm: \"(\S+)\"', res)
        storeInfoDic = {}
        storeInfoDic['name'] = name
        resultList.append(storeInfoDic)
    break    
with open(f"NaverHouse.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)        

         


# a = input() 

# #이름
# #가격



# html = wd.page_source
# soup = BeautifulSoup(html, "html.parser")
# allStore = soup.find_all("div", attrs={"class" : "matizCoverLayerContent"})
# resultList = []
# #태그분석
# for store in allStore : 
#     try :
#         name = store.select("div.store_txt > h2")[0].string
#         rtime = store.select("table.store_table > tbody > tr > td")[0].string
#         address = store.select("table.store_table > tbody > tr > td")[2].text
#         phone = store.select("table.store_table > tbody > tr > td")[3].string
#     #파싱한 정보 storeList에 저장    
#         storeInfoDic = {}
#         storeInfoDic['name'] = name
#         storeInfoDic['time'] = rtime
#         storeInfoDic['address'] = address
#         storeInfoDic['phone'] = phone
#         resultList.append(storeInfoDic)
#     except : 
#         continue
    
#     #storeList json 파일로 저장
# with open(f"Coffebean.json", "w", encoding="utf8") as outfile :
#     retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
#     outfile.write(retJson)

# #matizCoverLayer3Content > div > div > div.store_txt > table > tbody:nth-child(1) > tr:nth-child(3) > td