# -*- coding: utf-8 -*
"""
2019-11-23
pyecharts grid 布局改变尝试
"""
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Pie

bar1 = (
    Bar()
    .add_xaxis(Faker.choose())
    .add_yaxis("商家A", Faker.values(), stack="stack1")
    .add_yaxis("商家B", Faker.values(), stack="stack1")
    .set_global_opts(title_opts=opts.TitleOpts(title="Grid-Bar"))
)
bar2 = (
    Bar()
    .add_xaxis(Faker.choose())
    .add_yaxis("商家C", Faker.values(), stack="stack2")
    .add_yaxis("商家D", Faker.values(), stack="stack2")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Grid-Line", pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%"),
    )
)

c = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(Faker.choose(), Faker.values())],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-Radius"),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_top="15%", pos_left="2%"
        ),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

grid = (
    Grid()
    .add(bar1, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(c, grid_opts=opts.GridOpts(pos_top="60%"))
)
grid.render('grid.html')