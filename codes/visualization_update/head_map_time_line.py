# -*- coding: utf-8 -*
"""
2019-11-21
采用时间线轮播的方式展示每天分时到达和出发的热点图
"""
from heatmap_dataMaker import data_maker
from pyecharts import options as opts
from pyecharts.charts import BMap, Timeline
from pyecharts.globals import BMapType, ChartType, ThemeType
Baidu_AK = "EHuurxP38XIGCpLjqVP0cgze5vErTzz6"

# 一个标记24个小时的字符串label
hour_24_list = []
for hour in range(24):
    hour_24_list.append(str(hour)+ ':00' + '-' + str(hour+1) + ':00')

def bmap_heatmap(index_lngLat, index_value, title='', width="1000px", height="900px") -> BMap:
    c = (
        BMap(init_opts = opts.InitOpts(theme = "white", width=width, height=height))
        .add_schema(baidu_ak=Baidu_AK, center=[110.3131940000, 20.0274250000], zoom=13)  #缩放比例12-14之间可行
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

def get_chart_of_hour(date, hour, position, position_count):
    '''
    根据传入的时间取对应的数据画图
    '''
    title = date + ' ' + hour
    html = date + '_' + hour.split(":")[0] + '_heatMap'
    heat_map = bmap_heatmap(position, position_count, title=title, width="1000px", height="600px" )
    heat_map.render(html + '.html')

def draw_time_line(date, position_list, position_count_list):
    for hour_i, position, position_count in zip(hour_24_list, position_list, position_count_list):
        get_chart_of_hour(date, hour_i, position, position_count)

if __name__ == '__main__':
    # 选择日期
    date = '2017-09-20'
    position_list, position_count_list = data_maker(select=date)  # 返回24个小时内对应的热力点的数据

    # 可视化
    draw_time_line(date, position_list, position_count_list)
