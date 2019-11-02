# -*- coding: utf-8 -*
"""
2019-10-25
dump data 导出需要分析的数据，按照每天-每周-每月的数据
"""
import pandas as pd
import datetime
from util_data_load_dump import load_data, select_df_of


DATA_PATH = "D:/CCF2019/data/processed_data/"
DATA_FILTERED_FILE = "extracted_11_features_of_merged_data_filtered.csv"
FILTERED_DATA = DATA_PATH + DATA_FILTERED_FILE

RESULT_DIR = "D:/CCF2019/data/selected_data/"

# DAY_WEEKDAY, 09/20, 周三，多云
# DAY_WEEKEND, 10/14, 周六, 多云
# DAY_BAD_WEATHER, 10/17, 周二, 中到大雨
# WEEK_IN_WORK, 06/12 ~ 06/18
# WEEK_5_1, 05/01 ~ 05/07
# WEEK_10_1, 10/01 ~ 10/07
# MONTH, 6月

def dump_day_weakday(df):
    date = ['2017-09-20', '2017-09-20']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'DAY_WEEKDAY_0920.csv')
    print("DAY_WEEKDAY_0920" + " done")

def dump_day_weekend(df):
    date = ['2017-10-14', '2017-10-14']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'DAY_WEEKEND_1014.csv')
    print("DAY_WEEKEND_1014" + " done")

def dump_day_bad_weather(df):
    date = ['2017-10-17', '2017-10-17']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'DAY_BAD_WEATHER_1017.csv')
    print("DAY_BAD_WEATHER_1017" + " done")

def dump_week_in_work(df):
    date = ['2017-06-12', '2017-06-18']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'WEEK_IN_WORK_0612_0618.csv')
    print("WEEK_IN_WORK_0612_0618" + " done")

def dump_week_5_1(df):
    date = ['2017-05-01', '2017-05-07']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'WEEK_5_1.csv')
    print("WEEK_5_1" + " done")

def dump_week_10_1(df):
    date = ['2017-10-01', '2017-10-07']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'WEEK_10_1.csv')
    print("WEEK_10_1" + " done")

def dump_month(df):
    date = ['2017-06-01', '2017-06-30']
    df_select = select_df_of(df, dates=date)
    df_select.to_csv(RESULT_DIR + 'MONTH_06.csv')
    print("MONTH_06" + " done")

if __name__ == '__main__':
    df = load_data()
    print(" loading done")
    # dump_day_weakday(df)
    # dump_day_weekend(df)
    # dump_day_bad_weather(df)
    # dump_week_in_work(df)
    # dump_week_5_1(df)
    # dump_week_10_1(df)
    dump_month(df)