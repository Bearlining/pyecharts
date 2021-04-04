import pandas as pd
import pyecharts as pe
import warnings

warnings.filterwarnings('ignore')
pan = pd.read_excel('100day_panel.xlsx', index_col='日期')

pan['现存'] = pan['确诊'] - pan['死亡'] - pan['治愈'] # 计算每日现存病例数
data_china = pan.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()  # 得到全国的时间序列数据
data_hb = pan[pan['省市'] == '湖北']  # 由于湖北省的数据和其他省的数据放在一起分析不合适，所以单独创建一个
data_nohb = pan[pan['省市'] != '湖北'].groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()  # 非湖北省的数据合计

data_china['确诊新增'] = data_china['确诊'] - data_china['确诊'].shift()
data_china['死亡新增'] = data_china['死亡'] - data_china['死亡'].shift()
data_china['治愈新增'] = data_china['治愈'] - data_china['治愈'].shift()

data_china['确诊增长率'] = data_china['确诊新增'] / data_china['确诊'].shift()
data_china['确诊增长率'] = data_china['确诊增长率'].round(2)

data_china['治愈率'] = data_china['治愈'] / data_china['确诊'].shift()
data_china['治愈率'] = data_china['治愈率'].round(2)
data_china['治愈率'].tail(20)

data_hb['确诊新增'] = data_hb['确诊'] - data_hb['确诊'].shift()
data_hb['死亡新增'] = data_hb['死亡'] - data_hb['死亡'].shift()
data_hb['治愈新增'] = data_hb['治愈'] - data_hb['治愈'].shift()
data_hb['现存新增'] = data_hb['现存'] - data_hb['现存'].shift()

data_nohb['确诊新增'] = data_nohb['确诊'] - data_nohb['确诊'].shift()
data_nohb['死亡新增'] = data_nohb['死亡'] - data_nohb['死亡'].shift()
data_nohb['治愈新增'] = data_nohb['治愈'] - data_nohb['治愈'].shift()
data_nohb['现存新增'] = data_nohb['现存'] - data_nohb['现存'].shift()

bar1 = pe.Bar('全国累计确诊柱状图', title_pos='left')  # 定义一个图表对象并设置图表标题及其位置（左中右或百分比）
x = data_china.index.astype('str') # 将日期数据转换为文本型
y = data_china['确诊']

bar1.add('确诊', x, y, is_datazoom_show=True, datazoom_type='both', 
         is_datazoom_extra_show=True, tooltip_trigger='axis', tooltip_axispointer_type='cross')
bar1

bar2 = pe.Bar('全国治愈与死亡数据', title_pos='right')
x = data_china.index.astype('str')
y1 = data_china['治愈']
y2 = data_china['死亡']

bar2.add('治愈', x, y1, is_stack=True)
bar2.add('死亡', x, y2, is_stack=True)
bar2

bar3 = pe.Bar('湖北省现存病例数量变化')
x = data_hb.index.astype('str')
y = data_hb['现存']

bar3.add('现存', x, y, is_convert=True)
bar3
