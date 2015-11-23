# -*- coding: utf-8 -*-

# Scrapy settings for appcrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'appcrawl'

SPIDER_MODULES = ['appcrawl.spiders']
NEWSPIDER_MODULE = 'appcrawl.spiders'

ITEM_PIPELINES = ['appcrawl.pipelines.AppcrawlPipeline']
LOG_LEVEL='INFO'

#DOWNLOAD_HANDLERS = {
#	'http': 'scrapyjs.dhandler.WebkitDownloadHandler',
#	'https': 'scrapyjs.dhandler.WebkitDownloadHandler',
#}

#DOWNLOADER_MIDDLEWARES = {
#	'scrapyjs.middleware.WebkitDownloader': 1,
#}

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
	'appcrawl.useragent.RotateUserAgentMiddleware' :400
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'appcrawl (+http://www.yourdomain.com)'
HTTPCACHE_ENABLED = False
HTTPCACHE_DIR = 'httpcache'
