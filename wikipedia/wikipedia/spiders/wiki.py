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


    def parse(self, response):
        tem=response.selector.xpath('//div[contains(@id,"mw-content-text")]/p')
        #提取文本内容
        tem_content=tem.xpath('string(.)').extract()
        content=''.join(tem_content)
        print type(content)
        form = "\[\d*\]"
        result, number = re.subn(form, '', content)
        #提取entity
        tem_title = response.selector.xpath('//div[contains(@id,"mw-content-text")]/p/a[@title and starts-with(@href,"/wiki/")]/@title').extract()
        tem_link=response.selector.xpath('//div[contains(@id,"mw-content-text")]/p/a[@title and starts-with(@href,"/wiki/")]/@href').extract()
        print 'title:',len(tem_title)
        print 'href:',len(tem_link)
        entity_idd=[]
        entity_title=[]
        for i in range(len(tem_link)):
            if tem_title[i]!='':
                entity_link = "https://en.wikipedia.org" + tem_link[i]
                #print entity_link
                str_tmp=self.parse_wikipage(entity_link)
                if len(str_tmp)!=0:
                    entity_id = str_tmp[30:len(str_tmp)]
                else:
                    continue
                if entity_id not in self.entity_set:
                    self.entity_set.append(entity_id)
                    entity_idd.append(entity_id)
                    entity_title.append(tem_title[i])
        #提取wiki info
        tem_label=response.selector.xpath('//span[@class="wikibase-title-label"]/text()').extract()
        tem_id=response.selector.xpath('//span[@class="wikibase-title-id"]/text()').extract()


        item=WikipediaItem()
        item['sentences']=result
        item['entity_id']=entity_idd
        item['title']=entity_title
        item['label']=tem_label
        item['idd']=tem_id
        return item

    def start_requests(self):
        for link in self.init_links:
            yield Request(self.start_urls[0]+'wiki'+link)
        #yield Request(self.start_urls[1])

    def parse_wikipage(self,link):
        try:
            req=urllib2.Request(link)
            wiki_page=urllib2.urlopen(req)
            wiki_page = wiki_page.read().decode('utf-8')
            links = Selector(text=wiki_page).xpath('//li[@id="t-wikibase"]/a/@href').extract()
            links=links[0]
        #print links
        except Exception:
            links = []
        return links






