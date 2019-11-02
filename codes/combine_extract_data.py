# -*- coding: utf-8 -*
"""
2019-09-17
将原始数据合并，并提取若干字段，输出至csv文件
提取字段：order_id, start_dest_distance, arrive_time, departure_time, 
normal_time, dest_lng, dest_lat, starting_lng, starting_lat, month, day
"""
import pandas as pd

# pandas打印设置
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为10，默认为50
pd.set_option('max_colwidth',10)

## 指定数据集位置
OUTPUT_FILE_PATH = '../data/processed_data/'
DATA_FILE_PATH = '../data/Haikou_Order/'  # 目标文件夹地址

# 原始数据集中的所有字段
ALL_COLUMN_NAMES = ['order_id','product_id','city_id','district','county','type','combo_type',
                    'traffic_type','passenger_count','driver_product_id','start_dest_distance',
                    'arrive_time','departure_time','pre_total_fee','normal_time','bubble_trace_id',
                    'product_1level','dest_lng','dest_lat','starting_lng','starting_lat','year','month','day']

def merge_extract_data(num_list, column_list):
    data_file_list = []  # 原始数据文件名list
    for i in num_list:
        data_file_list.append('dwv_order_make_haikou_' + str(i) + '.txt')

    # 读取数据，合并并提取需要的数据
    extracted_data = None
    for file in data_file_list:
        data_file = DATA_FILE_PATH + file
        data = pd.read_table(data_file, header=None, names=ALL_COLUMN_NAMES, usecols=column_list, skiprows=1)  #跳过第一行（标签名）

        if extracted_data is None:
            extracted_data = data
        else:
            extracted_data = pd.concat([extracted_data, data], axis=0)  # 将数据按照行拼接
    return extracted_data

def dump_to_csv(df, file_name, file_path=OUTPUT_FILE_PATH):
    df.to_csv(file_path + file_name + '.csv', index=False)


if __name__ == '__main__':
    # 选择所需要的字段，主要是4类：位置，距离，时间，时长，
    target_columns = ['order_id','start_dest_distance','arrive_time','departure_time',
                      'normal_time','dest_lng','dest_lat','starting_lng','starting_lat','month','day']

    # 选择要合并的文件(用后缀数字表示)，一共8个文件
    merge_file_list = [1,2,3,4,5,6,7,8]

    extract_data = merge_extract_data(merge_file_list, target_columns)
    print(extract_data.shape)
    print(extract_data.head())

    # 导出至csv文件
    dump_to_csv(extract_data, 'extracted_11_features_of_merged_data')