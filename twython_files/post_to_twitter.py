"""Decides what to post to twitter on @ScraperNews.
First we read items.json to load all valid items, then read recents.txt to load all previously tweeted stories. Then for
any story that's not in recents, i.e. any story not already tweeted, we tweet it then add the story to recents to
prevent future duplicates, truncating stories to keep recents to length 30, since only 30 stories appear on the
frontpage at a time.
"""

from twython import Twython
import json
import secrets
import logging
import time
import datetime

logging.basicConfig(filename='logs.log',level=logging.DEBUG)
time_begin = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S %z")
logging.info("{} - Begin posting".format(time_begin))

twitter = Twython(secrets.APP_KEY, secrets.APP_SECRET,
                  secrets.OAUTH_TOKEN, secrets.OAUTH_TOKEN_SECRET)

items = []
try:
  with open("items.json") as file_in:
    # read all items with greater than MIN_COMMENTS comments as not dropped by pipelines.py
    items = json.load(file_in)
except ValueError as e:
  # if the json can't be read
  logging.debug("ValueError while loading items.json")
  logging.debug(e)
except IOError as e:
  # if the file can't be found
  logging.debug("IOError while loading items.json")
  logging.debug(e)
finally:
  # no matter what, clear the file for the next round to not encounter ValueErrors next time
  file_out = open("items.json", "w") # clear old file since scrapy doesn't overwrite for some reason
  file_out.close()

try:
  with open("recents.txt") as file_in:
    # read all recently tweeted item_ids to avoid duplicates
    recents = [int(x.strip('\n')) for x in file_in.readlines()]
except IOError as e:
  logging.debug("IOError while loading recents.txt")
  logging.debug(e)

for item in items:
  if item['item_id'] not in recents:
    # if we've not already tweeted this link yet, tweet it
    status = "{} - https://news.ycombinator.com/item?id={}".format(item['title'], str(item['item_id']))
    try:
      logging.info("Attempting to post status: {}".format(status))
      # this line actually tweets the story
      twitter.update_status(status=status)
      logging.info("Status posted: {}".format(status))
      # once tweeted we want to log that it happened by adding it to recents for the next iteration
      recents.append(item['item_id'])
    except Exception as e:
      logging.debug("Error posting status ({}):".format(item['item_id']))
      logging.debug(e)

recents_len = len(recents)
if recents_len >= 30:
  # we only keep the last 30 entries since only 30 appear on the page, removing them FIFO
  recents = recents[recents_len-30:]

try:
  # overwrite old file with new recently tweeted item_ids
  file_out = open("recents.txt", "w")
  for item_id in recents:
    file_out.write("{}\n".format(item_id))
  file_out.close()
except IOError as e:
  logging.debug("IOError while writing to recents.txt")
  logging.debug(e)
finally:
  time_end = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
  logging.info("{} - End posting".format(time_end))
  logging.info("====================")
