# -*- coding: utf-8 -*
"""
2019-11-25
对出行距离、接单时间和出行时间的展示
"""
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from stack_data_make import get_stack_data

# 一个标记24个小时的字符串label
hour_24_list = []
for hour in range(24):
    hour_24_list.append(str(hour)+ ':00' + '-' + str(hour+1) + ':00')


def overlap_bar_line(date, data) -> Bar:
    distance_data = data['distance']
    wait_time_data = data['wait_time']
    normal_time_data = data['normal_time']

    for key, value in data.items():
        '''
        对三类数据分别画图
        '''
        if key == 'distance':
            y1_label = '占比'
            y2_label = '平均行程距离'
            mark = 'km'
            title = date + ' 订单行程距离'
            html = 'distance_stack' + '.html'
        elif key == 'wait_time':
            y1_label = '占比'
            y2_label = '乘客等待时间'
            mark = '分钟'
            title = date + ' 乘客等待时间'
            html = 'wait_time_stack' + '.html'
        elif key == 'normal_time':
            y1_label = '占比'
            y2_label = '乘车时间'
            mark = '分钟'
            title = date + ' 行程时间'
            html = 'normal_time_stack' + '.html'

        bar_data = value['bar_data']
        line_data = value['line_data']

        bar = (
            Bar(init_opts = opts.InitOpts(theme=ThemeType.DARK, width="1000px", height="600px"))
            .add_xaxis(hour_24_list))

        # print(bar_data)
        for key, value in bar_data.items():
            bar.add_yaxis(key, value, stack='a')

        bar.extend_axis(
            yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} "+mark), interval=1
            )
        )
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value}"+" %")
            ),
        )
        

        line = Line().add_xaxis(hour_24_list).add_yaxis(y2_label, line_data, yaxis_index=1)
        bar.overlap(line)
    
        bar.render(html)

if __name__ == '__main__':
    # 指定时间
    date = '2017-09-20'

    # 读取数据
    data = get_stack_data(date)

    overlap_bar_line(date, data)