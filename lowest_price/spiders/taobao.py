# -*- coding: utf-8 -*-
import scrapy
import re
import json
from lowest_price.items import LowestPriceItem


class TaobaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["taobao.com"]
    base_url = 'https://s.taobao.com/search?q=伊婉&bcoffset=12&s='
    offset = 0
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        data = re.findall('g_page_config = (\{.+\})', response.text)[0]
        data = json.loads(data)
        items = data['mods']['itemlist']['data']['auctions']

        for info in items:
            item = LowestPriceItem()
            item['link'] = f"https://detail.tmall.com/item.htm?id={info['nid']}"
            item['hospital_name'] = info['nick']
            item['title'] = info['raw_title']
            item['price'] = info['view_price']
            yield item

        if self.offset < 2000:
            self.offset += 44
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)
