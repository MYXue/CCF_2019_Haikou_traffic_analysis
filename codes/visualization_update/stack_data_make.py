# -*- coding: utf-8 -*
"""
2019-11-25
画bar_line overlap图需要的数据
"""
import pickle
import datetime
import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from util_data_load_dump import select_df_of

# 订单数据（从原始数据中挑选出来的一些对应日期的数据集）
ORDER_DATA_DIR = 'D:/CCF2019/data/selected_data/'

def distance_statistc(nums):
    '''
    划分行程距离的几个分界线
    0-5km, 5-10km, 10-15km, 15km以上
    '''
    km_0_5 = 0
    km_5_10 = 0
    km_10_15 = 0
    km_15 = 0
    for n in nums:
        if n >= 0 and n < 5000:
            km_0_5 += 1
        elif n >= 5000 and n < 10000:
            km_5_10 += 1
        elif n >= 10000 and n < 15000:
            km_10_15 += 1
        else:
            km_15 += 1

    km_0_5 = round(km_0_5/len(nums)*100)
    km_5_10 = round(km_5_10/len(nums)*100)
    km_10_15 = round(km_10_15/len(nums)*100)
    km_15 = max(100 - km_0_5 - km_5_10 - km_10_15, 0)

    return ([['0-5km', km_0_5], ['5-10km', km_5_10], ['10-15km', km_10_15], ['15km以上', round(km_15)]], round(np.mean(nums)/1000, 2))

def wait_time_statistic(nums):
    '''
    划分接单时间的几个分界线
    1分钟以内，1-3分钟，3-5分钟，5-8分钟，8分钟以上
    '''
    wait_1 = 0
    wait_1_3 = 0
    wait_3_5 = 0
    wait_5_8 = 0
    wait_8 = 0
    for n in nums:
        if n >= 0 and n < 1:
            wait_1 += 1
        elif n >= 1 and n < 3:
            wait_1_3 += 1
        elif n >= 3 and n < 5:
            wait_3_5 += 1
        elif n >= 5 and n < 8:
            wait_5_8 += 1
        else:
            wait_8 += 1

    wait_1 = round(wait_1/len(nums)*100)
    wait_1_3 = round(wait_1_3/len(nums)*100)
    wait_3_5 = round(wait_3_5/len(nums)*100)
    wait_5_8 = round(wait_5_8/len(nums)*100)
    wait_8 = max(100 - wait_1 - wait_1_3 - wait_3_5 - wait_5_8, 0)
    return ([['1分钟以内', wait_1], ['1-3分钟', wait_1_3], ['3-5分钟', wait_3_5], ['5-8分钟', wait_5_8], ['8分钟以上', wait_8]], round(np.mean(nums), 2))

def normal_time_statistic(nums):
    '''
    划分乘车时间的几个分界线
    0-8分钟、8-15分钟、15-25分钟、25-40分钟、40分钟以上
    '''
    normal_8 = 0
    normal_8_15 = 0
    normal_15_25 = 0
    normal_25_40 = 0
    normal_40 = 0
    for n in nums:
        if n >= 0 and n < 8:
            normal_8 += 1
        elif n >= 8 and n < 15:
            normal_8_15 += 1
        elif n >= 15 and n < 25:
            normal_15_25 += 1
        elif n >= 25 and n < 40:
            normal_25_40 += 1
        else:
            normal_40 += 1

    normal_8 = round(normal_8/len(nums)*100)
    normal_8_15 = round(normal_8_15/len(nums)*100)
    normal_15_25 = round(normal_15_25/len(nums)*100)
    normal_25_40 = round(normal_25_40/len(nums)*100)
    if (normal_8 + normal_8_15 + normal_15_25 + normal_25_40) > 100:
        normal_25_40 -= 1
    normal_40 = max(100 - normal_8 - normal_8_15 - normal_15_25 - normal_25_40, 0)
    return ([['8分钟以内', normal_8], ['8-15分钟', normal_8_15], ['15-25分钟', normal_15_25], ['25-40分钟', normal_25_40], ['40分钟以上', normal_40]], round(np.mean(nums), 2))


