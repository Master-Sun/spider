# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:26:31 2019

@author: Administrator
"""

#http://tieba.baidu.com/f?kw=%E6%A0%A1%E8%8A%B1&pn=150
#pn从0开始，每次+50

#爬取指定贴吧的图片

from lxml import etree
import requests,time

#爬取百度贴吧图片
class BaiduTB(object):
    def __init__(self):
        self.tb_baseurl = 'http://tieba.baidu.com'
        self.baseurl = 'http://tieba.baidu.com/f'
        self.headers = {'User-Agent':'Mozilla/5.0'}
    
    #获取一页中帖子链接
    def getPageUrl(self,pn,kw):
        d = {'kw':kw,'pn':str(pn)}
        res = requests.get(self.baseurl,params=d,headers=self.headers)
        res.encoding = 'utf-8'
        print(res.url)
        html = res.text
        parseHtml = etree.HTML(html)
        rList = parseHtml.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        print(rList)
    
    #获取帖子中图片的链接
    def getImgUrl(self,html):
        pass
        
    
     #保存图片
    def writeImg(self):
        pass
    
    def workOn(self):
        kw = input('请输入要爬取图片的贴吧:')
        start_page = int(input('请输入起始页:'))
        end_page = int(input('请输入终止页:'))
        for page in range(start_page,end_page+1):
            pn = (page - 1) * 50 
            self.getPageUrl(pn,kw)
    
if __name__ == '__main__':
    spider = BaiduTB()
    spider.workOn()
    
    
    
    
    
    