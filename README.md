Scraper News
============

Scrapes [Hacker News](https://news.ycombinator.com) and tweets ([@ScraperNews](http://twitter.com/ScraperNews)) all posts with at least 70 comments.

To run, install [scrapy](https://github.com/scrapy/scrapy) and [twython](https://github.com/ryanmcgrath/twython) (I installed them with [pip](https://github.com/pypa/pip)). You must have your own twitter handle and app ([apps.twitter.com](http://apps.twitter.com)) with your phone number attached in order to have read/write access.

Currently runs every 15 minutes with a cron job that calls a scrapy scraper to populate items.json then runs post_to_twitter.py to read the json, check against the recents queue for duplicates, then tweet any posts that have not been posted yet to [@ScraperNews](http://twitter.com/ScraperNews).

I'm more interested in posts that generate discussion than posts that could potentially get upvoted for interesting titles, which is why I chose comments instead of votes as the delimeter.
