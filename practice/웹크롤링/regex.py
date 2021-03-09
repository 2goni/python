#regular expression
import re

tempStr = "python"
# ^ : 문자열의 시작을 나타낸다.
# . : 글자 하나를 나타낸다.
p = re.compile('^..thon') # 정규 표현식 만드는 구문
m = p.match(tempStr) # 문자열의 처음부터 정규식과 매치되는지 조사

if m :
    print(m.group())
else :
    print("매칭되지 않음")

tempStr = "program lang : python"
# search 문자열 전체를 검색해서 정규식과 매치되는지 조사
matchObj = re.search("..thon", tempStr)
print(matchObj.group())

# . : 문자하나를 의미
# ^ : 문자열의 시작
# $ : 문자열의 끝
# ? : 앞문자 있어도되고 없어도된다. ex) appl?e => apple, appe
# (?!) : 대소문자를 구분하지 않는다.
# | : 다자 택일 (or) ex) a|bpple => apple, bpple
# 반복기호 : * 0번이상, + 1번이상, {m,n} m~n번 반복 
#           ex) a^pple => apple, pple, aaaaaaaaaapple
#           ex) a+pple => apple, aaaaaaaaaapple
#           ex) a+pple => apple, aaaaaaaaaapple
            
# 문자 클래스 [] : [] 사이의 문자들과 매치 ex) [abc]pple => bpple, apple, cpple
# 그룹 () : () 사이의 문자와 모두 매치 

# 문자 클래스 특수용도
# [0-9] 연속값 처리 => [0,1,2,3,4,5,6,7,8,9]
# [a-z] => [a,b,c,......,z]
# [a-zA-Z] => 모든 알파벳
# \d - 모든 숫자 [0-9]
# \D - 숫자가 아닌것과 매치[^0-9]
# \w - 문자 + 숫자 매치 [a-zA-Z0-9]
# \W - (문자+숫자) 아닌것과 매치 [^a-zA-Z0-9]
# \s - whitespace 문자와 매치, [\t\n\r\f\v]
# \S - whitespace 아닌 문자와 매치
# \b - 단어의 경계, 공백, 탭, 컴마, 대시 등 (정규 표현식 'r')
# \B - 단어의 경계, 공백, 탭, 컴마, 대시 가 아닌것 

# match() : 문자열의 처음부터 정규식과 매치되는지 조사
# search() : 문저열 전제를 검색하여 정규식과 매치되는지 조사
# findall() : 정규식과 매치되는 모든 문자열을 리스트로 돌려준다.
# split() : 정규식과 매치되는 문자열을 기준으로 파싱하여 리스트로 돌려준다.

m = re.search('ca.e', "Good care")
print("일치하는 문자열 :", m.group())
print("입력받은 문자열 :", m.string)
print("일치하는 문자열의 시작 인덱스 :", m.start())
print("일치하는 문자열의 끝 인덱스 :", m.end())
print("일치하는 문자열 시작과 끝 인덱스 :", m.span())

mList = re.findall('[\w]*berry', "berry apple, strawberry kiwi rasberry")
print(mList)

mList = re.findall('one|self|the', 'oneself is the one thing')
print(mList)

m = re.search('\d{4}-(\d\d)-(\d\d)', '2021-03-09')
print(m.group())
print(m.group(0))
print(m.group(1))
print(m.group(2))

tr_tag = '<tr id="abc123", class="ddd">hello</tr>'
m = re.search('<tr.*id="(.*)",.*>(.*)</tr>', tr_tag)
print(m.group())
print(m.group(0)) 
print(m.group(1))
print(m.group(2))

m = re.search('((ab)+), ((123)+) is repetitive\.','Hmm... ababab, 123123 is repetitive.')
print(m.group(0))
print(m.group(1))
print(m.group(2))

m_list = re.findall(r'((\w)(\w)\2)','토마토 ABC abc xyxy')
print(m_list)

sList = re.split(',', '14.5,12,18,19,등등등,abc')
print(sList)

sList = re.split('\s+', '14.5          12                   18         19 등등등    abc')
print(sList)

#조건 표현식
#표현식1(?=표현식2): 표현식 1 뒤의 문자열이 표현식2와 매치되면 표현식1 
mList = re.findall(r'\b(hello(?=World)\w*)\b','helloWorld byeWorld helloJames')
print(mList)

#/b 단어의 경계, 공백, 탭, 컴마, 대시 등 (정규 표현식 'r')
mList = re.findall(r'\bline\b', 'outline linear line')
print(mList)


# (.+)cat(.+)을 포함한 글자는 가져오지만, cat혹은 cat(.+), (.+)cat 제외시키기
mList = re.search(r'\B(\w*cat\w*)\B', 'cat catch copycat scatter')
print(mList.group())

#432 2344 12930 1888199, 1~4자리 숫자에 일치하는 숫자만 가져오도록
mList = re.findall(r'\b\d{1,4}\b', '432 2344 12930 1888199')
print(mList)

#txt, pdf, hwp, xls 파일 확장자만 검색할 수 있도록 정규 표현식 완성하시오.
#abc.txt, test.xls, regex.py(x)
mList = re.findall(r'\S+\.(?:txt|xls|hwp)', 'abc.txt, test.xls, regex.py, cat.jpg, hi.hwp, main,jsp')
print(mList)




