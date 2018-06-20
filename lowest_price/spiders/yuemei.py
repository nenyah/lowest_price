# -*- coding: utf-8 -*-
import scrapy
from lowest_price.items import LowestPriceItem
import re


class YuemeiSpider(scrapy.Spider):
    name = "yuemei"
    allowed_domains = ["yuemei.com"]
    start_urls = ['https://so.yuemei.com/tao/%E4%BC%8A%E5%A9%89/p1.html']

    def parse(self, response):
        list_info = response.xpath('//a[@class="taoItem _yma"]')
        if list_info is None:
            raise CloseSpider(reason='cancelled')

        for info in list_info:
            item = LowestPriceItem()
            item['link'] = info.xpath('./@href').extract_first()
            item['hospital_name'] = self.__get_hospital_name(info)
            item['title'] = self.__get_title(info)
            item['price'] = self.__get_price(info)
            yield item

        next_page = response.xpath(
            '//a[@class="next-page-btn"]/@href').extract_first()
        if next_page:
            next_page_url = f"https://so.yuemei.com/{next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def __get_title(self, response):
        result = response.xpath(
            './/p[@class="listInfo-item2"]/text()').extract_first().strip()

        if result is None:
            raise AttributeError('title is None')
        return result

    def __get_hospital_name(self, response):
        result = response.xpath(
            './/p[@class="listInfo-item4"]/text()').extract_first().strip()

        if result is None:
            raise AttributeError('hospital name is None')
        return result

    def __get_price(self, response):
        result = response.xpath(
            './/p[@class="ymPrice"]//text()').extract()

        if result is None:
            raise AttributeError('price is None')

        result = re.findall(r'\w+', ''.join(result))
        if len(result) > 1:
            result.insert(1, '/')
        result = ''.join(result)
        return result
