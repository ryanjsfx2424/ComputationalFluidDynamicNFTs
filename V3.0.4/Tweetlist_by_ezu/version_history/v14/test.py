## init_fetch_likes_ezu_tweet_activity.py
import os
import ast
import time
from init_auth import init_auth

CURL_BASE = "curl --request GET --url '"
CURL_HEADER = "' --header 'Authorization: Bearer "
#TWITTER_API_BASE = "https://api.twitter.com/2/tweets?ids="
TWITTER_API_BASE = "https://api.twitter.com/2/tweets/"

tweet_id = "1547281103853178882"

url  = TWITTER_API_BASE
url += tweet_id # not for replies tho
url += "/liking_users?"
url += "&user.fields=username&tweet.fields=public_metrics"
    
auth = init_auth()
os.system(CURL_BASE + url + CURL_HEADER + auth + "' > " + "test3_likes.txt")

