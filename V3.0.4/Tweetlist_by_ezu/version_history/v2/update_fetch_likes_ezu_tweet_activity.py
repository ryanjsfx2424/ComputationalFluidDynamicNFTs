## update_fetch_likes_ezu_tweet_activity.py
import os
import ast
import time
from init_auth import init_auth

CURL_BASE = "curl --request GET --url '"
CURL_HEADER = "' --header 'Authorization: Bearer "
TWITTER_API_BASE = "https://api.twitter.com/2/tweets/"

LONG_SLEEP  = 60.1
QUICK_SLEEP =  0.1

def update_fetch_likes_activity(tweet_id):
    """tweet_id should be a string"""
    print("[tweet_id]: ", [tweet_id])
    print("begin update_fetch_likes_activity")

    fname = "data_big/likes/activity_ezu_xyz_" + tweet_id + ".txt"
    if not os.path.exists(fname):
      print("err, passed fname does not exist! Did you mean to call init instead?")
      raise
    # end if

    with open(fname, "r") as fid:
      lines = fid.readlines()
    # end with
    last_lines = lines[-4:]
    token = last_lines[0]
    token = token.split("next_token: ")[1]
    token = token.replace(" ","").replace("\n","")

    url  = TWITTER_API_BASE
    url += tweet_id # not for replies tho
    url += "/liking_users?"
    url += "user.fields=username&max_results=100&tweet.fields=public_metrics"
    url_og = url + ""
    
    auth = init_auth()

    wcnt = 0
    while token != "None":
      wcnt += 1; print("wcnt: ", wcnt)
      url = url_og + "&pagination_token=" + token

      cmd = CURL_BASE + url + CURL_HEADER + auth + "' > " + fname + "_"
      print("\n\ncmd: ", cmd)
      result = os.system(cmd)
      if result != 0:
        print("error during curl, lost wifi?")
        time.sleep(LONG_SLEEP)
        continue
      # end if

      with open(fname + "_", "r") as fid:
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
        print("result count zero")
        with open(fname, "w") as fid:
          for ll in lines:
            if ll[-1] != "\n":
              ll += "\n"
            # end if
            fid.write(ll)
          # end for
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
        if lines[-1][-1] != "\n":
          lines[-1] += "\n"
        # end if

        for ll in lines:
          fid.write(ll)
        # end for

        new_lines = ["next_token: " + next_token + "\n",
                     "results_count: " + str(line["meta"]["result_count"]) + "\n",
                     "twitter_ids: "       + str(twids ) + "\n",
                     "twitter_usernames: " + str(unames)
                    ]
        for ll in new_lines:
          fid.write(ll)
        # end for
        lines = lines + new_lines
      # end with open
      print("token old: ", [token])
      print("next_token: ", [next_token])
      token = next_token + ""

      if "None" not in token:
        print("about to sleep a minute")
        time.sleep(LONG_SLEEP)
      # end if
    # end while
    if wcnt == 0:
      return False
    # end if

    print("SUCCESS update_fetch_likes_activity")
    return True
# end update_fetch_likes_activity

if __name__ == "__main__":
    with open("data_big/tweet_ids_ezu_xyz", "r") as fid:
        line = fid.read()
    # end with open
    tweet_ids = line.split(", ")
    tweet_ids[ 0] = tweet_ids[ 0].replace("[","")
    tweet_ids[-1] = tweet_ids[-1].replace("]","")

    #tweet_ids = tweet_ids[:int(len(tweet_ids)/2)]
    for tweet_id in tweet_ids:
        tweet_id = tweet_id.replace("'","").replace('"',"")
        result = update_fetch_likes_activity(tweet_id)
        if result:
          print("sleeping a minute between likes fetches")
          time.sleep(LONG_SLEEP)
        # end if
    # end for
    print("SUCCESS update_fetch_likes_ezu_tweet_activity")
# end if __name__ == "__main__"
## end update_fetch_likes_ezu_tweet_activity.py
