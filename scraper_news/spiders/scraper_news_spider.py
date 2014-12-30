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
    """Parses the webpage given in start_urls.

    Logs the start time then parses each Hacker News story into a ScraperNewsItem (items.py), containing id, title, url,
    and the number of comments. Each item is appended to items and returned as an array.
    """

    logging.basicConfig(filename='logs.log',level=logging.DEBUG)
    logging.info("====================")
    time_begin = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
    logging.info("{} - Begin crawl".format(time_begin))

    # this array will be returned, each index is a ScraperNewsItem object (items.py)
    items = []

    # there are a couple extra trs at the beginning and each story is a clump of three trs, so we iterate through every
    # three trs essentially to group each story
    for sel in response.xpath("//body/center/table/tr[position()=3]/td/table/tr[(position() -1) mod 3 = 0 and position() >= 1]"):
      item = ScraperNewsItem()

      num_comments = sel.xpath("following-sibling::tr[position() = 1]/td[@class=\"subtext\"]/a[last()]/text()").extract()
      if (len(num_comments) > 0):
        # we want to isolate the number of comments from "83 comments"
        num_comments = num_comments[0].split(" ")
        if (len(num_comments) > 1):
          # if it's not something like "discuss" or a jobs post
          item['num_comments'] = int(num_comments[0])
        else:
          item['num_comments'] = None
      else:
        item['num_comments'] = None

      item_id = sel.xpath("following-sibling::tr[position() = 1]/td[@class=\"subtext\"]/a[last()]").re("\d+")
      if (len(item_id) > 0):
        item['item_id'] = int(item_id[0])
      else:
        # cannot find id
        item['item_id'] = None

      title = sel.xpath("td[@class=\"title\"]/a/text()").extract()
      if (len(title) > 0):
        # remove smart quotes and dashes that aren't unicode and mess with python printing
        item['title'] = title[0].replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c","\"").replace(u"\u201d", "\"").replace(u"\u2013", "-")
      else:
        # cannot find title
        item['title'] = None

      url = sel.xpath("td[@class=\"title\"]/a/@href").extract()
      if (len(url) > 0):
        if (url[:5] == "item?"):
          # for self posts
          url = "https://news.ycombinator.com/" + url
        item['url'] = url
      else:
        # cannot find url
        item['url'] = None

      items.append(item)

    time_end = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
    logging.info("{} - End crawl".format(time_end))

    return items
