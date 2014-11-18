import scrapy
import logging
import time
import datetime

from scraper_news.items import ScraperNewsItem

class ScraperNewsSpider(scrapy.Spider):
  name = "scraper_news"
  allowed_domains = ["news.ycombinator.com"]
  start_urls = ["https://news.ycombinator.com/"]

  def parse(self, response):
    logging.basicConfig(filename='logs.log',level=logging.DEBUG)
    logging.info("====================")
    time_now = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
    logging.info("{0} - Begin crawl".format(time_now))

    items = []

    for sel in response.xpath("//body/center/table/tr[position()=3]/td/table/tr[(position() -1) mod 3 = 0 and position() >= 1]"):
      item = ScraperNewsItem()

      num_comments = sel.xpath("following-sibling::tr[position() = 1]/td[@class=\"subtext\"]/a[last()]/text()").extract()
      if (len(num_comments) > 0):
        num_comments = num_comments[0].split(" ")
        if (len(num_comments) > 1):
          item['num_comments'] = int(num_comments[0])
        else: # no comments
          item['num_comments'] = None
      else: # no comments
        item['num_comments'] = None

      item_id = sel.xpath("following-sibling::tr[position() = 1]/td[@class=\"subtext\"]/a[last()]").re("\d+")
      if (len(item_id) > 0):
        item['item_id'] = int(item_id[0])
      else: # cannot find id
        item['item_id'] = None

      title = sel.xpath("td[@class=\"title\"]/a/text()").extract()
      if (len(title) > 0):
        item['title'] = title[0].replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c","\"").replace(u"\u201d", "\"").replace(u"\u2013", "-") # remove smart quotes and dashes
      else: # cannot find title
        item['title'] = None

      url = sel.xpath("td[@class=\"title\"]/a/@href").extract()
      if (len(url) > 0):
        if (url[:5] == 'item?'): # for self posts
          url = "https://news.ycombinator.com/" + url
        item['url'] = url
      else: # cannot find url
        item['url'] = None

      items.append(item)

    return items
