# -*- coding: utf-8 -*
"""
2019-10-22
尝试调用百度地图API根据起始点终止点位置输出路径规划中的一系列坐标
"""
import requests
 
url = 'https://api.map.baidu.com/direction/v1'
 

def get_route_list(departure, arrive):
    origin = str(departure[1]) + ',' + str(departure[0])
    destination = str(arrive[1]) + ',' + str(arrive[0])
    params = {
            'mode':'driving',
            'origin':origin,
            'destination':destination,
            'origin_region':'海口',
            'destination_region':'海口',
            'output':'json',
            'ak':'dRcnjydlLG1v7V6RxW7I4iwAsdUmQ1Gx'#需自己填写
            }
 
    r = requests.get(url, params)
    r_js = r.json()
    # 返回js数据
 
    # print(r_js)
    routes_ = r_js['result']['routes'][0]
    dis_ = routes_['distance']
    time_ = routes_['duration']
 
    # print('总行程距离为：'+str(dis_)+'米，总时间为：'+str(time_)+'秒')
  
    steps_ = routes_['steps']

    route_list = []
    for step in steps_:
        path_ = step['path']
        point_lst =path_.split(';')
        for point in point_lst:
            lng = point.split(',')[0]
            lat = point.split(',')[1]
            # print(str(lng) + ',' + str(lat) + '\n')
            route_list.append([float(lng), float(lat)])
    return route_list