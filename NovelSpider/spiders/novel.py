# -*- coding: utf-8 -*-
import scrapy
import json
from time import time
from urllib.parse import quote
from NovelSpider.items import NovelspiderItem
novel_name='圣墟'

class NovelSpider(scrapy.Spider):
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)["data"]
        f.close()
    name = 'novel'
    web_switch = 0

    allowed_domains = ['52bqg.com','novel.luckymorning.cn']
    start_urls =['http://novel.luckymorning.cn/']

    t1 = time()
    url_main=''

    def parse(self, response):
        print("1.进入搜索")
        print("2.切换网站")
        print("0.结束")
        web_title = self.config[self.web_switch]["title"]
        i = int(input())
        if i == 1:
            print("请输入书名，默认搜索网站:%s" % web_title)
            text_temp = input()
            novel_name=text_temp
            if self.config[self.web_switch]['search_type']=='GET':
                yield scrapy.Request(self.config[self.web_switch]['start_urls'] + self.config[self.web_switch]['urls_search']+quote(text_temp.encode("gbk")),callback=self.parse_search)
            elif self.config[self.web_switch]['search_type']=='POST':
                data = {
                    self.config[self.web_switch]['post_date']: text_temp
                }
                yield  scrapy.FormRequest(
                    url=self.config[self.web_switch]['start_urls'] + self.config[self.web_switch]['urls_search'],
                    formdata=data, callback=self.parse_search)
            print()
        elif i == 2:
            j = 0
            for item in self.config:
                j += 1
                print(str(j) + "." + item["title"] )
            k = int(input())
            print("已切换至" + self.config[k - 1]["title"] )
            self.web_switch = k - 1
            self.parse(response)
        elif i == 0:
            return 0
        t2 = time()
        print("已耗时：" + str(round(t2 - self.t1)))
    def parse_search(self, response):

        url=response.xpath(self.config[self.web_switch]['search_xpath_url']).get()

        if url is None:
            print('未找到该小说')
        else:
            self.url_main=self.config[self.web_switch]['start_urls']+url
            yield scrapy.Request(self.config[self.web_switch]['start_urls']+url,callback=self.parse_page)
    def parse_page(self, response):
        print(response.body.decode(response.encoding))
        for each in response.xpath(self.config[self.web_switch]['main_xpath']):
            url = each.get()
            yield scrapy.Request(self.url_main+url,callback=self.parse_index)

    def parse_index(self, response):
        item = NovelspiderItem()
        item['title']= response.xpath(self.config[self.web_switch]['page_xpath_title']).get()
        item['txt']=''
        for each in response.xpath(self.config[self.web_switch]['page_xpath_txt']):
            item['txt']=item['txt']+each.get().replace('<br />','').replace('&nbsp;',' ').replace('\r','')
        print(item['txt'])
        if item['title'] is not None:
            yield item







