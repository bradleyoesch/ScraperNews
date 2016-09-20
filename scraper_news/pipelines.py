# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import logging

class ScraperNewsPipeline(object):

  MIN_COMMENTS = 90

  def process_item(self, item, spider):
    """Run through a several different ways the item could be dropped, namely if the item is missing any values or if
    the number of comments is less than the MIN_COMMENTS threshold. Otherwise we keep the item to test against the
    already tweeted stories in post_to_twitter.py
    """

    if not item['num_comments']:
      raise DropItem("No comments found.")
    elif item['num_comments'] < self.MIN_COMMENTS:
      raise DropItem("Less than {} comments found, dropping item.".format(self.MIN_COMMENTS))
    elif not item['item_id']:
      raise DropItem("No ID found.")
    elif not item['title']:
      raise DropItem("No title found.")
    elif not item['url']:
      raise DropItem("No url found.")

    # otherwise if we've made it this far we haven't dropped the item
    logging.basicConfig(filename='logs.log',level=logging.DEBUG)
    logging.info("Not dropped: {}".format(item['item_id']))
    return item
