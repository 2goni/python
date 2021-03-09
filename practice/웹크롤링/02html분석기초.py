from bs4 import BeautifulSoup
import urllib.request 
import datetime

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

url = "https://comic.naver.com/index.nhn"
html = getRequestUrl(url)

#BeatifulSoup 객체생성
soup = BeautifulSoup(html, 'html.parser')

#객체에 저장된 html 내용을 확인
print(soup.prettify())

#클래스 검색
li_list = soup.select("div.tab_gr>ul>li")
for li in li_list :
     print(li.a.string)

for a in soup.find_all('a') :
    print(a)

#다르게 찾는법
tag_div = soup.find("div", attrs = {'class' : 'tab_gr'})
tag_ul = tag_div.ul
tag_li = tag_div.find_all("li")

print(tag_li)

