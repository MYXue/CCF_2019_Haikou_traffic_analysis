# -*- coding: utf-8 -*
"""
2019-10-21
pyecharts 连线图
可以筛选某一时间段内从机场/车站出发的人，或者是到达机场/车站的人，都分别来自哪里
调好df的筛选功能即可，最后生成html文件即可
"""
import sys
sys.path.append('../')
from util_data_load_dump import load_data_of, get_datda_near
import json

from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import BMapType, ChartType, SymbolType

Baidu_AK = "EHuurxP38XIGCpLjqVP0cgze5vErTzz6"

def get_lng_lat_route(df, key='DEPARTURE'):
    result_dict = {}
    route_pair_list = []
    for index, row in df.iterrows():
        result_dict[str(index)+'depa'] = [row['starting_lng'], row['starting_lat']]
        result_dict[str(index)+'arri'] = [row['dest_lng'], row['dest_lat']]
        route_pair_list.append({"coords":[[row['starting_lng'], row['starting_lat']], [row['dest_lng'], row['dest_lat']]],"lineStyle":{"normal":{"color":"rgba(223,90,90,1)"}}})
    return result_dict, route_pair_list

def make_value(index_lngLat):
    '''
    给输入json中的每个点赋值，最后输出成list格式
    '''
    result_list = []
    for key in index_lngLat.keys():
        result_list.append([key, 10])
    return result_list

def draw_linemap(index_lngLat, index_value, route_pair):
    def bmap_linemap() -> BMap:
        c = (
            BMap(init_opts = opts.InitOpts(theme = "white", width="800px", height="600px"))
            .add_schema(baidu_ak=Baidu_AK, center=[110.3131940000, 20.0274250000], zoom=13)  #缩放比例12-14之间可行
            .set_global_opts(
                title_opts=opts.TitleOpts(title="09/20 工作日 机场到达"),  # 更改title====================
                visualmap_opts=opts.VisualMapOpts(),
            )
        )
        # 增加坐标点
        for key, value in index_lngLat.items():
            c.add_coordinate(key, value[0], value[1])

         # 增加坐标点的值
        c.add(
            "",
            index_value,
            type_=ChartType.EFFECT_SCATTER,
            symbol_size=4,
            label_opts=opts.LabelOpts(is_show=False),
            color="white",
        )

        # 增加连线图
        c.add(
            "出行起始位置",
            route_pair,
            type_=ChartType.LINES,
            is_large=True,
            large_threshold=100,
            effect_opts=opts.EffectOpts(
                symbol=SymbolType.ARROW, symbol_size=3, color="blue"
            ),
            linestyle_opts=opts.LineStyleOpts(curve=0.1, opacity=0.7),
        )
        # c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))


        c.add_control_panel(navigation_control_opts=opts.BMapNavigationControlOpts(offset_height=30),
                            scale_control_opts=opts.BMapScaleControlOpts(),)
        return c

    #可视化
    geo = bmap_linemap()
    geo.render( 'line_bmap.html')


if __name__ == '__main__':
    data_file = "D:/CCF2019/data/selected_data/" + "DAY_WEEKDAY_0920" + ".csv"  # 选择数据======================
    date_imterval = ['2017-09-20', '2017-09-20']  #  选择时间===========================
    time_interval = [0, 24]  #  选择时间===========================

    df = load_data_of(file=data_file,
                      dates=date_imterval, time_interval=time_interval,
                      columns=['order_id', 'departure_time', 'arrive_time', 'dest_lng', 'dest_lat', 'starting_lng', 'starting_lat','normal_time'])
    # print(df)
    print(df.shape)

    df = get_datda_near(df, position='海口美兰机场', key='ARRIVE')
    print(df.shape)

    ## 需要对经纬度坐标进行一下纠偏
    df['starting_lng'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[0], axis=1)
    df['starting_lat'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[1], axis=1)
    df['dest_lng'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[0], axis=1)
    df['dest_lat'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[1], axis=1)
    # print(df.head())

    index_lngLat, route_pair = get_lng_lat_route(df)
    # print(index_lngLat)
    # print(route_pair)
    index_value = make_value(index_lngLat)
    # print(index_value)
    draw_linemap(index_lngLat, index_value, route_pair)