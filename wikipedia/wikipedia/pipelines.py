# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

class WikipediaPipeline(object):
    def __init__(self):
        self.entity_file=codecs.open('f:/entity.txt','a+','utf-8')
        self.input_file=codecs.open('f:/input.txt','a+','utf-8')
    def process_item(self, item, spider):
        self.input_file.write(item['sentences']+'\r\n')
        for i in range(len(item['title'])):
            self.entity_file.write(item['title'][i]+'\t'+item['entity_id'][i]+'\r\n')
        for i in range(len(item['idd'])):
            self.entity_file.write(item['label'][i]+'\t'+item['idd'][i]+'\r\n')
    def spider_closed(self,spider):
        self.entity_file.close()
        self.input_file.close()
