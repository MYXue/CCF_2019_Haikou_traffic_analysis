# -*- coding: utf-8 -*
"""
2019-10-21
pyecharts 画热力图
展示某一时间段城市整体的交通热度情况，可以将出发点和到达点用不同颜色的点分开
注意去掉原点上的标签，可以调整原点的大小
"""
import sys
sys.path.append('../')
from util_data_load_dump import load_data_of, get_datda_near
from data_statistic import gcj02_to_bd09
import json

from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import BMapType, ChartType, ThemeType
from map_style import get_map_style
Baidu_AK = "EHuurxP38XIGCpLjqVP0cgze5vErTzz6"

def get_index_of_postion(df):
    position_dict = {}
    for index, row in df.iterrows():
        position_dict[(row['starting_lng'], row['starting_lat'])] = [row['starting_lng'], row['starting_lat']]
        position_dict[(row['dest_lng'], row['dest_lat'])] = [row['dest_lng'], row['dest_lat']]
    return position_dict


def get_position_count(df):
    '''
    分别返回出发点和到达各点的统计数量
    '''
    departure_position_count = {}
    arrive_position_count = {}
    for index, row in df.iterrows():
        departure_position_count[(row['starting_lng'], row['starting_lat'])] = departure_position_count.get((row['starting_lng'], row['starting_lat']),0) + 1
        arrive_position_count[(row['dest_lng'], row['dest_lat'])] = arrive_position_count.get((row['dest_lng'], row['dest_lat']), 0) + 1

    departure_count = []
    for key, value in departure_position_count.items():
        departure_count.append([key, value])
    arrive_count = []
    for key, value in arrive_position_count.items():
        arrive_count.append([key, value])

    return departure_count, arrive_count

def bmap_heatmap(index_lngLat, index_value, title='', width="1000px", height="600px") -> BMap:
    c = (
        BMap(init_opts = opts.InitOpts(theme = "white", width=width, height=height))
        # .add_schema(baidu_ak=Baidu_AK, center=[110.3131940000, 20.0274250000], zoom=13, map_style=get_map_style())  #缩放比例12-14之间可行
        .add_schema(baidu_ak=Baidu_AK, center=[110.3131940000, 20.0274250000], zoom=13)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title), 
            visualmap_opts=opts.VisualMapOpts(pos_top='5%', pos_right='5%')
        )
    )
    # 增加坐标点信息
    for key, value in index_lngLat.items():
        c.add_coordinate(key, value[0], value[1])

   # 热力图
    c.add(
            "出发地热力图",
            index_value[0],
            type_="heatmap",
            label_opts=opts.LabelOpts(formatter="{b}"),
        )

    # 点图
    c.add(
            "出发地位置",
            index_value[0],
            type_="scatter",
            symbol_size=3,
            # color='rgb(1, 1, 1)',
            # itemstyle_opts= opts.ItemStyleOpts(color='rgb(1, 1, 1)'),
            label_opts=opts.LabelOpts(is_show=False),
        )
    # 热力图
    c.add(
            "到达地热力图",
            index_value[1],
            type_="heatmap",
            label_opts=opts.LabelOpts(formatter="{b}"),
        )

     # 点图
    c.add(
            "到达地位置",
            index_value[1],
            type_="scatter",
            symbol_size=3,
            label_opts=opts.LabelOpts(is_show=False),
        )


    c.add_control_panel(navigation_control_opts=opts.BMapNavigationControlOpts(offset_height=30),
                        scale_control_opts=opts.BMapScaleControlOpts(),
                        )
    return c

def draw_heatmap(index_lngLat, index_value, title='', width="1000px", height="600px"):
    #可视化
    geo = bmap_heatmap(index_lngLat, index_value, title=title, width="1000px", height="600px")
    geo.render( 'heat_bmap.html')


if __name__ == '__main__':
    data_file = "D:/CCF2019/data/selected_data/" + "DAY_WEEKEND_1014" + ".csv"  # 选择数据======================
    date_imterval = ['2017-10-14', '2017-10-14']  #  选择时间===========================
    time_interval = [22, 24]  #  选择时间===========================
    title = "10/14 周六 22:00-24:00"   # 更改title====================

    df = load_data_of(file=data_file,
                      dates=date_imterval, time_interval=time_interval,
                      columns=['order_id', 'departure_time', 'arrive_time', 'dest_lng', 'dest_lat', 'starting_lng', 'starting_lat','normal_time'])
    # print(df)
    print(df.shape)
    print(df.columns)

    ## 需要对经纬度坐标进行一下纠偏
    df['starting_lng'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[0], axis=1)
    df['starting_lat'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[1], axis=1)
    df['dest_lng'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[0], axis=1)
    df['dest_lat'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[1], axis=1)
    # print(df.head())


    # df = get_datda_near(df, position='海口美兰机场', key='ARRIVE')
    # print(df.shape)

    # 生成各位置对应index
    position_dict = get_index_of_postion(df)

    # 统计各位置分别的出发数量和到达数量
    departure_count, arrive_count = get_position_count(df)
    index_value = [departure_count, arrive_count]
    draw_heatmap(position_dict, index_value, title=title)
