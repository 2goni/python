import re

mList = re.findall(r'ca.e', 'Good care car caee')
print(mList)

source = "<li>나이키</li><li>아디다스</li><li>퓨마</li>"

m = re.search(r'<li>(.*)</li>', source)
print(m.group(0))
print(m.group(1))

m = re.search(r'<li>(.*?)</li>', source) # +,*? 최소탐색 (탐욕적이지 않은 탐색)
print(m.group(0))
print(m.group(1))

tr_tag = '<tr href="dssdd", id= "abc123", class="ddd">hello</tr>'
#tr 태그의 href 속성값(address)과 태그값(hello) 가져오기
#정규표현식을 만들어 보세요

m = re.search(r'<tr.*href="(.*?)".*>(.*)</tr>', tr_tag)
print(m.group(0))
print(m.group(1))
print(m.group(2))