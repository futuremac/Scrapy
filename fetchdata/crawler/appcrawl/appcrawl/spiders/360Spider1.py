# -*- coding: utf-8 -*-
import sys 
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.spider import Spider
from scrapy.selector import Selector

from appcrawl.items import AppinfoItem
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

import re

class QihooInitialSpider(Spider):
	name = "360initial"
	allowed_domains = ["zhushou.360.cn"]
	#start_urls = ["http://zhushou.360.cn/game/","http://zhushou.360.cn/soft/","http://zhushou.360.cn/list/hotList/cid/1","http://zhushou.360.cn/list/index/cid/2","http://zhushou.360.cn/list/index/cid/1","http://zhushou.360.cn/zhuanti/index/t/2","http://zhushou.360.cn/zhuanti/index/t/1"]
	start_urls = []
	#start_urls=["http://zhushou.360.cn/","http://zhushou.360.cn/search/index/?kw=a"]
	#start_urls=["http://zhushou.360.cn/search/index/?kw=a"]
	#rules = (
	#	Rule(LxmlLinkExtractor(allow=('detail/index/soft_id/\d+')), callback='parse_item',follow=True),
	#	#Rule(LxmlLinkExtractor(allow=('game|soft|index'))),
	#)
	
	pattern = re.compile(r'detail/index/soft_id/\d+')
	
	def __init__(self):
		self.setSeeds()
		print len(self.start_urls)

	def setSeeds(self):
		word=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		for i in xrange(100):
			for j in word:
				str="http://zhushou.360.cn/search/index/?kw=%s&page=%d" % (j,i+1)
				self.start_urls.append(str)
		char_file=open('../../data/single_char_top','r')
		for char in char_file:
			for i in xrange(100):
				for j in xrange(len(char)):	
					str="http://zhushou.360.cn/search/index/?kw=%s&page=%d" % (j,i+1)
					self.start_urls.append(str)
			
	#http://zhushou.360.cn/detail/index/soft_id/2572779
	def parse(self, response):
		"""
		The lines below is a spider contract. For more info see:
		http://doc.scrapy.org/en/latest/topics/contracts.html

		@url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
		@scrapes name
		"""
		sel = Selector(response)
		sites = sel.xpath('//@href')

		for site in sites:
			url = site.extract().strip()
			if url.find('zhushou360:') != -1:
				continue
			#print url
			curl="http://zhushou.360.cn" + url
			match=self.pattern.search(curl)
			if match:
				yield Request(curl, callback=self.parse_item)	
			
			yield Request(curl, callback=self.parse)

	def parse_item(self,response):
		item = AppcrawlItem() 

		sel = Selector(response)
		cururl=response.url
		
		pos=cururl.rfind('/')
		if pos != -1:
			end=cururl.rfind('?')
			item['appid'] = cururl[pos+1:end]
		else:
			pass

		apps = sel.xpath('//dl[@class="clearfix"]/dd')
		
		item['appname']= apps.xpath('h2/span/text()').extract()[0]
		item['score']=apps.xpath('div/span[1]/text()').extract()[0]
		item['comment']=apps.xpath('div/span[2]/a/span/text()').extract()[0]
		item['download']=apps.xpath('div/span[3]/text()').re('\d+.*')[0]
		item['size']=apps.xpath('div/span[4]/text()').extract()[0]
		item['desc'] =sel.xpath('//div[@class="sdesc clearfix"]/div/text()').extract()[0]
		item['url'] = response.url
		item['source'] = '360'
		#'baike_name': '大武侠OL Android_com.tx.wx.qihoo'
		findstr='\'baike_name\': \''
		start=response.body.find(findstr)
		if start != -1:
			end=response.body.find('\'',start+len(findstr)+1)
			#http://intf.baike.360.cn/index.php?name=&c=message&a=getmessage&start=0&count=10&_=1422875175206
			item['comment_url'] = "http://intf.baike.360.cn/index.php?name=" + response.body[start+len(findstr):end] + "&c=message&a=getmessage&start=0&count=10"

		return item
