# -*- coding: utf-8 -*
"""
2019-11-18
根据日期和天气, 对每天的订单量进行预测
"""

from visualization_update.data_maker import data_maker

import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list = data_maker()

# for a,b,c in zip(date_list, dayly_count_list,weather_list):
#     print(a,b,c)


## 如果要加入天气影响，需要根据天气情况描述给这个变量赋值


## 先尝试ARIMA回归
# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)
 
# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))
print(pdq)
 
# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print(seasonal_pdq)

