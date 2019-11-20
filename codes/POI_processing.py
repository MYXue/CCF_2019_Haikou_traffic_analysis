# -*- coding: utf-8 -*
"""
2019-11-18
海口poi数据处理，每个经纬度对应一个大类一个小类
"""
import pandas as pd
import numpy as np
import datetime
from combine_extract_data import dump_to_csv
from collections import Counter
import pickle


# pandas打印设置
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为10，默认为50
pd.set_option('max_colwidth', 20)
# 打印时每行显示长度
pd.set_option('display.width', 140)

## 指定读入文件位置
READ_FILE_PATH = '../data/haikou_poi/'
READ_FILE_NAME = 'haikou_poi' + '.txt'

## 指定输出文件位置
OUTPUT_FILE_PATH = '../data/haikou_poi/'


## 各个一级poi类别和对应的系列名
POI_1_NAME_DICT = {'购物服务':'购物', '餐饮服务':'餐饮', '生活服务':'生活',
                    '公司企业':'公司', '商务住宅':'住宅', '住宿服务':'酒店',
                    '科教文化服务':'教育', '医疗保健服务':'医疗', '政府机构及社会团体':'机构'}

def dump_position_poi_dict(df):
    '''
    以0.001为网格划分区间，找出每个点对应的若干poi_1信息，包括id和一级poi名称
    导出文件
    '''
    # 将经纬度位置精确到小数点后4位
    df['position'] = df.apply(lambda row: (round(row['lng'], 4), round(row['lat'], 4)), axis=1)
    print(df.head())

    # 统计每个position的功能点id和一级poi_level信息, 只选择9个最关注的poi_1类别
    position_poi_dict = {}
    for index, row in df.iterrows():
        if row['poi_1'] in POI_1_NAME_DICT.keys():
            position_poi_dict[row['position']] = position_poi_dict.get(row['position'], {})
            position_poi_dict[row['position']]['id'] = position_poi_dict[row['position']].get('id',[])
            position_poi_dict[row['position']]['id'].append(row['id'])
            position_poi_dict[row['position']]['poi_1'] = position_poi_dict[row['position']].get('poi_1',[])
            position_poi_dict[row['position']]['poi_1'].append(POI_1_NAME_DICT[row['poi_1']])

    for positon, value in position_poi_dict.items():
        position_poi_dict[positon]['most_poi'] = []
        # 找到出现类别和次数
        poi_count = Counter(value['poi_1'])
        if len(poi_count) >= 3:  # 如果出现的poi类型大于三个, 只检查前三个
            [first, second, third] = poi_count.most_common(3)
            position_poi_dict[positon]['most_poi'].append(first[0])
            if (first[1] - second[1]) / first[1] <= 0.25:  # 如果第二多与第一多的差值在第一多的1/4/之内
                position_poi_dict[positon]['most_poi'].append(second[0])
                if (first[1] - third[1]) / first[1] <= 0.25:
                    position_poi_dict[positon]['most_poi'].append(third[0])
        else:  # 只检查前两个
            if len(poi_count) == 2:
                [first, second] = poi_count.most_common(2)
                position_poi_dict[positon]['most_poi'].append(first[0])     
                if (first[1] - second[1]) / first[1] <= 0.25:  # 如果第二多与第一多的差值在第一多的1/4/之内
                    position_poi_dict[positon]['most_poi'].append(second[0])
            else:
                [first] = poi_count.most_common(1) 
                position_poi_dict[positon]['most_poi'].append(first[0])
            
    print(len(position_poi_dict))

    n = 0
    for key, value in position_poi_dict.items():
        print(key, value)
        n += 1
        if n > 100:
            break
    
    output = OUTPUT_FILE_PATH + 'position_poi_dict'
    f = open(output, 'wb')
    pickle.dump(position_poi_dict, f)
    print(output + ' dump finish!')

if __name__ == '__main__':
    poi_file = READ_FILE_PATH + READ_FILE_NAME
    df = pd.read_table(poi_file, encoding='gbk')
    print(len(df))
    # print(df.head())

    # 数据集整体信息检查
    # print("\n数据集整体信息：")
    # print (df.info()) #训练集的一些基本信息
    # print("\n检查各列是否有缺失值：")  # address有缺失值，但是poi type没有缺失值
    # print(df.isnull().any())

    # 检查一下第一级poi种类及个数
    df['poi_1'] = df['type'].apply(lambda s: s.split(';')[0])
    # c = Counter(df['poi_1'].tolist())
    # print(c)

    # # 检查某个poi_1对应的完整poi信息
    # print(df[df['poi_1'] == '通行设施'])

    dump_position_poi_dict(df)
    