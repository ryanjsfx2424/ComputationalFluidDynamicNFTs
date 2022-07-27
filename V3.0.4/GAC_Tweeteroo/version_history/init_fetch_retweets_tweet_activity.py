## init_fetch_retweets_tweet_activity.py
import os
import ast
import time
from init_auth import init_auth

CURL_BASE = "curl --request GET --url '"
CURL_HEADER = "' --header 'Authorization: Bearer "
TWITTER_API_BASE = "https://api.twitter.com/2/tweets/"

SLEEP_TIME = 60.1

def init_fetch_retweets_activity(tweet_id):
    """tweet_id should be a string"""
    print("[tweet_id]: ", [tweet_id])
    print("begin init_fetch_retweets_activity")

    os.system("mkdir -p data_big/retweets")
    fname = "data_big/retweets/activity_gac_" + tweet_id + ".txt"
    if os.path.exists(fname):
      return False
    # end if

    url  = TWITTER_API_BASE
    url += tweet_id # not for replies tho
    url += "/retweeted_by?"
    url += "user.fields=username&max_results=100&tweet.fields=public_metrics"
    
    auth = init_auth()
    os.system(CURL_BASE + url + CURL_HEADER + auth + "' > " + fname)

    with open(fname, "r") as fid:
        line = fid.read()
    # end with open
    line = ast.literal_eval(line)

    twids  = []
    unames = []

    next_token = "None"
    if "next_token" in line["meta"]:
      next_token = line["meta"]["next_token"]
    # end if

    if str(line["meta"]["result_count"]) == str(0):
      with open(fname, "w") as fid:
        fid.write("next_token: " + next_token + "\n")
        fid.write("results_count: " + str(line["meta"]["result_count"]) + "\n")
        fid.write("twitter_ids: "       + str(twids ) + "\n")
        fid.write("twitter_usernames: " + str(unames))
        return True
      # end with
    # end if

    for ii in range(len(line["data"])):
      twids.append( line["data"][ii]["id"])
      unames.append(line["data"][ii]["username"])
    # end for ii

    with open(fname, "w") as fid:
      fid.write("next_token: " + next_token + "\n")
      fid.write("results_count: " + str(line["meta"]["result_count"]) + "\n")
      fid.write("twitter_ids: "       + str(twids ) + "\n")
      fid.write("twitter_usernames: " + str(unames))
    # end with open
    print("SUCCESS init_fetch_retweets_activity")
    return True
# end init_fetch_retweets_activity

if __name__ == "__main__":
    with open("data_big/tweet_ids_gamingapeclub", "r") as fid:
        line = fid.read()
    # end with open
    tweet_ids = line.split(", ")
    tweet_ids[ 0] = tweet_ids[ 0].replace("[","")
    tweet_ids[-1] = tweet_ids[-1].replace("]","")

    for tweet_id in tweet_ids:
        tweet_id = tweet_id.replace("'","").replace('"',"")
        result = init_fetch_retweets_activity(tweet_id)
        if result:
          print("sleeping " + str(SLEEP_TIME) + "s between retweets fetches")
          time.sleep(SLEEP_TIME)
        # end if
    # end for
    print("SUCCESS init_fetch_retweets_tweet_activity")
# end if __name__ == "__main__"
## end init_fetch_retweets_tweet_activity.py
