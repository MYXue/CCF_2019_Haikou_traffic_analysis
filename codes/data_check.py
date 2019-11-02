# -*- coding: utf-8 -*
"""
2019-09-18
对数据进行缺失值，异常值及数据分布检查，导出过滤后的数据
"""
import pandas as pd
import numpy as np
import datetime
from util_drawing import value_distribution
from combine_extract_data import dump_to_csv

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
READ_FILE_PATH = '../data/processed_data/'
READ_FILE_NAME = 'extracted_11_features_of_merged_data' + '.csv'

## 指定输出图片文件位置
OUTPUT_FILE_PATH = 'D:/CCF2019/result/'

def load_date(file, rows=None):
    '''
    读入文件
    '''
    if rows is not None:
        return pd.read_csv(file, nrows=rows, dtype={'order_id': str})
    else:
        return pd.read_csv(file, dtype={'order_id': str})

def parse_time(timeStrs):
    '''
    时间数据格式，注意异常数据的处理
    '''
    if str(timeStrs) == "0000-00-00 00:00:00":
        return np.nan
    else:
        return datetime.datetime.strptime(str(timeStrs), "%Y-%m-%d %H:%M:%S")

def calculate_time_diff_dataCorrect(array_like):
    '''
    根据出发时间和到达时间计算时间差
    '''
    departure_time = array_like["departure_time"]
    arrive_time = array_like["arrive_time"]
    if pd.isna(arrive_time) is False:
        if departure_time < arrive_time:
            time_diff = arrive_time - departure_time
        else:
            time_diff = departure_time - arrive_time
        return time_diff
    else:
        return np.nan

def upper_bond(values):
    '''
    计算数据的异常值过滤上阈值
    '''
    values = values.dropna()
    # 1st quartile (25%)分位数
    Q1 = np.percentile(values, 25)
    # 3rd quartile (75%)分位数
    Q3 = np.percentile(values, 75)
    # quartile spacing (IQR)
    IQR = Q3 - Q1
    # outlier step
    outlier_step = 2.0 * IQR  # 一般用的是1.5倍，为了保险起见(为了保留更多的数据)这里用了2倍
    # upper bond
    upper = Q3 + outlier_step
    return upper

def df_description(df):
    '''
    打印数据集的一些基本特征
    '''
    # ========== 数据检查 ==========
    print("df shape:", df.shape)  # 数据集的行列数
    print("\n前几行示例：")
    print (df.head()) #打印表头和前几行
    print("\n数据集整体信息：")
    print (df.info()) #训练集的一些基本信息

    # 各列是否有缺失值
    print("\n检查各列是否有缺失值：")
    print(df.isnull().any())

    # ========== 缺失值 ==========
    # 只有normal_time列有缺失值，打印出normal_time缺失数据的前几行
    # print("\n只有normal_time列有缺失值，打印出normal_time缺失的数/据:")
    # print(df[df.isnull().values==True].head())
    # arrive_time 中有 形如 ‘0000-00-00 00:00:00’的无效数据
    # print("\nnormal_time 的缺失可能是由于arrive_time的数据错误引起的。也就是说有缺失值的行 arrive_time 和 normal_time均不可用。但有上下车点的地理位置、start_dest_distance 和 上车时间")
    # normal_time的缺失量占比
    print("\n数据缺失占比：", df["normal_time"].isnull().sum() / len(df))

    # ========== 数值型数据的分布情况 ==========
    print("\n数值型数据的描述性统计：")
    print(df.describe()) #描述性统计

def filter_abnormal_data(df):
    '''
    根据start_dest_distance, time_diff_in_minutes和normal_time对数据进行过滤
    只过滤了过大的异常值（根据原始数据的箱线图确定的）
    '''
    start_dest_distance_upper = upper_bond(df["start_dest_distance"])
    print("start_dest_distance_upper", start_dest_distance_upper)

    time_diff_in_minutes_upper = upper_bond(df["time_diff_in_minutes"])
    print("time_diff_in_minutes_upper", time_diff_in_minutes_upper)

    normal_time_upper = upper_bond(df["normal_time"])
    print("normal_time_upper", normal_time_upper)

    # 打印异常值
    # print("\nabnormal data:")
    # df_abnormal = df[(df["start_dest_distance"] > start_dest_distance_upper) | (df["time_diff_in_minutes"] > time_diff_in_minutes_upper) | (df["normal_time"] > normal_time_upper)]  
    # print(df_abnormal[["departure_time", "arrive_time", "normal_time", "time_difference_arrive_departure", "start_dest_distance", \
    #             "dest_lat", "starting_lat"]])

    df = df[(df["start_dest_distance"] <=start_dest_distance_upper) & (df["time_diff_in_minutes"] <= time_diff_in_minutes_upper) & (df["normal_time"] <= normal_time_upper)]
    return df

