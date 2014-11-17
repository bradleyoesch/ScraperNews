Scraper News
============

Scrapes Hacker News and tweets ([http://twitter.com/ScraperNews](@ScraperNews)) all posts with at least 50 comments.

To run, install [https://github.com/scrapy/scrapy](scrapy) and [https://github.com/ryanmcgrath/twython](twython) (I installed them with [https://github.com/pypa/pip](pip)). You must have your own twitter handle and app ([http://apps.twitter.com](apps.twitter.com)) with your phone number attached in order to have read/write access.

Currently runs every 15 minutes with a cron job that calls a scrapy scraper to populate items.json then runs post_to_twitter.py to read the json, checks against the recents file for duplicates, then tweets any posts that have not been posted yet to ([http://twitter.com/ScraperNews](@ScraperNews)).

I'm more interested in posts that generate discussion than posts that could potentially get upvoted for interesting titles, which is why I chose comments instead of votes as the delimeter.
