# -*- coding: utf-8 -*
"""
2019-11-25
展示原始订单数据与arima预测数据，以及预测的误差
"""
import pandas as pd
import numpy as np
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

def overlap_bar_line(x_label, true, prediction, MAPE) -> Bar:
    title='根据5-9月订单量预测10月订单量'
    line = (
        Line(init_opts = opts.InitOpts(theme=ThemeType.DARK, width="1000px", height="600px"))
        .add_xaxis(x_label))
    line.add_yaxis('预测量', prediction, linestyle_opts=opts.LineStyleOpts(width = 5, opacity = 0.5))
    line.add_yaxis('真实订单量', true, linestyle_opts=opts.LineStyleOpts(width = 3))

    line.extend_axis(
        yaxis=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"+" %"), interval=5, max_=50
        )
    )
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts()
        ),
    )
    

    bar = Bar().add_xaxis(x_label).add_yaxis('预测误差-MAPE', MAPE, yaxis_index=1).set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    line.overlap(bar)
    
    line.render('arima_prediction.html')

if __name__ == '__main__':
    # 指定文件
    file = 'D:/CCF2019/codes/arima_prediction/' + 'to_draw.csv'

    df = pd.read_csv(file)
    # print(df)

    x_label = df['date'].tolist()
    true = df['day_count'].tolist()
    prediction = df['predict'].apply(lambda x: round(x) if x > 0 else None).tolist()
    MAPE = df['MAPE'].apply(lambda x: round(x*100, 2) if isinstance(x, float) else None).tolist()

    # print(x_label)
    # print(true)
    # print(prediction)
    # print(MAPE)

    overlap_bar_line(x_label, true, prediction, MAPE)
