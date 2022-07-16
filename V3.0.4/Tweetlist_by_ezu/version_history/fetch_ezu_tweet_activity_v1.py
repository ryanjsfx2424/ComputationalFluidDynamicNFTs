## fetch_ezu_tweet_activity.py
import os
import ast
import time
from init_auth import init_auth

CURL_BASE = "curl --request GET --url '"
CURL_HEADER = "' --header 'Authorization: Bearer "
TWITTER_API_BASE = "https://api.twitter.com/2/tweets/"

def fetch_activity(tweet_id):
    """tweet_id should be a string"""
    print("[tweet_id]: ", [tweet_id])

    fname = "data_big/activity_ezu_xyz_" + tweet_id + ".txt"

    url = TWITTER_API_BASE[:-1] + "?ids=" + tweet_id \
        + "&tweet.fields=public_metrics"

    auth = init_auth()
    os.system(CURL_BASE + url + CURL_HEADER + auth + "' > " + fname)

    with open(fname, "r") as fid:
        line = fid.read()
    # end with open

    pubs = '"public_metrics":{'
    if pubs not in line:
        print("public metrics not there")
        print("url: ", url)
        raise
    # end if
    line = ast.literal_eval(line)
    line["data"]["public_metrics"]

    line = line.split(pubs)[1]
    cnt_rt    = line.split('"retweet_count":')[1].split(",")[0]
    cnt_reply = line.split(  '"reply_count":')[1].split(",")[0]

    time.sleep(0.1)
    print("SUCCESS fetch_activity")
# end fetch_activity

if __name__ == "__main__":
    with open("data_big/tweet_ids_ezu_xyz", "r") as fid:
        line = fid.read()
    # end with open
    tweet_ids = line.split(", ")
    tweet_ids[ 0] = tweet_ids[ 0].replace("[","")
    tweet_ids[-1] = tweet_ids[-1].replace("]","")

    for tweet_id in tweet_ids:
        fetch_activity(tweet_id)
        break
    # end for
    print("SUCCESS fetch_ezu_tweet_activity")
# end if __name__ == "__main__"
## end fetch_ezu_tweet_activity.py