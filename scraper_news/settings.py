# -*- coding: utf-8 -*-

# Scrapy settings for scraper_news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scraper_news'

SPIDER_MODULES = ['scraper_news.spiders']
NEWSPIDER_MODULE = 'scraper_news.spiders'

# pipeline values go in ascending order, convention is 1-1000, so I set as 500 to be a good middle for future expansion
ITEM_PIPELINES = {
  'scraper_news.pipelines.ScraperNewsPipeline': 500
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'scraper_news (+http://www.twitter.com/ScraperNews)'
