# -*- coding: utf-8 -*
"""
2019-10-24
造数据
"""
import pandas as pd
import random
import datetime

def random_24_list():
    result = []
    for i in range(24):
        result.append(random.randint(2000, 6000))
    return result

def data_faker():
    date_list = []  # 日期list, 字符串格式
    dayly_count_list = []  # 每天的数量count
    hourly_count_list = []  # 一个184*24的list
    # weather_list = []  # 每天的天气状况

    WEATHER_DIE = 'D:/CCF2019/data/weather_data/' + 'haikou_weather_2017.csv'
    df = pd.read_csv(WEATHER_DIE)
    date_list = df['日期'].to_list()
    weather_list = [wea + ' ' + str(minT) + '~' + str(maxT) + '度' for wea,minT,maxT in zip(df['天气'].to_list(),df['最低气温'].to_list(),df['最高气温'].to_list())]

    for date in date_list:
        dayly_count_list.append(random.randint(70000, 100000))
        hourly_count_list.append(random_24_list())

    # for a, b in zip(dayly_count_list, hourly_count_list):
    #     print(a, b)

    return date_list, dayly_count_list, hourly_count_list, weather_list

def data_maker(select=None):
    DATA_STATISTIC_DIR = 'D:/CCF2019/codes/' + 'data_dayly_hourly_count.csv'
    df_data = pd.read_csv(DATA_STATISTIC_DIR)
    date_list = df_data['date'].to_list()
    dayly_count_list = df_data['day_count'].to_list()
    hourly_count_list_temp = df_data['hour_count'].to_list()
    hourly_count_list = []
    for str_list in hourly_count_list_temp:
        value_list = str_list[1:-1].split(',')
        hourly_count_list.append([int(value) for value in value_list])

    WEATHER_DIE = 'D:/CCF2019/data/weather_data/' + 'haikou_weather_2017.csv'
    df = pd.read_csv(WEATHER_DIE)
    weather_list = [wea + ' ' + str(minT) + '~' + str(maxT) + '度' for wea,minT,maxT in zip(df['天气'].to_list(),df['最低气温'].to_list(),df['最高气温'].to_list())]

    weekday_list = []
    num_weekday = {0:'周一',1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}
    for date_str in date_list:
        date_ = datetime.datetime.strptime('2017/'+ date_str, '%Y/%m/%d').weekday()
        weekday_list.append(num_weekday[date_])

    if select == None:
        return date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list
    elif select == 'good_weather':
        date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select = [],[],[],[],[]
        for a, b, c, d, e in zip(date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list):
            if d.split()[0] in ('多云'):
                date_select.append(a)
                dayly_count_select.append(b)
                hourly_count_select.append(c)
                weather_select.append(d)
                weekday_select.append(e)
        return date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select
    elif select == 'bad_weather':
        date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select = [],[],[],[],[]
        for a, b, c, d, e in zip(date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list):
            if d.split()[0] in ('暴雨','大暴雨','大到暴雨','中到大雨','大雨'):
                date_select.append(a)
                dayly_count_select.append(b)
                hourly_count_select.append(c)
                weather_select.append(d)
                weekday_select.append(e)
        return date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select
    elif select == 'weekdays':
        date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select = [],[],[],[],[]
        for a, b, c, d, e in zip(date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list):
            if e not in ('周六','周日'):
                date_select.append(a)
                dayly_count_select.append(b)
                hourly_count_select.append(c)
                weather_select.append(d)
                weekday_select.append(e)
        return date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select
    elif select == 'weekends':
        date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select = [],[],[],[],[]
        for a, b, c, d, e in zip(date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list):
            if e in ('周六','周日'):
                date_select.append(a)
                dayly_count_select.append(b)
                hourly_count_select.append(c)
                weather_select.append(d)
                weekday_select.append(e)
        return date_select, dayly_count_select, hourly_count_select, weather_select, weekday_select


if __name__ == '__main__':
    date_list, dayly_count_list, hourly_count_list, weather_list, weekday_list = data_maker(select='good_weather')
    for date in date_list:
        print(date)
        print(type(date))
