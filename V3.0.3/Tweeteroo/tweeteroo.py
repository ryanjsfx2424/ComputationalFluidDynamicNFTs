## ScrapeTweets.py by Ryan Farber 2022-04-16 (@TheLunaLabs, @ToTheMoonsNFT)
"""
The purpose of this script is to grab all historical likes, retweets, replies,
and quote tweets of given twitter users as well as historical tweets and also
to monitor for new keywords + interactions and to assign points to users who
do so and to make this verifiable for trust-minimized web3 experience :)
"""
import os
import sys
import ast
import glob
import time
import copy
import datetime
import numpy as np
import asyncio
import discord
import snscrape.modules.twitter as sntwitter

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions import Button, ButtonStyle, ActionRow
from interactions.client import get
print("Begin ScrapeTweets")

start = time.time()
class ScrapeTweets(object):
  def __init__(self):
    self.twitter_api_base = "https://api.twitter.com/2/"

    self.curl_base = "curl --request GET --url '"
    self.curl_header = "' --header 'Authorization: Bearer "
    self.auth = os.environ["TW_BT"]

    self.max_calls_per_time_limit = 900 # 180 for keywords, 75 for Likes, 
                                        # RTs, QTs, 180 for replies

    self.api_calls = {"times": [], "buffer": 101}

    self.fsave_api_call_times = "api_call_times.txt"
    if os.path.isfile(self.fsave_api_call_times) and \
       os.stat(self.fsave_api_call_times) !=0:

      data = np.loadtxt(self.fsave_api_call_times)
      if len(data.shape) == 0:
        self.api_calls["times"] = [data.item()]
      else:
        self.api_calls["times"] = list(data)
      # end if/else
    # end if
  # end __init__

  def get_historical_tweets(self):
    """
    keyword query works. retweet one doesn't.
    """
    query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    query += " OR rootyroo OR rootroopnft OR troopsales)"
    query1 = query.replace(" ", "%20")
    query2 = "(retweets_of:rootroopnft OR retweets_of:troopsales)"
    query3 = '(url:"twitter.com/rootroopnft/status" OR "url:twitter.com/troopsales/status") is:quote'
    query4 = "(@rootroopnft OR @troopsales)"
    queries = [query1,query2,query3,query4]

    qnames = ["keywords", "retweets", "quotetweets", "mentions"]

    queries = [queries[-1]]
    qnames  = [qnames[ -1]]

    qcnt = -1
    for query in queries:
      qcnt += 1
      print("query: ", query)

      fsave = "historical_" + qnames[qcnt] + ".txt"

      cnt = 0
      data = []
      for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        cnt += 1
        if cnt % 100 == 0:
          print("cnt: ", cnt)
          with open(fsave, "w") as fid:
            fid.write(str(data))
          # end with
        # end if
        data.append(tweet)
      # end for tweets
    # end for queries
  # end get_historical_tweets

  def get_users_tweets(self):
    userids   = ["1447280926967304195", "1477912158730170370"]
    usernames = ["rootroopnft", "troopsales"]

    for ii in range(len(usernames)):
      userid   = userids[ii]
      username = usernames[ii]
      fsave_str  = "tweet_data_" + username + "_strs.txt"
      fsave_int  = "tweet_data_" + username + "_ints.txt"
      fsave_meti = "tweet_meta_" + username + "_ints.txt"
      fsave_mets = "tweet_meta_" + username + "_strs.txt"

      url = self.twitter_api_base + "users/" + userid + \
        "/tweets?tweet.fields=created_at,public_metrics&max_results=100"

      url_og = url + ""
      token = ""

      result_counts = []
      newest_ids = []
      oldest_ids = []
      next_tokens = []

      tweet_ids = []
      tweet_ids_ints = []
      tweet_contents = []
      tweet_creation_times = []
      tweet_creation_times_ints = []
      tweet_Likes = []
      tweet_Retweets = []
      tweet_QuoteTweets = []
      tweet_Replies = []

      if os.path.isfile(fsave_int) and \
         os.stat(fsave_int) !=0:

        data = np.loadtxt(fsave_int, dtype=int)
        tweet_ids_ints            = list(data[0,:])
        tweet_creation_times_ints = list(data[1,:])
        tweet_Likes               = list(data[2,:])
        tweet_Retweets            = list(data[3,:])
        tweet_QuoteTweets         = list(data[4,:])
        tweet_Replies             = list(data[5,:])
      # end if

      if os.path.isfile(fsave_str) and \
         os.stat(fsave_str) !=0:

        with open(fsave_str, "r") as fid:
          lines = fid.readlines()
        # end with open

        tweet_ids            = ast.literal_eval(lines[0])
        tweet_contents       = ast.literal_eval(lines[1])
        tweet_creation_times = ast.literal_eval(lines[2])
      # end if

      if os.path.isfile(fsave_meti) and \
         os.stat(fsave_meti) !=0:

        data = np.loadtxt(fsave_meti, dtype=int)
        print("data: ", data)
        if len(data.shape) == 1:
          result_counts = [data[0]]
          newest_ids    = [data[1]]
          oldest_ids    = [data[2]]
        else:
          result_counts = list(data[0,:])
          newest_ids    = list(data[1,:])
          oldest_ids    = list(data[2,:])
        # end if/else
      # end if

      if os.path.isfile(fsave_mets) and \
         os.stat(fsave_mets) !=0:

        with open(fsave_mets, "r") as fid:
          next_tokens = fid.read()
        # end with open
        next_tokens = ast.literal_eval(next_tokens)
        token = next_tokens[-1]
        url = url_og + "&pagination_token=" + token
      # end if

      num_loops = 0
      flag = True
      while flag:
        time.sleep(0.1) # so I can Cntrl-C
        num_loops += 1
        print("num_loops: ", num_loops)

        max_tries = 10
        request_succeeded = False
        for tcnt in range(max_tries):
          print("tcnt: ", tcnt)

          while len(self.api_calls["times"]) > self.max_calls_per_time_limit - self.api_calls["buffer"]:
            print("about to sleep a minute b/c too many recent api calls")
            time.sleep(60)
            offset = 0
            for jj in range(len(list(self.api_calls["times"]))):
              if time.time() - self.api_calls["times"][jj+offset] > 15*self.S_PER_MINUTE:
                del self.api_calls["times"][ii+offset]
                offset -= 1
              # end if
            # end for
          # end while

          result = os.system(self.curl_base + url + self.curl_header + self.auth +
                    "' --connect-timeout 30 --max-time 30 > temp.txt")
          #result = 0 # for testing

          tnow = time.time()
          self.api_calls["times"].append(tnow)
          np.savetxt(self.fsave_api_call_times, self.api_calls["times"])

          with open("temp.txt", "r") as fid:
            line = fid.read()
          # end with

          if '"status":503' not in line and '"status":443' not in line and result == 0:
            request_succeeded = True
            break
          # end if
          print("curl failed, sleeping 60s then trying again")
          time.sleep(60)
          os.system("rm temp.txt")
        # end for max_tries
        if request_succeeded == False:
          raise
        # end if

        ## okay, the request succeeded! Now to process the data
        #line = bytes(line.encode("utf-8")).decode("utf-8")
        line = ast.literal_eval(line)

        print("line: ", line)
        print("line keys: ", line.keys())
        print("len data: ", len(line["data"]))
        print("line data keys: ", line["data"][0].keys())
        print("line meta: ", line["meta"])
        print("line meta keys: ", line["meta"].keys())

        meta = line["meta"]
        result_counts.append(meta["result_count"])
        newest_ids.append(int(float(meta["newest_id"])))
        oldest_ids.append(int(float(meta["oldest_id"])))

        dcnt = 0
        for data in line["data"]:
          dcnt += 1
          if data["id"] not in tweet_ids:
            tweet_ids.append(data["id"])
            tweet_contents.append(data["text"])
            tweet_creation_times.append(data["created_at"])
            tweet_Likes.append(data["public_metrics"]["like_count"])
            tweet_Retweets.append(data["public_metrics"]["retweet_count"])
            tweet_QuoteTweets.append(data["public_metrics"]["quote_count"])
            tweet_Replies.append(data["public_metrics"]["reply_count"])

            tstr = data["created_at"].replace(".000Z","")
            ts = time.mktime(datetime.datetime.strptime(tstr, "%Y-%m-%dT%H:%M:%S").timetuple())
            tweet_creation_times_ints.append(ts)
            tweet_ids_ints.append(int(float(tweet_ids[-1])))
          # end if
        # end for data


        arr = [tweet_ids_ints, tweet_creation_times_ints, tweet_Likes, 
               tweet_Retweets, tweet_QuoteTweets, tweet_Replies]
        np.savetxt(fsave_int, arr, fmt="%i")
        
        arr = [tweet_ids, tweet_contents, tweet_creation_times]
        with open(fsave_str, "w") as fid:
          for el in arr:
            fid.write(str(el) + "\n")
          # end for
        # end with

        arr = [result_counts, newest_ids, oldest_ids]
        np.savetxt(fsave_meti, arr, fmt="%i")

        if "next_token" in meta.keys():
          next_tokens.append(meta["next_token"])
          token = next_tokens[-1]
          url = url_og + "&pagination_token=" + token
        else:
          print("next_token not found, should be done!")
          next_tokens.append("")
          flag = False
        # end if/else

        with open(fsave_mets, "w") as fid:
          fid.write(str(next_tokens) + "\n")
        # end with

        ''' For loading data:
        data = np.loadtxt(fsave_int)
        twids = data[0,:]

        with open(fsave_str, "r") as fid:
          lines = fid.readlines()
        # end with open
        twids = lines[0]
        '''
      # end while
    # end for usernames
  # end get_users_tweets
# end class ScrapeTweets

if __name__ == "__main__":
  tweet_scrape_instance = ScrapeTweets()
  #tweet_scrape_instance.get_historical_tweets()
  ## historical tweets to do: separate rootroopnft from troopsales in mentions search
  ## maybe do each keyword query individually (so I can add / remove them later)
  ## try historical RT/QT with the %20 replace thing and also check if rule is
  ## different (than for filter stream)

  tweet_scrape_instance.get_users_tweets()
# end if

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py