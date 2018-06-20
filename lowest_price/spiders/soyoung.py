# -*- coding: utf-8 -*-
import scrapy
import json
from lowest_price.items import LowestPriceItem


class SoyoungSpider(scrapy.Spider):
    name = "soyoung"
    allowed_domains = ["www.soyoung.com"]
    start_urls = ['http://www.soyoung.com/searchNew/product?keyword=%E4%BC%8A%E5%A9%89&cityId=1&_json=1&page_size=2000&page=1&sort=0&service=&coupon=&group=&maxprice=&minprice=']

    def parse(self, response):
        item = LowestPriceItem()
        data = json.loads(response.text)
        for info in data['responseData']['arr_product']:
            item['link'] = f"http://y.soyoung.com/cp{info['pid']}"
            item['hospital_name'] = info['hospital_name']
            item['title'] = info['title']
            item['price'] = info['price_online']
            yield item
