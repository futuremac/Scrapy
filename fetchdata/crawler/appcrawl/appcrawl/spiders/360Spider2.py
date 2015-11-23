# -*- coding: utf-8 -*-
import sys 
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.spider import Spider
from scrapy.selector import Selector

from appcrawl.items import AppinfoItem
from appcrawl.items import CommentItem
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

import re
import json

class QihooSpider(Spider):
	name = "360"
	allowed_domains = ["zhushou.360.cn"]
	#start_urls = ["http://zhushou.360.cn/game/","http://zhushou.360.cn/soft/","http://zhushou.360.cn/list/hotList/cid/1","http://zhushou.360.cn/list/index/cid/2","http://zhushou.360.cn/list/index/cid/1","http://zhushou.360.cn/zhuanti/index/t/2","http://zhushou.360.cn/zhuanti/index/t/1"]
	start_urls = []
	#start_urls=["http://zhushou.360.cn/","http://zhushou.360.cn/search/index/?kw=a"]
	#start_urls=["http://zhushou.360.cn/search/index/?kw=a"]
	#rules = (
	#	Rule(LxmlLinkExtractor(allow=('detail/index/soft_id/\d+')), callback='parse_item',follow=True),
	#	#Rule(LxmlLinkExtractor(allow=('game|soft|index'))),
	#)
	
	
	def __init__(self):
		self.setSeeds()
		print len(self.start_urls)

	def setSeeds(self):
		seed_file=open('../../data/360.url','r')
		for line in seed_file:
			arr=line.strip().split('\t')
			if len(arr) != 3:
				continue
			self.start_urls.append(arr[1])
			self.start_urls.append(arr[2])
		seed_file.close()
			
	def parse(self, response):
		"""
		The lines below is a spider contract. For more info see:
		http://doc.scrapy.org/en/latest/topics/contracts.html

		@url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
		@scrapes name
		"""
		url = response.url
		if url.find('appid=') != -1:
			return  self.parse_comment(response)
		else:
			return self.parse_maininfo(response)
			

	def parse_maininfo(self,response):
		item = AppinfoItem() 

		sel = Selector(response)
		cururl=response.url
		
		pos=cururl.rfind('/')
		if pos != -1:
			item['appid'] = cururl[pos+1:]
		else:
			pass

		apps = sel.xpath('//dl[@class="clearfix"]/dd')
		
		item['appname']= apps.xpath('h2/span/text()').extract()[0]
		item['score']=apps.xpath('div/span[1]/text()').extract()[0]
		item['comment']=apps.xpath('div/span[2]/a/span/text()').extract()[0]
		item['download']=apps.xpath('div/span[3]/text()').re('\d+.*')[0]
		item['size']=apps.xpath('div/span[4]/text()').extract()[0]
		item['desc'] =sel.xpath('//div[@class="sdesc clearfix"]/div').extract()[0].replace('\n','')
		item['url'] = response.url
		item['source'] = '360'

		return item
	
	def parse_comment(self,response):
		item = CommentItem()
		pos=response.url.rfind('appid=')
		if pos != -1:
			item['appid']=response.url[pos+6:]
		comment=json.loads(response.body)
		item['comment']=comment['data']['total']
		item['detail']=str(comment['data']['messages'])

		return item
