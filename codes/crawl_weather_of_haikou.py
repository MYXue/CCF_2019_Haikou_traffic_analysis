# -*- coding: utf-8 -*
'''
从历史天气网上爬取海口每天的天气状况
日期区间：2017-05-01 至 2017-10-31
'''
import requests                                                                      
from bs4 import BeautifulSoup                                                        

    
def get_url(city, year, month):
    url = 'http://lishi.tianqi.com/' + city + '/' + str(year) + str(month) + '.html'
    # print url
    return url

                                    
if __name__ == '__main__':
    print("begin main")
    city = 'haikou'
    year = '2017'
    months = ['05', '06', '07', '08', '09', '10']

    #依次爬取并写入文件
    file = open('haikou_weather.csv','w')   
    for month in months:
        url = get_url(city, year, month)   
        # print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.get(url, headers=headers)                                                            
        # response = requests.get(url)   
        # print(response)                                                  
        soup = BeautifulSoup(response.text, 'html.parser')                               
        weather_list = soup.select('div[class="tqtongji2"]')    
        print(weather_list)                         

        for weather in weather_list:                                                     
            weather_date = weather.select('a')[0].string.encode('utf-8')                 
            ul_list = weather.select('ul')                                               
            i=0                                                                          
            for ul in ul_list:                                                           
                li_list= ul.select('li')                                                 
                result=""                                                                   
                for li in li_list: 
                    print(li.string)                                                      
                    result += li.string
                    result += ','                                 
                if i!=0:                                                                 
                    file.write(result+'\n')                                                 
                i+=1                                                                         
    file.close() 