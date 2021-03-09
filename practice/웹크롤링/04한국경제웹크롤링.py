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

maxPage = 10
newsList = []
for i in range(1,maxPage +1) :
    pageNo = i
    url = f"https://www.hankyung.com/it?page={pageNo}"

    html = getRequestUrl(url)
    soup = BeautifulSoup(html, 'html.parser')
    tag_li_list = soup.select('div.inner_list>ul>li>div.article>h3>a')

    for a_tag in tag_li_list :
       newsDic = {}
       newsDic["title"] = a_tag.string
       newsDic["link"] = a_tag["href"]
       newsList.append(newsDic)

print("뉴스개수 : " + str(len(newsList)))
for news in newsList : 
    print(news)

news_table = pd.DataFrame(newsList, columns=('title', 'link'))

news_table.to_csv("itnews.csv", encoding="UTF-8", mode="w", index=True)

