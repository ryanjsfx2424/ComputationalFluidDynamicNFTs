## ScrapeTweets.py by Ryan Farber 2022-04-16 (@TheLunaLabs, @ToTheMoonsNFT)
"""
I decided to switch from single scripts to an object oriented approach.

NOTE: need to loop over tokens to actually get all values!!!

NOTE: need to see if there's alt text for this meme saying roo
      https://twitter.com/metacon68/status/1515389758842626048
      (leave this for later)

NOTE: for tweets not by RooTroopNFT I should check if content says "roo"
      in it.

Priorities:
  1) loop over all tokens!
  2) if not by RooTroopNFT, skip likes + RTs
  3) outside of tweets in the troop-raids channel, blindly search for "roo"
"""
import os
import re
import ast
import glob
import time
import datetime
import numpy as np
print("Begin ScrapeTweets")

S_PER_MINUTE = 60
S_PER_HOUR   = S_PER_MINUTE * 60
S_PER_DAY    = S_PER_HOUR * 24
S_PER_MONTH  = S_PER_DAY * 31
S_PER_YEAR   = S_PER_MONTH * 12

start = time.time()
class ScrapeTweets(object):
  def __init__(self):
    '''
    just initializes some strings to reduce duplication / for convenience
    '''
    self.twitter_api_base = "https://api.twitter.com/2/tweets/"
    self.curl_base = "curl --request GET --url '"
    self.curl_header = "' --header 'Authorization: Bearer "
    self.data_dir = "twitter_data"
    self.dtypes = ["Likes", "Retweets", "QuoteTweets", "Replies"]
    self.include_text = '"includes":\{"users":\[\{'
    self.meta_text = '"meta":\{"'
    self.result_text = '"result_count":'
    self.created_text = '"created_at":"'

    self.fname_activity = self.data_dir + "/activity_by_user.json"
    self.fname_user_info = self.data_dir + "/user_info.json"

    self.special_tweeters = {"1447280926967304195":"rootroopnft", 
                             "1477912158730170370":"troopsales"}
    self.max_loops = 300 # limit == 30,000 likes, RTs (note, max 900 requests per 15 minutes
    self.continuously_scrape_sleep_time = 2 # seconds

    self.keyword_query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    self.keyword_query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    self.keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"

    ## 900 requests per 15 minutes max but likes/retweets lookup is 75 (total or each so total is 150? unclear)
    self.api_calls_struct = {"time_limit_s": 15*S_PER_MINUTE, 
                             "max_calls_per_time_limit_all": 900,
                             "max_calls_per_time_limit": {
                                                      "Tweets": 900,
                                                      "keyword": 180,
                                                      "Likes": 75,
                                                      "Retweets": 75,
                                                      "QuoteTweets": 75,
                                                      "Replies": 180,
                                                      "Users": 900},
                             "buffer_size": 7,
                             "call_times":{
                                           "Tweets": [],
                                           "keyword": [],
                                           "Likes": [],
                                           "Retweets": [],
                                           "QuoteTweets": [],
                                           "Replies": [],
                                           "Users": []
                                          },
                             "call_count":0,
                             "fname":self.data_dir + "/api_call_times.txt",
                             "fname_stats":self.data_dir + "/api_call_stats.txt"
                            }

    os.system("mkdir -p " + self.data_dir)
    if not os.path.exists(self.api_calls_struct["fname"]) or \
           os.stat(self.api_calls_struct["fname"]).st_size == 0:
      with open(self.api_calls_struct["fname"], "w") as fid:
        fid.write(str(self.api_calls_struct["call_times"]))
      # end with
    # end if

    if not os.path.exists(self.api_calls_struct["fname_stats"]) or \
       os.stat(self.api_calls_struct["fname_stats"]).st_size == 0:
      with open(self.api_calls_struct["fname_stats"], "w") as fid:
        api_call_stats = {
          "1H": 
           {
            "time_in_s": 3600.0,
            "call_times_this": [], 
            "call_times_past_sum": 0.0, 
            "call_times_past_num": 0.0,
            "call_times_past_len": []}, 
          "1D": 
           {
            "time_in_s": 3600.0*24.0,
            "call_times_this": [], 
            "call_times_past_sum": 0.0, 
            "call_times_past_num": 0.0,
            "call_times_past_len": []}, 
          "30D": 
           {
            "time_in_s": 3600.0*24.0*30.0,
            "call_times_this": [], 
            "call_times_past_sum": 0.0, 
            "call_times_past_num": 0.0,
            "call_times_past_len": []}
        }
        fid.write(str(api_call_stats))
      # end with open
    # end if
  # end __init__

  #=====================================================
  #=====================================================
  #=====================================================

  # my laptop is almost 10 years old so I assume there's some
  # malware on here now (although I still haven't lost any crypto/nfts
  # in the 5 years I've been around...), so I make it harder for bots
  #  to snoop ;)
  def init_auth(self):
    '''
    gets twitter authentication token from local file and saves to self.auth
      inputs:  none
      outputs: none
      side effects: self.auth is assigned a value.
    '''
    print("begin init_auth")
    auth_str = ""
    with open("git_ignores_me.mp4", "r") as fid:
      for line in fid:
        cur_str = line.split(" = ")[1]
        cur_str = cur_str[1:-2] # remove quotes and newline char

        auth_str += cur_str
      # end for line
    # end with open
    self.auth = auth_str

    print("success init_auth")
  # end init_auth

  #=====================================================
  #=====================================================
  #=====================================================

  def init_tweet(self, tweet_url):
    print("begin init_tweet")

    self.tweet_id = tweet_url.split("status/")[1]
    if "?" in self.tweet_id:
      self.tweet_id = self.tweet_id.split("?")[0]
    # end if

    self.creator_username = tweet_url.split("/status")[0
                                    ].split("twitter.com/")[1]

    print("success init_tweet")
  # end init_tweet

  #=====================================================
  #=====================================================
  #=====================================================

  def get_tweet_time_s(self, tweet_time):
    print("begin get_tweet_time_s")

    yy,mo,dd = tweet_time.split("-")
    dd,hh    = dd.split("T")
    hh,mi,ss = hh.split(":")
    ss = ss[:-1]
    tweet_time_s = float(yy)*S_PER_YEAR   + float(mo)*S_PER_MONTH + \
                   float(dd)*S_PER_DAY    + float(hh)*S_PER_HOUR  + \
                   float(mi)*S_PER_MINUTE + float(ss)
    return tweet_time_s

    print("success get_tweet_time_s")
  # end get_tweet_time_s

  #=====================================================
  #=====================================================
  #=====================================================

  def save_url_to_file(self, url, fname):
    print("begin save_url_to_file")

    with open(self.api_calls_struct["fname"], "r") as fid:
      self.api_calls_struct["call_times"] = ast.literal_eval(fid.read())
    # end with

    with open(self.api_calls_struct["fname_stats"], "r") as fid:
      line = fid.read()
    # end with open
    api_call_stats = ast.literal_eval(line)

    if "query=conversation_id" in url:
      dtype = "Replies"
    elif "query" in url:
      dtype = "keyword"
    elif "/liking_users?" in url:
      dtype = "Likes"
    elif "/retweeted_by?" in url:
      dtype = "Retweets"
    elif "/quote_tweets?&expansions=author_id&" in url:
      dtype = "QuoteTweets"
    elif "https://api.twitter.com/2/tweets?ids=" in url:
      dtype = "Tweets"
    elif "https://api.twitter.com/2/users/" in url:
      dtype = "Users"
    else:
      print("uhhhh url not recognized in api_calls_struct")
      print("url: ", url)
      raise
    # end if/elifs
    print("dtype: ", dtype)

    call_times = self.api_calls_struct["call_times"][dtype]
    total_calls = 0
    for key in self.api_calls_struct["call_times"].keys():
      total_calls += len(self.api_calls_struct["call_times"][key])
    # end for
    max_calls_per_time_limit = self.api_calls_struct["max_calls_per_time_limit"][dtype]

    while (len(call_times) > (max_calls_per_time_limit - \
          self.api_calls_struct["buffer_size"])) or \
          (total_calls > (self.api_calls_struct["max_calls_per_time_limit_all"] \
        - self.api_calls_struct["buffer_size"])):

      time.sleep(60.1)
      for key in self.api_calls_struct["call_times"].keys():
        call_times_loop_arr = self.api_calls_struct["call_times"][key]
        offset = 0
        for ii in range(len(call_times_loop_arr)):
          if time.time() - self.api_calls_struct["call_times"][key][ii+offset] > 15*S_PER_MINUTE:
            del self.api_calls_struct["call_times"][key][ii+offset]
            offset -= 1
          # end if
        # end for
      # end for
    # end while

    flag = True
    cnt = 0
    while flag:
      result = os.system(self.curl_base + url + self.curl_header + self.auth + 
                "' >> " + fname)
      
      with open(fname, "r") as fid:
        line = fid.read()
        if '"status":503' not in line and '"status":443' not in line \
          and result == 0:
          flag = False
          break
        # end if
      # end with
      time.sleep(60.1)
      os.system("rm " + fname)
      cnt += 1
      if cnt > 10:
        print("curl failed 10 times! crashing now")
        raise
      # end if
    # end while
    time.sleep(0.1)
    self.api_calls_struct["call_count"] += 1
    
    tnow = time.time()
    self.api_calls_struct["call_times"][dtype].append(tnow)

    for key in api_call_stats.keys():
      ## check if it's a new time unit compared to old ones...
      ## if so, we compute the avg, update sum and num flush call_times_this
      ## and then whether it's a new time unit or not we append tnow :)

      if len(api_call_stats[key]["call_times_this"]) > 0:
        
        t0 = api_call_stats[key]["call_times_this"][ 0]
        tf = api_call_stats[key]["call_times_this"][-1]
        if (tf - t0) > api_call_stats[key]["time_in_s"]:
          num_calls = len(api_call_stats[key]["call_times_this"])

          if len(api_call_stats[key]["call_times_past_len"])+1 > int(1e6)-1:
            api_call_stats[key]["call_times_past_len"] = []
          # end if

          api_call_stats[key]["call_times_past_len"].append(num_calls)
          api_call_stats[key]["call_times_past_sum"] += num_calls
          api_call_stats[key]["call_times_past_num"] += 1
        # end if
      # end if
      api_call_stats[key]["call_times_this"].append(tnow)
    # end for

    with open(self.api_calls_struct["fname"], "w") as fid:
      fid.write(str(self.api_calls_struct["call_times"]))
    # end with open    

    with open(self.api_calls_struct["fname_stats"], "w") as fid:
      fid.write(str(api_call_stats))
    # end with open

    print("success save_url_to_file")
  # end save_url_to_file

  #=====================================================
  #=====================================================
  #=====================================================

  def build_activity_from_pairs(self, pairs, activity, line):
    for key in pairs.keys():
      activity += pairs[key]

      if key in line:
        vals = line.split(key)[1:]
      else:
        vals = []
        activity += 2*" "
      # end if/else

      for val in vals:
        val = val.split('"')[0]
        activity += '"' + val + '", '
      # end for vals
      activity = activity[:-2] + '], '
    # end for
    activity = activity[:-2]
    return activity
  # end build_activity_from_pairs

  #=====================================================
  #=====================================================
  #=====================================================

  def update_user_dict(self, line):
    user_dict = {}
    # next grab user_id to username pairs
    if os.path.isfile(self.fname_user_info) and os.stat(self.fname_user_info).st_size != 0:
      with open(self.fname_user_info, "r") as fid:
        user_dict = ast.literal_eval(fid.read())
      # end with
    else:
      user_dict["userId_to_username"] = {}
      user_dict["username_to_userId"] = {}
    # end if

    user_ids = []
    usernames = []
    keys = ['"id":"', '"username":"']
    for ii, key in enumerate(keys):
      if key in line:
        vals = line.split(key)[1:]
      else:
        vals = []
      # end if/else

      for val in vals:
        val = val.split('"')[0]
        if ii == 0:
          user_ids.append(val)
        else:
          usernames.append(val)
        # end if/else
      # end for
    # end for
    for ii in range(len(usernames)):
      user_dict["userId_to_username"][ user_ids[ii]] = usernames[ii]
      user_dict["username_to_userId"][usernames[ii]] = user_ids[ii]
    # end for

    with open(self.fname_user_info, "w") as fid:
      fid.write(str(user_dict))
    # end with open
  # end update_user_dict

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_data(self, tweet_url, dtype):
    '''
    for a given tweet, fetch the users that liked, retweeted, quote-tweeted,
    or replied, and saves json response to a file for later processing.
      inputs: 
        tweet_url (type == str)
        dtype (type == str) 
          valid values == 'Likes', 'Retweets', 'QuoteTweets', 'Replies',
      outputs: none
      side effects: writes files with the responses
    '''
    print("begin fetch_data")

    self.init_tweet(tweet_url)

    fname = self.data_dir + "/" + dtype + "_" + self.creator_username + "_" + \
            self.tweet_id + ".txt"
    print("fname: ", fname)

    url = self.twitter_api_base[:-1] + "?ids=" + self.tweet_id + \
          "&tweet.fields=public_metrics"

    self.save_url_to_file(url, fname)

    url_og = self.twitter_api_base
    if dtype != "Replies":
      url_og += self.tweet_id
    # end if

    if   dtype == "Likes":
      url_og += "/liking_users?"
    elif dtype == "Retweets":
      url_og += "/retweeted_by?"
    elif dtype == "QuoteTweets":
      url_og += "/quote_tweets?&expansions=author_id&"
    elif dtype == "Replies":
      url_og += "search/recent?query=conversation_id:" + \
        self.tweet_id + "&expansions=author_id,in_reply_to_user_id&"
    else:
      print("error! expected dtype in 'likes', 'retweets' but received: ", 
            dtype)
      raise
    # end if/elif
    url_og += "user.fields=username&max_results=100&tweet.fields=public_metrics"
    url = url_og + ""

    token = ""
    loop  = True
    num_loops = 0
    while loop and num_loops < self.max_loops:
      time.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
      print("num_loops: ", num_loops)
      num_loops += 1

      self.save_url_to_file(url, fname)

      if os.stat(fname).st_size == 0:
        print("error, didn't grab any data, probably url has a bug")
        raise
      # end if

      ## check if we grabbed all of them or not
      with open(fname, "r") as fid:
        for line in fid:
          #print("line1: ", line)
          inds = [m.start() for m in re.finditer(self.meta_text, line)]
          line = line[inds[-1]:]
          print("line2: ", line)
          print("inds: ", inds)

          substr = '"next_token":"'
          if substr in line:
            ind = line.find(substr) + len(substr)
            line = line[ind:]
            token = line.split('"')[0]
            print("token: ", token)

            url = url_og + "&pagination_token=" + token
          else:
            print("substr not in line!")
            print("substr: ", substr)
            loop = False
          # end if
        # end for
      # end with
    # end while

    print("success fetch_data")
  # end fetch_data

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_activity(self, tweet_url, creation_time, update=False):
    '''
    for a given tweet, fetch the users that liked, retweeted, quote-tweeted,
    or replied and saves json response to a single file for later processing.
      inputs: tweet_url (type == str), (optional) update (type == boolean)
      outputs: none
      side effects: calls fetch_likes, fetch_retweets, fetch_quote_tweets,
        fetch_replies and generates a dictionary containing all that data
        and saves to a file. Assigns self.activity
    '''
    print("begin fetch_activity")

    self.init_tweet(tweet_url)

    fname_out = self.data_dir + "/activity_" + self.creator_username + "_" + \
                self.tweet_id + ".txt"

    if os.path.isfile(fname_out) and update == False and os.stat(fname_out).st_size != 0:
      with open(fname_out, "r") as fid:
        for line in fid:
          activity = line
          self.activity = ast.literal_eval(activity)
          print("successfully loaded existing activity")
          return
        # end for
      # end with open
    # end if

    for dtype in self.dtypes:
      if len(glob.glob(self.data_dir + "/" + dtype + "*" + self.tweet_id + ".txt")) == 0:
        self.fetch_data(tweet_url, dtype)
    # end for

    activity  = '{"' + self.tweet_id + '":{"tweet_url":"' + tweet_url + '", '
    activity += '"tweet_author_username":"' + self.creator_username   + '", '
    activity += '"tweet_created_at":"' + creation_time + '", '

    dtype = "Likes"
    fname = self.data_dir + "/" + dtype + "_" + self.creator_username \
            + "_" + self.tweet_id + ".txt"

    with open(fname, "r") as fid:
      for line in fid:
        line = line.split('"public_metrics":{')[1].split("}")[0]
        print("line: ", line)
      # end for line
    # end with open
    activity += line + "}}"
    activity = ast.literal_eval(activity)
    print("activity: ", activity)

    user_dict = {}
    if os.path.isfile(self.fname_user_info) and os.stat(self.fname_user_info).st_size != 0:
      with open(self.fname_user_info, "r") as fid:
        user_dict = ast.literal_eval(fid.read())
      # end with
    else:
      user_dict["userId_to_username"] = {}
      user_dict["username_to_userId"] = {}
    # end if

    for dtype in self.dtypes:
      print("dtype: ", dtype)
      fname = self.data_dir + "/" + dtype + "_" + self.creator_username \
              + "_" + self.tweet_id + ".txt"

      activity[self.tweet_id][dtype] = {"ids":[], "usernames":[]}
      if dtype in ["Replies","QuoteTweets"]:
        activity[self.tweet_id][dtype]["contents" ] = []
        activity[self.tweet_id][dtype]["tweet_ids"] = []
      with open(fname, "r") as fid:
        line = fid.read()
      # end with
      lines = line.split("}{")[1:]
      for line in lines:
        line = "{" + line
        if "next_token" in line:
          print("hi")
          line = line + "}"
        # end if
        vals = ast.literal_eval(line)
        print("vals.keys: ", vals.keys())
        if "data" not in vals.keys():
          continue
        # end if
        if "includes" not in vals.keys():
          for val in vals["data"]:
            print("val: ", val)
            user_id = val["id"]
            username = val["username"]
            user_dict["userId_to_username"][user_id]  = username
            user_dict["username_to_userId"][username] = user_id

            activity[self.tweet_id][dtype]["ids"].append(user_id)
            activity[self.tweet_id][dtype]["usernames"].append(username)
          # end for
        else:
          for val in vals["includes"]["users"]:
            print("includes val users: ", val)
            user_id = val["id"]
            username = val["username"]
            user_dict["userId_to_username"][user_id]  = username
            user_dict["username_to_userId"][username] = user_id
          # end for
          for val in vals["data"]:
            print("includes val data: ", val)
            tweet_id = val["id"]
            author_id = val["author_id"]
            text = val["text"]
            
            activity[self.tweet_id][dtype]["ids"].append(author_id)
            activity[self.tweet_id][dtype]["contents"].append(text)
            activity[self.tweet_id][dtype]["usernames"].append(user_dict["userId_to_username"][author_id])
            activity[self.tweet_id][dtype]["tweet_ids"].append(tweet_id)
          # end for
        # end if
      # end for lines
    # end for dtypes

    with open(self.fname_user_info, "w") as fid:
      fid.write(str(user_dict))
    # end with open

    with open(fname_out, "w") as fid:
      fid.write(str(activity))
    # end with

    self.activity = activity

    # if all that was successful, we delete the old files to keep
    # things tidy :)
    for dtype in self.dtypes:
      fname = self.data_dir + "/" + dtype + "_" + self.creator_username \
              + "_" + self.tweet_id + ".txt"
      os.system("rm " + fname)
    # end for

    print("success fetch_activity")
  # end fetch_activity

  #=====================================================
  #=====================================================
  #=====================================================

  def process_all_tweets_by_user(self, user_id, update = False):
    print("begin process_all_tweets_by_user")

    try:
      username = self.special_tweeters[user_id]
    except:
      print("error: user_id not in special tweeters!")
      raise
    # end try/except

    fname = self.data_dir + "/TweetsByUser_" + user_id + ".txt"

    if not os.path.isfile(fname) or update == True or os.stat(fname).st_size == 0:
      self.fetch_all_tweets_by_user(user_id)
    # end if

    with open(fname, "r") as fid:
      line = fid.read()
    # end with open
    line = ast.literal_eval(line)

    if "tweets_processed" in line[-1].keys():
      processed_tweets = line[-1]["tweets_processed"]
    else:
      line[-1]["tweets_processed"] = []
      processed_tweets = []
    # end if/else
    for ii in range(len(line)):
      for jj in range(len(line[ii]["data"])):
        arr = line[ii]["data"][jj]
        tweet_id = arr["id"]
        creation_time = arr["created_at"]
        text = arr["text"]

        creation_time_s = self.get_tweet_time_s(creation_time)
        if creation_time_s > line[-1]["last_tweet_time_s"]:
          line[-1]["last_tweet_time_s"] = creation_time_s
        # end if

        ## note this was for debugging and can probly remove
        print("ii, jj, twid: ", ii, jj, tweet_id)
        print("creation_time: ", creation_time)
        try:
          print("text: ", text)
        except:
          print("some bad text, maybe first two chars okay?")
          try:
            print("text2: ", text[:2])
          except:
            print("nope first two chars of text bad too oh well")
          # end try/except
        # end try/except

        ## check if we are in the refresh time window or not
        tnow = datetime.datetime.now() - datetime.timedelta(days=1)
        tnow = tnow.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        tnow = self.get_tweet_time_s(tnow)
        refresh_time = tnow

        if tweet_id in processed_tweets and creation_time_s < refresh_time:
          print("tweet_id in processed_tweets and older than 3 days, so skipping")
          continue
        # end if
        print("tweet_id not in processed_tweets")

        RT_key = "RT @"
        if RT_key == text[:len(RT_key)]:
          print("it's a RT so we skip")
          continue
        # end if
        print("not a retweet so continuing")
        #input(">>")

        tweet_url = "https://twitter.com/" + username + "/status/" + tweet_id
        self.fetch_activity(tweet_url, creation_time)
        self.process_url_activity()

        line[-1]["tweets_processed"].append(tweet_id)
        
        with open(fname, "w") as fid:
          fid.write(str(line))
        # end with open
      # end for jj
    # end for ii

    print("success process_all_tweets_by_user")
  # end process_all_tweets_by_user

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_all_tweets_by_user(self, user_id):
    print("begin fetch_all_tweets_by_user")

    username = self.special_tweeters[user_id]
    fname = self.data_dir + "/activity_" + username + ".json"

    last_tweet_time = 0
    if os.path.exists(fname) and \
        os.stat(fname).st_size != 0:
      with open(fname, "r") as fid:
        activity = fid.read()
      # end with open
      activity = ast.literal_eval(activity)

      if "last_tweet_time_s" not in activity[0].keys() or \
         "last_tweet_time_s" not in activity[-1].keys():
        for tweet_dict in activity:
          print("tweet_dict: ", tweet_dict)
          keys = tweet_dict.keys()
          for key in keys:
            if "last_tweet_time_s" == key:
              continue
            # end if

            tweet_time = self.get_tweet_time_s(tweet_dict[key]["tweet_created_at"])
            last_tweet_time = max(last_tweet_time, tweet_time)
          # end for
        # end for
        for tweet_dict in activity:
          tweet_dict["last_tweet_time_s"] = last_tweet_time
        # end for    
      # end if
      last_tweet_time = max(last_tweet_time, activity[0]["last_tweet_time_s"], activity[-1]["last_tweet_time_s"])
    # end if

    fname = self.data_dir + "/TweetsByUser" + "_" + user_id + ".txt"
    print("fname: ", fname)

    with open(fname, "r") as fid:
      line = fid.read()
    # end with open
    line = ast.literal_eval(line)

    if "last_tweet_time_s" in line[0].keys():
      last_tweet_time = max(last_tweet_time, line[0]["last_tweet_time_s"])
      if "last_tweet_time_s" in line[-1].keys():
        last_tweet_time = max(last_tweet_time, line[-1]["last_tweet_time_s"])
      # end if
    else:
      for ii in range(len(line)):
        for jj in range(len(line[ii]["data"])):
          tweet_time = self.get_tweet_time_s(line[ii]["data"][jj]["created_at"])
          last_tweet_time = max(last_tweet_time, tweet_time)
        # end for jj
      # end for ii
      line[-1]["last_tweet_time_s"] = last_tweet_time
      line[ 0]["last_tweet_time_s"] = last_tweet_time
    # end if/else

    url = self.twitter_api_base[:-len("tweets/")] + "users/" + user_id + \
          "/tweets?tweet.fields=created_at&max_results=100"

    ## first we let it check for new tweets (possibly going all the way back)
    url_og = url + ""
    token = ""
    loop  = True
    num_loops = 0
    newest_tweet_time = 0
    while loop and num_loops < self.max_loops:
      time.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
      print("num_loops: ", num_loops)
      num_loops += 1

      os.system("rm -f temp.txt")
      self.save_url_to_file(url, "temp.txt")

      if os.stat(fname).st_size == 0:
        print("error, didn't grab any data, probably url has a bug")
        raise
      # end if

      with open("temp.txt", "r") as fid:
        line = fid.read()
      # end with
      line = ast.literal_eval(line)
      print(line.keys())

      recent_tweet_time = self.get_tweet_time_s(line["data"] [0]["created_at"])
      oldest_tweet_time = self.get_tweet_time_s(line["data"][-1]["created_at"])

      if oldest_tweet_time > recent_tweet_time: # switch 'em! (+0 ensures pass by val not by ref)
        temp = oldest_tweet_time + 0
        oldest_tweet_time = recent_tweet_time + 0
        recent_tweet_time = temp + 0
      # end if

      newest_tweet_time = max(last_tweet_time, recent_tweet_time, newest_tweet_time)

      print("last_tweet_time: ", last_tweet_time)
      print("recent_tweet_time: ", recent_tweet_time)
      print("oldest_tweet_time: ", oldest_tweet_time)
      print("newest_tweet_time: ", newest_tweet_time)
      #input(">>")

      if recent_tweet_time <= last_tweet_time and oldest_tweet_time < last_tweet_time:
        print("recent_tweet_time older than (or equal to) last saved tweet and oldest_tweet is too! Done here")
        break
      # end if

      with open(fname, "r") as fid:
        line_old = fid.read()
      # end with
      line_old = ast.literal_eval(line_old)

      if recent_tweet_time > last_tweet_time: # add tweets to file
        ## note that it's okay if we repeat some tweets since we check tweet_ids to
        ## avoid double processing later
        line_old[-1]["last_tweet_time_s"] = newest_tweet_time
        line_old[ 0]["last_tweet_time_s"] = newest_tweet_time
        new_line = "[" + str(line) + "," + str(line_old)[1:]

        with open(fname, "w") as fid:
          fid.write(new_line)
        # end with open
      # end if

      if oldest_tweet_time < last_tweet_time:
        print("oldest_tweet_time older than last tweet, time to break!")
        break
      # end if

      # otherwise keep going, find next_token
      ## first delete temp.txt

      os.system("rm -f temp.txt")

      if "next_token" in line["meta"].keys():
        token = line["meta"]["next_token"]
        url = url_og + "&pagination_token=" + token
      else:
        print("next_token not in line!")
        loop = False
        break
      # end if/else
    # end while

    ## then we check for old tweets
    ## first, grab the oldest tweet id
    with open(fname, "r") as fid:
      line = fid.read()
    # end with
    line = ast.literal_eval(line)

    oldest_line_num_ii = int(1e30)
    oldest_line_num_jj = int(1e30)
    oldest_tweet_id    = int(1e30)

    for ii in range(len(line)):
      for jj in range(len(line[ii]["data"])):
        tweet_id = int(float(line[ii]["data"][jj]["id"]))
        if tweet_id < oldest_tweet_id:
          oldest_line_num_ii = ii
          oldest_line_num_jj = jj
        # end if
      # end for jj
    # end for ii

    ## now we do a while loop
    url = self.twitter_api_base[:-len("tweets/")] + "users/" + user_id + \
          "/tweets?tweet.fields=created_at&max_results=100"
    url_og = url + ""
    token = ""
    loop  = True
    num_loops = 0
    newest_tweet_time = 0

    ## check if it exists first!
    if "next_token" in line[oldest_line_num_ii]["meta"].keys():
      token = line[oldest_line_num_ii]["meta"]["next_token"]
      url = url_og + "&pagination_token=" + token

      while loop and num_loops < self.max_loops:
        time.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
        print("num_loops: ", num_loops)
        num_loops += 1

        self.save_url_to_file(url, fname)

        if os.stat(fname).st_size == 0:
          print("error, didn't grab any data, probably url has a bug")
          raise
        # end if

        # otherwise keep going, find next_token
        ## first delete temp.txt

        with open(fname, "r") as fid:
          line = fid.read()
        # end with open
        line = ast.literal_eval(line)
        
        if "next_token" in line[-1]["meta"].keys():
          token = line["meta"]["next_token"]
          url = url_og + "&pagination_token=" + token
        else:
          print("next_token not in line!")
          loop = False
          break
        # end if/else
      # end while
    # end if

    os.system("rm -f temp.txt")
    print("success fetch_all_tweets_by_user")
  # end fetch_all_tweets_by_user

  #=====================================================
  #=====================================================
  #=====================================================

  def process_url_activity(self):
    print("begin process_url_activity")

    if os.path.exists(self.fname_activity) and \
       os.stat(self.fname_activity).st_size != 0:
      with open(self.fname_activity, "r") as fid:
        activity_by_user = fid.read()
      # end with open
      activity_by_user = ast.literal_eval(activity_by_user)
    else:
      print("data corruption? Something went wrong. Please contant Ryan.")
      raise
    # end if/else

    with open(self.fname_user_info, "r") as fid:
      user_dict = ast.literal_eval(fid.read())
    # end with

    fs = glob.glob(self.data_dir + "/activity_*.txt")
    for fname in fs:
      with open(fname, "r") as fid:
        for line in fid:
          pass
        # end for line
      # end with open
      activity_by_url = ast.literal_eval(line)
      tweet_id = list(activity_by_url.keys())[0]
      tweet_creation_time = activity_by_url[tweet_id]["tweet_created_at"]

      for dtype in self.dtypes:
        data = activity_by_url[tweet_id][dtype]
        for ii,user_id in enumerate(data["ids"]):
          if user_id not in list(activity_by_user.keys()):
            activity_by_user[user_id] = \
              {"usernames": [],
               "num_keyword_replies": 0,
               "num_keyword_retweets": 0,
               "tweet_ids": [],
               "tweet_contents": [],
               "tweet_creation_times": [],
               "Likes": {"num_Likes": 0, "tweet_ids": [], "tweet_creation_times": []},
               "Retweets": {"num_Retweets": 0, "tweet_ids": [], "tweet_creation_times": []},
               "QuoteTweets": {"num_QuoteTweets": 0, "tweet_ids": [], "tweet_creation_times": [], "tweet_contents": []},
               "Replies": {"num_Replies": 0, "tweet_ids": [], "tweet_creation_times": [], "tweet_contents": []}
              }
          # end if
          if tweet_id not in activity_by_user[user_id]["tweet_ids"]:
            activity_by_user[user_id]["tweet_ids"].append(tweet_id)
          # end if
          activity_by_user[user_id]["usernames"].append(user_dict["userId_to_username"][user_id])

          if dtype not in activity_by_user[user_id].keys():
            activity_by_user[user_id][dtype] = {"num_"+dtype: 1, "tweet_ids":[tweet_id], "tweet_creation_times":[tweet_creation_time]}
            if dtype in ["QuoteTweets", "Replies"]:
              activity_by_user[user_id][dtype]["tweet_contents"] = [data["contents"][ii]]
              activity_by_user[user_id][dtype]["tweet_ids"] = [data["tweet_ids"][ii]]
            # end if
          else:
            if tweet_id not in activity_by_user[user_id][dtype]["tweet_ids"]:
              print("user_id: ", user_id)
              print("act keys: ", activity_by_user[user_id].keys())
              print("dtype: ", dtype)
              activity_by_user[user_id][dtype]["num_"+dtype] += 1
              activity_by_user[user_id][dtype]["tweet_ids"].append(tweet_id)
              activity_by_user[user_id][dtype]["tweet_creation_times"].append(tweet_creation_time)
              if dtype in ["QuoteTweets", "Replies"]:
                activity_by_user[user_id][dtype]["tweet_contents"].append(data["contents"][ii])
                activity_by_user[user_id][dtype]["tweet_ids"][-1] = data["tweet_ids"][ii]
              # end if
            # end if
          # end if/else
        # end for user_ids
      # end for dtypes
      fname2 = fname.split("_")
      fname2 = fname2[0] + "_" + fname2[1] + "_" + fname2[2] + ".json"

      line2 = ""

      if os.path.exists(fname2) and \
       os.stat(fname2).st_size != 0:
        with open(fname2, "r") as fid:
          line2 = fid.read()
        # end with
      # end if

      if line not in line2:
        with open(fname2, "w") as fid:
          if len(line2) == len(""):
            line = "[" + line + "]"
          else:
            line = line2[:-1] +"," + line + "]"
          # end if/else
          fid.write(line)
        # end with
      # end if
      os.system("rm " + fname)
    # end for fnames
    
    with open(self.fname_activity, "w") as fid:
      fid.write(str(activity_by_user))
    # end with open

    print("success process_url_activity")
  # end process_url_activity

  #=====================================================
  #=====================================================
  #=====================================================

  def handle_url_activity(self, urls):
    if type(urls) == type([]):
      for url in urls:
        self.fetch_activity(url)
        self.process_url_activity()
      # end for
    else:
      self.fetch_activity(urls)
      self.process_url_activity()
    # end if/else
  # end handle_url_activity

  #=====================================================
  #=====================================================
  #=====================================================

  def update_keyword_data(self):
    print("begin update_keyword_data")

    activity_by_user = {"latest_tweet_time_s":0}
    fname_activity = self.data_dir + "/activity_by_user.json"
    if os.path.exists(fname_activity) and \
       os.stat(fname_activity).st_size != 0:
      with open(self.data_dir + "/activity_by_user.json", "r") as fid:
        activity_by_user = fid.read()
      # end with open
      activity_by_user = ast.literal_eval(activity_by_user)
    # end if

    dtime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    fname = self.data_dir + "/" + dtime + "_keyword_data.txt"
    
    #query  = "(Rooty Roo OR Rooty OR Rooty Woo OR rootywoo OR Roo Troop OR"
    #query += " rootroop OR rootroops OR tree roo OR Roo Roo)"
    #query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    #query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    #query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"
    query = self.keyword_query.replace(" ", "%20")
    url_og = "https://api.twitter.com/2/tweets/search/recent?query=" + query \
           + "&user.fields=username&expansions=author_id&max_results=100" \
           + "&tweet.fields=created_at"

    url = url_og + ""
    token = ""
    loop  = True
    num_loops = 0
    while loop and num_loops < self.max_loops:
      time.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
      print("num_loops: ", num_loops)
      num_loops += 1

      self.save_url_to_file(url, fname)

      if os.stat(fname).st_size == 0:
        print("error, didn't grab any data, probably url has a bug")
        raise
      # end if

      ## check if we grabbed all of them up to last tweet fetched or not
      with open(fname, "r") as fid:
        for line in fid:
          #print("line1: ", line)
          inds = [m.start() for m in re.finditer(self.created_text, line)]
          latest_tweet = line[inds[-1] + len(self.created_text):].split('"')[0]
          latest_tweet_s = self.get_tweet_time_s(latest_tweet)

          if latest_tweet_s < activity_by_user["latest_tweet_time_s"]:
            loop = False
            break
          # end if

          inds = [m.start() for m in re.finditer(self.meta_text, line)]
          line = line[inds[-1]:]
          print("line2: ", line)
          print("inds: ", inds)

          substr = '"next_token":"'
          if substr in line:
            ind = line.find(substr) + len(substr)
            line = line[ind:]
            token = line.split('"')[0]
            print("token: ", token)

            url = url_og + "&pagination_token=" + token
          else:
            print("substr not in line!")
            print("substr: ", substr)
            loop = False
          # end if
        # end for
      # end with
    # end while

    activity_by_user["query_url"] = url_og
    with open(fname_activity, "w") as fid:
      fid.write(str(activity_by_user))
    # end with open

    print("success update_keyword_data")
  # end update_keyword_data

  #=====================================================
  #=====================================================
  #=====================================================

  def process_keyword_data(self):
    print("begin process_keyword_data")

    activity_by_user = {"latest_tweet_time_s":0}
    fname_activity = self.data_dir + "/activity_by_user.json"
    if os.path.exists(fname_activity) and \
       os.stat(fname_activity).st_size != 0:
      with open(self.data_dir + "/activity_by_user.json", "r") as fid:
        activity_by_user = ast.literal_eval(fid.read())
      # end with open
    # end if

    ## needs to be oldest to most recent
    fs = np.sort(glob.glob(self.data_dir + "/*_keyword_data.txt"))

    for fname in fs:
      print("fname: ", fname)
      #sys.exit()
      with open(fname, "r") as fid:
        line = fid.read()
      # end with open
      try:
        line = ast.literal_eval(line)
      except:
        line = "[" + line + "]"
        line = line.replace("}{", "},{")
        line = ast.literal_eval(line)
      # end try/except
      if type(line) != type([]):
        line = [line]
      # end if

      latest_tweet_s = 0.0
      for ii in range(len(line)):
        for jj in range(len(line[ii]["data"])):
          tweet_time = self.get_tweet_time_s(line[ii]["data"][jj]["created_at"])
          latest_tweet_s = max(latest_tweet_s, tweet_time)
        # end for
      # end for

      if activity_by_user["latest_tweet_time_s"] >= latest_tweet_s:
        print("skipping")
        os.system("rm " + fname)
        continue
      # end if

      user_ids  = []
      usernames = []
      for ii in range(len(line)):
        for jj in range(len(line[ii]["includes"]["users"])):
          user_ids.append(line[ii]["includes"]["users"][jj]["id"])
          usernames.append(line[ii]["includes"]["users"][jj]["username"])
        # end for jj
      # end for ii

      user_ids_to_usernames = {}
      for ii in range(len(user_ids)):
        user_ids_to_usernames[user_ids[ii]] = usernames[ii]
      # end for ii

      tweet_ids = []
      contents  = []
      creations = []
      author_ids = []

      for ii in range(len(line)):
        for jj in range(len(line[ii]["data"])):
          tweet_ids.append(line[ii]["data"][jj]["id"])
          contents.append( line[ii]["data"][jj]["text"])
          creations.append(line[ii]["data"][jj]["created_at"])
          author_ids.append(line[ii]["data"][jj]["author_id"])
        # end for
      # end for

      latest_creation_time = np.sort(np.array(creations))[-1]
      latest_creation_time_s = self.get_tweet_time_s(latest_creation_time)
      activity_by_user["latest_tweet_time"] = latest_creation_time
      activity_by_user["latest_tweet_time_s"] = latest_creation_time_s

      for ii,author_id in enumerate(author_ids):
        if author_id not in list(activity_by_user.keys()):
          activity_by_user[author_id] = \
            {"usernames": [],
             "num_keyword_replies": 0,
             "num_keyword_retweets": 0,
             "tweet_ids": [],
             "tweet_contents": [],
             "tweet_creation_times": []
            }
        # end if

        user_dict = activity_by_user[author_id]
        if tweet_ids[ii] in user_dict:
          print("tweet_id in user_dict?")
          continue
        # end if

        if contents[ii][:2] == "RT":
          user_dict["num_keyword_retweets"] += 1
        else:
          user_dict["num_keyword_replies"] += 1
        # end if/else

        user_dict["usernames"].append(user_ids_to_usernames[author_id])
        user_dict["tweet_ids"].append(tweet_ids[ii])
        user_dict["tweet_contents"].append(contents[ii])
        user_dict["tweet_creation_times"].append(creations[ii])
      # end for ii
      with open(fname_activity, "w") as fid:
        fid.write(str(activity_by_user))
      # end with open
      os.system("rm " + fname)
    # end for fnames

    print("success process_keyword_data")
  # end process_keyword_data

  #=====================================================
  #=====================================================
  #=====================================================

  def generate_activity_tweet_urls(self):
    print("begin generate_activity_tweet_urls")
    ## load in activity_by_user.json and generate from the tweet_id + username
    print("success generate_activity_tweet_urls")
  # end generate_activity_tweet_urls

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_user_leaderboard(self, start_time="2020-05-04T23:59:59.000Z", 
    end_time="4022-05-04T23:59:59.000Z", method="Points"):
    print("begin fetch_user_leaderboard")
    self.init_auth()

    start_time_s = self.get_tweet_time_s(start_time)
    end_time_s   = self.get_tweet_time_s(end_time)

    with open(self.data_dir + "/activity_by_user.json", "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    keyword_replies  = []
    keyword_retweets = []
    usernames = []
    contents  = []
    tweet_ids = []

    num_dict = {"num_Likes":[],
                "num_Retweets":[],
                "num_QuoteTweets":[],
                "num_Replies":[]}
    for user in activity_by_user.keys():
      if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
        continue
      # end if
      for dtype in self.dtypes:
        if dtype in activity_by_user[user].keys():
          cnt = 0
          for tweet_time in activity_by_user[user][dtype]["tweet_creation_times"]:
            tweet_time = self.get_tweet_time_s(tweet_time)
            if tweet_time >= start_time_s and tweet_time <= end_time_s:
              cnt += 1
            # end if
          # end for
          num_dict["num_"+dtype].append(cnt)
        else:
          num_dict["num_"+dtype].append(0)
        # end if/else
      # end for
      print(activity_by_user[user])
      print(user)
      replies_cnt = 0
      retweets_cnt = 0
      for ii in range(len(activity_by_user[user]["tweet_contents"])):
        tweet_content = activity_by_user[user]["tweet_contents"][ii].lower()

        ## below if statement to exclude LuckyRooToken tweets...or we
        ## could just check for whitelisted users???
        if "#luckyroo" in tweet_content or "@luckyr" in tweet_content or \
           "#saita" in tweet_content or "@saita" in tweet_content or \
           "promote it on" in tweet_content: # last one to filter out spam bots
          continue
        # end if

        tweet_id = activity_by_user[user]["tweet_ids"][ii]
        if tweet_id in tweet_ids:
          continue
        # end if
        tweet_ids.append(tweet_id)

        tweet_time = activity_by_user[user]["tweet_creation_times"][ii]
        tweet_time = self.get_tweet_time_s(tweet_time)
        if tweet_time >= start_time_s and tweet_time <= end_time_s:
          if activity_by_user[user]["tweet_contents"][ii][:2] == "RT":
            retweets_cnt += 1
          else:
            replies_cnt += 1
            #print("inc replies_cnt")
          # end if/else
        # end if
      # end for

      #print("replies_cnt: ", replies_cnt)
      #input(">>")
      keyword_replies.append(replies_cnt)
      keyword_retweets.append(retweets_cnt)
      usernames.append(activity_by_user[user]["usernames"][-1])
      for content in activity_by_user[user]["tweet_contents"]:
        contents.append(content)
      # end for
    # end for

    keyword_replies = np.array(keyword_replies)
    keyword_retweets = np.array(keyword_retweets)
    num_Likes = np.array(num_dict["num_Likes"])
    num_Retweets = np.array(num_dict["num_Retweets"])
    num_QuoteTweets = np.array(num_dict["num_QuoteTweets"])
    num_Replies = np.array(num_dict["num_Replies"])

    points = keyword_replies*3 + num_Retweets*2 + keyword_retweets*2 + \
             num_Likes*1 + num_QuoteTweets*4 + num_Replies*3

    usernames = np.array(usernames)

    if   method == "Points":
      inds = np.argsort(points)[::-1]
      val = points
    elif method == "Likes":
      inds = np.argsort(num_Likes)[::-1]
      val = num_Likes
    elif method == "Retweets":
      inds = np.argsort(num_Retweets)[::-1]
      val = num_Retweets
    elif method == "QuoteTweets":
      inds = np.argsort(num_QuoteTweets)[::-1]
      val = num_QuoteTweets
    elif method == "Replies":
      inds = np.argsort(num_Replies)[::-1]
      val = num_Replies
    elif method == "keyword_replies":
      inds = np.argsort(keyword_replies)[::-1]
      val = keyword_replies
    elif method == "keyword_retweets":
      inds = np.argsort(keyword_retweets)[::-1]
      val = keyword_retweets
    # end if/elifs

    inds = inds[:20]
    leaderboard = ""
    for ii in range(len(inds)):
      leaderboard += str(ii) + ") " + usernames[inds][ii] + ": " + str(val[inds][ii])
      leaderboard += "\n"
      print(str(ii) + ") " + usernames[inds][ii] + ": ", val[inds][ii])
    # end for ii
    print("num usernames: ", len(usernames))
    print("num tweets: ", np.sum(keyword_replies) + np.sum(keyword_retweets) + \
          np.sum(num_dict["num_Replies"]) + np.sum(num_dict["num_QuoteTweets"]))
    print("method: ", method)

    #for ii in range(20):
    #  ind = np.random.randint(len(contents))
    #  print("\n" + contents[ind])
    ## end for ii

    ## note, this errors sometimes with a utf-8 issue so I guess
    ## sometimes it gets passes some dumb emoji :)
    #with open(self.data_dir + "/queryed_tweets.txt", "w") as fid:
    #  for ii in range(len(contents)):
    #    fid.write(contents[ii] + "\n\n")
      # end for line
    # end with open

    fname = self.data_dir + "/leaderboard_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
    tnow = datetime.datetime.now()
    tnow = tnow.strftime("%Y-%m-%d_%H:%M:%S")
    with open(fname, "w") as fid:
      fid.write("last updated: " + tnow + "\n")
      fid.write(leaderboard)
    # end with

    print("success fetch_user_leaderboard")
    return leaderboard
  # end fetch_user_leaderboard

  #=====================================================
  #=====================================================
  #=====================================================
  #=====================================================

  def verify_processed_tweet(self, tweet_url, username):
    self.init_tweet(tweet_url)

    with open(self.fname_activity, "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    print("tw_id: ", self.tweet_id)

    flag = False
    user_id = ""
    for user in activity_by_user.keys():
      if user[0].isdigit():
        for stored_username in activity_by_user[user]["usernames"]:
          if username.lower() == stored_username.lower():
            user_id = user
            flag = True
            break
          # end if
        # end for
      # end if
      if flag:
        break
      # end if
    # end for
    print("user_id: ", user_id)

    message  = "We don't recongize that username. If you're new to twitter\n"
    message += "then please try again in a few minutes. Or if you changed\n"
    message += "your username, try your old one (or send a keyword tweet\n"
    message += "with the new username and your profiles will automatically\n"
    message += "be merged. Anyway, I'm just a dumb bot so please send this message\n"
    message += "to ryanjsfx.eth|ToTheMoonsNFT|Luna#3479 on discord, @TheLunaLabs on Twitter\n"
    message += "or raise an issue at github.com/ryanjsfx2424/ComputationalFluidDynamicNFTs\n"
    message += "and my creator should look into this within 24-48H\n"
    message += "(or if at NFT NYC or similar maybe a week)."

    if user_id != "":
      print("user: ", activity_by_user[user_id])
      print("user twids: ", activity_by_user[user_id]["tweet_ids"])
      print("twid: ", self.tweet_id)
      print("twid in user twids: ", self.tweet_id in activity_by_user[user_id]["tweet_ids"])
      if self.tweet_id in activity_by_user[user_id]["tweet_ids"]:
        message = "SUCCESS! Your tweet was already processed :)"
        print(message)
        return [message,True]
      # end if
    # end if
        
    url = self.twitter_api_base[:-1] + "?ids=" + self.tweet_id \
        + "&tweet.fields=created_at"

    os.system(self.curl_base + url + self.curl_header + self.auth + 
              "' > " + "delete_me.txt")

    with open("delete_me.txt", "r") as fid:
      line = fid.read()
    # end with open

    print("self created_text: ", self.created_text)
    print("line: ", line)
    print("line split self created_text: ", line.split(self.created_text))
    tweet_time = line.split(self.created_text)[1].split('"')[0]
    tweet_time_s = self.get_tweet_time_s(tweet_time)

    if activity_by_user["latest_tweet_time_s"] < tweet_time_s:
      message = "This tweet created after last query was made"
      print(message)
      return [message,False]
    # end if

    print(message)
    return [message,False]
  # end verify_processed_tweet

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_user_data(self, username):
    with open(self.fname_activity, "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    for user in activity_by_user.keys():
      if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
        continue
      # end if
      for stored_username in activity_by_user[user]["usernames"]:
        if username.lower() == stored_username.lower():
          return activity_by_user[user]
      
        # end if
      # end for
    # end for
    err = "Error! Couldn't find that username."
    print(err)
    return err
  # def fetch_user_data

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_user_points(self, user_data):
    ## uses result of fetch_user_data above

    num_dict = {"num_Likes":0,
                "num_Retweets":0,
                "num_QuoteTweets":0,
                "num_Replies":0,
                "num_keyword_retweets":0,
                "num_keyword_replies":0}
    for dtype in self.dtypes:
      if dtype in user_data.keys():
        num_dict["num_"+dtype] = user_data[dtype]["num_" + dtype]
      # end if
    # end for

    keyword_replies  = 0
    keyword_retweets = 0
    for tweet_content in user_data["tweet_contents"]:
      tweet_content.lower()

      ## below if statement to exclude LuckyRooToken tweets...or we
      ## could just check for whitelisted users???
      if "#luckyroo" in tweet_content or "@luckyr" in tweet_content or \
         "#saita" in tweet_content or "@saita" in tweet_content or \
         "promote it on" in tweet_content: # last one to filter out spam bots
        continue
      # end if

      if tweet_content[:2] == "RT".lower():
        keyword_retweets += 1
      else:
        keyword_replies += 1
      # end if/else

      num_dict["num_keyword_replies"] = keyword_replies
      num_dict["num_keyword_retweets"] = keyword_retweets
    # end for

    points = num_dict["num_keyword_replies" ]*3 + num_dict["num_Retweets"]*2 \
           + num_dict["num_keyword_retweets"]*2 + num_dict["num_Likes"]*1 \
           + num_dict["num_QuoteTweets"]*4 + num_dict["num_Replies"]*3
    
    message  = "Points: " + str(points) + "\n"
    message += "Likes: " + str(num_dict["num_Likes"]) + "\n"
    message += "Retweets: " + str(num_dict["num_Retweets"]) + "\n"
    message += "QuoteTweets: " + str(num_dict["num_QuoteTweets"]) + "\n"
    message += "Replies: " + str(num_dict["num_Replies"]) + "\n"
    message += "num_keyword_replies: " + str(num_dict["num_keyword_replies"]) + "\n"
    message += "num_keyword_retweets: " + str(num_dict["num_keyword_retweets"]) + "\n\n"
    message += "Note that points are computed as Likes + Retweets*2 + keyword_retweets*2 + Replies*3 + keyword_replies*3 + QuoteTweets*4\n"
    message += "where Likes,Retweets,Replies,QuoteTweets are interactions with @RooTroopNFT and/or @TroopSales, while keyword_replies (misnomer, includes if you start the tweet) and keyword_retweets use the keyword search. Use 'rtt keywords' for more info on those.\n\n"

    print("SUCCESS fetch_user_points")
    return message
  # end fetch_user_points

  #=====================================================
  #=====================================================
  #=====================================================

  def continuously_scrape(self):
    self.init_auth()
    cs_start = time.time()
    reset_time = time.time()

    while True:
      loop_start = time.time()
      self.update_keyword_data()
      self.process_keyword_data()

      if reset_time - time.time() > 5*60:
        for user_id in self.special_tweeters.keys():
          if self.special_tweeters[user_id] == "troopsales":
            continue
          print(user_id)
        #input(">>")
        #continue
        self.process_all_tweets_by_user(user_id, update=True)
      # end for

      msg1 = "last loop executed in: " + str(time.time() - loop_start)
      msg2 = "time since continuous scraping started: " + str(time.time() - cs_start)
      msg3 = "current date/time: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S"))
      print("\n\n\n\n\n\n\n\n" + msg1)
      print(msg2)
      print(msg3 + "\n\n\n\n\n\n\n\n")

      fname = self.data_dir + "/continuous_scrape_times.txt"
      with open(fname, "a") as fid:
        fid.write(msg1 + "\n")
        fid.write(msg2 + "\n")
        fid.write(msg3 + "\n")
      # end with

      #break
      time.sleep(self.continuously_scrape_sleep_time)
    # end while
  # end def continuously_scrape

  #=====================================================
  #=====================================================
  #=====================================================

  def discord_bot(self):
    print("begin discord_bot")
    import discord
    client = discord.Client()
    print("client loaded")

    ## bot would like read messages/view channels + send messages + read msg history permissions: 68608
    # for ToTheMoons
    BOT_COMMANDS_CID = 932056137518444594

    @client.event
    async def on_ready():
      print("We have logged in as {0.user}".format(client))
      channel = client.get_channel(BOT_COMMANDS_CID)
      await channel.send("I AM ALIVE! MWAHAHAHA")
    # end

    @client.event
    async def on_message(message):
      channel = client.get_channel(message.channel.id)

      msg = message.content.lower()
      if msg.startswith("rtt"):
        edit = False

        if "help" in msg or "halp" in msg:
          msg2  = "Hi! I'm Twitteroo, developed by ryanjsfx.eth\n"
          msg2 += "AKA TheLunaLabs.eth, copyright 2022\n."

          if "lb" in msg or "leaderboard" in msg:
            # expand on leaderboard options
            msg2 += "  options: rtt lb like (likes leaderboard),\n"
            msg2 += "  options: rtt lb retweet (retweets leaderboard),\n"
            msg2 += "    alt:   rtt lb rt\n"
            msg2 += "  options: rtt lb QuoteTweets (QuoteTweets leaderboard),\n"
            msg2 += "    alt:   rtt lb qt\n"
            msg2 += "  options: rtt lb Replies (Replies leaderboard),\n"
            msg2 += "    alt:   rtt lb reply\n"
            msg2 += "  options: rtt lb keywords (keywords leaderboard),\n"
            msg2 += "    alt:   rtt lb key\n\n"
            msg2 += "you can also use the following time commands (warning, unkown time commands will just use all data)\n"
            msg2 += "  today (alt == 24H): past 24 hours (time-zone agnostic)\n"
            msg2 += "  Q1: data from 2022-01-01,0:0:0 to 2022-04-01,0:0:0\n"
            msg2 += "  Q2: data from 2022-04-01,0:0:0 to 2022-07-01,0:0:0\n"
            msg2 += "  last year (alt==2021): data from 2021-01-01,0:0:0 to 2022-01-01,0:0:0\n"
            msg2 += "  last month (alt==april): data from 2022-04-01,0:0:0 to 2022-05-01,0:0:0\n"
            msg2 += "  month (alt==may): data from 2022-05-01,0:0:0 to 2022-06-01,0:0:0\n"
            msg2 += "  Jan: data from 2022-01-01,0:0:0 to 2022-02-01,0:0:0\n"
            msg2 += "  Feb: data from 2022-02-01,0:0:0 to 2022-03-01,0:0:0\n"
            msg2 += "  Mar: data from 2022-03-01,0:0:0 to 2022-04-01,0:0:0\n"
            msg2 += "  start:blah, end:blah == user defined. Must fit expected style and spaces matter! Example: start:2022-01-01Z13:45:51.000Z, end:2022-03-03Z03:33:33.000Z"
          else:
            # print a minimal list of commands.
            msg2 += "Here are my commands\n"
            msg2 += "which are case insensitive :)\n"
            msg2 += "rtt help: display this command ;)\n"
            msg2 += "  alts: rtt halp\n\n"
            msg2 += "rtt lb: display leaderboard for given command options\n"
            msg2 += "  alts: rtt leabderboard\n"
            msg2 += "  defaults: points leaderboard, all data\n"
            msg2 += "  more info: rtt help lb\n\n"
            msg2 += "rtt keywords: display keywords we use to find tweets\n"
            msg2 += "rtt verify: verify if we've processed your tweet/interaction\n"
            msg2 += "  usage: rtt verify url:blah, username:blah\n"
            msg2 += "rtt me: display user's points, likes, etc.\n"
            msg2 += "  usage: rtt me username:blah\n"
          # end if/else

        elif msg.startswith("rtt me"):
          username = ""
          try:
            username  = msg.split("username:")[1]
          except:
            msg2  = "sorry, I couldn't parse that. I'm loooking for smtg like\n"
            msg2 += "rtt me username:TheLunaLabs"
          # end try/except
          if username != "":
            self.init_auth()
            await channel.send("fetching user data")
            user_data = self.fetch_user_data(username)
            print(user_data)
            await channel.send("and now computing user points")
            msg2 = self.fetch_user_points(user_data)
          # end if

        elif "verify" in msg:
          username = ""
          try:
            tweet_url = msg.split("url:")[1].split("username:")[0]
            tweet_url = tweet_url.replace(",", "").replace(" ", "")
            username  = msg.split("username:")[1]
            username  = username.replace(",", "").replace(" ", "")
          except:
            msg2  = "sorry, I couldn't parse that. I'm loooking for smtg like\n"
            msg2 += "rtt verify url:https://twitter.com/RooTroopNFT/status/1499858580568109058, username:TheLunaLabs"
          # end try/except
          if username != "":
            self.init_auth()
            print("username: ", username)
            await channel.send("okay! will verify if we processed that tweet for that user yet or not")
            print("tweet_url: ", tweet_url)
            status = False
            while not status:
              msg2,status = self.verify_processed_tweet(tweet_url, username)
              if status == False:
                await channel.send(msg2)
                await channel.send("We'll wait 20s and then try again.")
                time.sleep(20)
              # end if
            # end while
          # end if

        elif "lb" in msg or "leaderboard" in msg:
          method = "Points"
          if "like" in msg:
            method = "Likes"
          elif "rt" in msg[3:] or "retweet" in msg:
            method = "Retweets"
          elif "qt" in msg or "quote" in msg:
            method = "QuoteTweets"
          elif "repl" in msg:
            method = "Replies"
          elif "key" in msg:
            method = "keyword_replies"
          # end if/elifs

          start_time = "2020-05-04T23:59:59.000Z"
          end_time   = "4022-05-04T23:59:59.000Z"
          tnow = datetime.datetime.now()
          tstr = "%Y-%m-%dT%H:%M:%S.000Z"
          time_str = "all"
          if "today" in msg or "24H" in msg:
            ## to be time-zone agnostic we start 24H ago and end now
            start_time = (tnow - datetime.timedelta(days=1)).strftime(tstr)
            end_time = tnow.strftime(tstr)
            time_str = "past 24 hours"
          elif "Q1" in msg:
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2022-04-01T00:00:00.000Z"
            time_str = "Q1 (2022)"
          elif "Q2" in msg:
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-07-01T00:00:00.000Z"
            time_str = "Q2 (2022)"
          elif "last year" in msg or "2021" in msg:
            start_time = "2021-01-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "2021"
          elif "year" in msg or "2022" in msg:
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
          elif "last month" in msg or "april" in msg:
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-05-01T00:00:00.000Z"
            time_str = "April 2022"
          elif "month" in msg or "may" in msg:
            start_time = "2022-05-01T00:00:00.000Z"
            end_time   = "2022-06-01T00:00:00.000Z"
            time_str = "May 2022"
          elif "jan" in msg:
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2022-02-01T00:00:00.000Z"
            time_str = "Jan 2022"
          elif "feb" in msg:
            start_time = "2022-02-01T00:00:00.000Z"
            end_time   = "2022-03-01T00:00:00.000Z"
            time_str = "Feb 2022"
          elif "mar" in msg:
            start_time = "2022-03-01T00:00:00.000Z"
            end_time   = "2022-04-01T00:00:00.000Z"
            time_str = "Mar 2022"
          elif "start:" in msg and ", end:" in msg:
            start_time = msg.split("start:")[1].split(", end:")[0]
            end_time = msg.split("end:")[1]
            time_str = "user defined"
          # end if/elifs

          fname = self.data_dir + "/leaderboard_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
          if os.path.exists(fname) and os.stat(fname).st_size != 0:
            msg2  = "Okay, grabbing the updated " + method + " leaderboard for "
            msg2 += time_str + " data range. Note it'll take me ~30-60s to update (y'all raid hard :O\n\n"
            await channel.send(msg2)

            msg2 = "In the meantime, here's the last version of that leaderboard.\n"
            with open(fname, "r") as fid:
              for line in fid:
                msg2 += line
              # end for
            # end with
            dmsg = await channel.send(msg2)
            edit = True
          else:
            msg2  = "Okay, grabbing the " + method + " leaderboard for "
            msg2 += time_str + " data range for the first time."
            msg2 += "\nY'all raid hard so this can take a while (30s-60s)"
            msg2 += "\nso please be patient with me :D"
            await channel.send(msg2)
          # end if/else

          msg2 = self.fetch_user_leaderboard(start_time=start_time, 
                 end_time=end_time, method=method)
          msg2 += "\nI've now updated the above leaderboard :)"
          print("discord bot hi here's the " + method + " leaderboard")
          print(msg2)

        elif "key" in msg:
          msg2 = "Hi! These are the keywords I use to scrape for tweets:\n"
          for keyword in self.keyword_query.split("OR"):
            msg2 += keyword + "\n"
          # end for

        else:
          msg2  = "sorry! I didn't understand that command. Try 'rtt help(?)'\n"
          msg2 += "without the quotes..."
        # end if/elif/else
        if not edit:
          await channel.send(msg2)
        else:
          await dmsg.edit(content=msg2)
      # end if rtt
    # end async

    secret = os.environ.get("rttBotPass")
    client.run(secret)
  # end discord_bot
# end class ScrapeTweets

if __name__ == "__main__":
  tweet_scrape_instance = ScrapeTweets()
  tweet_scrape_instance.discord_bot()
  #tweet_scrape_instance.continuously_scrape()

  '''
  tweet_scrape_instance.init_auth()
  tweet_url = "https://twitter.com/TheLunaLabs/status/1517817479644524545"
  tweet_url = "https://twitter.com/MorganStoneee/status/1521909270018592768"
  tweet_scrape_instance.verify_processed_tweet(tweet_url, "MorganStoneee")
  '''

  '''
  tweet_scrape_instance.init_auth()
  start_time = "2022-05-04T23:59:59.000Z"
  #start_time = "2021-05-04T23:59:59.000Z"
  end_time   = "2022-05-05T23:59:59.000Z"
  methods = ["Points", "Likes", "Retweets", "QuoteTweets", "Replies", "keyword_replies", "keyword_retweets"]

  for method in methods:
    tweet_scrape_instance.fetch_user_leaderboard(start_time, end_time, method)
    input(">>")
  '''
# end if

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
