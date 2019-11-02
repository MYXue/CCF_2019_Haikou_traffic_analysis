# -*- coding: utf-8 -*
"""
2019-10-19
经纬度的检查和位置的处理
数据中给的经纬度精确到了小数点后4位，经过粗略估计，精度和维度分别差0.0001，实际距离大约是10m
也就是说原始数据相当于在城市中每隔十米有一个点，精度还是比较高的
需要把所有的经纬坐标对影成一个一个的“位置”以方便画图，即 '位置1'：[精度1, 纬度1], '位置2'：[]...
其中粒度的划分是比较重要的
"""
import pandas as pd
from util_data_load_dump import load_data
from collections import Counter

RESULT_PATH = "../data/processed_data/"

def check_lng_lat_number():
    lng_lat_features = ['dest_lng', 'dest_lat', 'starting_lng', 'starting_lat']
    df = load_data(columns=lng_lat_features)
    print(df.shape)
    # print(df.info())
    # print(df)

    # # 经过检查，一共是3161个维度值，4505个精度值
    # # 假设这些值密集排列，两个点之间相差10m的话，总区域应该差不多是一个 31km * 45km 的形状
    # print(len(pd.unique(df[['starting_lat', 'dest_lat']].values.ravel())))
    # print(len(pd.unique(df[['starting_lng', 'dest_lng']].values.ravel())))

    
    # # 在所有的出发经纬度对中，有25个位置出现的次数超过了10000
    # # 在所有的到达经纬度对中，有97个位置出现的次数超过了10000（说明到达的位置更集中一点啊）
    # position_appearNum = {}
    # for a, b in zip(df['dest_lng'], df['dest_lat']):
    #     position_appearNum[(a, b)] = position_appearNum.get((a, b), 0) + 1
    # print(len(position_appearNum.keys())) 

    # value_counter = Counter(position_appearNum.values())
    # for appear_num, num_count in sorted(value_counter.items(), key=lambda x:x[0]):
    #     print(appear_num, num_count)

    # for key, value in sorted(position_appearNum.items(), key=lambda x:x[1], reverse=1):
    #     if value > 10000:
    #         print(key[0], key[1], value)
    #     else:
    #         break


    # 所有经纬度对的总数有358525个，删除仅出现一次的经纬度对之后还剩下198215个
    # 将这198215个经纬度输出到文件
    position_appearNum = {}
    for a, b in zip(df['starting_lng'], df['starting_lat']):
        position_appearNum[(a, b)] = position_appearNum.get((a, b), 0) + 1
    for a, b in zip(df['dest_lng'], df['dest_lat']):
        position_appearNum[(a, b)] = position_appearNum.get((a, b), 0) + 1
    print(len(position_appearNum.keys()))  # 所有经纬度对的总数

    lng_lat_pair_list = []
    appear_num_list = []
    for lng_lat_pair, appear_num in sorted(position_appearNum.items(), key=lambda x: x[1], reverse=1):
        if appear_num > 1:
            lng_lat_pair_list.append(lng_lat_pair)
            appear_num_list.append(appear_num)
        else:
            break

    data = {'lng_lat_pair':lng_lat_pair_list,
           'appear_num':appear_num_list}
    df = pd.DataFrame(data)
    print(df.shape)
    df.to_csv(RESULT_PATH + 'lng_lat_pair_appearNum.csv')


def select_unique_position():
    '''
    为每个经纬度编号，对于只出现了一次的position，将其定位漂移一下
    '''
    pass
    # 一共多少个经纬度，每个经纬度出现了多少次，删掉出现次数少的？
    # 把出现次数少的归并到临近的位置中，那个出现的多分到那个里面去（左右有0.0001的误差应该影响不大）

if __name__ == '__main__':
    lng_lat_features = ['dest_lng', 'dest_lat', 'starting_lng', 'starting_lat']
    df = load_data(columns=lng_lat_features)
    print(df.shape)
    # print(df.info())
    # print(df)
