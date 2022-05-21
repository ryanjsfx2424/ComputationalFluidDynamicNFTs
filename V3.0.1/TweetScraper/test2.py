import time

import_start = time.time()
from ScrapeTweets import ScrapeTweets
print("imported in (s): ", time.time() - import_start)

instance_start = time.time()
tweet_scrape_instance = ScrapeTweets()
print("instantiated in (s): ", time.time() - instance_start)

save_start = time.time()
tweet_scrape_instance.safe_save(tweet_scrape_instance.fname_activity,
  tweet_scrape_instance.activity_by_user)
print("saved in (s): ", time.time() - save_start)
