from warnings import catch_warnings
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import time
import json
import re
from soupsieve.css_parser import SelectorPattern

area = input('구를 입력하세요 ex)강남구')
url = f"https://m.land.naver.com/search/result/{area}"

wd = webdriver.Chrome("chromedriver.exe")
wd.implicitly_wait(10)

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
hd = webdriver.Chrome('chromedriver.exe', options=options)
hd.implicitly_wait(10)

wd.maximize_window()
wd.get(url)
time.sleep(2)
html = wd.page_source
soup = BeautifulSoup(html, "html.parser")
allbuttons = soup.find_all("div", attrs={"class" : "marker_circle _marker _markerEnv"})
resultList = []
for button in allbuttons : 
    try :
        key = button['key']
        lgeo = button['lgeo']
        elem = wd.find_element_by_xpath(f'//*[@key="{key}"]')
        elem.click()
        ihtml = wd.page_source
        soup = BeautifulSoup(ihtml, "html.parser")
        lat = re.search(r"lat: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
        lon = re.search(r"lon: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
        z = re.search(r"z: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
        cortarNo = re.search(r"cortarNo: \'(\S+)\'" , soup.select_one("#mapSearch > script").string).group(1)
        i = 1
        while True :
            url = f"https://m.land.naver.com/cluster/ajax/articleList?itemId={key}&lgeo={lgeo}&srletTpCd=APT&tradTpCd=A1%3AB1%3AB2&z={z}&lat={lat}&lon={lon}&cortarNo={cortarNo}&sort=rank&page={i}"
            hd.get(url)
            res = json.loads(hd.find_element_by_css_selector("body > pre").text)
            if res['body'] :
                resultList.append(res['body'])
                print(f"값 불러오기 완료")
                i += 1               
            else :
                print('버튼완료')
                break
    except selenium.common.exceptions.NoSuchElementException: 
        print(f"오류발생(봇감지). key : {key}")
    except selenium.common.exceptions.ElementClickInterceptedException :
        print(f"오류발생(화면밖의 버튼입니다.) key : {key}")
        
with open(f"NaverRealty.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)        
    print("저장완료")

         

