# -*- coding: utf-8 -*
"""
2019-10-24
采用时间线轮播的方式展示每天数据量及分时数据量
"""
# import sys
# sys.path.append('../')
# from util_data_load_dump import load_data_of
# import json
# from crawl_routes import get_route_list

# from pyecharts.charts import BMap
from data_maker import data_maker, data_faker
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Grid, Timeline, Line

date_list = []  # 日期list, 字符串格式
dayly_count_list = []  # 每天的数量count
hour_24_list = []  # 一个24位的list，'0-1时'
hourly_count_list = []  # 一个184*24的list
weather_list = []  # 每天的天气状况

for hour in range(24):
    hour_24_list.append(str(hour)+ ':00' + '-' + str(hour+1) + ':00')

KEY_WORD = None
date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list = data_maker(select=KEY_WORD)

def get_chart_of_date(date):
    #  一个只标注出对应日期，其他是空字符串的list
    date_mark = [0]*len(date_list)
    date_mark[date_list.index(date)] = dayly_count_list[date_list.index(date)]
    # print(date_mark)
    line_chart = (Line()
                    .add_xaxis(date_list)
                    .add_yaxis("", dayly_count_list, linestyle_opts=opts.LineStyleOpts(width=3))
                    .add_yaxis("", date_mark, markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max')]))
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    .set_global_opts(title_opts=opts.TitleOpts(title='2017年海口市5至10月正常天气滴滴每日出行总量', pos_top='50%'))
                    )

    bar_chart = (Bar()
                    .add_xaxis(xaxis_data=hour_24_list)
                    .add_yaxis(series_name='', yaxis_data=hourly_count_list[date_list.index(date)],
                                label_opts=opts.LabelOpts(is_show=True, position='top', formatter='{c}'),)
                    .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True)),
                                     yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True)),
                                     title_opts=opts.TitleOpts(title=date + '各时段出行量  天气：' + weather_list[date_list.index(date)] + ', ' + weekday_list[date_list.index(date)]))
                    )

    grid = (
            Grid()
            .add(bar_chart, grid_opts=opts.GridOpts(pos_bottom="60%"))
            .add(line_chart, grid_opts=opts.GridOpts(pos_top="60%"))
        )

    return grid


def draw_time_line():
    time_line = Timeline(init_opts=opts.InitOpts(width='1000px', height='600px',
                                                theme=ThemeType.DARK))

    for date_i in date_list:
        date_i_chart = get_chart_of_date(date_i)
        time_line.add(date_i_chart, time_point=date_i)

    time_line.add_schema(
        axis_type= "category",
        orient='horizontal',
        symbol='arrow',
        is_auto_play=True,
        is_inverse=False,
        play_interval=2000,
        pos_left='null',
        pos_right='null',
        pos_top='null',
        pos_bottom='10',
        height='40',
        label_opts=opts.LabelOpts(is_show=False, color='#fff'))

    return time_line

if __name__ == '__main__':
    # 每天对应的数据可以设置成全局变量
    #可视化
    time_line = draw_time_line()
    time_line.render( 'time_line.html')