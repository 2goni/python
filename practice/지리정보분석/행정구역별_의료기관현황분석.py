from os import kill
import pandas as pd
import numpy as np

data = pd.read_csv("./지리정보분석/보건복지부_공공보건 의료기관 현황_20161231.csv", \
    index_col=0, encoding="cp949", engine="python")

#print(data.head())

#공공보건 의료기관 주소 정리 -> 행정구역 파악
#주소에서 시도, 군구 정보 분리
addr = pd.DataFrame(data['주소'].apply(lambda v: v.split()[:2]).tolist(), columns=('시도','군구'))
#print(addr.head())
#print(addr[addr['시도'] == "천안시"])
addr.iloc[99] = ["대전광역시", "유성구"]
addr.iloc[22] = ["경기도", "안산시"]
addr.iloc[172] = ["경기도", "고양시"]
addr.iloc[24] = ["경상남도", "통영시"]
addr.iloc[25] = ["경상남도", "사천시"]
addr.iloc[26] = ["경상남도", "사천시"]
addr.iloc[28] = ["경상남도", "김해시"]
addr.iloc[77] = ["경상남도", "양산시"]
addr.iloc[78] = ["경상남도", "양산시"]
addr.iloc[115] = ["경상남도", "창원시"]
addr.iloc[27] = ["경상남도", "창원시"]
addr.iloc[31] = ["경상남도", "창원시"]
addr.iloc[47] = ["경상북도", "경산시"]
addr.iloc[49] = ["경상북도", "청도군"]
addr.iloc[114] = ["경상북도", "경산시"]
addr.iloc[116] = ["경상북도", "포항시"]
addr.iloc[84] = ["충청북도", "청주시"]
addr.iloc[110] = ["충청북도", "청원구"]
addr.iloc[92] = ["서울특별시", "강동구"]
addr.iloc[97] = ["서울특별시", "종로구"]
addr.iloc[135] = ["서울특별시", "노원구"]
addr.iloc[159] = ["서울특별시", "중랑구"]
addr.iloc[173] = ["서울특별시", "강남구"]
addr.iloc[98] = ["부산광역시", "해운대구"]
addr.iloc[111] = ["충청남도", "계룡시"]
addr.iloc[112] = ["충청남도", "논산시"]
addr.iloc[113] = ["전라남도", "함평군"]
addr.iloc[149] = ["전라남도", "고흥군"]
addr.iloc[195] = ["전라북도", "완주군"]
addr.iloc[196] = ["전라북도", "완주군"]
addr.iloc[209] = ["충청남도", "천안시"]
addr.iloc[210] = ["충청남도", "천안시"]
#print(addr['시도'].unique())
#print(addr[addr['군구'] == "아란13길"])
#print(addr['군구'].unique())
addr.iloc[75] = ["제주특별자치도", "제주시"]

addr['시도군구'] = addr.apply(lambda r : r['시도'] + ' ' + \
                            r['군구'], axis=1)
addr['count'] = 0
#print(addr.head())

addr_group = pd.DataFrame(addr.groupby(['시도', '군구',\
                            '시도군구'], as_index=False).count())
#print(addr_group.head())             
addr_group =  addr_group.set_index("시도군구")
#print(addr_group.head())

population = pd.read_excel('./지리정보분석/행정구역_시군구_별__성별_인구수_20210315171045.xlsx')
#print(population.head())
#pip install xlrd
#pip install openpyxl
population =  population.rename(\
    columns={'행정구역(시군구)별(1)':'시도', \
        '행정구역(시군구)별(2)':'군구'})
#print(population.head())
#데이터 공백제거
for i in range(len(population)) :
    population['시도'][i] = population['시도'][i].strip()
    population['군구'][i] = population['군구'][i].strip()

population['시도군구'] = population.apply(lambda r : r['시도'] + ' ' + \
                            r['군구'], axis=1)
population = population[population.군구 != '소계']
population = population.set_index("시도군구")
print(population.head())

 
#데이터 병합 - addr_group 과 population
addr_population_merge = pd.merge(addr_group, \
                        population, how='inner', \
                        left_index=True, right_index=True)
#print(addr_population_merge.head())
local_MC_Population = addr_population_merge[['시도_x', \
                    '군구_x', 'count', '총인구수 (명)']]
MC_count = local_MC_Population['count']
local_MC_Population['MC_ratio'] = MC_count.div( \
        local_MC_Population['총인구수 (명)'], axis=0) * 100000
#print(local_MC_Population.head())
local_MC_Population = local_MC_Population.rename(columns=\
            {"시도_x":"시도", "군구_x":"군구",\
                "총인구수 (명)" : "인구수"})
#막대 그래프로 시각화
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rcParams, style
from matplotlib import font_manager, rc

