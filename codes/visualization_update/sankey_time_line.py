# -*- coding: utf-8 -*
"""
2019-11-21
采用时间线轮播的方式展示每天数据量及分时数据量
"""
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Grid, Timeline, Line, Pie, Sankey, Page
from sankey_data_make import get_sankey_page_date

# 一个标记24个小时的字符串label
hour_24_list = []
for hour in range(24):
    hour_24_list.append(str(hour)+ ':00' + '-' + str(hour+1) + ':00')


def sankey_base(links, title="出发地与到达地附近的地点") -> Sankey:
    nodes = [
        {"name": "出发：餐饮购物生活区附近"},
        {"name": "出发：住宅区附近"},
        {"name": "出发：公司商务区附近"},
        {"name": "出发：其他区域"},
        {"name": "到达：餐饮购物生活区附近"},
        {"name": "到达：住宅区附近"},
        {"name": "到达：公司商务区附近"},
        {"name": "到达：其他区域"},
    ]

    links = links
    c = (
        Sankey(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(
            "",
            nodes,
            links,
            linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
        .set_series_opts(label_opts=opts.LabelOpts(color='white', position='right'))
    )

    return c

def get_pie_radius(label_num_list, title='title_pie', radius=["20%", "40%"]) -> Pie:
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(
            "",
            label_num_list,
            radius=radius,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title, pos_left='center', pos_top='middle', 
                                        title_textstyle_opts=opts.TextStyleOpts(font_size=10)),
            legend_opts=opts.LegendOpts(
                orient="vertical", is_show=False
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c

def get_bar(y_data, time, x_label=hour_24_list, title='title_bar'):
    date_mark = [0] * 24
    date_mark[hour_24_list.index(time)] = y_data[hour_24_list.index(time)]
    b = (Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(xaxis_data=x_label)
        .add_yaxis(series_name='', yaxis_data=y_data,
                    label_opts=opts.LabelOpts(is_show=True, position='top', formatter='{c}', font_size=8),
                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(coord=[x_label[x_label.index(time)], y_data[x_label.index(time)]+200])]))
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True)),
                        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True)),
                        title_opts=opts.TitleOpts(title=title))
                    )
    return b

def get_chart_of(date_str, time_str, sankey_data, orderNums_24, distanceNum, waitTimeNum, normalTimeNum):
    '''
    根据传入的时间取对应的数据画图
    '''
    sankey = sankey_base(sankey_data, title='出发地与到达地附近的地点类型 ' + date_str + ' ' + time_str)
    sankey.chart_id = "sankey_timeline_sankey"
    bar_chart = get_bar(orderNums_24, time_str, title=date_str + ' 每小时订单量')
    bar_chart.chart_id = "sankey_timeline_bar"
    pie_chart_distance = get_pie_radius(distanceNum, title='乘车距离')
    pie_chart_distance.chart_id = "sankey_timeline_pie1"
    pie_chart_wait_time = get_pie_radius(waitTimeNum, title='等待时间')
    pie_chart_wait_time.chart_id = "sankey_timeline_pie2"
    pie_chart_normal_time = get_pie_radius(normalTimeNum, title='乘车时间')
    pie_chart_normal_time.chart_id = "sankey_timeline_pie3"

    page = Page(layout=Page.DraggablePageLayout)
    page.add(sankey, bar_chart, pie_chart_distance, pie_chart_wait_time, pie_chart_normal_time)
    # page.render("page.html")
    return page


def draw_time_line(date, data):
    sankey_data = data['poi_pair']
    orderNums_24 = data['order_num']
    distanceNum_list = data['distance']
    waitTimeNum_list = data['wait_time']
    normalTimeNum_list = data['normal_time']

    # 可视化
    for i in range(24):
        sankey_data_i = sankey_data[i]
        distanceNum_i = distanceNum_list[i]
        waitTimeNum_i = waitTimeNum_list[i]
        normalTimeNum_i = normalTimeNum_list[i]

        hour_i = hour_24_list[i]
        hour_i_chart = get_chart_of(date, hour_i, sankey_data_i, orderNums_24, distanceNum_i, waitTimeNum_i, normalTimeNum_i)
        
        hour = hour_i.split(":")[0]
        hour_i_chart.render('sankey_' + hour + '.html')
        Page.save_resize_html('sankey_' + hour + '.html', cfg_file="chart_config.json", dest=date + '_sankey_' + hour + '.html')


def generate_page_layout(date, data):
    '''
    先生成一个layout
    '''
    # 挑选一个小时的数据先生成layout
    sankey_data = data['poi_pair'][20]
    orderNums_24 = data['order_num']
    distanceNum = data['distance'][20]
    waitTimeNum = data['wait_time'][20]
    normalTimeNum = data['normal_time'][20]

    time_str = hour_24_list[20]
    page = get_chart_of(date, time_str, sankey_data, orderNums_24, distanceNum, waitTimeNum, normalTimeNum)
    page.render('sankey_layout.html')
    Page.save_resize_html("sankey_page_.html", cfg_file="chart_config.json", dest="page_new_charts.html")

if __name__ == '__main__':
    # 指定时间
    date = '2017-09-20'

    # 读取数据
    data = get_sankey_page_date(date)

    # 是否需要传入日期至画图数据中
    # Page无法直接添加到time line上
    draw_time_line(date, data)

    # 生成一个layout之后，之后的相同格式的html都可以套用这个layout格式
    # generate_page_layout(date, data)
    # Page.save_resize_html("sankey_layout.html", cfg_file="chart_config.json", dest="sankey_page_charts.html")

