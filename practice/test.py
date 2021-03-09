import os #디렉터리 다루는 라이브러리

with open('대전.csv', 'r') as f :
    tempList = f.readlines()
    


#개행문자 제거
regionList = []
for region in tempList :
    region = region.replace('\n','')
    regionList.append(region)

#print(regionList)

guList = regionList[0].split(',')



#'구'값을 키로하고 동네 리스트를 value
regionDic = {}
for guName in guList :
    regionDic[guName] = []
    
for dongInfo in regionList[1:] :
    dongList = dongInfo.split(',')
    for i, guName in enumerate(guList) :
        tempList=[]
        tempList.append(dongList[i])
        regionDic[guName] += tempList

print(regionDic)

curPath = os.getcwd()
regionName = "대전"
os.mkdir(regionName)

for key, value in regionDic.items():
    os.chdir(curPath + '\\' + regionName)
    os.mkdir(key)
    for dongName in value :
        if dongName != '' :
            os.chdir(curPath + '\\' + regionName + '\\' +key)
            os.mkdir(dongName)

