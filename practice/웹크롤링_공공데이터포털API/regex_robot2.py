import re

def getRobotData(section, dataName, fileText) :
    #section 안의 데이터 들의 텍스트만 가져옴
    m = re.search(r'#\d+\s*' + section + r'\n([\w\W]+?)(?:#|$)', fileText)
    if m :
        dataText = m.group(1)
    else :
        dataText = ""
    #dataName에 해당하는 data 가져오기
    m = re.search(r'-\s*' + dataName + r'=([\w.,]*)', dataText)
    if m : 
        data = m.group(1)
    else :
        data = ""

    #data가 한개인 경우와 ',' 기준으로 여러개인경우
    #문자열 data를 정수 혹은 실수로 바꾼다
    if data.find(',') > 0 :
        data = data.split(',')
        for i,num in enumerate(data) :
            if num.find('.') > 0 :
                data[i] = float(num)
            else : 
                data[i] = int(num)
    else :
        if data.find('.') > 0 :
            data = [float(data)]
        else :
            data = [int(data)]
    return data 

with open('ROBOT.CON', 'r', encoding='utf8') as f :
    fileText = f.read() #f.read() 함수는 전체 파일읽어서 문자열로 반환한다.
section = "Conveyor configuration setting"
dataName = "Sampling time"
print(getRobotData(section, dataName, fileText))
