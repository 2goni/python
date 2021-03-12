from selenium import webdriver
from selenium.webdriver.common import keys
from soupsieve.css_parser import SelectorPattern
from selenium.webdriver.common.keys import Keys

wd = webdriver.Chrome("chromedriver.exe")
wd.implicitly_wait(10)
wd.maximize_window()

i = 0
while True :
    if i > 1001 :
        break
    try :
        url = f"http://www.riss.kr/search/Search.do?searchGubun=true&viewYn=OP&queryText=&strQuery=big+data&exQuery=language%3Aeng%E2%97%88&exQueryText=%EC%9E%91%EC%84%B1%EC%96%B8%EC%96%B4+%5B%EC%98%81%EC%96%B4%5D%40%40language%3Aeng%E2%97%88&order=%2FDESC&on&strSort=RANK&p_year1=&p_year2=&iStartCount={i}&fsearchMethod=search&sflag=1&icate=re_a_over&colName=re_a_over&pageScale=100&isTab=Y&query=big+data"
        wd.get(url)
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        wd.find_element_by_css_selector("#divContent > div.rightContent > div > div.srchResultW > div.srchResultTop.bottom > div.resultTop1 > label > span").click()
        wd.find_element_by_css_selector("#divContent > div.rightContent > div > div.srchResultW > div.srchResultTop.bottom > div.resultTop1 > ul > li:nth-child(1) > a").click()
        wd.switch_to_window(wd.window_handles[1]) 
        wd.get_window_position(wd.window_handles[1])
        wd.find_element_by_css_selector("#wrap > form > div > div.popCont > div:nth-child(1) > div > ul > li:nth-child(3) > label").click()
        wd.find_element_by_css_selector("#riss_gubun > div.btnBunch > a.btnType1").click()
        wd.switch_to_window(wd.window_handles[0]) 
        wd.get_window_position(wd.window_handles[0])
        i+=100
    except :
        break

a = input()
