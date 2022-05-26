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
import asyncio
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
    self.continuously_scrape_sleep_time = 10 # seconds

    self.keyword_query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    self.keyword_query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    self.keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"

    self.tab = 4*" "
    tab = self.tab
    help_msg_base = ">>> Hi! I'm Twitteroo, developed by TheLunaLabs © 2022\n"
    self.help     = help_msg_base + \
                    "Below are my commands, "         + \
                    "which are case insensitive:\n\n" + \
                    "**__!rtt help__**\n" + tab       + \
                    "Display this help menu\n\n"      + \
                    "**__!rtt lb__**\n" + tab         + \
                    "Display leaderboard (all data)\n" + tab + \
                    "To see options for granular leaderboards, run command:\n**__!rtt help lb__**\n\n" + \
                    "**__!rtt keywords__**\n" + tab + \
                    "Display keywords we use to find Tweets that count towards your rank\n\n" + \
                    "**__!rtt verify <url>, <username>__**\n" + tab  + \
                    "Verify if we've processed your interaction\n\n" + \
                    "**__!rtt stats <username>__**\n" + tab + \
                    "Display user's points, likes, etc.\n"

    self.help_lb  = help_msg_base + \
                    "This is the help menu for querying the leaderboard." + \
                    " The following commands are available:\n\n" + \
                    "**__LEADERBOARD TYPES__**\n\n"             + \
                    "**__!rtt lb likes__**\n" + tab             + \
                    "Displays the Likes leaderboard.\n\n"       + \
                    "**__!rtt lb Retweets__**\n" + tab          + \
                    "Displays the Retweets leaderboard.\n\n"    + \
                    "**__!rtt lb quotetweets__**\n" + tab       + \
                    "Displays the QuoteTweets leaderboard.\n\n" + \
                    "**__!rtt lb replies__**\n" + tab           + \
                    "Displays the Replies leaderboard.\n\n"     + \
                    "**__!rtt lb keywords__**\n" + tab          + \
                    "Displays the Keywords leaderboard.\n\n"    + \
                    "**__!rtt lb points__**\n" + tab            + \
                    "Displays the Points leaderboard.\n\n"      + \
                    "**__LEADERBOARD BY TIME RANGE__**\n\n"     + \
                    "**__!rtt lb today__**\n" + tab             + \
                    "Past 24 hours (time-zone agnostic)\n\n"    + \
                    "**__!rtt lb Q1__**\n" + tab                + \
                    "Data from January 1st, 2022 - April 1st, 2022\n\n" + \
                    "**__!rtt lb Q2__**\n" + tab                        + \
                    "Data from April 1st, 2022 - July 1st, 2022\n\n"    + \
                    "**__!rtt lb last year__**\n" + tab                 + \
                    "Data from January 1st, 2021 - January 1st, 2022\n\n" + \
                    "**__!rtt lb last month__**\n" + tab                  + \
                    "Data from the last month.\n\n"                       + \
                    "**__!rtt lb <month>__**\n" + tab                     + \
                    "Data from the specified month.\n\n"                  + \
                    "**__!rtt lb start: <month day,year; time>, end: <month, day, year, time>__**\n" + tab + \
                    "Data from the specified timeframe. **Must fit expected style and spaces matter!**\n" + tab + \
                    "Example: !rtt lb start:2022-01-01Z13:45:51.000Z, end:2022-03-03Z03:33:33.000Z\n\n" + \
                    "**NOTE**: leaderboard type & time range options can be combined! \nExample:\n" + \
                    "**__!rtt lb Likes February__**\n" + tab + \
                    "Displays the Likes leaderboard for February tweets.\n"

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

    self.user_dict = self.safe_load(self.fname_user_info)
    if self.user_dict == {}:
      self.user_dict["userId_to_username"] = {}
      self.user_dict["username_to_userId"] = {}
    # end if

    with open("discord_data/linked_3.json", "r") as fid:
      line = ast.literal_eval(fid.read())
      self.linked_usernames = []
      self.linked_userIds = []
      for el in line:
        self.linked_usernames.append(str(el["handle"]))
        self.linked_userIds.append(str(el["id"]))
      
        self.user_dict["userId_to_username"][str(el["id"])] = str(el["handle"])
        self.user_dict["username_to_userId"][str(el["handle"])] = str(el["id"])
      # end for
    # end with open
    self.safe_save(self.fname_user_info, self.user_dict)
    print("loaded linked_usernames!")    

    #self.activity_by_user = self.safe_load(self.fname_activity)
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

    tweet_id = tweet_url.split("status/")[1]
    if "?" in tweet_id:
      tweet_id = tweet_id.split("?")[0]
    # end if

    creator_username = tweet_url.split("/status")[0
                                    ].split("twitter.com/")[1]

    print("success init_tweet")
    return [tweet_id, creator_username]
  # end init_tweet

  #=====================================================
  #=====================================================
  #=====================================================

  def get_tweet_time_s(self, tweet_time):
    #print("begin get_tweet_time_s")

    yy,mo,dd = tweet_time.split("-")
    dd,hh         = dd.split("T")
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

  async def save_url_to_file(self, url, fname):
    print("begin save_url_to_file")
    await asyncio.sleep(0.02)

    self.api_calls_struct["call_times"] = self.safe_load(self.api_calls_struct["fname"])
    api_call_stats = self.safe_load(self.api_calls_struct["fname_stats"])

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

      print("about to sleep a minute because too many recent requests!")
      await asyncio.sleep(60.1)
      for key in self.api_calls_struct["call_times"].keys():
        call_times_loop_arr = self.api_calls_struct["call_times"][key]
        offset = 0
        for ii in range(len(call_times_loop_arr)):
          if time.time() - self.api_calls_struct["call_times"][key][ii+offset] > 15*S_PER_MINUTE:
            del self.api_calls_struct["call_times"][key][ii+offset]
            offset -= 1
          # end if
        # end for
        await asyncio.sleep(0.03)
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
      print("curl failed, sleeping 60s then trying again. will try at most 10 times")
      print("current cnt (to be incremented after sleep: ", cnt)
      await asyncio.sleep(60.1)
      os.system("rm " + fname)
      cnt += 1
      if cnt > 10:
        print("curl failed 10 times! crashing now")
        raise
      # end if
    # end while
    await asyncio.sleep(0.1)
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

    self.safe_save(self.api_calls_struct["fname"], self.api_calls_struct["call_times"])
    self.safe_save(self.api_calls_struct["fname_stats"], api_call_stats)

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
      self.user_dict["userId_to_username"][ user_ids[ii]] = usernames[ii]
      self.user_dict["username_to_userId"][usernames[ii]] = user_ids[ ii]
    # end for

    self.safe_save(self.fname_user_info, self.user_dict)
  # end update_user_dict

  #=====================================================
  #=====================================================
  #=====================================================

  async def fetch_data(self, tweet_url, dtype):
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

    self_tweet_id, self_creator_username = self.init_tweet(tweet_url)

    fname = self.data_dir + "/" + dtype + "_" + self_creator_username + "_" + \
               self_tweet_id + ".txt"
    print("fname: ", fname)

    url = self.twitter_api_base[:-1] + "?ids=" + self_tweet_id + \
          "&tweet.fields=public_metrics"

    await self.save_url_to_file(url, fname)

    url_og = self.twitter_api_base
    if dtype != "Replies":
      url_og += self_tweet_id
    # end if

    if   dtype == "Likes":
      url_og += "/liking_users?"
    elif dtype == "Retweets":
      url_og += "/retweeted_by?"
    elif dtype == "QuoteTweets":
      url_og += "/quote_tweets?&expansions=author_id&"
    elif dtype == "Replies":
      url_og += "search/recent?query=conversation_id:" + \
        self_tweet_id + "&expansions=author_id,in_reply_to_user_id&"
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
      await asyncio.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
      print("num_loops: ", num_loops)
      num_loops += 1

      await self.save_url_to_file(url, fname)

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
            ind   = line.find(substr) + len(substr)
            line  = line[ind:]
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

  async def fetch_activity(self, tweet_url, creation_time, update=False):
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

    self_tweet_id, self_creator_username = self.init_tweet(tweet_url)

    fname_out = self.data_dir + "/activity_" + self_creator_username + "_" + \
                   self_tweet_id + ".txt"

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
      if len(glob.glob(self.data_dir + "/" + dtype + "*" + self_tweet_id + ".txt")) == 0:
        await self.fetch_data(tweet_url, dtype)
      # end if
    # end for

    activity  = '{"' + self_tweet_id + '":{"tweet_url":"' + tweet_url + '", '
    activity += '"tweet_author_username":"' + self_creator_username   + '", '
    activity += '"tweet_created_at":"' + creation_time + '", '

    dtype = "Likes"
    fname = self.data_dir + "/" + dtype + "_" + self_creator_username \
               + "_" + self_tweet_id + ".txt"

    with open(fname, "r") as fid:
      for line in fid:
        line = line.split('"public_metrics":{')[1].split("}")[0]
        print("line: ", line)
      # end for line
    # end with open
    activity += line + "}}"
    activity = ast.literal_eval(activity)
    print("activity: ", activity)

    for dtype in self.dtypes:
      print("dtype: ", dtype)
      fname = self.data_dir + "/" + dtype + "_" + self_creator_username \
              + "_" + self_tweet_id + ".txt"

      activity[self_tweet_id][dtype] = {"ids":[], "usernames":[]}
      if dtype in ["Replies","QuoteTweets"]:
        activity[self_tweet_id][dtype]["contents" ] = []
        activity[self_tweet_id][dtype]["tweet_ids"] = []
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
            self.user_dict["userId_to_username"][user_id]  = username
            self.user_dict["username_to_userId"][username] = user_id

            activity[self_tweet_id][dtype]["ids"].append(user_id)
            activity[self_tweet_id][dtype]["usernames"].append(username)
          # end for
        else:
          for val in vals["includes"]["users"]:
            print("includes val users: ", val)
            user_id = val["id"]
            username = val["username"]
            self.user_dict["userId_to_username"][user_id]  = username
            self.user_dict["username_to_userId"][username] = user_id
          # end for
          for val in vals["data"]:
            print("includes val data: ", val)
            tweet_id = val["id"]
            author_id = val["author_id"]
            text = val["text"]
            
            activity[self_tweet_id][dtype]["ids"].append(author_id)
            activity[self_tweet_id][dtype]["contents"].append(text)
            activity[self_tweet_id][dtype]["usernames"].append(self.user_dict["userId_to_username"][author_id])
            activity[self_tweet_id][dtype]["tweet_ids"].append(tweet_id)
          # end for
        # end if
      # end for lines
    # end for dtypes

    ## safe_save here!!
    self.safe_save(self.fname_user_info, self.user_dict)

    with open(fname_out, "w") as fid:
      fid.write(str(activity))
    # end with

    self.activity = activity

    # if all that was successful, we delete the old files to keep
    # things tidy :)
    for dtype in self.dtypes:
      fname = self.data_dir + "/" + dtype + "_" + self_creator_username \
              + "_" + self_tweet_id + ".txt"
      os.system("rm " + fname)
    # end for

    print("success fetch_activity")
  # end fetch_activity

  #=====================================================
  #=====================================================
  #=====================================================

  async def process_all_tweets_by_user(self, user_id, update = False):
    print("begin process_all_tweets_by_user")

    try:
      username = self.special_tweeters[user_id]
    except:
      print("error: user_id not in special tweeters!")
      raise
    # end try/except

    fname = self.data_dir + "/TweetsByUser_" + user_id + ".txt"

    await asyncio.sleep(0.1)
    if not os.path.isfile(fname) or update == True or os.stat(fname).st_size == 0:
      await self.fetch_all_tweets_by_user(user_id)
    # end if
    await asyncio.sleep(0.1)

    line = self.safe_load(fname)
    if "tweets_processed" in line[-1].keys():
      processed_tweets = line[-1]["tweets_processed"]
    else:
      line[-1]["tweets_processed"] = []
      processed_tweets = []
    # end if/else

    for ii in range(len(line)):
      await asyncio.sleep(0.1)
      for jj in range(len(line[ii]["data"])):
        arr = line[ii]["data"][jj]
        tweet_id = arr["id"]
        creation_time = arr["created_at"]
        text = arr["text"]

        creation_time_s = self.get_tweet_time_s(creation_time)
        if creation_time_s > line[-1]["last_tweet_time_s"]:
          line[-1]["last_tweet_time_s"] = creation_time_s
        # end if

        ## check if we are in the refresh time window or not
        num_days = 1
        tnow = datetime.datetime.now() - datetime.timedelta(days=num_days)
        tnow = tnow.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        tnow = self.get_tweet_time_s(tnow)
        refresh_time = tnow

        if tweet_id in processed_tweets and creation_time_s < refresh_time:
          print("tweet_id in processed_tweets and older than " + str(num_days) + " days, so skipping")
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
        await self.fetch_activity(tweet_url, creation_time)
        self.process_url_activity()

        line[-1]["tweets_processed"].append(tweet_id)
        
        fname_temp   = fname + "_temp"
        fname_backup = fname + "_backup"
        os.system("cp " + fname + " " + fname_backup)
        with open(fname_temp, "w") as fid:
          fid.write(str(line))
        # end with open
        os.system("mv " + fname_temp + " " + fname)
      # end for jj
    # end for ii

    print("success process_all_tweets_by_user")
  # end process_all_tweets_by_user

  #=====================================================
  #=====================================================
  #=====================================================

  async def fetch_all_tweets_by_user(self, user_id):
    print("begin fetch_all_tweets_by_user")

    username = self.special_tweeters[user_id]
    fname = self.data_dir + "/activity_" + username + ".json"

    last_tweet_time = 0
    if os.path.exists(fname) and \
        os.stat(fname).st_size != 0:
      try:
        with open(fname, "r") as fid:
          activity = ast.literal_eval(fid.read())
        # end with
      except:
        print("exception triggered when trying to load activity")
        print("now we're trying to load the backup.")
        with open(fname + "_backup", "r") as fid:
          activity = ast.literal_eval(fid.read())
        # end with open
        print("we loaded the backup (fatbu activity) so now we'll re-set the file with the backup")
        os.system("cp " + fname + "_backup " + \
                    fname)
      # end try/except
      await asyncio.sleep(0.1)

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
      last_tweet_time = max(last_tweet_time, 
          activity[0]["last_tweet_time_s"], activity[-1]["last_tweet_time_s"])
    # end if

    fname = self.data_dir + "/TweetsByUser" + "_" + user_id + ".txt"
    print("fname: ", fname)

    line = self.safe_load(fname)
    await asyncio.sleep(0.1)

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
    await asyncio.sleep(0.1)

    url = self.twitter_api_base[:-len("tweets/")] + "users/" + user_id + \
          "/tweets?tweet.fields=created_at&max_results=100"

    ## first we let it check for new tweets (possibly going all the way back)
    url_og = url + ""
    token = ""
    loop  = True
    num_loops = 0
    newest_tweet_time = 0
    while loop and num_loops < self.max_loops:
      print("\n\nsleeping in process_all_tweets_by_user while loop\n\n")
      await asyncio.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
      print("num_loops: ", num_loops)
      num_loops += 1

      os.system("rm -f temp.txt")
      await self.save_url_to_file(url, "temp.txt")

      if os.stat("temp.txt").st_size == 0:
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

      await asyncio.sleep(0.1)
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
    await asyncio.sleep(0.1)

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
        await asyncio.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
        print("num_loops: ", num_loops)
        num_loops += 1

        await self.save_url_to_file(url, fname)

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
          if user_id not in list(self.activity_by_user.keys()):
            self.activity_by_user[user_id] = \
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
          if tweet_id not in list(self.activity_by_user[user_id]["tweet_ids"]):
            self.activity_by_user[user_id]["tweet_ids"].append(tweet_id)
          # end if
          self.activity_by_user[user_id]["usernames"].append(self.user_dict["userId_to_username"][user_id])

          if dtype not in list(self.activity_by_user[user_id].keys()):
            self.activity_by_user[user_id][dtype] = {"num_"+dtype: 1, "tweet_ids":[tweet_id], "tweet_creation_times":[tweet_creation_time]}
            if dtype in ["QuoteTweets", "Replies"]:
              self.activity_by_user[user_id][dtype]["tweet_contents"] = [data["contents"][ii]]
              self.activity_by_user[user_id][dtype]["tweet_ids"] = [data["tweet_ids"][ii]]
            # end if
          else:
            if tweet_id not in list(self.activity_by_user[user_id][dtype]["tweet_ids"]):
              print("user_id: ", user_id)
              print("act keys: ", self.activity_by_user[user_id].keys())
              print("dtype: ", dtype)
              self.activity_by_user[user_id][dtype]["num_"+dtype] += 1
              self.activity_by_user[user_id][dtype]["tweet_ids"].append(tweet_id)
              self.activity_by_user[user_id][dtype]["tweet_creation_times"].append(tweet_creation_time)
              if dtype in ["QuoteTweets", "Replies"]:
                self.activity_by_user[user_id][dtype]["tweet_contents"].append(data["contents"][ii])
                self.activity_by_user[user_id][dtype]["tweet_ids"][-1] = data["tweet_ids"][ii]
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

    self.safe_save(self.fname_activity, self.activity_by_user)

    print("success process_url_activity")
  # end process_url_activity

  #=====================================================
  #=====================================================
  #=====================================================

  async def update_keyword_data(self):
    print("begin update_keyword_data")
    start = time.time()

    dtime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    fname = self.data_dir + "/" + dtime + "_keyword_data.txt"
    
    query = self.keyword_query.replace(" ", "%20")
    url_og = "https://api.twitter.com/2/tweets/search/recent?query=" + query \
           + "&user.fields=username&expansions=author_id&max_results=100" \
           + "&tweet.fields=created_at"

    url = url_og + ""
    token = ""
    loop  = True
    num_loops = 0
    while loop and num_loops < self.max_loops:
      await asyncio.sleep(0.1) # otherwise Cntrl-C alwyas just kills the curl :(
      print("num_loops: ", num_loops)
      num_loops += 1

      await self.save_url_to_file(url, fname)

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

          if latest_tweet_s < self.activity_by_user["latest_tweet_time_s"]:
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

    self.activity_by_user["query_url"] = url_og

    self.safe_save(self.fname_activity, self.activity_by_user)

    print("ukd executed in (s): ", time.time() - start)
    print("success update_keyword_data")
  # end update_keyword_data

  #=====================================================
  #=====================================================
  #=====================================================

  def safe_save(self, fname, data):
    fname_temp = fname + "_temp"
    fname_backup = fname + "_backup"

    os.system("cp " + fname + " " + fname_backup)
    with open(fname_temp, "w") as fid:
      fid.write(str(data))
    # end with open
    os.system("mv " + fname_temp + " " + fname)
  # end safe_save

  #=====================================================
  #=====================================================
  #=====================================================

  async def process_keyword_data(self):
    print("begin process_keyword_data")
    start = time.time()

    ## needs to be oldest to most recent
    fs = np.sort(glob.glob(self.data_dir + "/*_keyword_data.txt"))

    for fname in fs:
      await asyncio.sleep(0.1)
      print("fname: ", fname)
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
      await asyncio.sleep(0.02)

      if self.activity_by_user["latest_tweet_time_s"] >= latest_tweet_s:
        print("skipping")
        os.system("rm " + fname)
        continue
      # end if

      user_ids  = []
      usernames = []
      for ii in range(len(line)):
        for jj in range(len(line[ii]["includes"]["users"])):
          user_ids.append(  line[ii]["includes"]["users"][jj]["id"])
          usernames.append( line[ii]["includes"]["users"][jj]["username"])
        # end for jj
      # end for ii
      await asyncio.sleep(0.02)

      user_ids_to_usernames = {}
      for ii in range(len(user_ids)):
        user_ids_to_usernames[user_ids[ii]] = usernames[ii]
      # end for ii
      await asyncio.sleep(0.02)

      tweet_ids = []
      contents  = []
      creations = []
      author_ids = []

      for ii in range(len(line)):
        for jj in range(len(line[ii]["data"])):
          tweet_ids.append( line[ii]["data"][jj]["id"])
          contents.append(  line[ii]["data"][jj]["text"])
          creations.append( line[ii]["data"][jj]["created_at"])
          author_ids.append(line[ii]["data"][jj]["author_id"])
        # end for
      # end for
      await asyncio.sleep(0.02)

      latest_creation_time = np.sort(np.array(creations))[-1]
      latest_creation_time_s = self.get_tweet_time_s(latest_creation_time)
      self.activity_by_user["latest_tweet_time"] = latest_creation_time
      self.activity_by_user["latest_tweet_time_s"] = latest_creation_time_s

      for ii,author_id in enumerate(author_ids):
        if author_id not in list(self.activity_by_user.keys()):
          self.activity_by_user[author_id] = \
            {"usernames": [],
             "num_keyword_replies": 0,
             "num_keyword_retweets": 0,
             "tweet_ids": [],
             "tweet_contents": [],
             "tweet_creation_times": []
            }
        # end if

        if tweet_ids[ii] in self.activity_by_user[author_id]:
          print("tweet_id in abu?")
          continue
        # end if

        if contents[ii][:2] == "RT":
          self.activity_by_user[author_id]["num_keyword_retweets"] += 1
        else:
          self.activity_by_user[author_id]["num_keyword_replies"] += 1
        # end if/else

        self.activity_by_user[author_id]["usernames"].append(user_ids_to_usernames[author_id])
        self.activity_by_user[author_id]["tweet_ids"].append(tweet_ids[ii])
        self.activity_by_user[author_id]["tweet_contents"].append(contents[ii])
        self.activity_by_user[author_id]["tweet_creation_times"].append(creations[ii])
      # end for ii
      await asyncio.sleep(0.02)

      self.safe_save(self.fname_activity, self.activity_by_user)
      os.system("rm " + fname)
    # end for fnames

    print("pkd executed in (s): ", time.time() - start)
    print("success process_keyword_data")
  # end process_keyword_data

  #=====================================================
  #=====================================================
  #=====================================================
  #=====================================================

  async def fetch_user_leaderboard(self, start_time="2020-05-04T23:59:59.000Z", 
    end_time="4022-05-04T23:59:59.000Z", method="Points", sharded=True):
    print("begin fetch_user_leaderboard")
    tstart = time.time()
    self.init_auth()

    await asyncio.sleep(0.1)

    start_time_s = self.get_tweet_time_s(start_time)
    end_time_s   = self.get_tweet_time_s(end_time)

    keyword_replies  = []
    keyword_retweets = []
    usernames = []
    contents  = []
    tweet_ids = []

    num_dict = {"num_Likes":[],
                "num_Retweets":[],
                "num_QuoteTweets":[],
                "num_Replies":[]}

    for user in list(self.activity_by_user.keys()):
      if sharded:
        if user not in self.linked_userIds:
          continue
        # end if
      else:
        if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
          continue
        # end if
      # end if/else
      print("user: ", user)
      await asyncio.sleep(0.001)

      tweet_times_dict = {}
      for dtype in self.dtypes:
        tweet_times_dict[dtype] = []
        if dtype in self.activity_by_user[user].keys():
          cnt = 0
          for ii,tweet_time in enumerate(list(self.activity_by_user[user][dtype]["tweet_creation_times"])):
            if tweet_time in tweet_times_dict[dtype]:
              continue
            # end if
            tweet_times_dict[dtype].append(tweet_time)
            tweet_ids.append(self.activity_by_user[user][dtype]["tweet_ids"][ii])

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
      #print(self.activity_by_user[user])
      print(user)
      replies_cnt = 0
      retweets_cnt = 0
      tweet_contents = []
      for ii in range(len(self.activity_by_user[user]["tweet_contents"])):
        ## avoiding double counting via looking at the tweet_ids from Likes etc
        ## currently won't work since at the root level tweet_ids contains all tweet_ids
        ## not just the ones from keyword stuff :(
        ## so either I gotta live with double counting or kind of start over.
        #if self.activity_by_user[user]["tweet_ids"][ii] in tweet_ids:
          #continue
        tweet_content = self.activity_by_user[user]["tweet_contents"][ii]
        if tweet_content in tweet_contents:
          continue
        # end if
        tweet_contents.append(tweet_content)
        tweet_content = tweet_content.lower()

        ## below if statement to exclude LuckyRooToken tweets...or we
        ## could just check for whitelisted users???
        if "#luckyroo" in tweet_content or "@luckyr" in tweet_content or \
           "#saita" in tweet_content or "@saita" in tweet_content or \
           "promote it on" in tweet_content: # last one to filter out spam bots
          continue
        # end if


        tweet_time = self.activity_by_user[user]["tweet_creation_times"][ii]
        tweet_time = self.get_tweet_time_s(tweet_time)
        if tweet_time >= start_time_s and tweet_time <= end_time_s:
          if self.activity_by_user[user]["tweet_contents"][ii][:3] == "RT ":
            retweets_cnt += 1
          else:
            replies_cnt += 1
          # end if/else
        # end if
      # end for

      keyword_replies.append(replies_cnt)
      keyword_retweets.append(retweets_cnt)
      usernames.append(self.activity_by_user[user]["usernames"][-1])
      for content in list(self.activity_by_user[user]["tweet_contents"]):
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

    inds      = inds[:20]
    usernames = usernames[inds]
    val       = val[inds]

    max_name_len = 0
    max_val_len  = 0
    for ii in range(len(inds)):
      max_name_len = max(max_name_len, len(usernames[ii]))
      max_val_len  = max(max_val_len,  len(str(val[ii])))
    # end for ii

    leaderboard = ">>> ```"
    for ii in range(len(inds)):
      leaderboard += str(ii).rjust(2) + ") " + \
        (usernames[ii] + ":").ljust(max_name_len+1) + " " + \
           str(val[ii]).rjust(max_val_len)
      leaderboard += "\n"
      print(str(ii) + ") " + usernames[ii] + ": ", val[ii])
    # end for ii
    leaderboard += "```"
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

    await asyncio.sleep(0.03)
    lb_str = "leaderboard"
    if sharded == True:
      lb_str += "Sharded"
    # end if
    fname = self.data_dir + "/" + lb_str + "_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
    tnow = datetime.datetime.now()
    tnow = tnow.strftime("%Y-%m-%d_%H:%M:%S")
    with open(fname, "w") as fid:
      fid.write("last updated: " + tnow + "\n")
      fid.write(leaderboard)
    # end with

    print("fuls executed in (s): ", time.time() - tstart)
    print("success fetch_user_leaderboard")
    return leaderboard
  # end fetch_user_leaderboard

  #=====================================================
  #=====================================================
  #=====================================================
  #=====================================================

  def verify_processed_tweet(self, tweet_url, username=""):
    self_tweet_id, self_creator_username = self.init_tweet(tweet_url)
    print("tw_id: ", self_tweet_id)
    print("cr_un: ", self_creator_username)
    
    special_usernames = []
    for special_uid in self.special_tweeters.keys():
      special_usernames.append(self.special_tweeters[special_uid])
    # end for

    if self_creator_username not in special_usernames:
      username = self_creator_username
    # end if

    print("username: ", username)

    if username == "":
      error_msg  = ">>> error! Didn't supply username and we were asked to verify"
      error_msg += " interaction with @RooTroopNFT or @TroopSales"
      return [error_msg, False]
    # end if

    status, user_data = self.fetch_user_data(username)

    if status == False:
      return [">>> error! username isn't linked??", False]
    # end if

    if str(self_tweet_id) in user_data["tweet_ids"]:
      message = ">>> SUCCESS! Your tweet was already processed :)"
      print(message)
      return [message,True]
    # end if
        
    print("ud twids: ", user_data["tweet_ids"])
    print("self_tweet_id: ", self_tweet_id)
    print("ud un0: ", user_data["usernames"][0])

    url = self.twitter_api_base[:-1] + "?ids=" + self_tweet_id \
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

    if self.activity_by_user["latest_tweet_time_s"] < tweet_time_s:
      message = "This tweet created after last query was made"
      print(message)
      return [message,False]
    # end if

    message = ">>> Hmmm. Are you sure that tweet had a keyword in it / an interaction with @RooTroopNFT? If so, please let Ryan know about this :) and have mercy on me, I'm just a dumb bot :*("

    print(message)
    return [message,False]
  # end verify_processed_tweet

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_user_data(self, username):
    try:
      for stored_username in self.user_dict["username_to_userId"].keys():
        if username.lower() == stored_username.lower():
          user_id = self.user_dict["username_to_userId"][stored_username]
          return [True, self.activity_by_user[user_id]]
        # end if
      # end for
      for key in list(self.activity_by_user.keys()):
        if key[0].isdigit():
          for stored_username in self.activity_by_user[key]["usernames"]:
            if username.lower() == stored_username.lower():
              self.user_dict["username_to_userId"][stored_username] = key
              self.user_dict["userId_to_username"][key] = stored_username
              return [True, self.activity_by_user[key]]
            # end if
          # end for
        # end if
      # end for
      return [False, "error! username not found :("]
    except:
      for key in list(self.activity_by_user.keys()):
        if key[0].isdigit():
          for stored_username in self.activity_by_user[key]["usernames"]:
            if username.lower() == stored_username.lower():
              self.user_dict["username_to_userId"][stored_username] = key
              self.user_dict["userId_to_username"][key] = stored_username
              return [True, self.activity_by_user[key]]
            # end if
          # end for
        # end if
      # end for
      return [False, "error! username not found :("]
    # end try/except
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

    tweet_times = {}
    tweet_ids = []
    for dtype in self.dtypes:
      tweet_times[dtype] = []
      if dtype in user_data.keys():
        for ii,tweet_time in enumerate(user_data[dtype]["tweet_creation_times"]):
          if tweet_time in tweet_times[dtype]:
            continue
          # end if
          num_dict["num_"+dtype] += 1
          tweet_times[dtype].append(tweet_time)
          tweet_ids.append(user_data[dtype]["tweet_ids"][ii])
        # end for
      # end if
    # end for

    keyword_replies  = 0
    keyword_retweets = 0
    tweet_contents = []
    for ii,tweet_content in enumerate(user_data["tweet_contents"]):
      #if user_data["tweet_ids"][ii] in tweet_ids:
      #  continue
      # end if
      ## the above is to avoid double counting from the interactions with the keyword
      ## stuff. No need to append to tweet_ids :)
      ## But it doesn't work currently, see note in fetch_user_leaderboard... :*(

      if tweet_content in tweet_contents:
        continue
      # end if
      tweet_contents.append(tweet_content)
      tweet_content = tweet_content.lower()

      ## below if statement to exclude LuckyRooToken tweets...or we
      ## could just check for whitelisted users???
      if "#luckyroo" in tweet_content or "@luckyr" in tweet_content or \
         "#saita" in tweet_content or "@saita" in tweet_content or \
         "promote it on" in tweet_content: # last one to filter out spam bots
        continue
      # end if

      if user_data["tweet_contents"][ii][:3] == "RT ":
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
    
    vals = {
      "Points":           points,
      "Likes":            num_dict["num_Likes"],
      "Retweets":         num_dict["num_Retweets"],
      "QuoteTweets":      num_dict["num_QuoteTweets"],
      "Replies":          num_dict["num_Replies"],
      "Keyword Replies":  num_dict["num_keyword_replies"],
      "Keyword Retweets": num_dict["num_keyword_retweets"]
    }

    max_str    = 0
    max_digits = 0
    for key in vals.keys():
      max_str = max(max_str, len(key))
      max_digits = max(max_digits, len(str(vals[key])))
    # end for keys
    print("max_str: ", max_str)
    print("max_digits: ", max_digits)

    message    = ">>> ```"
    for key in vals.keys():
      message += key + ":" + (max_str-len(key))*" " + 4*" " + \
        (max_digits - len(str(vals[key])))*" " + str(vals[key]) + "\n"
    # end for
    message += "```"

    '''
    message  = ">>> ```Points: " + str(points) + "\n"
    message += "Likes: " + str(num_dict["num_Likes"]) + "\n"
    message += "Retweets: " + str(num_dict["num_Retweets"]) + "\n"
    message += "QuoteTweets: " + str(num_dict["num_QuoteTweets"]) + "\n"
    message += "Replies: " + str(num_dict["num_Replies"]) + "\n"
    message += "Keyword Replies: " + str(num_dict["num_keyword_replies"]) + "\n"
    message += "Keyword Retweets: " + str(num_dict["num_keyword_retweets"])
    '''

    print("SUCCESS fetch_user_points")
    return message
  # end fetch_user_points

  #=====================================================
  #=====================================================
  #=====================================================

  def safe_load(self, fname):
    ## first, load activity by user :D
    result = {}
    if os.path.exists(fname) and \
       os.stat(fname).st_size != 0:
      try:
        with open(fname, "r") as fid:
          result = ast.literal_eval(fid.read())
        # end with
      except:
        print("exception triggered when trying to load " + fname + "in safe load")
        print("now we're trying to load the backup.")
        with open(fname + "_backup", "r") as fid:
          result = ast.literal_eval(fid.read())
        # end with open
        print("we loaded the backup (sl) so now we'll re-set the file with the backup2")
        os.system("cp " + fname + "_backup " + \
                    fname)
      # end try/except
    # end if
    return result
  # end safe_load

  #=====================================================
  #=====================================================
  #=====================================================

  async def shard_data(self):
    """The purpose of this method is to break down activity_by_user.json
    into one file per userid so that at least certain actions can be
    done a lot quicker. Only sharding users that link in discord."""
    print("BEGIN shard_data")

    save_dir = self.data_dir + "/user_data"
    os.system("mkdir -p " + save_dir)

    with open("discord_data/linked_3.json", "r") as fid:
      line = ast.literal_eval(fid.read())
      linked_usernames = []
      for el in line:
        linked_usernames.append(el["handle"])
      # end for
    # end with open
    print("loaded linked_usernames!")

    for key in list(self.activity_by_user.keys()):
      print("key: ", key)
      if key[0].isdigit():
        flag = False
        for username in list(self.activity_by_user[key]["usernames"]):
          for linked_username in linked_usernames:
            if username.lower() == linked_username.lower():
              flag = True
              user_data = self.activity_by_user[key]
              fname = save_dir + "/" + key + ".json"
              with open(fname, "w") as fid:
                fid.write(str(user_data))
              # end with open
              break
            # end if
          # end for linked_usernames
          if flag:
            flag = False
            break
          # end if
        # end for usernames
      # end if
      await asyncio.sleep(0.2)
    # end for keys
    print("SUCCESS shard_data")
  # end def shard_data

  async def remove_duplicates(self):
    for userId in list(self.activity_by_user.keys()):
      if not userId[0].isdigit():
        continue
      # end if

      usernames = []
      for username in list(self.activity_by_user[userId]["usernames"]):
        if username not in usernames:
          usernames.append(username)
        # end if
      # end for
      self.activity_by_user[userId]["usernames"] = usernames

      ## there are other duplicates I could remove although 
      ## the calculate points things handle them so no real need...

      print("")

  #=====================================================
  #=====================================================
  #=====================================================

  async def continuously_scrape(self):
    import random
    print("hello from: ", random.random()*1e3)
    await asyncio.sleep(1)
    self.init_auth()
    cs_start = time.time()
    reset_time = time.time() - 400

    while True:
      await asyncio.sleep(0.1)
      loop_start = time.time()
      await self.update_keyword_data()
      await asyncio.sleep(0.1)
      await self.process_keyword_data()

      if time.time() - reset_time > S_PER_HOUR:
        ## cs_user_id to avoid naming collisions
        for cs_user_id in self.special_tweeters.keys():
          if self.special_tweeters[cs_user_id] == "troopsales":
            continue
          # end if
          print(cs_user_id)
          await self.process_all_tweets_by_user(cs_user_id, update=True)
        # end for
        reset_time = time.time()
      # end if

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
      await asyncio.sleep(self.continuously_scrape_sleep_time)
    # end while
  # end def continuously_scrape

  #=====================================================
  #=====================================================
  #=====================================================

  def discord_bot(self):
    print("begin discord_bot")
    #import discord # slash commands from pip3 installl discord-py-slash-command
    #client = discord.Client()
    #from discord.ext import commands
    #client = commands.Bot(command_prefix = ["!rtt"], help_command=None)
    import interactions
    secret = os.environ.get("rttBotPass")
    client = interactions.Client(secret)
    print("client loaded")

    ## bot would like read messages/view channels + send messages + read msg history permissions: 68608
                         # for ToTheMoons
    BOT_COMMANDS_CIDS = [932056137518444594, 
                         978015025585336420]
                         # for Roo Troop

    @client.event
    async def on_ready():
      print("logged in!")
      #print("We have logged in as {0.user}".format(client))
      for BOT_COMMANDS_CID in BOT_COMMANDS_CIDS:
        channel = client.get_channel(BOT_COMMANDS_CID)
        await channel.send("I AM ALIVE! MWAHAHAHA")
      # end for
      ## note, only looks for keywords atm
      #await self.continuously_scrape()
    # end

    @client.command(
name="help",
description="help menu",
scope=931482273440751638,
)
    async def help(ctx: interactions.CommandContext):
      self.command_triggered = True
      await ctx.send(self.help)#, ephemeral=True)

    @client.command(
name="halp",
description="halp menu",
scope=931482273440751638,
)
    async def halp(ctx: interactions.CommandContext):
      self.command_triggered = True
      await ctx.send(self.help)#, ephemeral=True)

    @client.command(
name="hlp",
description="hlp menu",
scope=931482273440751638,
)
    async def hlp(ctx: interactions.CommandContext):
      self.command_triggered = True
      await ctx.send(self.help)#, ephemeral=True)

    #@client.command(aliases=["helplb","hlplb","lbhlp","lbhalp","lbhelp"])
    #async def halplb(ctx): # ctx == context
    #  self.command_triggered = True
    #  await ctx.send(self.help_lb)#, ephemeral=True)

    @client.event
    async def on_message(message):
      if message.author == client.user:
        return
      # end if

      channel = client.get_channel(message.channel.id)
      if message.channel.id not in BOT_COMMANDS_CIDS:
        return
      # end if

      message.content = message.content.lower().replace(" ","")
      self.command_triggered = False
      await client.process_commands(message)
      if self.command_triggered:
        return
      # end if

      tab = self.tab
      msg = message.content
      if msg.startswith("!rtt"):
        edit = False
        msg = msg.replace("@","")

        if "help" in msg or "halp" in msg:
          #copyright = "\U+00A9"
          msg2  = ">>> Hi! I'm Twitteroo, developed by TheLunaLabs © 2022\n"

          if "lb" in msg or "leaderboard" in msg:
            # expand on leaderboard options
            msg2 += "This is the help menu for querying the leaderboard."
            msg2 += " The following commands are available:\n\n"
            msg2 += "**__LEADERBOARD TYPES__**\n\n"
            msg2 += "**__!rtt lb likes__**\n" + tab + "Displays the Likes leaderboard.\n\n"
            msg2 += "**__!rtt lb Retweets__**\n" + tab + "Displays the Retweets leaderboard.\n\n"
            msg2 += "**__!rtt lb quotetweets__**\n" + tab + "Displays the QuoteTweets leaderboard.\n\n"
            msg2 += "**__!rtt lb replies__**\n" + tab + "Displays the Replies leaderboard.\n\n"
            msg2 += "**__!rtt lb keywords__**\n" + tab + "Displays the Keywords leaderboard.\n\n"
            msg2 += "**__!rtt lb points__**\n" + tab + "Displays the Points leaderboard.\n\n"
            msg2 += "**__LEADERBOARD BY TIME RANGE__**\n\n"
            msg2 += "**__!rtt lb today__**\n" + tab + "Past 24 hours (time-zone agnostic)\n\n"
            msg2 += "**__!rtt lb Q1__**\n" + tab + "Data from January 1st, 2022 - April 1st, 2022\n\n"
            msg2 += "**__!rtt lb Q2__**\n" + tab + "Data from April 1st, 2022 - July 1st, 2022\n\n"
            msg2 += "**__!rtt lb last year__**\n" + tab + "Data from January 1st, 2021 - January 1st, 2022\n\n"
            msg2 += "**__!rtt lb last month__**\n" + tab + "Data from the last month.\n\n"
            msg2 += "**__!rtt lb <month>__**\n" + tab + "Data from the specified month.\n\n"
            msg2 += "**__!rtt lb start: <month day,year; time>, end: <month, day, year, time>__**\n" + tab + "Data from the specified timeframe. **Must fit expected style and spaces matter!**\n"
            msg2 += tab + "Example: !rtt lb start:2022-01-01Z13:45:51.000Z, end:2022-03-03Z03:33:33.000Z\n\n"
            msg2 += "**NOTE**: leaderboard type & time range options can be combined! \nExample:\n"
            msg2 += "**__!rtt lb Likes February__**\n" 
            msg2 += tab + "Displays the Likes leaderboard for February tweets.\n"
          else:
            # print a minimal list of commands.
            msg2 += "Here are my commands, "
            msg2 += "which are case insensitive :)\n\n"
            msg2 += "**__!rtt help__**\n" + tab + "Displays this help menu\n\n"
            msg2 += "**__!rtt lb__**\n" + tab + "Display leaderboard (all data)\n" + tab
            msg2 += "To see options for granular leaderboards, run command:\n**__!rtt help lb__**\n\n"
            msg2 += "**__!rtt keywords__**\n" + tab + "Display keywords we use to find Tweets that count towards your rank\n\n"
            msg2 += "**__!rtt verify <url>, <username>__**\n" + tab + "Verify if we've processed your interaction\n\n"
            msg2 += "**__!rtt stats <username>__**\n" + tab + "Display user's points, likes, etc.\n"
          # end if/else

        elif msg.startswith("!rttstats") or msg.startswith("!rttstats"):
          username = ""
          try:
            username  = msg.split("username:")[1].replace(" ","")
          except:
            msg2  = ">>> sorry, I couldn't parse that. I'm loooking for smtg like\n"
            msg2 += 2*tab + "*!rtt stats username:TheLunaLabs*"
          # end try/except
          if username != "":
            self.init_auth()
            print(">>> fetching user data")
            status, user_data = self.fetch_user_data(username)
            if status == False:
              msg2 = user_data
            else:
              #print(user_data)
              print(">>> and now I'm computing user points")
              msg2 = self.fetch_user_points(user_data)
            # end if/else
          # end if

        elif "verify" in msg:
          username = ""
          try:
            tweet_url = msg.split("url:")[1]
            if "username:" in msg:
              tweet_url = tweet_url.split("username:")[0]
              username  = msg.split("username:")[1]
              username  = username.replace(",", "").replace(" ", "")
              print("username: ", username)
            # end if
            tweet_url = tweet_url.replace(",", "").replace(" ", "")
            if "?" in tweet_url:
              tweet_url = tweet_url.split("?")[0]
            # end if
          except:
            msg2  = ">>> sorry, I couldn't parse that. I'm loooking for smtg like\n"
            msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
          # end try/except
          if "https://" not in tweet_url:
            msg2  = ">>> sorry, I couldn't parse that. I'm loooking for smtg like\n"
            msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
          else:
            self.init_auth()
            await channel.send(">>> okay! will verify if we processed that tweet for that user yet or not")
            print("tweet_url: ", tweet_url)
            msg2,status = self.verify_processed_tweet(tweet_url, username)

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
          if "today" in msg or "24h" in msg:
            print("today or 24H in msg")
            ## to be time-zone agnostic we start 24H ago and end now
            start_time = (tnow - datetime.timedelta(days=1)).strftime(tstr)
            end_time = tnow.strftime(tstr)
            time_str = "past 24 hours"
          elif "q1" in msg:
            print("Q1 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2022-04-01T00:00:00.000Z"
            time_str = "Q1 (2022)"
          elif "q2" in msg:
            print("Q2 in msg")
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-07-01T00:00:00.000Z"
            time_str = "Q2 (2022)"
          elif "last year" in msg or "2021" in msg:
            print("last year or 2021 in msg")
            start_time = "2021-01-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "2021"
          elif "year" in msg or "2022" in msg:
            print("year or 2022 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
          elif "last month" in msg or "april" in msg:
            print("last month or april in msg")
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-05-01T00:00:00.000Z"
            time_str = "April 2022"
          elif "month" in msg or "may" in msg:
            print("month or may in msg")
            start_time = "2022-05-01T00:00:00.000Z"
            end_time   = "2022-06-01T00:00:00.000Z"
            time_str = "May 2022"
          elif "jan" in msg:
            print("jan in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2022-02-01T00:00:00.000Z"
            time_str = "Jan 2022"
          elif "feb" in msg:
            print("feb in msg")
            start_time = "2022-02-01T00:00:00.000Z"
            end_time   = "2022-03-01T00:00:00.000Z"
            time_str = "Feb 2022"
          elif "mar" in msg:
            print("mar in msg")
            start_time = "2022-03-01T00:00:00.000Z"
            end_time   = "2022-04-01T00:00:00.000Z"
            time_str = "Mar 2022"
          elif "start:" in msg and ", end:" in msg:
            print("custom time range!")
            start_time = msg.split("start:")[1].split(", end:")[0]
            end_time = msg.split("end:")[1]
            time_str = "user defined"
          # end if/elifs

          fname = self.data_dir + "/leaderboard_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
          if "rtt lbAll".lower() in msg:
            fname = fname.replace("/leaderboard_", "/leaderboardSharded_")
          # end if

          if os.path.exists(fname) and os.stat(fname).st_size != 0:
            msg2  = ">>> Okay, grabbing the updated " + method + " leaderboard for "
            msg2 += time_str + " data range."
            await channel.send(msg2)

            '''
            msg2 = ">>> In the meantime, here's the last version of that leaderboard.\n"
            msg2 += "```"
            with open(fname, "r") as fid:
              for line in fid:
                msg2 += line
              # end for
            # end with
            msg2 += "```"
            dmsg = await channel.send(msg2)
            edit = True
            '''
          else:
            msg2  = ">>> Okay, grabbing the " + method + " leaderboard for "
            msg2 += time_str + " data range."
            await channel.send(msg2)
          # end if/else

          print("msg: ", msg)
          if "rtt lbAll".lower() in msg or "rttlbAll".lower() in msg:
            print("in lbAll")
            #input(">>")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time,
                   end_time=end_time, method=method, sharded=False)
          else:
            print("in reg lb")
            #input(">>")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time, 
                   end_time=end_time, method=method, sharded=True)
          print("discord bot hi here's the " + method + " leaderboard")
          print(msg2)

        elif "key" in msg:
          msg2 = ">>> Hi! These are the keywords I use to scrape for tweets:\n"
          for keyword in self.keyword_query.split("OR"):
            keyword = keyword.replace(")","")
            keyword = keyword.replace("("," ")
            msg2 += 2*tab + keyword + "\n"
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

    #secret = os.environ.get("rttBotPass")
    #client.run(secret)
    client.start()
  # end discord_bot
# end class ScrapeTweets

if __name__ == "__main__":
  tweet_scrape_instance = ScrapeTweets()
  tweet_scrape_instance.discord_bot()

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
