from selenium import webdriver

wd = webdriver.Chrome("chromedriver.exe")
wd.get("https://www.naver.com")



elem = wd.find_element_by_class_name("link_login")
elem.click()

wd.back()
wd.forward()
wd.refresh()
wd.back()

elem = wd.find_element_by_id("query")
from selenium.webdriver.common.keys import Keys
elem.send_keys("파이썬")
elem.send_keys(Keys.ENTER)

elem = wd.find_elements_by_tag_name("a")
for e in elem :
    print(e.get_attribute("href"))

wd.get("https://www.naver.com")
elem = wd.find_element_by_class_name("link_login")
elem.click()

wd.find_element_by_id("id").send_keys("2goni")
wd.find_element_by_id("pw").send_keys("2456456!")
wd.find_element_by_id("log.login").click()

wd.find_element_by_id("id").send_keys("2goni")
wd.find_element_by_id("id").clear()
wd.find_element_by_id("id").send_keys("my_id")

html = wd.page_source
print(html)


