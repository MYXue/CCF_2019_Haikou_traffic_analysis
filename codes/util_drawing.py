# -*- coding: utf-8 -*
"""
2019-10-05
作图及保存
"""
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
import datetime
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def value_distribution(values, bins, value_name, save_name, save_dir):
    '''
    对于数值型数据，画箱线图及分布图并保存
    '''
    fig = plt.figure()  
      
    ax1 = fig.add_subplot(121)  
    ax1.hist(values, bins=bins)
    ax1.set_xlabel(value_name)
    ax1.set_ylabel('数量')
      
    ax2 = fig.add_subplot(122)  
    ax2.boxplot(values, showcaps=True, showbox=True, showfliers=True, showmeans=True)
    ax2.set_xlabel(value_name)

    plt.tight_layout()  # 为了让label显示完全
    plt.savefig(save_dir + '/' + save_name + '.png')
    plt.close()
    print(save_name + " done")