from twython import Twython
import json
import secrets

twitter = Twython(secrets.APP_KEY, secrets.APP_SECRET,
                  secrets.OAUTH_TOKEN, secrets.OAUTH_TOKEN_SECRET)

items = []
try:
  with open("items.json") as file_in: # read all items with greater than 50 comments
    items = json.load(file_in)
  try_counter = 3
except ValueError as e: # if the json can't be read
  print e
except IOError as e: # if the file can't be found
  print e
finally: # no matter what, clear the file for the next round
  file_out = open("items.json", "w") # clear old file since scrapy doesn't overwrite for some reason
  file_out.close()

try:
  with open("recents.txt") as file_in: # read all recently tweeted item_ids, to avoid duplicates
    recents = [int(x.strip('\n')) for x in file_in.readlines()]
except IOError as e:
  print e

for item in items:
  if item['item_id'] not in recents: # if we've not already tweeted this link yet, tweet it
    status = "{0} - https://news.ycombinator.com/item?id={1}".format(item['title'], str(item['item_id']))
    # twitter.update_status(status=status)
    print "Status posted: {0}".format(status)
    recents.append(item['item_id']) # once tweeted we want to log that it happened
    if len(recents) >= 30: # we only keep the last 30 entries since only 30 appear on the page
      recents = recents[1:31] # we remove them FIFO

file_out = open("recents.txt", "w") # overwrite old file with new recently tweeted item_ids
for item_id in recents:
  file_out.write("{0}\n".format(item_id))
file_out.close()


print "testing_twitter.py run completed!" # run scripts every 15 minutes (900 seconds)
