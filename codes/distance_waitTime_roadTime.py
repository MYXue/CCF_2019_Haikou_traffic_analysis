# -*- coding: utf-8 -*
"""
2019-11-19
找到每条订单对应的接单时间、道路行驶时间和道路行驶距离
"""
from util_data_load_dump import load_data, parse_time
import pandas as pd
import numpy as np
from collections import Counter
# pandas打印设置
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为10，默认为50
pd.set_option('max_colwidth',100)

# 指定输入文件位置
DATA_PATH = "D:/CCF2019/data/processed_data/"
RAW_DATA_FILE = "extracted_11_features_of_merged_data.csv"
RAW_DATA = DATA_PATH + RAW_DATA_FILE

ADD_DATA_FILE = "extracted_6_type_features_of_merged_data.csv"
ADD_DATA = DATA_PATH + ADD_DATA_FILE

## 指定输出文件位置
OUTPUT_FILE = '../data/processed_data/' + 'distance_time_fee.csv'

## 一些被挑选出来的指定日期的数据
SELECTED_DIR = "D:/CCF2019/data/selected_data/"

def load_joined_date():
    # 读取原始数据中的距离和时间信息
    columns_raw = ['order_id', 'start_dest_distance', 'arrive_time', 'departure_time', 'normal_time']
    df_raw = load_data(RAW_DATA, columns=columns_raw)
    df_raw.drop_duplicates(subset=None, keep='first', inplace=True)
    print(df_raw.columns)
    print(len(df_raw))
    print("\n")
    
    # 读取订单类型和费用信息
    columns_add = ['order_id', 'type','pre_total_fee']
    df_add = load_data(ADD_DATA, columns=columns_add)
    df_add.drop_duplicates(subset=None, keep='first', inplace=True)
    print(df_add.columns)
    print(len(df_raw))
    print("\n")
    
    # join两个表
    df_merged = df_raw.merge(df_add, on='order_id')
    print("after merge")
    print(len(df_merged))
    print(df_merged.head())

    return df_merged

def get_wait_time(row):
    '''
    根据司机出发时间和到达时间计算接单时间（乘客等待时间）
    '''
    if type == 1:
        return 0  # 如果是预约单则认为顾客等待时间为0
    else:
        if row['arrive_time'] == np.nan or row['departure_time'] == np.nan:
            print(row)
            return None
        else:
            time_delta = (row['arrive_time'] - row['departure_time']).seconds / 60
            return round(time_delta, 1)  # 返回格式是保留1位小数的分钟

def merge_and_dump():
    # 合并数据和导出数据
    df = load_joined_date()
    df.to_csv(OUTPUT_FILE, index=False)
    print("output finished")

if __name__ == '__main__':
    # df = load_data(OUTPUT_FILE)
    # print("load df done")
    # df['arrive_time'] = df['arrive_time'].apply(parse_time)
    # df['departure_time'] = df['departure_time'].apply(parse_time)
    # print("time parse done")

    # # 数据中的距离start_dest_distance, 行驶时间normal_time, 预估费用pre_total_fee都可以直接使用
    # # 需要处理的是接单时间, 即顾客等待时间; 以及OD之间的距离（变成千米）
    # df['wait_time'] = df.apply(get_wait_time, axis=1)
    # print("wait time parse done")
    # df['distance'] = df['start_dest_distance'].apply(lambda x: round(x / 1000, 1))
    # print('distance parse done')

    ## 根据输入的日期，以及该天的订单编号，计算该天各个小时的wait_time、start_dest_distance、normal_time的分布
    ## wait_time其实就是之前数据中的time_diff_in_minutes
    # 指定输入的文件 ========================
    file_name = 'DAY_WEEKDAY_0920' + '.csv'
    selected_file =  SELECTED_DIR + file_name
    columns = ['order_id', 'start_dest_distance', 'departure_time', 'normal_time', 'time_diff_in_minutes']
    df_selected = load_data(selected_file,columns=columns, rows=10000)
    print(df_selected.columns)
    df_selected['departure_time'] = df_selected['departure_time'].apply(parse_time)
    df_selected['distance'] = df_selected['start_dest_distance'].apply(lambda x: round(x / 1000, 1))
    print("load selected data done")
    # print(df_selected)

    # 要分析分布的几个变量 wait_time, distance, normal_time
    wait_time_result = df_selected['time_diff_in_minutes'].groupby(by=df_selected['departure_time'].dt.hour).agg(lambda nums: dict(Counter(nums)))
    hour_list = wait_time_result.index.values
    assert len(hour_list) == 24
    wait_time_list = wait_time_result.values.tolist()

    distance_result = df_selected['distance'].groupby(by=df_selected['departure_time'].dt.hour).agg(lambda nums: dict(Counter([round(num) for num in nums])))
    distance_list = distance_result.values.tolist()

    normal_time_result = df_selected['normal_time'].groupby(by=df_selected['departure_time'].dt.hour).agg(lambda nums: dict(Counter(nums)))
    normal_time_list = normal_time_result.values.tolist()

    result_dict = {}
    result_dict['wait_time'] = {}
    result_dict['distance'] = {}
    result_dict['normal_time'] = {}
    for a, b, c, d in zip(hour_list, wait_time_list, distance_list, normal_time_list):
        # print(a, b, c)
        result_dict['wait_time'][a] = b
        result_dict['distance'][a] = c
        result_dict['normal_time'][a] = d

    result_df = pd.DataFrame(result_dict)
    print(result_df['normal_time'])
    # result_df.to_csv("data_dayly_hourly_count.csv")
    # print("load data done")

