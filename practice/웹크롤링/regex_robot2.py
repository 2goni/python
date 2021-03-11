import re

with open('ROBOT.CON', 'r', encoding='utf8') as f :
    fileText = f.read()

section = "Control enviroment setting"
dataName = "Return length[mn]"
m = re.search(r'#\d+ ' + section + r'\n([\w\W]+?)#', fileText)

dataText = m.group(1)

#dataName에 해당하는 data 가져오기
m = re.search(r'-\s*' + dataName + r'=([\w.,]*)', dataText)
print(m.group(1))