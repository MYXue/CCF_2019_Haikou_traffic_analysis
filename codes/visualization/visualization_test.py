# -*- coding: utf-8 -*
"""
2019-10-18
pyecharts 画图尝试
"""

# ========== 一个最基本的柱状图可视化 ==========
# import pyecharts
# from pyecharts.charts import Bar
# from pyecharts import options as opts
# # V1 版本开始支持链式调用
# # 你所看到的格式其实是 `black` 格式化以后的效果
# # 可以执行 `pip install black` 下载使用
# # 不习惯链式调用的开发者依旧可以单独调用方法
# bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# bar.set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
# html_file = 'bar_v2.html'
# bar.render(html_file)

# ========== 一个基本坐标系的可视乎 ==========
# from pyecharts.faker import Collector, Faker
# from pyecharts import options as opts
# from pyecharts.charts import Geo
# from pyecharts.globals import ChartType, SymbolType
# def geo_base() -> Geo:
#     c = (
#         Geo()
#         .add_schema(maptype="海口")
#         # .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
#         .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#         .set_global_opts(
#             visualmap_opts=opts.VisualMapOpts(),
#             title_opts=opts.TitleOpts(title="Geo-基本示例"),
#         )
#     )
#     c.add_coordinate("海南海口秀英秀英向荣", 110.263727, 20.001732)
#     c.add_coordinate("海南海口龙华海垦海秀", 110.328492, 20.031007)
#     c.add("geo", [['海南海口秀英秀英向荣', 100], ['海南海口龙华海垦海秀', 50]])
#     return c

# #可视化
# geo = geo_base()
# geo.render( 'haikou.html')

Baidu_AK = "nglMpYVKorG0aVPcom2BLWsemWbQ7P39"
# ========== 一个百度地图的尝试 ==========
from pyecharts.charts import BMap
from pyecharts.faker import Collector, Faker
from pyecharts import options as opts
import os,json
from pyecharts.globals import BMapType, ChartType

def bmap_heatmap() -> BMap:
    c = (
        BMap()
        .add_schema(baidu_ak=Baidu_AK, center=[110.3014600000, 20.0132350000], zoom=13)  #缩放比例12-14之间可行
        .set_global_opts(
            title_opts=opts.TitleOpts(title="BMap-热力图"),
            visualmap_opts=opts.VisualMapOpts(),
        )
    )
    # 增加坐标点
    c.add_coordinate("海南海口秀英秀英向荣", 110.263727, 20.001732)
    c.add_coordinate("海南海口龙华海垦海秀", 110.328492, 20.031007)

    # 增加坐标点之间的值
    c.add(
            "bmap",
            [['海南海口秀英秀英向荣', 100], ['海南海口龙华海垦海秀', 50]],
            type_="heatmap",
            label_opts=opts.LabelOpts(formatter="{b}"),
        )
    return c

#可视化
geo = bmap_heatmap()
geo.render( 'china_bmap.html')