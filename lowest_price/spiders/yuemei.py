# -*- coding: utf-8 -*-
import scrapy
from lowest_price.items import LowestPriceItem
import re


class YuemeiSpider(scrapy.Spider):
    name = "yuemei"
    allowed_domains = ["yuemei.com"]
    start_urls = ['https://so.yuemei.com/tao/%E4%BC%8A%E5%A9%89/p1.html']

    def parse(self, response):
        page_links = response.xpath(
            '//a[@class="taoItem _yma"]/@href').extract()
        print(page_links)
        for link in page_links:
            yield scrapy.Request(link, callback=self.parse_page)

        next_page = response.xpath(
            '//a[@class="next-page-btn"]/@href').extract_first()
        if next_page:
            next_page_url = f"https://so.yuemei.com/{next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_page(self, response):
        item = LowestPriceItem()
        item['link'] = response.url
        item['hospital_name'] = response.xpath(
            '//a[@id="HosName"]/text()').extract_first()
        item['title'] = response.xpath('//h2/text()').extract_first()
        item['price'] = self.__get_price(response)
        yield item

    def __get_price(self, response):
        price = response.xpath('//span[@class="priceNum"]//text()').extract()
        price = re.findall(r'\w+', ''.join(price))
        price.insert(1, '/')
        price = ''.join(price)
        return price
