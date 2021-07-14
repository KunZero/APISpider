# coding: utf-8
# Author：KZ
# Date ：2020/11/5 12:02
# APISpider
# Tool ：PyCharm
# coding=utf-8
import requests
from fake_useragent_kz.fake_useragent_kz import UserAgent

#2021.07.14


def get_json(region):
    headers = {
        'User-Agent': UserAgent().random()
    }

    print(headers)

    params = {
        'query': '珠宝店',                #检索关键字
        'region': region,               #检索行政区划区域
        'output': 'json',               #输出格式为json
        'scope': '2',                   #检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
        'page_size': 20,                #单次召回POI数量，默认为10条记录，最大返回20条。
        'page_num': 0,                  #分页页码，默认为0,0代表第一页，1代表第二页，以此类推。
        'ak': 'Kcl9bynY5Icf1yGv6mQPzS7Phhkuw0Pb'
        # 'ak': 'RKQ9801uAsskHHarNfGNNyqUwjKC9PUS'
    }


    res = requests.get("http://api.map.baidu.com/place/v2/search", params=params, headers=headers)
    print(res.json())
    return res.json()


data=get_json("中国")

result=data.get('results')



