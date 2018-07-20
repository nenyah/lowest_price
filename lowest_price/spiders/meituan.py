# -*- coding: utf-8 -*-
import scrapy
from lowest_price.cityid import test_id
from lowest_price.items import LowestPriceItem
import re
from urllib.parse import quote

city_id = test_id


class MeituanSpider(scrapy.Spider):
    name = "meituan"
    allowed_domains = ["meituan.com"]
    root_url = 'http://apimobile.meituan.com/group/v4/poi/pcsearch/'
    KEYWORD = '伊婉'

    def start_requests(self):
        urls = []
        for cid in city_id:
            urls.append(self.make_url(cid, self.KEYWORD))
        return urls

    def parse(self, response):
        if response.status == 200:
            html = response.text
            data = re.findall(r'(\{.+\})', html)[0]
            data = json.loads(data)
            totalCount = data['data']['totalCount']
            if int(totalCount) > 0:
                real_url = response.url + f'&limit={totalCount}'
                yield scrapy.Request(real_url, callback=self.parse_detail)
        else:
            pass

    def make_url(self, city_id, keyword):
        return f'{self.root_url}{str(city_id)}?offset=0&q={quote(self.KEYWORD)}'

    def parse_datail(self, response):
        item = LowestPriceItem()
        html = response.text
        data = re.findall(r'(\{.+\})', html)[0]
        data = json.loads(data)
        infos = data['data']['searchResult']
        for info in infos:
            if info['deals'] is not None:
                for deal in info['deals']:
                    item['link'] = 'http://www.meituan.com/jiankangliren/' + \
                        str(info['id']) + '/'
                    item['hospital_name'] = info['title']
                    item['title'] = deal['title']
                    item['price'] = deal['price']
                    yield item
