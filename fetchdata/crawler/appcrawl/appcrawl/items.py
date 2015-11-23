# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class AppinfoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	appid=Field()
	appname=Field()
	url=Field()
	desc=Field()
	score=Field()
	comment=Field()
	comment_url=Field()
	download=Field()
	size=Field()
	source=Field()
	package_name=Field()

class CommentItem(Item):
	appid=Field()
	comment=Field()
	detail=Field()
