# -*- coding: utf-8 -*
"""
2019-11-18
pyecharts 画热力图
展示各poi类型在地图上的位置
"""
import sys
sys.path.append('../')
from util_data_load_dump import load_data_of, get_datda_near
from data_statistic import gcj02_to_bd09
import json
import pandas as pd

from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import BMapType, ChartType, ThemeType
Baidu_AK = "EHuurxP38XIGCpLjqVP0cgze5vErTzz6"

## 指定读入文件位置
READ_FILE_PATH = 'D:/CCF2019/data/haikou_poi/'
READ_FILE_NAME = 'haikou_poi' + '.txt'

## 各个一级poi类别和对应的系列名
POI_1_NAME_DICT = {'购物服务':'购物', '餐饮服务':'餐饮', '生活服务':'生活',
                    '公司企业':'公司', '商务住宅':'住宅', '住宿服务':'酒店',
                    '科教文化服务':'教育', '医疗保健服务':'医疗', '政府机构及社会团体':'机构'}
# POI_1_NAME_DICT = {'购物服务':'购物'}

def get_index_of_postion(df):
    position_dict = {}
    for index, row in df.iterrows():
        position_dict[row['name']] = [row['lng'], row['lat']]
    return position_dict

def get_diff_poi_index(df):
    '''
    找到不同类别poi对应的地点name, 数量全部置1
    每个系列都是[[name, 1]..]格式
    '''
    result_dict = {}
    for name, label in POI_1_NAME_DICT.items():
        result_dict[label] = []

    for index, row in df.iterrows():
        if row['poi_1'] in POI_1_NAME_DICT.keys():
            label = POI_1_NAME_DICT[row['poi_1']]
            result_dict[label].append([row['name'],1])

    return result_dict


def draw_heatmap(index_lngLat, index_value):
    def bmap_heatmap() -> BMap:
        c = (
            BMap(init_opts = opts.InitOpts(theme = "white", width="1000px", height="600px"))
            .add_schema(baidu_ak=Baidu_AK, center=[110.3131940000, 20.0274250000], zoom=13)  #缩放比例12-14之间可行
            .set_global_opts(
                title_opts=opts.TitleOpts(title="POI分布"),  # 更改title====================
                visualmap_opts=opts.VisualMapOpts(pos_top='5%', pos_right='5%')
            )
        )
        # 增加坐标点信息
        for key, value in index_lngLat.items():
            c.add_coordinate(key, value[0], value[1])

        # # 不同类数据的点图
        # for label, data in index_value.items():
        #     c.add(
        #             label,
        #             data,
        #             type_="scatter",
        #             symbol_size=3,
        #             # color='rgb(1, 1, 1)',
        #             # itemstyle_opts= opts.ItemStyleOpts(color='rgb(1, 1, 1)'),
        #             label_opts=opts.LabelOpts(is_show=False),
        #         )

        # 不同类数据的热力图
        for label, data in index_value.items():
            c.add(
                    label,
                    data,
                    type_="heatmap",
                    label_opts=opts.LabelOpts(formatter="{b}"),
                )

        c.add_control_panel(navigation_control_opts=opts.BMapNavigationControlOpts(offset_height=30),
                            scale_control_opts=opts.BMapScaleControlOpts(),
                            )
        return c

    #可视化
    geo = bmap_heatmap()
    geo.render( 'heat_bmap.html')


if __name__ == '__main__':
    poi_file = READ_FILE_PATH + READ_FILE_NAME
    df = pd.read_table(poi_file, encoding='gbk')
    df['poi_1'] = df['type'].apply(lambda s: s.split(';')[0])

    ## 需要对经纬度坐标进行一下纠偏
    df['lng'] = df.apply(lambda row: gcj02_to_bd09(row['lng'], row['lat'])[0], axis=1)
    df['lat'] = df.apply(lambda row: gcj02_to_bd09(row['lng'], row['lat'])[1], axis=1)

    # 生成各位置对应index
    position_dict = get_index_of_postion(df)

    # 统计不同类别的poi的位置和数量, 系列和对应的数据
    poi_1_index_value = get_diff_poi_index(df)
    
    draw_heatmap(position_dict, poi_1_index_value)
