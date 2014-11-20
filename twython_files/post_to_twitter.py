from twython import Twython
import json
import secrets
import logging
import time
import datetime

logging.basicConfig(filename='logs.log',level=logging.DEBUG)

twitter = Twython(secrets.APP_KEY, secrets.APP_SECRET,
                  secrets.OAUTH_TOKEN, secrets.OAUTH_TOKEN_SECRET)

items = []
try:
  with open("items.json") as file_in: # read all items with greater than MIN_COMMENTS comments
    items = json.load(file_in)
except ValueError as e: # if the json can't be read
  logging.debug("ValueError while loading items.json")
  logging.debug(e)
except IOError as e: # if the file can't be found
  logging.debug("IOError while loading items.json")
  logging.debu(e)
finally: # no matter what, clear the file for the next round
  file_out = open("items.json", "w") # clear old file since scrapy doesn't overwrite for some reason
  file_out.close()

try:
  with open("recents.txt") as file_in: # read all recently tweeted item_ids, to avoid duplicates
    recents = [int(x.strip('\n')) for x in file_in.readlines()]
    logging.info("Length of recents: {0}".format(len(recents)))
except IOError as e:
  logging.debug("IOError while loading recents.txt")

for item in items:
  if item['item_id'] not in recents: # if we've not already tweeted this link yet, tweet it
    status = "{0}. Or is it??? - https://news.ycombinator.com/item?id={1}".format(item['title'], str(item['item_id']))
    try:
      logging.info("Attempting to post status: {0}".format(status))
      twitter.update_status(status=status)
      logging.info("Status posted: {0}".format(status))
      recents.append(item['item_id']) # once tweeted we want to log that it happened
    except Exception as e:
      logging.debug("Error posting status ({0}):".format(item['item_id']))
      logging.debug(e)

recents_len = len(recents)
if recents_len >= 30: # we only keep the last 30 entries since only 30 appear on the page
  recents = recents[recents_len-30:] # we remove them FIFO

try:
  file_out = open("recents.txt", "w") # overwrite old file with new recently tweeted item_ids
  for item_id in recents:
    file_out.write("{0}\n".format(item_id))
  file_out.close()
except IOError as e:
  logging.debug("IOError while writing to recents.txt")
  logging.debug(e)
finally:
  time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
  logging.info("{0} - End crawl".format(time))
  logging.info("====================")
