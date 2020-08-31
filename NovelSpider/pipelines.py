# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from NovelSpider.spiders.novel import novel_name

class NovelspiderPipeline(object):

    def __init__(self):
        self.filename=open(novel_name+".txt","w",encoding='utf-8')
    def process_item(self, item, spider):
        if item['title'] is None:
            pass
        else:
            self.filename.write(item['title']+"\n")
            self.filename.write(item['txt'] + "\n")
        return item
    def __del__(self):
        self.filename.close()

