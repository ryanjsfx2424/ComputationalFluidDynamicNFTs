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
import pathlib
import datetime
print("Begin ScrapeTweets")

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

    tweet_id = tweet_url.split("status/")[1]
    if "?" in tweet_id:
      tweet_id = tweet_id.split("?")[0]
    # end if
    print("tweet_id: ", tweet_id)
    print("tweet_url: ", tweet_url)

    creator_username = tweet_url.split("/status")[0].split("twitter.com/")[1]
    print("creator_username: ", creator_username)

    fname = self.data_dir + "/" + dtype + "_" + creator_username + "_" + \
            tweet_id + ".txt"
    print("fname: ", fname)

    url = self.twitter_api_base[:-1] + "?ids=" + tweet_id + \
          "&tweet.fields=public_metrics"
    os.system(self.curl_base + url + self.curl_header + self.auth + 
              "' >> " + fname)

    url_og = self.twitter_api_base
    if dtype != "Replies":
      url_og += tweet_id
    # end if

    if   dtype == "Likes":
      url_og += "/liking_users?"
    elif dtype == "Retweets":
      url_og += "/retweeted_by?"
    elif dtype == "QuoteTweets":
      url_og += "/quote_tweets?&expansions=author_id&"
    elif dtype == "Replies":
      url_og += "search/recent?query=conversation_id:" + \
        tweet_id + "&expansions=author_id,in_reply_to_user_id&"
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
        print("warning, didn't grab any data, probably tweet is old")
        return
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

    self.fname_likes = fname
    print("success fetch_data")
  # end fetch_data

  def fetch_replies(self, tweet_id):
    '''
    for a given tweet, fetch the users that replied to it (and
    reply content) and saves json
    response to a file for later processing.
      inputs: tweet_id
      outputs: none
      side effects: a file is (re-)written & self.fname_replies is assigned.
    '''
    print("begin fetch_replies")

    fname = self.data_dir + "/replies_to_" + tweet_id + ".txt"

    url = self.twitter_api_base + "search/recent?query=conversation_id:" + \
        tweet_id + "&max_results=100&expansions=author_id,in_reply_to_user_id&user.fields=username"

    os.system(self.curl_base + url + self.curl_header + self.auth +
              "' > " + fname)

    self.fname_replies = fname
    print("success fetch_replies")
  # end fetch_replies

  def fetch_activity(self, tweet_id):
    '''
    for a given tweet, fetch the users that liked, retweeted, quote-tweeted,
    or replied and saves json response to a single file for later processing.
      inputs: tweet_id
      outputs: none
      side effects: calls fetch_likes, fetch_retweets, fetch_quote_tweets,
        fetch_replies and generates a dictionary containing all that data
        and saves to a file. Assigns self.activity
    '''
    print("begin fetch_activity")
    fname_activity = self.data_dir + "/activity_for_" + tweet_id + ".txt"

    try:
      fnames = [self.fname_likes, self.fname_retweets, self.fname_quote_tweets,
                self.fname_replies]
      print("got self.fnames!")
    except:
      fnames = glob.glob(self.data_dir + "/*" + tweet_id + ".txt")
      print("globbed fnames!")
    # end try/except

    if len(fnames) == 0:
      print("grabbing new fnames!")
      self.fetch_likes(tweet_id)
      self.fetch_retweets(tweet_id)
      self.fetch_quote_tweets(tweet_id)
      self.fetch_replies(tweet_id)
      fnames = [self.fname_likes, self.fname_retweets, self.fname_quote_tweets,
                self.fname_replies]
    # end if

    include_text = 'includes":{"users'

    activity = "{"
    for fname in fnames:
      if "activity" in fname:
        continue
      # end if

      with open(fname, "r") as fid:
        for line in fid:
          line = line.split(r',"meta":{')[0]
          if "like" in fname:
            name = "likes"
          elif "retweet" in fname:
            name = "retweets"
          elif "quote_tweet" in fname:
            name = "quote_tweets"
          elif "replies" in fname:
            name = "replies"
          # end if
          line = line.replace('{"data"', '"' + name + '"')
          line = line.replace(include_text, name + "_" + include_text)

          if line == '{"meta":{"result_count":0}}':
            continue
          # end if

          activity += line + ", "
        # end for
      # end with open
    # end for fnames
    activity = activity[:-2] + "}"

    with open(fname_activity, "w") as fid:
      fid.write(activity)
    # end with

    self.activity = ast.literal_eval(activity)
    print("success fetch_activity")
  # end fetch_activity

  ## prob need to give this a better doc string, getting tired
  def process_activity(self, url):
    '''
    creates a csv file with tweet activity
    '''
    print("begin process_activity")

    tweet_id = url.split("status/")[1]
    if "?" in tweet_id:
      tweet_id = tweet_id.split("?")[0]
    # end if

    try:
      self.activity += "" # does nothing
    except:
      self.fetch_activity(tweet_id)
    # end try/except

    keys = [
            'quote_tweets_includes', 
            'replies_includes', 
            'likes',
            'retweets', 
            'quote_tweets', 
            'replies' 
           ]

    print(self.activity.keys())
    print(keys)

    activity_new = {}
    key_ext_ids = "_ids_csv"
    key_ext_use = "_use_csv"
    for key in keys:
      print("key: ", key)

      new_key_ids = key + key_ext_ids
      new_key_use = key + key_ext_use
      activity_new[new_key_ids] = ""
      activity_new[new_key_use] = ""

      if key not in list(self.activity.keys()):
        continue
      # end if

      if "includes" in key:
        new_key = key + "_id_to_username"
        activity_new[new_key] = {}

        items = self.activity[key]["users"]

        for item in items:
          author_id = item["id"]
          activity_new[new_key][author_id] = item["username"]
        # end for
        continue
      # end if

      items = self.activity[key]

      item_key = "id"
      if key in ["quote_tweets", "replies"]:
        item_key = "author_id"
      # end if

      for item in items:
        author_id = item[item_key]
        if key in ["quote_tweets", "replies"]:
          new_key = key + "_includes_id_to_username"
          author_username = activity_new[new_key][author_id]
        else:
          author_username = item["username"]
        # end if/else

        activity_new[new_key_ids] += author_id + ","
        activity_new[new_key_use] += author_username + ","
      # end for item
      activity_new[new_key_ids] = activity_new[new_key_ids][:-1]
      activity_new[new_key_use] = activity_new[new_key_use][:-1]
    # end for keys
    self.activity = activity_new

    ## next, get the usernames corresponding to the ids, which
    ## is more human readable :)

    fname = pathlib.Path("twitter_data/users_liked_tweet_" + 
                         tweet_id + ".txt")
    mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime, 
            tz=datetime.timezone.utc)
    dtime = mtime.strftime("%Y-%m-%d_%H:%M:%S")

    url_base = "https://twitter.com/RooTroopNFT/status/"
    header = "Tweet ID," + tweet_id + "," + "Data Pulled (UTC):," + \
             dtime + ",URL:," + url_base + tweet_id + "\n"

    with open(self.data_dir + "/RooTroopActivityUsernames.csv", "a") as fid:
      fid.write(header)

      csv_keys = ["likes"        + key_ext_use,
                  "retweets"     + key_ext_use,
                  "quote_tweets" + key_ext_use,
                  "replies"      + key_ext_use
                 ]
      print(self.activity.keys())
      for key in csv_keys:
        name = key.split("_")[0]
        if key in self.activity.keys():
          line = name + "," + self.activity[key] + "\n"
        else:
          line = name + ",\n"
        # end if/else
        fid.write(line)
      # end for
      fid.write("\n\n")
    # end with open

    with open(self.data_dir + "/RooTroopActivityIds.csv", "a") as fid:
      fid.write(header)

      csv_keys = ["likes"        + key_ext_ids,
                  "retweets"     + key_ext_ids,
                  "quote_tweets" + key_ext_ids,
                  "replies"      + key_ext_ids
                 ]
      print(self.activity.keys())
      for key in csv_keys:
        name = key.split("_")[0]
        if key in self.activity.keys():
          line = name + "," + self.activity[key] + "\n"
        else:
          line = name + ",\n"
        # end if/else
        fid.write(line)
      # end for
      fid.write("\n\n")
    # end with open

    print("success process_activity")
  # end process_activity

  def process_tweets(self, urls):
    '''
    calls process_activity for each tweet_id passed in.
    '''
    print("begin process_tweets")


    for url in urls:
      self.process_activity(url)

      try:
        del self.activity, self.fname_likes, self.fname_retweets,\
            self.fname_quote_tweets, self.fname_replies
      except:
        pass
    # end for

    print("success_process_tweets")
  # end process_tweets
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
tweet_url = "https://twitter.com/mooneynft/status/1515382011267014657?s=20&t=pulk5_II0hc-Te5sP2NVIQ"
tweet_url = "https://twitter.com/RooTroopNFT/status/1515482071849865218"

#tweet_scrape_instance.fetch_data(tweet_url, dtype)
#tweet_scrape_instance.fetch_replies(tweet_id)
tweet_scrape_instance.fetch_activity(tweet_url)
#tweet_scrape_instance.process_activity(tweet_id)

#tweet_scrape_instance.process_tweets(urls)

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
