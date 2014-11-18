# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import logging

class ScraperNewsPipeline(object):

  MIN_COMMENTS = 70

  def process_item(self, item, spider):
    if (not item['num_comments']):
      raise DropItem("No comments found.")
    elif (item['num_comments'] < self.MIN_COMMENTS):
      raise DropItem("Less than {0} comments found, dropping item.".format(self.MIN_COMMENTS))
    elif (not item['item_id']):
      raise DropItem("No ID found.")
    elif (not item['title']):
      raise DropItem("No title found.")
    elif (not item['url']):
      raise DropItem("No url found.")
    logging.basicConfig(filename='logs.log',level=logging.DEBUG)
    logging.info("Not dropped: {0}".format(item['item_id']))
    return item
