# -*- coding: utf-8 -*
"""
2019-11-24
画桑基图所需要的数据，包含桑基图poi数据，24小时的订单数量数据，以及三个饼图需要的距离、等待时间和乘车时间的数据
根据输入的时间、返回dict格式的数据
"""
import pickle
import datetime
import pandas as pd
import sys
sys.path.append('../')
from util_data_load_dump import select_df_of
from data_statistic import gcj02_to_bd09

# od_poi_pair文件位置
OD_POI_DIR = 'D:/CCF2019/data/OD_poi_type_counter/'

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
    return [['0-5km', km_0_5], ['5-10km', km_5_10], ['10-15km', km_10_15], ['15km以上', km_15]]

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
    return [['1分钟以内', wait_1], ['1-3分钟', wait_1_3], ['3-5分钟', wait_3_5], ['5-8分钟', wait_5_8], ['8分钟以上', wait_8]]

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
    return [['8分钟以内', normal_8], ['8-15分钟', normal_8_15], ['15-25分钟', normal_15_25], ['25-40分钟', normal_25_40], ['40分钟以上', normal_40]]

def get_sunkey_data(date):
    '''
    得到指定日期的每小时od_pair的对应Poi数据
    '''
    # 读入数据
    counter_f = open(OD_POI_DIR + date, 'rb')
    OD_poi_pair_list = pickle.load(counter_f)

    OD_poi_pair_result = []
    for OD_poi_pair_ in OD_poi_pair_list:
        od_pair_of_i = []
        for key, value in OD_poi_pair_.items():
            od_pair_of_i.append({"source": "出发："+key[0], "target": "到达："+key[1], "value": value})
        OD_poi_pair_result.append(od_pair_of_i)

    return OD_poi_pair_result

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

    # 对数据格式进行一些修正, 对经纬度进行一些纠偏
    df['starting_lng'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[0], axis=1)
    df['starting_lat'] = df.apply(lambda row: gcj02_to_bd09(row['starting_lng'], row['starting_lat'])[1], axis=1)
    df['dest_lng'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[0], axis=1)
    df['dest_lat'] = df.apply(lambda row: gcj02_to_bd09(row['dest_lng'], row['dest_lat'])[1], axis=1)

    # 将数据按照小时分组，并依次统计各项数据
    orderNums_24 = df['order_id'].groupby(by=df['departure_time'].dt.hour).count().tolist()  # 每小时订单数，为了画柱状图
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

    print("returned data made from orders")
    return orderNums_24, distanceNum_list, waitTimeNum_list, normalTimeNum_list

def get_sankey_page_date(date):
    '''
    date: 字符串格式，形如"2019-10-10"
    返回dict, 包含4类需要的数据
    '''
    sankey_data = get_sunkey_data(date)  # 一个长为24的list
    orderNums_24, distanceNum_list, waitTimeNum_list, normalTimeNum_list = get_order_data(date)

    data_made = {}
    data_made['poi_pair'] = sankey_data
    data_made['order_num'] = orderNums_24
    data_made['distance'] = distanceNum_list
    data_made['wait_time'] = waitTimeNum_list
    data_made['normal_time'] = normalTimeNum_list
    return data_made


if __name__ == '__main__':
    date = '2017-09-20'
    data = get_sankey_page_date(date)
    for key, value in data.items():
        print(len(value))
        print(key)
        print(value)
        print("\n")

