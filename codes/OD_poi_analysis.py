# -*- coding: utf-8 -*
"""
2019-11-19
对出发点到达点的poi信息进行分析
"""
import pickle
from collections import Counter
import numpy as np
from util_data_load_dump import load_data_of, get_datda_near

POI_RESULT_FILE = '../data/haikou_poi/' + 'position_poi_dict'
f = open(POI_RESULT_FILE, 'rb')
position_poi_dict = pickle.load(f)

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
        return None
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
        else:  # 只检查前两个
            if len(poi_count) == 2:
                [first, second] = poi_count.most_common(2)
                result_list.append(first[0])     
                if (first[1] - second[1]) / first[1] <= 0.25:  # 如果第二多与第一多的差值在第一多的1/4/之内
                    result_list.append(second[0])
            else:
                [first] = poi_count.most_common(1) 
                result_list.append(first[0])
        return result_list

def generate_OD_poi_pair_type(O_poi, D_poi):
    '''
    根据O_poi, D_poi生成 poi 对
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
    # data_file = "D:/CCF2019/data/selected_data/" + "DAY_WEEKDAY_0920" + ".csv"  # 选择数据======================
    # date_imterval = ['2017-09-20', '2017-09-20']  #  选择时间===========================
    # time_interval = [17, 19]  #  选择时间===========================

    # df = load_data_of(file=data_file,
    #                   dates=date_imterval, time_interval=time_interval,
    #                   columns=['order_id', 'departure_time', 'arrive_time', 'dest_lng', 'dest_lat', 'starting_lng', 'starting_lat','normal_time'])
    # # print(df)
    # print(df.shape)
    # print(df.columns)

    # df['dest_near_poi'] = df.apply(lambda row: find_near_poi((row['dest_lng'], row['dest_lat'])), axis=1)
    # df['starting_near_poi'] = df.apply(lambda row: find_near_poi((row['starting_lng'], row['starting_lat'])), axis=1)

    # df['OD_poi_pair'] = df.apply(lambda row: generate_OD_poi_pair_type(row['starting_near_poi'], row['dest_near_poi']), axis=1)
    # # print(df)

    # OD_poi_pair_ = Counter(df['OD_poi_pair'].tolist())
    # print(OD_poi_pair_)


    # # 导出counter数据
    # counter_f = open('poi_counter', 'wb')
    # pickle.dump(OD_poi_pair_, counter_f)
    # print("dump done")

    # 读入数据
    counter_f = open('poi_counter', 'rb')
    OD_poi_pair_ = pickle.load(counter_f)

    # 按照归类后的poi再次合并一下poi type
    od_poi_type_dict = {}
    for key, value in dict(OD_poi_pair_).items():
        key_new = (define_poi_type(key[0]), define_poi_type(key[1]))
        od_poi_type_dict[key_new] = od_poi_type_dict.get(key_new, 0) + value
    # print(od_poi_type_dict)

    for key, value in sorted(od_poi_type_dict.items(), key=lambda x: x[1], reverse=True):
        print(key, value)