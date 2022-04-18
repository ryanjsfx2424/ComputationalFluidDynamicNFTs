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
    self.special_tweeters = ["rootroopnft", "troopsales"]

    os.system("mkdir -p " + self.data_dir)
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
    os.system(self.curl_base + url + self.curl_header + self.auth + 
              "' >> " + fname)

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
    max_loops = 300 # limit == 30,000 likes, RTs (note, max 900 requests per 15 minutes
    num_loops = 0
    while loop and num_loops < max_loops:
      print("num_loops: ", num_loops)
      num_loops += 1
      os.system(self.curl_base + url + self.curl_header + self.auth + 
                "' >> " + fname)

      if os.stat(fname).st_size == 0:
        print("error, didn't grab any data, probably url has a bug")
        raise
      # end if

      ## check if we grabbed all of them or not
      with open(fname, "r") as fid:
        for line in fid:
          #print("line1: ", line)
          inds = [m.start() for m in re.finditer(self.result_text, line)]
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

  def fetch_activity(self, tweet_url, update=False):
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

    if os.path.isfile(fname_out) and update == False:
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
      self.fetch_data(tweet_url, dtype)
    # end for

    activity  = '{"' + self.tweet_id + '":{"tweet_url":"' + tweet_url + '", '
    activity += '"tweet_author_username":"' + self.creator_username   + '", '

    dtype = "Likes"
    fname = self.data_dir + "/" + dtype + "_" + self.creator_username \
            + "_" + self.tweet_id + ".txt"

    with open(fname, "r") as fid:
      for line in fid:
        line = line.split('"public_metrics":{')[1].split("}")[0]
        print("line: ", line)
      # end for line
    # end with open
    activity += line + ", "
    print("activity: ", activity)

    meta_text = '"meta":{"'
    include_text = '"includes":{"users":[{'
    keys = ['"id":"', '"username":"']
    activity_keys = ['"ids":[', '"usernames":[']
    for dtype in self.dtypes:
      fname = self.data_dir + "/" + dtype + "_" + self.creator_username \
              + "_" + self.tweet_id + ".txt"

      activity += '"' + dtype + '": {'
      with open(fname, "r") as fid:
        for line in fid:
          key = '"public_metrics":{'
          ind = line.find(key) + len(key)
          line = line[ind:]

          if include_text in line:
            ## first we'll grab content
            activity += '"contents":['
            key = '"text":"'
            inds = [m.start() for m in re.finditer(key, line)]
            inds = inds[1:]
            for ind in inds:
              val = line[ind:].split(key)[1].split('"')[0]
              val = val.replace('[','').replace(']','')
              val += " "
              activity += '"' + val + '", '
            # end for inds
            activity = activity[:-2] + '], '

            new_line = ""
            sections = line.split(include_text)[1:]
            for section in sections:
              new_line += section.split(meta_text)[0]
            # end for sections
            line = new_line
          # end if

          for ii,key in enumerate(keys):
            activity += activity_keys[ii]

            inds = [m.start() for m in re.finditer(key, line)]
            for ind in inds:
              activity += '"' + line[ind:].split(key)[1
                                         ].split('"')[0] + '", '
            # end for inds
            activity = activity[:-2] + '], '
          # end for keys
          activity = activity[:-2]
        # end for line
      # end with open
      activity += '}, ' # closes Likes {
    # end for dtypes
    activity = activity[:-2]
    activity += '}' # closes tweet_id everything-y
    activity += '}' # closes all tweet_ids
    print(activity)

    with open(fname_out, "w") as fid:
      fid.write(activity)
    # end with

    self.activity = ast.literal_eval(activity)

    # if all that was successful, we delete the old files to keep
    # things tidy :)
    for dtype in self.dtypes:
      fname = self.data_dir + "/" + dtype + "_" + self.creator_username \
              + "_" + self.tweet_id + ".txt"
      os.system("rm " + fname)
    # end for

    print("success fetch_activity")
  # end fetch_activity

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

    fs = glob.glob(self.data_dir + "/activity_*.txt")
    for fname in fs:
      with open(fname, "r") as fid:
        for line in fid:
          pass
        # end for line
      # end with open
      activity_by_url = ast.literal_eval(line)
      tweet_id = list(activity_by_url.keys())[0]
      tweet_username = activity_by_url[tweet_id]["tweet_author_username"]
      if tweet_username not in self.special_tweeters:
        print("warning, skipping url b/c we assume keyword query picks up random raids")
        continue
      # end if

      for dtype in self.dtypes:
        data = activity_by_url[tweet_id][dtype]
        for ii,user_id in enumerate(data["ids"]):
          if user_id not in list(activity_by_user.keys()):
            activity_by_user[user_id] = \
              {"usernames": [],
               "num_keyword_entries": 0,
               "tweet_ids": [],
               "tweet_contents": [],
               "tweet_creation_times": [],
               "num_Likes": 0,
               "num_Retweets": 0,
               "num_QuoteTweets": 0,
               "num_Replies": 0
              }
          # end if
          if tweet_id in activity_by_user[user_id]["tweet_ids"]:
            continue
          # end if
          activity_by_user[user_id]["usernames"].append(data["usernames"][ii])

          if "num_"+dtype not in activity_by_user[user_id].keys():
            activity_by_user[user_id]["num_"+dytpe]  = 1
          else:
            activity_by_user[user_id]["num_"+dtype] += 1
          # end if/else
          if dtype == self.dtypes[-1]:
            activity_by_user[user_id]["tweet_ids"].append(tweet_id)
          # end if
        # end for user_ids
      # end for dtypes
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

  def fetch_keyword_data(self):
    print("are you sure you don't want to update keyword data?")
    raise
    dtime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    fname = self.data_dir + "/" + dtime + "_keyword_data.txt"
    
    #query  = "(Rooty Roo OR Rooty OR Rooty Woo OR rootywoo OR Roo Troop OR"
    #query += " rootroop OR rootroops OR tree roo OR Roo Roo)"
    query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    query += " OR rootyroo OR RootyRoo OR rootroopnft)"
    query = query.replace(" ", "%20")
    url_og = "https://api.twitter.com/2/tweets/search/recent?query=" + query \
           + "&user.fields=username&expansions=author_id&max_results=100" \
           + "&tweet.fields=created_at"

    url = url_og + ""
    token = ""
    loop  = True
    max_loops = 300 # limit == 30,000 likes, RTs (note, max 900 requests per 15 minutes
    num_loops = 0
    while loop and num_loops < max_loops:
      print("num_loops: ", num_loops)
      num_loops += 1
      os.system(self.curl_base + url + self.curl_header + self.auth + 
                "' >> " + fname)

      if os.stat(fname).st_size == 0:
        print("error, didn't grab any data, probably url has a bug")
        raise
      # end if

      ## check if we grabbed all of them or not
      with open(fname, "r") as fid:
        for line in fid:
          #print("line1: ", line)
          inds = [m.start() for m in re.finditer("result_count", line)]
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
    with open(fname, "a") as fid:
      fid.write("\n\n" + url_og)
    # end with open
  # end fetch_keyword_data

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
    query += " OR rootyroo OR RootyRoo OR rootroopnft)"
    query = query.replace(" ", "%20")
    url_og = "https://api.twitter.com/2/tweets/search/recent?query=" + query \
           + "&user.fields=username&expansions=author_id&max_results=100" \
           + "&tweet.fields=created_at"

    url = url_og + ""
    token = ""
    loop  = True
    max_loops = 300 # limit == 30,000 likes, RTs (note, max 900 requests per 15 minutes
    num_loops = 0
    while loop and num_loops < max_loops:
      print("num_loops: ", num_loops)
      num_loops += 1
      os.system(self.curl_base + url + self.curl_header + self.auth + 
                "' >> " + fname)

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

          inds = [m.start() for m in re.finditer(self.result_text, line)]
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

    os.system("rm " + fname)
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
        continue
      # end if
      print
      print("hi2")

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

      keys = ['"id":"', '"text":"', '"created_at":"']

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

      key = keys[2]
      inds = [m.start() for m in re.finditer(key, line2)]
      for ind in inds:
        creations.append(line2[ind:].split(key)[1].split('"')[0])
      # end for inds
      print("hi6")

      latest_creation_time = np.sort(np.array(creations))[-1]
      latest_creation_time_s = self.get_tweet_time_s(latest_creation_time)
      activity_by_user["latest_tweet_time"] = latest_creation_time
      activity_by_user["latest_tweet_time_s"] = latest_creation_time_s

      for ii,user_id in enumerate(user_ids):
        if user_id not in list(activity_by_user.keys()):
          activity_by_user[user_id] = \
            {"usernames": [],
             "num_keyword_entries": 0,
             "tweet_ids": [],
             "tweet_contents": [],
             "tweet_creation_times": []
            }
        # end if

        user_dict = activity_by_user[user_id]
        if tweet_ids[ii] in user_dict:
          continue
        # end if

        user_dict["num_keyword_entries"] += 1
        user_dict["usernames"].append(usernames[ii])
        user_dict["tweet_ids"].append(tweet_ids[ii])
        user_dict["tweet_contents"].append(contents[ii])
        user_dict["tweet_creation_times"].append(creations[ii])
      # end for ii
      with open(fname_activity, "w") as fid:
        json.dump(activity_by_user, fid)
      # end with open
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

    entries   = []
    usernames = []
    contents  = []

    num_Likes       = []
    num_Retweets    = []
    num_QuoteTweets = []
    num_Replies     = []
    for user in activity_by_user.keys():
      if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
        continue
      # end if
      if "num_Likes" in activity_by_user[user].keys():
        num_Likes.append(      activity_by_user[user]["num_Likes"])
      else:
        num_Likes.append(0)
      if "num_Retweets" in activity_by_user[user].keys():
        num_Retweets.append(   activity_by_user[user]["num_Retweets"])
      else:
        num_Retweets.append(0)
      if "num_QuoteTweets" in activity_by_user[user].keys():
        num_QuoteTweets.append(activity_by_user[user]["num_QuoteTweets"])
      else:
        num_QuoteTweets.append(0)
      if "num_Replies" in activity_by_user[user].keys():
        num_Replies.append(    activity_by_user[user]["num_Replies"])
      else:
        num_Replies.append(0)
      # end if/else
      entries.append(activity_by_user[user]["num_keyword_entries"])
      usernames.append(activity_by_user[user]["usernames"][-1])
      for content in activity_by_user[user]["tweet_contents"]:
        contents.append(content)
      # end for
    # end for
    num_Likes       = np.array(num_Likes)
    num_Retweets    = np.array(num_Retweets)
    num_QuoteTweets = np.array(num_QuoteTweets)
    num_Replies     = np.array(num_Replies)
    entries   = np.array(entries)

    points = entries*3 + num_Retweets*2 + num_Likes*1

    usernames = np.array(usernames)
    inds = np.argsort(points)[::-1]
    inds = inds[:20]
    for ii in range(len(inds)):
      print(str(ii) + ") " + usernames[inds][ii] + ": ", points[inds][ii])
    # end for ii
    print("num usernames: ", len(usernames))
    print("num tweets: ", np.sum(entries))

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

    url = self.twitter_api_base[:-1] + "?ids=" + self.tweet_id \
        + "&tweet.fields=created_at"

    os.system(self.curl_base + url + self.curl_header + self.auth + 
              "' >> " + "delete_me.txt")

    with open("delete_me.txt", "r") as fid:
      line = fid.read()
    # end with open

    tweet_time = line.split(self.created_text)[1].split('"')[0]
    tweet_time_s = self.get_tweet_time_s(tweet_time)

    with open(self.fname_activity, "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    if activity_by_user["latest_tweet_time_s"] < tweet_time_s:
      print("This tweet created after last query was made")
      return False
    # end if

    for user in activity_by_user.keys():
      if user in ["latest_tweet_time", "latest_tweet_time_s", "query_url"]:
        continue
      # end if
      if username in activity_by_user[user]["usernames"]:
        if self.tweet_id in activity_by_user[user]["tweet_ids"]:
          print("verified tweet processed")
          return True
        # end if
      # end if
    # end for
    print("Error! There's a bug. Please contact Ryan.")
    return False
  # end verify_processed_tweet

# end class ScrapeTweets

if __name__ == "__main__":
  tweet_scrape_instance = ScrapeTweets()
  tweet_scrape_instance.init_auth()

  tweet_url = "https://twitter.com/RooTroopNFT/status/1515482071849865218"

  #tweet_scrape_instance.update_keyword_data()
  #tweet_scrape_instance.process_keyword_data()
  #tweet_scrape_instance.fetch_user_leaderboard()

  tweet_scrape_instance.handle_url_activity(tweet_url)

  tweet_scrape_instance.process_tweets(urls)
# end if

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
