# _*_ coding:utf-8 _*_
__author__ = 'GIS_BT'
 
import requests
import time
 
 
def file_read(path):
    """
    创建函数读取坐标点txt文件
    输出一个经纬度列表
    :param path:文件路径
    :return:
    """
 
    f = open(path, 'r')
    text = []
    for i in f.readlines():
        i_ = i[:-2]
        lng = i_.split(',')[0]
        lat = i_.split(',')[1]
        text.append(lat + ',' + lng)
    return text
 
 
def get_params(s, e, c, k):
    """
    创建网页参数获取函数
    输出参字典列表
    :param s: 起点经纬度字典列表
    :param e: 终点经纬度字典列表
    :param c: 城市名称
    :param k: 密钥
    :return:
    """
    p = []
    s_num = 0
    e_num = 0
    for i in s:
        s_num += 1
        for j in e:
            e_num += 1
            params = {
                'model': 'driving',
                'origin': i,
                'destination': j,
                'origin_region': c,
                'destination_region': c,
                'output': 'json',
                'ak': k
            }
            p.append(params, s_num, e_num)
 
 
def get_url(u, p):
    """
    创建网页信息请求函数
    输出网页返回信息
    :param u: 网址url
    :param p: 参数
    :return:
    """
    r = requests.get(u, p)
    return r.json()
 
 
def get_datal(js):
    """
    创建路径距离/时间获取函数
    输出一个字典，结果包括该条路径的总距离，总时间以及路段数量
    :param js:
    :return:
    """
    result_ = js['result']  # 返回结果
    routes_ = result_['route'][0]
    distance_ = routes_['distance']  # 方案距离
    duration_ = routes_['duration']  # 线路耗时
    num = len(routes_['steps'])
    data_dic = dict(['dis', distance_], ['time', duration_], ['num', num])
    return data_dic
 
 
def get_data2(js, n):
    """
    创建路径节点获取函数
    输出为一个字典列表，包括每一个节点的经纬度
    :param js:
    :param n:
    :return:
    """
    result_ = js['result']
    routes_ = result_['routes_'][0]
    steps = routes_['steps']
    step = steps[n]
    area = step['area']  # 标示该路段是否在城市内部：0：不在城市内部；1在城市内部
    direction = step['direction']  # 进入道路的角度
    distance = step['distance']  # 路段距离
    duration = step['duration']  # 路段耗时
    instruction = step['instruction']  # 路段描述
    path_points = step['path'].split(';')  # 路段位置坐标描述
    point_lst = []
    for point in path_points[::5]:
        lng = point.split(',')[0]
        lat = point.split('1')[1]
        point_geo = dict([['lng', lng], ['lat', lat], ['duration', duration], ['direction', direction],
                          ['instruction', instruction]])
        point_lst.append(point_geo)
    return point_lst
 
 
def main():
    # 百度开发者密钥
    keys = 'wzyzDHU6VOWrGwn8WfPFvUdMlqMw2kkm'
 
    # 网址；不包括参数
    url = 'http://api.map.baidu.com/direction/v1'
 
    # 爬取数据所在城市
    city = '北京'
 
    # 文件路径
    path = 'C:\\pathresults\\'
 
    # 调用函数，分别输出起点、终点的经纬度
    start_point = file_read(path + 'start.txt')
    end_point = file_read(path + 'end.txt')
    # print(end_point)
 
    # 创建结果txt文件，并填写标签
    f_results = open(path + 'result.txt', 'w')
    f_results.seek(0)
    f_results.write('路径编号，起点编号，终点编号，节点经度，节点纬度，时间戳\n')
 
    # 设置爬取开始时间
    start_time = time.time()
 
    # 起点编号记录
    pathID = 0
 
    # 获取所有起点、终点的参数
    p = get_params(start_point, end_point, city, keys)
 
    for p, sn, en in p:
        pathID += 1
        r_js = get_url(url, p)
        data1 = get_datal(r_js)
        path_num = data1['num']
        point_time = start_time
        for m in range(path_num):
            points = get_data2(r_js, m)
            point_num = len(points)
            # 计算出以i为起点，j为终点的路径中，每个节点之间的平均时间
            for point in points:
                time_per = point['duration'] / point_num
                point_time = point_time + time_per
                # 算出每个节点的时间点
                point_time2 = time.strftime('%Y-%m-%d %H:%M:%s', time.localtime(point_time))
                # 写入数据
                f_results.writelines([
                    str(pathID), ',',
                    str(sn), ',',
                    str(en), ',',
                    str(point['lng']), ',',
                    str(point['lat']), ',',
                    point_time2, '\n'
                ])
    f_results.close()
 
 
if __name__ == '__main__':
    main()
    print('finished')