# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class ScraperNewsPipeline(object):

  min_comments = 50

  def process_item(self, item, spider):
    if (not item['num_comments']):
      raise DropItem("No comments found.")
    elif (item['num_comments'] < self.min_comments):
      raise DropItem("Less than %d comments found, dropping item." % self.min_comments)
    elif (not item['item_id']):
      raise DropItem("No ID found.")
    elif (not item['title']):
      raise DropItem("No title found.")
    elif (not item['url']):
      raise DropItem("No url found.")
    return item