#테마 바꾸기
style.use("ggplot")
font_path = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname = font_path)\
                        .get_name()
matplotlib.rc("font", family = font_name)
# MC_ratio = local_MC_Population[["MC_ratio"]]
# MC_ratio = MC_ratio.sort_values("MC_ratio", ascending=False)
# plt.rcParams['figure.figsize'] = (25,5)
# MC_ratio.plot(kind = 'bar', rot=90)
# plt.show()
# print(MC_ratio.head())

data_draw_korea = pd.read_csv('./지리정보분석/data_draw_korea.csv', index_col=0, encoding="utf-8", engine="python")
data_draw_korea["시도군구"] = data_draw_korea.apply(lambda r : r['광역시도'] + ' ' + r['행정구역'], axis=1)
data_draw_korea = data_draw_korea.set_index("시도군구")

data_all = pd.merge(data_draw_korea, local_MC_Population, how="outer", left_index=True, right_index=True)
print(data_all.head())


#블록맵 행정구역 경계선 x,y 데이터
BORDER_LINES = [
    [(3, 2), (5, 2), (5, 3), (9, 3), (9, 1)], # 인천
    [(2, 5), (3, 5), (3, 4), (8, 4), (8, 7), (7, 7), (7, 9), (4, 9), (4, 7), (1, 7)], # 서울
    [(1, 6), (1, 9), (3, 9), (3, 10), (8, 10), (8, 9),
     (9, 9), (9, 8), (10, 8), (10, 5), (9, 5), (9, 3)], # 경기도
    [(9, 12), (9, 10), (8, 10)], # 강원도
    [(10, 5), (11, 5), (11, 4), (12, 4), (12, 5), (13, 5),
     (13, 4), (14, 4), (14, 2)], # 충청남도
    [(11, 5), (12, 5), (12, 6), (15, 6), (15, 7), (13, 7),
     (13, 8), (11, 8), (11, 9), (10, 9), (10, 8)], # 충청북도
    [(14, 4), (15, 4), (15, 6)], # 대전시
    [(14, 7), (14, 9), (13, 9), (13, 11), (13, 13)], # 경상북도
    [(14, 8), (16, 8), (16, 10), (15, 10),
     (15, 11), (14, 11), (14, 12), (13, 12)], # 대구시
    [(15, 11), (16, 11), (16, 13)], # 울산시
    [(17, 1), (17, 3), (18, 3), (18, 6), (15, 6)], # 전라북도
    [(19, 2), (19, 4), (21, 4), (21, 3), (22, 3), (22, 2), (19, 2)], # 광주시
    [(18, 5), (20, 5), (20, 6)], # 전라남도
    [(16, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10)], # 부산시
]

#블록맵의 블록에 데이터 매핑 후 색을 표시하여 블록맵 그리는 함수

def draw_blockMap(blockedMap, targetData, title, color ):
    whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + min(blockedMap[targetData])

    datalabel = targetData

    vmin = min(blockedMap[targetData])
    vmax = max(blockedMap[targetData])

    mapdata = blockedMap.pivot(index='y', columns='x', values=targetData)
    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
    
    plt.figure(figsize=(8, 13))
    plt.title(title)
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=color, edgecolor='#aaaaaa', linewidth=0.5)

    # 지역 이름 표시
    for idx, row in blockedMap.iterrows():
        annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

        if row.isna()[0] :
            continue
        dispname = row['shortName']
        """
        # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다. (중구, 서구)
        if row['광역시도'].endswith('시') and not row['광역시도'].startswith('세종'):
            dispname = '{}\n{}'.format(row['광역시도'][:2], row['행정구역'][:-1])
            if len(row['행정구역']) <= 2:
                dispname += row['행정구역'][-1]
        else:
            dispname = row['행정구역'][:-1]
        """       
        # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 7.5, 1.5
        else:
            fontsize, linespacing = 11, 1.2

        plt.annotate(dispname, (row['x']+0.5, row['y']+0.5), weight='bold',
                      fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)
    
    # 시도 경계 그린다.
    for path in BORDER_LINES:
        ys, xs = zip(*path)
        plt.plot(xs, ys, c='black', lw=4)

    plt.gca().invert_yaxis()
    #plt.gca().set_aspect(1)
    plt.axis('off')
    
    cb = plt.colorbar(shrink=.1, aspect=10)
    cb.set_label(datalabel)

    plt.tight_layout()
    plt.savefig('.\\지리정보분석\\' + 'blockMap_' + targetData + '.png')
    plt.show()      

    
draw_blockMap(data_all, 'count', '행정구역별 공공보건의료기관 수', 'Blues')

draw_blockMap(data_all, 'MC_ratio', '행정구역별 인구수 대비 공공보건의료기관 비용', 'Reds')