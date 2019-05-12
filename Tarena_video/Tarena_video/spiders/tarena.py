# -*- coding: utf-8 -*-
import scrapy


class TarenaSpider(scrapy.Spider):
    # 爬虫名
    name = 'tarena'
    # 允许爬取文档域名
    allowed_domains = ['videotts.it211.com.cn']
    # 起始url地址
    start_urls = ['http://videotts.it211.com.cn/aid19010430am/aid19010430am.m3u8']

    # 解析页面，提取数据
    def parse(self, response):
        response.xpath('')
