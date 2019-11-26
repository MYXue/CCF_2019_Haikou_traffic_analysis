# -*- coding: utf-8 -*
"""
2019-11-21
尝试画一下桑基图
"""
import json
import os
import pickle
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Page, Sankey

# od_poi_pair文件位置
OD_POI_DIR = 'D:/CCF2019/data/OD_poi_type_counter/'

def sankey_base(links) -> Sankey:
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
        .set_global_opts(title_opts=opts.TitleOpts(title="出发地-到达地位置附近poi + 具体小时"))
        .set_series_opts(label_opts=opts.LabelOpts(color='white', position='right'))
    )

    return c

def get_a_sunkey():
    # 读入数据
    counter_f = open(OD_POI_DIR + '2017-09-20', 'rb')
    OD_poi_pair_ = pickle.load(counter_f)

    OD_poi_pair_ = OD_poi_pair_[0]
    od_poi_result = []
    for key, value in OD_poi_pair_.items():
        print(key, value)
        od_poi_result.append({"source": "出发："+key[0], "target": "到达："+key[1], "value": value})

    sankey = sankey_base(od_poi_result)
    return sankey

if __name__ == '__main__':
    # 读入数据
    counter_f = open(OD_POI_DIR + '2017-09-20', 'rb')
    OD_poi_pair_ = pickle.load(counter_f)

    od_poi_result = []
    for key, value in OD_poi_pair_.items():
        print(key, value)
        od_poi_result.append({"source": "出发："+key[0], "target": "到达："+key[1], "value": value})

    sankey = sankey_base(od_poi_result)
    sankey.render('sankey.html')
