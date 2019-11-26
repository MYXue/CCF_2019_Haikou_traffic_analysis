# -*- coding: utf-8 -*
"""
2019-10-05
加载数据的工具函数
"""

DATA_PATH = "D:/CCF2019/data/processed_data/"
DATA_FILTERED_FILE = "extracted_11_features_of_merged_data_filtered.csv"
FILTERED_DATA = DATA_PATH + DATA_FILTERED_FILE

POI_POSITION_DIR = 'D:/CCF2019/data/' + 'POI_lng_lat.csv'

import datetime
import numpy as np
import pandas as pd
from collections import Counter
# pandas打印设置
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为10，默认为50
pd.set_option('max_colwidth',20)
# 打印时每行显示长度
pd.set_option('display.width', 140)


def parse_time(timeStrs):
    '''
    时间数据格式，注意异常数据的处理
    '''
    if str(timeStrs) == "0000-00-00 00:00:00":
        return np.nan
    else:
        return datetime.datetime.strptime(str(timeStrs), "%Y-%m-%d %H:%M:%S")

def load_data(file=FILTERED_DATA, columns=None, rows=None):
    df = pd.read_csv(file, nrows=rows, usecols=columns)
    return df

def load_data_of(file=FILTERED_DATA, columns=None, dates=None, time_interval=None, rows=None):
    '''
    根据指定的日期和时间段提取指定区间的数据
    只有这个函数做了出发到达时间矫正！！
    '''
    df = pd.read_csv(file, usecols=columns, nrows=rows)

    if dates == None:
        dates = ['2017-05-01', '2017-11-01']
    if time_interval == None:
        time_interval = [0,24]

    date_begin = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
    date_end = datetime.datetime.strptime(dates[1], '%Y-%m-%d') + datetime.timedelta(days=1)  # 到之后一天的0点

    time_begin = time_interval[0]
    time_end = time_interval[1]

    # 根据时长对出发到达时间做矫正
    df['departure_time'] = df['departure_time'].apply(parse_time)
    df['arrive_time'] = df['arrive_time'].apply(parse_time)
    print("len before drop", len(df))
    df.dropna(subset=['departure_time','arrive_time'],inplace=True)  
    print("len after drop", len(df))
    df['departure_time'] = df['arrive_time']
    df['arrive_time'] =df.apply(lambda row: row['departure_time'] + datetime.timedelta(minutes=row['normal_time']), axis=1)

    # 先提取对应的天的
    df = df[(df['departure_time'] >= date_begin) & (df['departure_time'] < date_end)]
    # 再抽取对应的时间段的
    df['departure_time_hour'] = df['departure_time'].apply(lambda x: x.hour)
    df = df[(df['departure_time_hour'] >= time_begin) & (df['departure_time_hour'] < time_end)]
    del df['departure_time_hour']
    return df


def select_df_of(df, dates=None, time_interval=None):
    '''
    这里是根据读取的df的时间区间直接提取，没有做时间的矫正
    '''
    if dates == None:
        dates = ['2017-05-01', '2017-10-31'] # 这代表包含10月31号
    if time_interval == None:
        time_interval = [0,24] # 这代表0到24时之间的不包含24

    date_begin = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
    date_end = datetime.datetime.strptime(dates[1], '%Y-%m-%d') + datetime.timedelta(days=1)  # 到之后一天的0点

    time_begin = time_interval[0]
    time_end = time_interval[1]

    # 先提取对应的天的
    df['departure_time'] = df['departure_time'].apply(parse_time)
    if 'arrive_time' in df.columns.values:
        df['arrive_time'] = df['arrive_time'].apply(parse_time)  
    df = df[(df['departure_time'] >= date_begin) & (df['departure_time'] < date_end)]
    # 再抽取对应的时间段的
    df['departure_time_hour'] = df['departure_time'].apply(lambda x: x.hour)
    df = df[(df['departure_time_hour'] >= time_begin) & (df['departure_time_hour'] < time_end)]  # 小于这个时间的
    del df['departure_time_hour']
    return df


def get_datda_near(df, position='海口美兰机场', key='DEPARTURE'):
    '''
    返回出发点或到达点在某个地点附近的数据
    '''
    poi_dict = load_poi_position()
    center_lng = poi_dict[position][0]
    center_lat = poi_dict[position][1]

    # 选择距离center上下左右经纬度只差分别为 lag 的距离
    if position in ('海口美兰机场'):
        tag = 0.008  # 对应在地图上大约800+米
    elif position in ('海口骑楼小吃街'):
        tag = 0.002
    else:
        tag = 0.004

    if key == 'DEPARTURE':
        df_select = df[(df['starting_lng']<center_lng+tag) & (df['starting_lng']>center_lng-tag) & (df['starting_lat']<center_lat+tag) & (df['starting_lat']>center_lat-tag)]
    elif key == 'ARRIVE':
        df_select = df[(df['dest_lng']<center_lng+tag) & (df['dest_lng']>center_lng-tag) & (df['dest_lat']<center_lat+tag) & (df['dest_lat']>center_lat-tag)]

    return df_select

def load_poi_position():
    POI_POSITION_DICT = {}
    df = pd.read_csv(POI_POSITION_DIR)
    for index, row in df.iterrows():
        POI_POSITION_DICT[row['name']] = [float(row['lng']), float(row['lat'])]
    # for key, value in POI_POSITION_DICT.items():
    #     print(key, value)
    return POI_POSITION_DICT

if __name__ == '__main__':
    # file = DATA_PATH + DATA_FILTERED_FILE
    # # df = load_data(rows=5, columns=['dest_lng', 'dest_lat', 'starting_lng', 'starting_lat'])
    # # print(df.columns.values)
    # # # print(df)

    # df = load_data_of(dates=['2017-05-19', '2017-05-20'], time_interval=[0,24], rows=100000,
    #                   columns=['order_id', 'departure_time', 'dest_lng', 'dest_lat', 'starting_lng', 'starting_lat'])
    # print(df.columns.values)
    # print(df.shape)
    # # print(df)
    # # print(len(pd.unique(df[['starting_lat', 'dest_lat']].values.ravel())))
    # # print(len(pd.unique(df[['starting_lng', 'dest_lng']].values.ravel())))
    # # print(len(pd.unique(df[['order_id']].values.ravel())))

    # df = get_datda_near(df)
    # print(df.columns.values)
    # print(df.shape)

    df = load_data(rows=10)
    df['departure_time'] = df['departure_time'].apply(parse_time)
    print(df)





