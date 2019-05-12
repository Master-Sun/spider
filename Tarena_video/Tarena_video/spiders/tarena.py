# -*- coding: utf-8 -*-
import scrapy


class TarenaSpider(scrapy.Spider):
    name = 'tarena'
    allowed_domains = ['videotts.it211.com.cn']
    start_urls = ['http://videotts.it211.com.cn/']

    def parse(self, response):
        pass
