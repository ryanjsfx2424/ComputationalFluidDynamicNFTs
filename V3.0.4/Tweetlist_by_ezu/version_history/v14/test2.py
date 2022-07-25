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

keyword_query  = "(Rooty Roo OR 🦘)"# OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
#keyword_query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
#keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"
#keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales OR 🌳)"
#keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales OR 🌳🦘)"
#keyword_query += " OR \uD83C\uDF33"
#keyword_query += " OR 🌳"
#keyword_query += " OR 🌳🦘"


url  = TWITTER_API_BASE
url += tweet_id # not for replies tho
url += "/liking_users?"
url += "&user.fields=username&tweet.fields=public_metrics"

query = keyword_query.replace(" ", "%20")
url = "https://api.twitter.com/2/tweets/search/recent?query=" + query \
    + "&user.fields=username&expansions=author_id&max_results=100" \
    + "&tweet.fields=created_at"

auth = init_auth()
cmd = CURL_BASE + url + CURL_HEADER + auth + "'"# > " + "EmojiTest2.txt"
cmd = cmd.encode("utf-16", "surrogatepass").decode("utf-16")
print("cmd: ", cmd)
os.system(cmd)

