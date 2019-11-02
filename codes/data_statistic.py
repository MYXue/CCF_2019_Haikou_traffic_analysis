# -*- coding: utf-8 -*
"""
2019-10-24
对每一天及每小时的数据量进行统计
"""
import pandas as pd
from util_data_load_dump import load_data_of

def select_data_of_date(df):
    '''
    根据输入日期选取对应时间的数据
    '''
    pass

def count_hourly_num(df):
    '''
    从输入的一天的数据中统计出每小时的数据量
    '''
    group_result = df['order_id'].groupby(by=df['departure_time'].dt.hour).count()

    hour_list = group_result.index.values
    # assert len(hour_list) == 24
    # print("len of hour", len(hour_list))
    # print("hour_list", hour_list)
    hourcount_list = group_result.values.tolist()
    return hourcount_list

def count_of_days(df):
    '''
    计算每一天的订单量，输出 日期、 对应订单总量、以及分小时订单量的统计
    '''
    group_result = df['order_id'].groupby(by=df['departure_time'].dt.date).count()
    # print(group_result)
    # print(type(group_result))
    datetime_list = group_result.index.values
    date_list = []
    for item in datetime_list:
        date_list.append(item.strftime('%m/%d'))
    daycount_list = group_result.values.tolist()

    # 对每一天的数据，统计其每小时的数据量
    hourCount_of_days = []
    for date in datetime_list:
        df_i = df[df['departure_time'].dt.date == date]
        hour_count_list = count_hourly_num(df_i)
        hourCount_of_days.append(hour_count_list)
        print(date.strftime('%m/%d') + ' done')
    return date_list, daycount_list, hourCount_of_days


if __name__ == '__main__':
    df = load_data_of(columns=['order_id', 'departure_time'])
    day_list, count_list, hourcount_list = count_of_days(df)
    

    result_dict = {}
    result_dict['day_count'] = {}
    result_dict['hour_count'] = {}
    for a, b, c in zip(day_list, count_list, hourcount_list):
        print(a, b, c)
        result_dict['day_count'][a] = b
        result_dict['hour_count'][a] = c

    result_df = pd.DataFrame(result_dict)
    result_df.to_csv("data_dayly_hourly_count.csv")
    print("load data done")