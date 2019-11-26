# -*- coding: utf-8 -*
"""
2019-11-23
造数据，为了画随时间变化的热力图
"""
import sys
sys.path.append('../')
from util_data_load_dump import select_df_of
from data_statistic import gcj02_to_bd09
from heat_map import get_position_count, get_index_of_postion
import pandas as pd
import random
import datetime

# pandas打印设置
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为20，默认为50
pd.set_option('max_colwidth',20)
# 打印时每行显示长度
pd.set_option('display.width', 140)

def data_maker(select='2017-09-20'):
    '''
    指定日期，返回这天各小时的热点位置、订单数、订单距离、时间等数据
    '''
    data_dir = 'D:/CCF2019/data/selected_data/'
    date_select = datetime.datetime.strptime(select, '%Y-%m-%d')
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

    # 读取对应的文件
    df = pd.read_csv(data_dir + file, parse_dates=['arrive_time', 'departure_time'])
    print("read file done")
    # print(df.head())

    # 先读取对应日的数据
    df = select_df_of(df, dates=[select, select], time_interval=[0,24]) # 只选择一整天的数据
    print("select data done")

    # 对数据格式进行一些修正, 对经纬度进行一些纠偏
    df['starting_lng'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[0], axis=1)
    df['starting_lat'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[1], axis=1)
    df['dest_lng'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[0], axis=1)
    df['dest_lat'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[1], axis=1)

    # 将数据按照小时分组，并依次统计各项数据
    position_list = []
    position_count_list = []
    # 遍历24个小时找结果
    for i in range(24):
        sub_df = df[df['departure_time'].dt.hour == i]
        
        # 每小时热力图, 生成各位置对应index
        position_dict = get_index_of_postion(sub_df)
        # 统计各位置分别的出发数量和到达数量
        departure_count, arrive_count = get_position_count(sub_df)
        index_value = [departure_count, arrive_count]
        position_list.append(position_dict)
        position_count_list.append(index_value)

    print("returned made data")
    return position_list, position_count_list

if __name__ == '__main__':
    # date = '2017-09-20'
    # data_maker(date)

    data_dir = 'D:/CCF2019/data/selected_data/'
    file = 'DAY_WEEKDAY_0920.csv'
    df = pd.read_csv(data_dir + file, parse_dates=['arrive_time', 'departure_time'])
    print("read file done")
    print("before drop duplicate：", len(df))
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    print("after drop duplicate：", len(df))