def show_value_distribution(df):
    '''
    对于那几列数值型数据，画图展示一下数据分布
    '''
    # start_dest_distance 起落车距离的分布情况
    value_distribution(df["start_dest_distance"].tolist(), 40, "start_dest_distance",  "start_dest_distance", OUTPUT_FILE_PATH)
    # normal_time 时间的分布情况
    value_distribution([item for item in df["normal_time"].tolist() if pd.isna(item) is False], 30, "normal_time","normal_time", OUTPUT_FILE_PATH)
    # 起落车时间差分布情况
    value_distribution([item for item in df["time_diff_in_minutes"].tolist() if pd.isna(item) is False], 30, "time_difference between arrive_departure", "time_difference between arrive_departure", OUTPUT_FILE_PATH)


if __name__ == '__main__':
    read_file = READ_FILE_PATH + READ_FILE_NAME

    # 读取数据，可指定读取的条数，默认读取全部数据
    df = load_date(read_file)
    # ========== 过滤前的数据检查 ==========
    print("过滤前：")
    df_description(df)


    # ========== 时间格式数据处理及异常时间数据 ==========
    # 对arrive_time和departure_time的处理, 将其转变成python的时间格式
    df["arrive_time"] = df["arrive_time"].apply(parse_time)
    df["departure_time"] = df["departure_time"].apply(parse_time)
    print("\ntime parse done!\n")
   
    # 计算arrive_time和departure_time的时间差
    df["time_difference_arrive_departure"] = df.apply(calculate_time_diff_dataCorrect, axis=1)
    df["time_diff_in_minutes"] = df["time_difference_arrive_departure"].apply(lambda x: x.seconds//60 if pd.isna(x) is False else np.nan)
    print("\ntime diff calculate done\n")
  
    # 另外，在数据处理的过程中，发现部分数据arrive_time和departure_time标反了，也要进行处理  
    # 修正一下arrive_time和departure_time颠倒的数据
    df["correct_tag"] = df.apply(lambda row: 1 if row['departure_time'] >= row['arrive_time'] else 0, axis=1)
    df["arrive_time_temp"] = df["arrive_time"]
    df["arrive_time"] = df.apply(lambda row: row["departure_time"] if row['correct_tag'] == 1 else row["arrive_time"], axis=1)
    df["departure_time"] = df.apply(lambda row: row["arrive_time_temp"] if row['correct_tag'] == 1 else row["departure_time"], axis=1)
    del df["arrive_time_temp"]
    print("time correct done!")

    # # 检查数值型数据'start_dest_distance','normal_time', "time_difference_arrive_departure"是否有异常值，画箱线图，分布图，看均值和分布情况
    # show_value_distribution(df)


    # =========== 数值型数据的异常值处理 ===========
    # # 画完图之后从上面的结果中发现，几个数值型数据都有过大的异常值，需要检查一下
    # print("\nstart_dest_distance 异常数据，通过检查结果应该是经纬度的获取有问题，位置不准确导致的：")
    # print(df[df["start_dest_distance"] > 1000000])  # 超过100公里的
    # print("\nnormal_time 异常数据：")
    # print(df[df["normal_time"] > 300])  # 超过5小时的
    # print("\ntime_difference_arrive_departure 异常数据，可能是出发或到达时间记录有误（有的不是同一日期）：")
    # print(df[df["time_diff_in_minutes"] > 300])  # 超过5小时的
    print("before filter:", len(df))
    df = filter_abnormal_data(df)
    print("after filter", len(df))
    # # 检查数值型数据'start_dest_distance','normal_time', "time_difference_arrive_departure"是否有异常值，画箱线图，分布图，看均值和分布情况
    show_value_distribution(df)


    # ========== arrive_time与departure_time的差 与normal_time的关系与含义 ==========
    # 根据上下车时间计算出来的时间差过小，感觉上和乘坐出租车的平均时长不太一致
    # 所以这就意味着数据中的上车时间和下车时间至少有一个是不可信的，或者说都是不可信的
    # 另一个提供的时间数据 normal_time 的分布更符合直观感觉
    # 另外，也需要结合start_dest_distance与用时的关系
    # 可以选择时间段画两两指标的散点图


    # ========== 过滤后的数据检查及导出 ==========
    # 数据检查
    print("\n过滤后：")
    df_description(df)

    # 数据导出
    dump_to_csv(df, "extracted_11_features_of_merged_data_filtered")