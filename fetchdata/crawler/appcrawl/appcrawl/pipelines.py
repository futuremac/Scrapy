# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime,timedelta
from appcrawl.items import AppinfoItem
from appcrawl.items import CommentItem

class AppcrawlPipeline(object):
	def __init__(self):
		rundate=datetime.now().strftime('%Y%m%d')
		self.file = open('../../data/items.jl.'+rundate, 'wb')
	def process_item(self, item, spider):
		if isinstance(item,AppinfoItem):
			if item['appid']:
				item['appname']=item['appname'].encode('utf8')
				item['score']=item['score'].encode('utf8')
				item['desc']=item['desc'].encode('utf8')
			else:
				raise DropItem("Missing appname in %s" % item)
			self.file.write(item['appid'] + '\t' + item['appname'] + '\t' + item['download'] + '\t' +item['score'] + '\t' + item['comment'] + '\t' + item['size'] + '\t' + item['source'] +'\t'+item['desc'] + '\n')
		elif isinstance(item,CommentItem):
			if not item['appid']:
				raise DropItem("Missing appname in %s" % item)
			str_comment=item['detail'].encode('utf8')
			self.file.write(item['appid'] + '\t' + str(item['comment']) + '\t' + str_comment)

		return item
	
	def close_spider(self,spider):
		self.file.close()
