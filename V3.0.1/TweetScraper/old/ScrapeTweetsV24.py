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
import json
import pathlib
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

    if not os.path.exists(self.api_calls_struct["fname"]) or \
       os.stat(self.api_calls_struct["fname"]).st_size == 0:
      with open(self.api_calls_struct["fname_stats"], "w") as fid:
        api_call_stats = {"1H": {}, "1D": [], "30D": []}
      # end with open
    # end if

  # end __init__

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

  def save_url_to_file(self, url, fname):
    print("begin save_url_to_file")

    with open(self.api_calls_struct["fname"], "r") as fid:
      self.api_calls_struct["call_times"] = ast.literal_eval(fid.read())
    # end with

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
    while flag:
      os.system(self.curl_base + url + self.curl_header + self.auth + 
                "' >> " + fname)
      
      with open(fname, "r") as fid:
        line = fid.read()
        if '"status":503' not in line:
          flag = False
          break
        # end if
      # end with
      time.sleep(60.1)
      os.system("rm " + fname)
    # end while
    time.sleep(0.1)
    self.api_calls_struct["call_count"] += 1
    
    self.api_calls_struct["call_times"][dtype].append(time.time())

    with open(self.api_calls_struct["fname"], "w") as fid:
      fid.write(str(self.api_calls_struct["call_times"]))
    # end with open    

    fname = self.data_dir + "api_call_stats.txt"
    api_call_stats = {}
    if os.path.exists(self.api_calls_struct["fname"]) and \
       os.stat(self.api_calls_struct["fname"]).st_size != 0:
     with open(fname, "r") as fid:
        line = fid.read()
      # end with open
    # end if
    fname

    #print("api_calls_struct: ", self.api_calls_struct)
    #print("len call_times: ", len(self.api_calls_struct["call_times"]))
    #if self.api_calls_struct["call_count"] > 600:
      #input(">>")

    print("success save_url_to_file")
  # end save_url_to_file

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
      json.dump(user_dict, fid)
    # end with open
  # end update_user_dict

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
      json.dump(user_dict, fid)
    # end with open

    with open(fname_out, "w") as fid:
      json.dump(activity, fid)
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

        if tweet_id in processed_tweets:
          print("tweet_id in processed_tweets so skipping")
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
      input(">>")

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
      json.dump(activity_by_user, fid)
    # end with open

    print("success process_url_activity")
  # end process_url_activity

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
    query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"
    query = query.replace(" ", "%20")
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
      json.dump(activity_by_user, fid)
    # end with open

    print("success update_keyword_data")
  # end update_keyword_data

  def process_keyword_data(self):
    print("begin process_keyword_data")

    activity_by_user = {"latest_tweet_time_s":0}
    fname_activity = self.data_dir + "/activity_by_user.json"
    if os.path.exists(fname_activity) and \
       os.stat(fname_activity).st_size != 0:
      with open(self.data_dir + "/activity_by_user.json", "r") as fid:
        activity_by_user = fid.read()
      # end with open
      activity_by_user = ast.literal_eval(activity_by_user)
    # end if

    fs = np.sort(glob.glob(self.data_dir + "/*_keyword_data.txt"))

    for fname in fs:
      print("fname: ", fname)
      with open(fname, "r") as fid:
        for line in fid:
          break
        # end for line
      # end with open
      print("hi1")

      key = '"created_at":"'
      latest_tweet = line[line.find(key) + len(key):].split('"')[0]
      latest_tweet_s = self.get_tweet_time_s(latest_tweet)
      if activity_by_user["latest_tweet_time_s"] >= latest_tweet_s:
        print("skipping")
        os.system("rm " + fname)
        continue
      # end if

      ## first get user ids and usernames
      inds_start = [m.start() for m in re.finditer(self.include_text, line)]
      inds_end   = [m.start() for m in re.finditer(self.meta_text,    line)]

      line2 = ""
      for ii in range(len(inds_start)):
        line2 += line[inds_start[ii]:inds_end[ii]]
      # end for ii
      print("hi2")
    
      keys = ['"id":"', '"username":"']

      user_ids  = []
      usernames = []

      key = keys[0]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        user_ids.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi3")

      key = keys[1]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        usernames.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi4")

      user_ids_to_usernames = {}
      for ii in range(len(user_ids)):
        user_ids_to_usernames[user_ids[ii]] = usernames[ii]
      # end for ii

      ## next get tweet ids and content and creation time
      inds_start = [0] + [m.start() for m in re.finditer(self.meta_text, line)][:-1]
      inds_end   = [m.start() for m in re.finditer(self.include_text,    line)]

      line2 = ""
      for ii in range(len(inds_start)):
        line2 += line[inds_start[ii]:inds_end[ii]]
      # end for ii

      tweet_ids = []
      contents  = []
      creations = []
      author_ids = []

      keys = ['"id":"', '"text":"', '"created_at":"', '"author_id":"']

      key = keys[0]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        tweet_ids.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi5")

      key = keys[1]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        contents.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi6")

      key = keys[2]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        creations.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi7")

      key = keys[3]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        author_ids.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi8")

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
        json.dump(activity_by_user, fid)
      # end with open
      #os.system("rm " + fname)
    # end for fnames

    print("success process_keyword_data")
  # end process_keyword_data

  def generate_activity_tweet_urls(self):
    print("begin generate_activity_tweet_urls")
    ## load in activity_by_user.json and generate from the tweet_id + username
    print("success generate_activity_tweet_urls")
  # end generate_activity_tweet_urls

  def fetch_user_leaderboard(self):
    print("begin fetch_user_leaderboard")

    with open(self.data_dir + "/activity_by_user.json", "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    keyword_replies  = []
    keyword_retweets = []
    usernames = []
    contents  = []

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
         num_dict["num_"+dtype].append(activity_by_user[user][dtype]["num_" + dtype])
        else:
          num_dict["num_"+dtype].append(0)
        # end if/else
      # end for
      print(activity_by_user[user])
      print(user)
      keyword_replies.append(activity_by_user[user]["num_keyword_replies"])
      keyword_retweets.append(activity_by_user[user]["num_keyword_retweets"])
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
    inds = np.argsort(points)[::-1]
    inds = inds[:20]
    for ii in range(len(inds)):
      print(str(ii) + ") " + usernames[inds][ii] + ": ", points[inds][ii])
    # end for ii
    print("num usernames: ", len(usernames))
    print("num tweets: ", np.sum(keyword_replies) + np.sum(keyword_retweets))

    #for ii in range(20):
    #  ind = np.random.randint(len(contents))
    #  print("\n" + contents[ind])
    ## end for ii

    with open(self.data_dir + "/queryed_tweets.txt", "w") as fid:
      for ii in range(len(contents)):
        fid.write(contents[ii] + "\n\n")
      # end for line
    # end with open

    print("success fetch_user_leaderboard")
  # end fetch_user_leaderboard

  def verify_processed_tweet(self, tweet_url, username):
    self.init_tweet(tweet_url)

    with open(self.fname_activity, "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    print("tw_id: ", self.tweet_id)
    for user in activity_by_user.keys():
      if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
        continue
      # end if
      if username in activity_by_user[user]["usernames"]:
        print("username in usernames")
        print("tw_ids: ", activity_by_user[user]["tweet_ids"])
        print("user: ", user)
        print("act usernames: ", activity_by_user[user]["usernames"])
        print("act contents: ", activity_by_user[user]["tweet_contents"])
        sys.exit()
        if self.tweet_id in activity_by_user[user]["tweet_ids"]:
          print("verified tweet processed")
          return True
        # end if
      # end if
    # end for

    url = self.twitter_api_base[:-1] + "?ids=" + self.tweet_id \
        + "&tweet.fields=created_at"

    os.system(self.curl_base + url + self.curl_header + self.auth + 
              "' >> " + "delete_me.txt")

    with open("delete_me.txt", "r") as fid:
      line = fid.read()
    # end with open

    tweet_time = line.split(self.created_text)[1].split('"')[0]
    tweet_time_s = self.get_tweet_time_s(tweet_time)

    if activity_by_user["latest_tweet_time_s"] < tweet_time_s:
      print("This tweet created after last query was made")
      return False
    # end if

    print("Error! There's a bug. Please contact Ryan.")
    return False
  # end verify_processed_tweet

  def fetch_user_data(self, username):
    with open(self.fname_activity, "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    for user in activity_by_user.keys():
      if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
        continue
      # end if
      if username in activity_by_user[user]["usernames"]:
        return activity_by_user[user]

# end class ScrapeTweets

if __name__ == "__main__":
  tweet_scrape_instance = ScrapeTweets()
  tweet_scrape_instance.init_auth()

  #tweet_url = "https://twitter.com/RooTroopNFT/status/1515482071849865218"
  #tweet_url = "https://twitter.com/TheLunaLabs/status/1516536571608145928"
  #tweet_url = "https://twitter.com/TheLunaLabs/status/1517817479644524545"

  tweet_scrape_instance.update_keyword_data()
  tweet_scrape_instance.process_keyword_data()
  #tweet_scrape_instance.fetch_user_leaderboard()

  #tweet_scrape_instance.handle_url_activity(tweet_url)

  #tweet_scrape_instance.process_tweets(urls)

  #tweet_scrape_instance.verify_processed_tweet(tweet_url, "TheLunaLabs")
  #TLL_data = tweet_scrape_instance.fetch_user_data("TheLunaLabs")
  #print(TLL_data)

  RooTroopNFT = "1447280926967304195"
  TroopSales = "1477912158730170370"
  
  ## note, just set update=True in process_all_tweets to fetch_all_tweets
  #tweet_scrape_instance.fetch_all_tweets_by_user(RooTroopNFT)
  #tweet_scrape_instance.process_all_tweets_by_user(TroopSales, update=True)
  tweet_scrape_instance.fetch_user_leaderboard()

# end if

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
