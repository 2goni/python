from os import kill
import pandas as pd
import numpy as np
import re
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rcParams, style
from matplotlib import font_manager, rc

data = pd.read_csv("./지리정보분석/hollys.csv", index_col=0, encoding="cp949", engine="python")

addr = pd.DataFrame(data['region'].apply(lambda v: v.split()[:2]).tolist(), columns=('시도','군구'))
for i in range(5) :
    print(addr.iloc[i])
addr['count'] = 0

addr['시도'] = addr['시도'].replace(['서울','세종','충북','강원','경기','경북','울산','인천','대구','부산','대전','광주','경남','충남','전북','전남','제주'],\
    ['서울특별시','세종특별자치시','충청북도','강원도','경기도','경상북도','울산광역시','인천광역시'\
        ,'대구광역시','부산광역시','대전광역시','광주광역시','경상남도','충청남도','전라북도','전라남도','제주특별자치도'])

for i in range(5) :
    print(addr.iloc[i])
addr_group = pd.DataFrame(addr.groupby(['시도','군구'], as_index=False).count())

addr_group['시도군구'] = addr_group.apply(lambda x : x['시도'] + ' ' + x['군구'], axis=1)
addr_group = addr_group.set_index("시도군구")

population = pd.read_excel('./지리정보분석/행정구역_시군구_별__성별_인구수_20210315171045.xlsx')
population = population.rename(columns={'행정구역(시군구)별(1)' : '시도', '행정구역(시군구)별(2)' : '군구'})

for i in range(len(population)) :
    population['시도'][i] = population['시도'][i].strip()
    population['군구'][i] = population['군구'][i].strip()

population = population[population.군구 != '소계']
population['시도군구'] = population.apply(lambda r : r['시도'] + ' ' + r['군구'], axis=1)

population = population.set_index("시도군구")

addr_population_merge = pd.merge(addr_group, population, how='inner', left_index=True, right_index=True)

local_MC_Population = addr_population_merge[['시도_x', '군구_x','count','총인구수 (명)']]
local_MC_Population = local_MC_Population.rename(columns={"시도_x":"시도", "군구_x":"군구","총인구수 (명)":"인구수"})

# for i in range(len(local_MC_Population)):
#     tmp = re.findall(r'([0-9]*)\,?([0-9]*)\,?([0-9]+)',local_MC_Population['인구수'][i])
#     local_MC_Population['인구수'][i] = tmp[0][0] + tmp[0][1] + tmp[0][2]
# local_MC_Population['인구수'] = local_MC_Population['인구수'].astype('int')

MC_count = local_MC_Population['count']
local_MC_Population['MC_ratio'] = MC_count.div(local_MC_Population['인구수'], axis=0) * 100000

style.use("ggplot")
font_path = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname = font_path).get_name()
matplotlib.rc("font", family = font_name)

data_draw_korea = pd.read_csv('./지리정보분석/data_draw_korea.csv', index_col=0, encoding="utf-8", engine="python")

data_draw_korea['시도군구'] = data_draw_korea.apply(lambda r : r['광역시도'] + ' ' + r['행정구역'], axis=1)
data_draw_korea = data_draw_korea.set_index('시도군구')

data_all = pd.merge(data_draw_korea, local_MC_Population, how="outer", left_index=True, right_index=True)
for i in data_all['MC_ratio']:
    print(i)

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

    for idx, row in blockedMap.iterrows():
        annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

        if row.isna()[0] :
            continue
        dispname = row['shortName']
        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 7.5, 1.5
        else:
            fontsize, linespacing = 11, 1.2

        plt.annotate(dispname, (row['x']+0.5, row['y']+0.5), weight='bold',
                      fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)
    
    for path in BORDER_LINES:
        ys, xs = zip(*path)
        plt.plot(xs, ys, c='black', lw=4)

    plt.gca().invert_yaxis()
    plt.axis('off')
    
    cb = plt.colorbar(shrink=.1, aspect=10)
    cb.set_label(datalabel)

    plt.tight_layout()
    plt.show()      

draw_blockMap(data_all, "MC_ratio", "행정구역별 인구수 대비 hollys커피 매장 비율", 'Reds')
