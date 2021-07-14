# coding: utf-8
# Author：KZ
# Date ：2020/11/5 15:53
# APISpider
# Tool ：PyCharm
import requests
from fake_useragent_kz.fake_useragent_kz import UserAgent

#7.14

def get_json(uid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
    }


    params = {
        'uid': uid,
        'output': 'json',               #输出格式为json
        'scope': '2',                   #检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
        'ak': 'Kcl9bynY5Icf1yGv6mQPzS7Phhkuw0Pb'
    }


    res = requests.get("http://api.map.baidu.com/place/v2/detail", params=params, headers=headers).json()
    return res

if __name__ == '__main__':
    data=get_json('5daa9abbd8d1c5773a04b185')
    print(data)