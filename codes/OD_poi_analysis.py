# -*- coding: utf-8 -*
"""
2019-11-19
对出发点到达点的poi信息进行分析
"""
import pickle
from collections import Counter
import numpy as np
import pandas as pd
from util_data_load_dump import load_data_of, get_datda_near, select_df_of

# pandas打印设置
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为20，默认为50
pd.set_option('max_colwidth',20)
# 打印时每行显示长度
pd.set_option('display.width', 140)

# poi汇总结果-输入文件
POI_RESULT_FILE = '../data/haikou_poi/' + 'position_poi_dict'
f = open(POI_RESULT_FILE, 'rb')
position_poi_dict = pickle.load(f)

# od_poi_pair输出文件位置
OUT_PUT_DIR = 'D:/CCF2019/data/OD_poi_type_counter/'

def poi_data_check():
    ## 检查下数据量比较多的点
    for key, value in position_poi_dict.items():
        if len(value['id']) > 5 and len(value['id']) < 10:
            print(key)
            print(value['poi_1'])
            print(Counter(value['poi_1']).most_common(3))
            print(value['most_poi'])
            print("\n")


def find_near_poi(position):
    '''
    根据输入的经纬度，找到附近所有位置的poi，根据这个汇总的poi给它一个功能定义
    附近的位置定义为上下左右各50米的正方形区域里
    如果附近都没有poi信息则返回None
    '''
    lng, lat = round(position[0], 4), round(position[1], 4)
    poi_list = []
    for lng_ in np.arange(lng - 0.0005, lng + 0.0006, 0.0001):
        for lat_ in np.arange(lat - 0.0005, lat + 0.0006, 0.0001):
            position_ = (round(lng_, 4), round(lat_, 4))
            if position_ in position_poi_dict.keys():
                poi_list += position_poi_dict[position_]['poi_1']

    if poi_list == []:
        return ['其他']  # 当临近的区域内没有poi功能点被找到时
    else:
        result_list = []
        poi_count = Counter(poi_list)
        if len(poi_count) >= 3:  # 如果出现的poi类型大于三个, 只检查前三个
            [first, second, third] = poi_count.most_common(3)
            result_list.append(first[0])
            if (first[1] - second[1]) / first[1] <= 0.25:  # 如果第二多与第一多的差值在第一多的1/4/之内
                result_list.append(second[0])
                if (first[1] - third[1]) / first[1] <= 0.25:
                    result_list.append(third[0])
            if '住宅' in  poi_list and '住宅' not in result_list:
                result_list.append('住宅')
        else:  # 只检查前两个
            if len(poi_count) == 2:
                [first, second] = poi_count.most_common(2)
                result_list.append(first[0])     
                if (first[1] - second[1]) / first[1] <= 0.25:  # 如果第二多与第一多的差值在第一多的1/4/之内
                    result_list.append(second[0])
            else:
                [first] = poi_count.most_common(1) 
                result_list.append(first[0])
            if '住宅' in  poi_list and '住宅' not in result_list:
                result_list.append('住宅')
        
        return result_list

def define_od_poi_pair(O_poi, D_poi):
    '''
    根据O_poi, D_poi生成 poi 对list
    '''
    poi_pair_list = []
    for o_ in O_poi:
        for d_ in D_poi:
            poi_pair_list.append((o_, d_))
    return poi_pair_list


def generate_OD_poi_pair_type(O_poi, D_poi):
    '''
    根据O_poi, D_poi生成 poi 对, 其中分别将O和D各自的poi功能认为是一个整体描述
    '''
    if O_poi is None:
        O_ = 'None'
    else:
        O_ = '-'.join(O_poi)

    if D_poi is None:
        D_ = 'None'
    else:
        D_ = '-'.join(D_poi)

    return (O_, D_)

def combine_poi(poi_list):
    '''
    把某些相近的poi进行合并
    最后只剩下，餐饮购物生活区附近、住宅区附近、公司商务区附近、其他区域
    '''
    result = set()
    for s in poi_list:
        if s == '餐饮' or s == '生活' or s == '购物':
            result.add('餐饮购物生活区附近')
        elif s == '住宅':
            result.add('住宅区附近')
        elif s == '公司':
            result.add('公司商务区附近')
        else:
            result.add('其他区域')
    result = list(result)
    return result

def OD_poi_pair_count(df):
    '''
    统计OD对的poi对的情况
    '''
    poi_pair_count = {}
    miss = 0
    for index, row in df.iterrows():
        O_position = (round(row['starting_lng'], 4), round(row['starting_lat'], 4))
        D_position = (round(row['dest_lng'], 4), round(row['dest_lat'], 4))
        if O_position in position_poi_dict.keys() and D_position in position_poi_dict.keys():
            O_poi = '-'.join(position_poi_dict[O_position]['most_poi']) 
            D_poi = '-'.join(position_poi_dict[D_position]['most_poi'])
            poi_pair_count[(O_poi, D_poi)] = poi_pair_count.get((O_poi, D_poi), 0) + 1
        else:
            print(O_position, D_position)
            miss += 1

    print("missed count:", miss)
    for key, value in sorted(poi_pair_count.items(), key = lambda item: item[1], reverse=True):
        print(key, value)

def define_poi_type(ss):
    if '住宅' in ss:
        return '住宅'
    elif '公司' in ss:
        return '公司'
    elif '购物' in ss or '餐饮' in ss or '生活' in ss:
        return '休闲娱乐'
    else:
        return '其他'


if __name__ == '__main__':
    data_file = "D:/CCF2019/data/selected_data/" + "DAY_WEEKDAY_0920" + ".csv"  # 选择数据======================
    date_imterval = ['2017-09-20', '2017-09-20']  #  选择时间===========================

    df = load_data_of(file=data_file,
                      columns=['order_id', 'departure_time', 'arrive_time', 'dest_lng', 'dest_lat', 'starting_lng', 'starting_lat','normal_time'])
    print("df total data:")
    print(df.shape)
    print(df.columns)

    poi_counter_24 = []
    for i in range(24):
        time_interval = [i, i+1]  #  选择时间===========================
        sub_df = select_df_of(df, dates=date_imterval, time_interval=time_interval)

        sub_df['dest_near_poi'] = sub_df.apply(lambda row: find_near_poi((row['dest_lng'], row['dest_lat'])), axis=1)
        sub_df['starting_near_poi'] = sub_df.apply(lambda row: find_near_poi((row['starting_lng'], row['starting_lat'])), axis=1)
    
        # 对poi进行一个合并
        sub_df['dest_type'] = sub_df['dest_near_poi'].apply(combine_poi)
        sub_df['starting_type'] = sub_df['starting_near_poi'].apply(combine_poi)
        sub_df['OD_poi_pair'] = sub_df.apply(lambda row: define_od_poi_pair(row['starting_type'], row['dest_type']), axis=1)

        # print(sub_df.head())
        OD_poi_pair_ = Counter([a for b in sub_df['OD_poi_pair'].tolist() for a in b])
        # print(OD_poi_pair_)
        poi_counter_24.append(OD_poi_pair_)
    
    # 导出counter数据
    out_put_file = date_imterval[0]
    counter_f = open(OUT_PUT_DIR + out_put_file, 'wb')
    pickle.dump(poi_counter_24, counter_f)
    print("dump done")

    # # 读入数据
    # counter_f = open('poi_counter', 'rb')
    # OD_poi_pair_ = pickle.load(counter_f)
    # print(OD_poi_pair_)