def get_order_file(date):
    '''
    根据所选日期判断文件的名称
    '''
    date_select = datetime.datetime.strptime(date, '%Y-%m-%d')
    if date_select == datetime.datetime.strptime('2017-10-17', '%Y-%m-%d'):
        file = 'DAY_BAD_WEATHER_1017.csv'
    elif date_select == datetime.datetime.strptime('2017-09-20', '%Y-%m-%d'):
        file = 'DAY_WEEKDAY_0920.csv'
    elif date_select == datetime.datetime.strptime('2017-10-14', '%Y-%m-%d'):
        file = 'DAY_WEEKEND_1014.csv'
    elif date_select >= datetime.datetime.strptime('2017-05-01', '%Y-%m-%d') and date_select <= datetime.datetime.strptime('2017-05-07', '%Y-%m-%d'):
        file = 'WEEK_5_1.csv'
    elif date_select >= datetime.datetime.strptime('2017-10-01', '%Y-%m-%d') and date_select <= datetime.datetime.strptime('2017-10-07', '%Y-%m-%d'):
        file = 'WEEK_10_1.csv'
    elif date_select >= datetime.datetime.strptime('2017-06-12', '%Y-%m-%d') and date_select <= datetime.datetime.strptime('2017-06-18', '%Y-%m-%d'):
        file = 'WEEK_IN_WORK_0612_0618.csv'
    elif date_select >= datetime.datetime.strptime('2017-06-01', '%Y-%m-%d') and date_select <= datetime.datetime.strptime('2017-06-30', '%Y-%m-%d'):
        file = 'MONTH_06.csv'
    return file

def get_order_data(date):
    '''
    得到指定日期的24小时订单详情数据
    包括每小时订单量，乘车距离、接单时间、乘车时间的分布情况
    '''
    file = get_order_file(date)  # 根据指定日期决定数据文件

    # 读取对应的文件
    df = pd.read_csv(ORDER_DATA_DIR + file, parse_dates=['arrive_time', 'departure_time'])  # 将时间列以时间格式读入
    print("read order file done")
    # print(df.head())

    # 先读取对应日的数据
    df = select_df_of(df, dates=[date, date], time_interval=[0,24]) # 只选择一整天的数据
    print("select order data done")

    # 将数据按照小时分组，并依次统计各项数据
    distanceNum_list = []
    waitTimeNum_list = []
    normalTimeNum_list = []

    # 遍历24个小时找结果
    for i in range(24):
        sub_df = df[df['departure_time'].dt.hour == i]

        # 饼图需要的数据统计
        distanceNum_list.append(distance_statistc(sub_df['start_dest_distance']))
        waitTimeNum_list.append(wait_time_statistic(sub_df['time_diff_in_minutes']))
        normalTimeNum_list.append(normal_time_statistic(sub_df['normal_time']))

    distance = {}
    distance['bar_data'] = {}
    distance['line_data'] = []
    for distanceNum, avg in distanceNum_list:
        distance['line_data'].append(avg)
        for [name, num] in distanceNum:
            distance['bar_data'][name] = distance['bar_data'].get(name, [])
            distance['bar_data'][name].append(num)

    wait_time = {}
    wait_time['bar_data'] = {}
    wait_time['line_data'] = []
    for wait_timeNum, avg in waitTimeNum_list:
        wait_time['line_data'].append(avg)
        for [name, num] in wait_timeNum:
            wait_time['bar_data'][name] = wait_time['bar_data'].get(name, [])
            wait_time['bar_data'][name].append(num)

    normal_time = {}
    normal_time['bar_data'] = {}
    normal_time['line_data'] = []
    for normal_timeNum, avg in normalTimeNum_list:
        normal_time['line_data'].append(avg)
        for [name, num] in normal_timeNum:
            normal_time['bar_data'][name] = normal_time['bar_data'].get(name, [])
            normal_time['bar_data'][name].append(num)

    print("returned data made from orders")
    return distance, wait_time, normal_time

def get_stack_data(date):
    '''
    date: 字符串格式，形如"2019-10-10"
    返回dict, 包含3类需要的数据
    '''

    distanceNum_list, waitTimeNum_list, normalTimeNum_list = get_order_data(date)

    data_made = {}
    data_made['distance'] = distanceNum_list
    data_made['wait_time'] = waitTimeNum_list
    data_made['normal_time'] = normalTimeNum_list

    return data_made


if __name__ == '__main__':
    date = '2017-09-20'
    data = get_stack_data(date)
    # for key, value in data.items():
    #     print(len(value))
    #     print(key)
    #     print(value)
    #     print("\n")

    for key, value in data.items():
        print(key)
        print(value)
        print("\n")
