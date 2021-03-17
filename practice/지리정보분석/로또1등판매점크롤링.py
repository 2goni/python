import urllib.request 
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
wd = webdriver.Chrome("chromedriver.exe", options=options)
# 창 최대화
wd.maximize_window()

StoreList = []
i = 954
while True :
    url = f"https://www.dhlottery.co.kr/store.do?method=topStore&pageGubun=L645&drwNo={i}"
    wd.get(url)
    html = wd.page_source
    soup = BeautifulSoup(html, "html.parser")
    tag_div = soup.find('div',attrs={'class' : 'group_content' })
    try :  
        a=tag_div.find_all('tr')
        for storeInfo in tag_div.find_all('tr')[1:] :
            #매장 정보가 없으면 반목문 나가기
            tag_td = storeInfo.find_all('td')
            storeDic = {}
            storeDic["name"] = tag_td[1].string #매장이름
            storeDic["address"] = tag_td[3].string #주소
            StoreList.append(storeDic)       
    except :
        break
    i-=1

lotto_table = pd.DataFrame(StoreList, columns=('name', 'address'))
lotto_table.to_csv("lotto.csv", encoding="UTF-8", mode="w", index=True)