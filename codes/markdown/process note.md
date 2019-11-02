## 背景信息
共14160162条数据，月均2360027条，日均78668条，平均每小时3278条，每分钟55条

以下来自百度百科：
截至2018年末，全市常住人口230.23万人（北京的十分之一左右）  
海口市位于北纬19°31′～20°04′，东经110°07′～110°42′之间。  
海口由本岛海南岛（部分）、离岛海甸岛、新埠岛组成，全市总面积3145.93平方公里，其中，陆地面积2284.49平方公里，海域面积861.44平方公里。  
海口市辖秀英区、龙华区、琼山区、美兰区4个区（县级）；下设21个街道、22个镇、207个社区、245个行政村。  
包含一个机场：海口美兰国际机场，三个火车站：海口站、海口东站、美兰机场站。  
2018年末全市民用汽车拥有量80万辆，比上年增长8.1%。其中，私人汽车70.6万辆，增长7.1%。  
旅游业发展持续向好。2018年，全市共接待游客2670.85万人次，比上年增长10%。其中，接待入境游客26.13万人次，增长43.6%；人均逗留天数1.46天，延长0.02天。实现旅游总收入298.11亿元，增长12.1%。其中，入境旅游收入8193.4万美元，增长38%。全市A级旅游景区10家，其中4A级及以上旅游景区4家；星级宾馆酒店39家，其中五星级宾馆酒店4家。  

##10/7 之前的处理（myx）
combine_extract_data.py：
将原来分散在8个txt中的原始数据合并，并提取了用于初步分析的11个features，省略了其他信息，生成的文件为processed_data/extracted_11_features_of_merged_data.csv  
使用的feature有'order_id','start_dest_distance','arrive_time','departure_time',
'normal_time','dest_lng','dest_lat','starting_lng','starting_lat','month','day'

data_check.py:
对原始数据进行有效性及数值范围的检查，修正部分有误数据，并过滤异常值，过滤后的数据再次输出为csv文件processed_data/extracted_11_features_of_merged_data_filtered.csv。
在extracted_11_features_of_merged_data_filtered.csv中，增加了三列feature，分别是'arrive_time','departure_time'的时间差、二者时间差的分钟表示、correct_tag（标志数据是否经过修正，部分数据'arrive_time','departure_time'是反的颠倒了一下）
这个数据可以直接用来初步可视化，可以百度云直接下载

util_drawing.py:
一个辅助画图的函数

## 发现的问题
时长 normal_time 不是 arrive_time与departure_time 的时间差  
根据arrive_time与departure_time计算出来的时间差过小，感觉上和乘坐出租车的平均时长不太一致，所以这就意味着数据中的arrive_time与departure_time至少有一个是不可信的，或者说都是不可信的；另一个提供的时间数据 normal_time 的分布更符合直观感觉上的乘车时间  

怀疑'arrive_time','departure_time'并非乘客的到达时间和出发时间，而是司机到达接客点时间和真正的出发时间？ 'normal_time'可能是乘车时间 或 估计的乘车时间

而在我们的分析中，比较重要的是乘客出行真正的出发时间和到达时间，所以总之现在就是要确定出发和到达的相对比较准确的时间。 我的建议是可以先把departure_time作为真正的出发时间，先固定这一个时间，做一下可视化看看是否有异常的地方。

另外，原始数据中部分数据的arrive_time和normal_time有缺失（占比大约10+%），过滤后的数据没有缺失。


