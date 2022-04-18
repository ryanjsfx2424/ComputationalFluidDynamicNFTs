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

  def fetch_keyword_data(self):
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

    fname = np.sort(glob.glob(self.data_dir + "/*_keyword_data.txt"))[-1]
    with open(fname, "r") as fid:
      for line in fid:
        break
      # end for
    # end with open
    last_tweet = line.split('"created_at":"')[1].split('"')[0]
    yy,mo,dd = last_tweet.split("-")
    dd,hh    = dd.split("T")
    hh,mi,ss = hh.split(":")
    ss = ss[:-1]
    last_tweet_s = float(yy)*S_PER_YEAR   + float(mo)*S_PER_MONTH + \
                   float(dd)*S_PER_DAY    + float(hh)*S_PER_HOUR  + \
                   float(mi)*S_PER_MINUTE + float(ss)

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
          print(latest_tweet)
          print(last_tweet)
          print(last_tweet_s)

          yy,mo,dd = latest_tweet.split("-")
          dd,hh    = dd.split("T")
          hh,mi,ss = hh.split(":")
          ss = ss[:-1]
          latest_tweet_s = float(yy)*S_PER_YEAR   + float(mo)*S_PER_MONTH + \
                           float(dd)*S_PER_DAY    + float(hh)*S_PER_HOUR  + \
                           float(mi)*S_PER_MINUTE + float(ss)

          if latest_tweet_s < last_tweet:
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

    with open(fname, "a") as fid:
      fid.write("\n\n" + url_og)
    # end with open

    print("success update_keyword_data")
  # end update_keyword_data

  def process_keyword_data(self):
    print("begin process_keyword_data")

    fname = np.sort(glob.glob(self.data_dir + "/*_keyword_data.txt"))[-1]

    with open(fname, "r") as fid:
      for line in fid:
        break
      # end for line
    # end with open

    ## first get user ids and usernames
    inds_start = [m.start() for m in re.finditer(self.include_text, line)]
    inds_end   = [m.start() for m in re.finditer(self.meta_text,    line)]

    line2 = ""
    for ii in range(len(inds_start)):
      line2 += line[inds_start[ii]:inds_end[ii]]
    # end for ii
    
    keys = ['"id":"', '"username":"']

    user_ids  = []
    usernames = []

    key = keys[0]
    inds = [m.start() for m in re.finditer(key, line2)]
    for ind in inds:
      user_ids.append(line2[ind:].split(key)[1].split('"')[0])
    # end for inds

    key = keys[1]
    inds = [m.start() for m in re.finditer(key, line2)]
    for ind in inds:
      usernames.append(line2[ind:].split(key)[1].split('"')[0])
    # end for inds

    ## next get tweet ids and content
    inds_start = [0] + [m.start() for m in re.finditer(self.meta_text, line)][:-1]
    inds_end   = [m.start() for m in re.finditer(self.include_text,    line)]

    line2 = ""
    for ii in range(len(inds_start)):
      line2 += line[inds_start[ii]:inds_end[ii]]
    # end for ii

    tweet_ids = []
    contents  = []

    keys = ['"id":"', '"text":"']

    key = keys[0]
    inds = [m.start() for m in re.finditer(key, line2)]
    for ind in inds:
      tweet_ids.append(line2[ind:].split(key)[1].split('"')[0])
    # end for inds

    key = keys[1]
    inds = [m.start() for m in re.finditer(key, line2)]
    for ind in inds:
      contents.append(line2[ind:].split(key)[1].split('"')[0])
    # end for inds

    activity_by_user = {}
    for ii,user_id in enumerate(user_ids):
      if user_id not in list(activity_by_user.keys()):
        activity_by_user[user_id] = \
          {"usernames": [],
           "num_keyword_entries": 0,
           "tweet_ids": [],
           "tweet_contents": []
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
    # end for ii
    with open(self.data_dir + "/activity_by_user.json", "w") as fid:
      json.dump(activity_by_user, fid)
    # end with open

    print("success process_keyword_data")
  # end process_keyword_data

  def fetch_user_leaderboard(self):
    print("begin fetch_user_leaderboard")

    with open(self.data_dir + "/activity_by_user.json", "r") as fid:
      activity_by_user = fid.read()
    # end with open
    activity_by_user = ast.literal_eval(activity_by_user)

    entries   = []
    usernames = []
    contents  = []
    for user in activity_by_user.keys():
      entries.append(activity_by_user[user]["num_keyword_entries"])
      usernames.append(activity_by_user[user]["usernames"][-1])
      for content in activity_by_user[user]["tweet_contents"]:
        contents.append(content)
      # end for
    # end for
    entries   = np.array(entries)
    usernames = np.array(usernames)
    inds = np.argsort(entries)[::-1]
    inds = inds[:20]
    for ii in range(len(inds)):
      print(str(ii) + ") " + usernames[inds][ii] + ": ", entries[inds][ii])
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
# end class ScrapeTweets

urls = [
"https://twitter.com/mooneynft/status/1515382011267014657?s=20&t=pulk5_II0hc-Te5sP2NVIQ"
]
'''
        "https://twitter.com/ImHudda/status/1515285705165275145"
"https://twitter.com/cryptojoel66/status/1515253719117541387"
"https://twitter.com/gronkwizard/status/1515310628386209796"
"https://twitter.com/SpicegirlNFT/status/1515312882950369284"
"https://twitter.com/Nomad_eth/status/1515051853301571596"
"https://twitter.com/greeneteam25/status/1515374193784852485"
"https://twitter.com/NFTGUYY/status/1515386302237396994"
]
'''

tweet_scrape_instance = ScrapeTweets()
tweet_scrape_instance.init_auth()

tweet_id = "1515382011267014657"
#tweet_url = "https://twitter.com/cryptocom/status/1373877690130821120"
tweet_url = "https://twitter.com/RooTroopNFT/status/1515482071849865218"
tweet_url = "https://twitter.com/RooTroopNFT/status/1515139514880061445"
tweet_url = "https://twitter.com/mooneynft/status/1515382011267014657?s=20&t=pulk5_II0hc-Te5sP2NVIQ"
#tweet_url = "https://twitter.com/ProjectKaitu/status/1515106498879397891"

#tweet_scrape_instance.fetch_keyword_data()
#tweet_scrape_instance.process_keyword_data()
#tweet_scrape_instance.fetch_user_leaderboard()

tweet_scrape_instance.update_keyword_data()

#tweet_scrape_instance.fetch_data(tweet_url, dtype)
#tweet_scrape_instance.fetch_replies(tweet_id)
#tweet_scrape_instance.fetch_activity(tweet_url)
#tweet_scrape_instance.process_activity(tweet_id)

#tweet_scrape_instance.process_tweets(urls)

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
