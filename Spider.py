# coding: utf-8
# Author：KZ
# Date ：2020/11/5 16:25
# APISpider
# Tool ：PyCharm
import time
import requests
import xlwings as xw
from fake_useragent_kz.fake_useragent_kz import UserAgent


class Spider():
    def __init__(self,query):
        self.query=query
        self.url = 'http://api.map.baidu.com/place/v2/search'
        self.app = xw.App(visible=True, add_book=False)
        self.wb = self.app.books.open('DIY\CNDIY.xlsx')
        self.sht = self.wb.sheets['Sheet1']
        self.count = 0
        self.total = 1
        self.ID = 1

    def new_sheet(self):
        pass

    def params(self, region, num=0):
        params = {
            'query': self.query,  # 检索关键字
            'region': region,  # 检索行政区划区域
            'output': 'json',  # 输出格式为json
            'scope': '2',  # 检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
            'page_size': 20,  # 单次召回POI数量，默认为10条记录，最大返回20条。
            'page_num': num,  # 分页页码，默认为0,0代表第一页，1代表第二页，以此类推。
            # 'ak': 'Kcl9bynY5Icf1yGv6mQPzS7Phhkuw0Pb'
            'ak': 'RKQ9801uAsskHHarNfGNNyqUwjKC9PUS'
        }
        return params

    def parse_province(self, province):
        headers = {'User-Agent': UserAgent().random()}
        cities = requests.get(self.url, params=self.params(province), headers=headers).json().get('results')
        # print(cities)
        return cities

    def run(self, province,region=True):
        if region:
            cities = self.parse_province(province)
            for city in cities:
                city = city.get('name')
                print(city)
                self.parse_city(city)
                self.count = 0
                self.total = 1
                time.sleep(1)
        else:
            self.parse_city(province)

    def parse_city(self, city):
        headers = {'User-Agent': UserAgent().random()}
        while self.count < self.total:
            response = requests.get(self.url, params=self.params(city, self.count), headers=headers).json()
            judge = response.get('total', None)
            while judge == None:
                print(response)
                input('wait: ')
                response = requests.get(self.url, params=self.params(city, self.count), headers=headers).json()
            if int(response.get('total')) // 20 == int(response.get('total')) / 20:
                self.total = int(response.get('total')) // 20
            else:
                self.total = int(response.get('total')) // 20 + 1
            self.count += 1
            results = response.get('results')
            for result in results:
                data = {}
                data['name'] = result.get('name')
                data['address'] = result.get('address')
                data['telephone'] = result.get('telephone')
                data['province'] = result.get('province')
                data['city'] = result.get('city')
                data['area'] = result.get('area')
                data['tag'] = result.get('detail_info', {}).get('tag')
                data['detail_url'] = result.get('detail_info', {}).get('detail_url')
                data['rating'] = result.get('detail_info', {}).get('overall_rating')
                data['comment'] = result.get('detail_info', {}).get('comment_num')
                data['lat'] = result.get('location', {}).get('lat')
                data['lng'] = result.get('location', {}).get('lng')
                self.save_data(data)
            time.sleep(1)

    def save_data(self, data):
        print('第 {} 条数据 ： '.format(self.ID))
        print(data)
        row = self.ID + 1
        self.sht.range('A{row}'.format(row=row)).value = data.get('name')
        self.sht.range('B{row}'.format(row=row)).value = data.get('address')

        self.sht.range('C{row}'.format(row=row)).value = data.get('province')
        self.sht.range('D{row}'.format(row=row)).value = data.get('city')
        self.sht.range('E{row}'.format(row=row)).value = data.get('area')

        self.sht.range('F{row}'.format(row=row)).value = data.get('telephone')
        self.sht.range('G{row}'.format(row=row)).value = data.get('tag')
        self.sht.range('H{row}'.format(row=row)).value = data.get('rating')
        self.sht.range('I{row}'.format(row=row)).value = data.get('comment')
        self.sht.range('J{row}'.format(row=row)).value = data.get('lat')
        self.sht.range('K{row}'.format(row=row)).value = data.get('lng')
        self.sht.range('L{row}'.format(row=row)).value = data.get('detail_url')
        self.ID += 1

    def close(self, province):
        self.wb.save('{query}数据（{province}）.xlsx'.format(query=self.query,province=province))
        self.wb.close()
        self.app.quit()


if __name__ == '__main__':
    query='牛杂火锅店'
    kz = Spider(query)
    province = '广州市'
    kz.run(province,region=False)
    kz.close(province)
