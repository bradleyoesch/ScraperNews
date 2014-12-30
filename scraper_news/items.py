# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScraperNewsItem(scrapy.Item):
    item_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    num_comments = scrapy.Field()
    pass
