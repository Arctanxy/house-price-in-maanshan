import requests
import lxml.html
import urllib.parse
import pandas as pd
import numpy as np
import re
import time
'''
1. 搜索毛坯房、产权属性：住宅
2. 多线程或多进程运行
3. 根据编号来识别房源，避免重复爬取
4. 包含信息：小区名、楼层、面积、价格、发布时间五项信息
5. 先通过dataframe存入到csv中，后期再将代码改为MySQL或mongodb（因为mongodb存储读取速度快）存储
6. 目前100页相当于半个月的时间跨度，预计需要2000-4000页（1-2年）的信息才算完成信息收集
'''
#####毛坯三房非顶层
#####使用data会被网页侦查到，返回一个提示框，所以先爬取数据，再进行筛选
url = 'http://www.0555fc.com/Search.asp?AreaId=&Decoration=&PropertyType=&CountF=&CountT=&CountW=&sbm=yes&tj.x=55&tj.y=20&jg1=&jg2=&mj1=&mj2=&Address=&lei=1&trade=%B3%F6%CA%DB'
def get_price_per_square(url):

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
    }

    data = {
        'Decoration':urllib.parse.quote('毛坯'),
        'CountF':'3'
    }

    r = requests.get(url,headers = headers)

    tree = lxml.html.fromstring(r.content)

    df = pd.DataFrame()

    #k = tree.xpath('//table[@class="search_list"]/tr/td/text()')
    #m = tree.xpath('//table[@class="search_list"]/tr/td/b/text()')

    info_list = tree.xpath('//table[@class="search_list"]/tr[@class="seatr"]')#抓取表头
    print(info_list)

    id = []
    location = []
    strict = []
    roomnumber = []
    floor = []
    area = []
    price = []
    media = []
    publishtime = []



    info = tree.xpath('//table[@class="search_list"]/tr')

    for item in info:
        text = item.xpath('./td/text()')#其他元素
        others = item.xpath('./td/b/text()')#包含编号，面积，价格三个元素
        strict = item.xpath('./td/a/text()')#小区信息
        if len(others) == 3:
            pattern = re.compile(r'\d+\.?\d+')#匹配整数或者小数
            square = pattern.findall(others[1])
            id.append(others[0])
            area.append(float(square[0]))
            price.append(float(others[2]))
        print(text)
        print(strict)
    area = np.array(area)
    price = np.array(price)

    price_per_square = price*10000/area
    return price_per_square
start_url = 'http://www.0555fc.com/Search.asp?lei=1&trade=%B3%F6%CA%DB&AreaId=&PropertyType=&CountF=&CountT=&CountW=&Decoration=%C3%AB%C5%F7&Direction=&sbm=yes&tj.x=61&tj.y=16&jg1=0&jg2=9000&mj1=&mj2=&Floor1=&Floor2=&PropertyId=&Address=&page='
#毛坯房网址
urllist = []
for i in range(1):
    urllist.append(start_url + str(i+1))
price_list = []
j = 0
for each_url in urllist:
    time.sleep(1)
    try:
        price_list.extend(get_price_per_square(each_url))
        print(j)
        j += 1
    except:
        pass
print(price_list)

#np.savetxt('new.csv',price_list,delimiter=',')