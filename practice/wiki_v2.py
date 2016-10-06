# -*- coding: utf-8 -*-
import scrapy
import urllib
import urllib2
import codecs
import re
from scrapy import Request
from scrapy import Selector
from wikipedia.items import *

class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["wikipedia.org"]
    start_urls = (
        'http://www.wikipedia.org/',
        'https://en.wikipedia.org/wiki/Neil_Armstrong',
    )
    entity_set=[]
    req=urllib2.Request(start_urls[1])
    init_wikipage=urllib2.urlopen(req)
    init_wikipage=init_wikipage.read().decode('utf-8')
    init_links=Selector(text=init_wikipage).xpath('//div[contains(@id,"mw-content-text")]/p/a/@href').re(r'/wiki*(.*)')
    print 'init temp link successfully'
    print "init_links:",len(init_links)
    init_links.append('/Neil_Armstrong')


    def parse_wiki(self, response):
        item=WikipediaItem()
        tem=response.selector.xpath('//div[contains(@id,"mw-content-text")]/p')
        #提取文本内容
        tem_content=tem.xpath('string(.)').extract()
        content=''.join(tem_content)
        print type(content)
        form = "\[\d*\]"
        result, number = re.subn(form, '', content)
        f_input=codecs.open('f:/input.txt','a+','utf-8')
        f_input.write(result)
        f_input.close()
        # 提取wiki info
        tem_label = response.selector.xpath('//span[@class="wikibase-title-label"]/text()').extract()
        tem_id = response.selector.xpath('//span[@class="wikibase-title-id"]/text()').extract()
        if len(tem_label)!=0:
            f_entity=codecs.open('f:/entity.txt','a+','utf-8')
            for i in range(len(tem_label)):
                f_entity.write(tem_label[i] + '\t' + tem_id[i] + '\r\n')
            f_entity.close()
        #提取entity
        tem_title = response.selector.xpath('//div[contains(@id,"mw-content-text")]/p/a[@title and starts-with(@href,"/wiki/")]/@title').extract()
        tem_link=response.selector.xpath('//div[contains(@id,"mw-content-text")]/p/a[@title and starts-with(@href,"/wiki/")]/@href').extract()
        print 'title:',len(tem_title)
        print 'href:',len(tem_link)
        for i in range(len(tem_link)):
            entity_link = "https://en.wikipedia.org" + tem_link[i]
            item['title'].append(tem_title[i])
            #print entity_link
            request=Request(entity_link,callback=self.parse_wikipage)
            request.meta['item']=item
            return request


    def start_requests(self):
        #for link in self.temp_link:
        #yield Request(self.start_urls[0]+'wiki'+self.init_links)
        return Request(self.start_urls[1],callback=self.parse_wiki)

    def parse_wikipage(self,response):
        print 'ok'
        str_cmp=response.selector.xpath('//li[@id="t-wikibase"]/a/@href').extract()[0]
        item=response.meta['item']
        item['entity_id']=[]
        if len(str_cmp)!=0:
            item['entity_id'].append(str_cmp[30:len(str_cmp)])
            if item['entity_id'][0] not in self.entity_set:
                self.entity_set.append(item['entity_id'][0])
            else:
                item['title']=[]
        return item







