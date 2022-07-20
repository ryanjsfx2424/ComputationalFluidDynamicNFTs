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
import sys
import re
import ast
import glob
import time
import copy
import datetime
import numpy as np
import asyncio
import discord

sys.path.append("./interactions-ryanjsfx")
import interactions
from interactions import Button, ButtonStyle, ActionRow
from interactions.client import get
print("Begin ScrapeTweets")

start = time.time()
class ScrapeTweets(object):
  def __init__(self):
    '''
    just initializes some strings to reduce duplication / for convenience
    '''
    self.pages = {}
    self.force_update = False
    self.twitter_api_base = "https://api.twitter.com/2/tweets/"
    self.curl_base = "curl --request GET --url '"
    self.curl_header = "' --header 'Authorization: Bearer "
    self.data_dir = "twitter_data"
    self.dtypes = ["Likes", "Retweets", "QuoteTweets", "Replies"]
    self.include_text = '"includes":\{"users":\[\{'
    self.meta_text = '"meta":\{"'
    self.result_text = '"result_count":'
    self.created_text = '"created_at":"'

    self.fname_activity = self.data_dir + "/activity_by_user3.json"
    self.fname_user_info = self.data_dir + "/user_info.json"

    self.GUILDS = [893963935672324118, # roo troop
                   931482273440751638] # toTheMoons

    ## bot would like read messages/view channels + send messages + read msg history permissions: 68608
    self.BOT_COMMANDS_CIDS = [932056137518444594, # toTheMoons 
                              978015025585336420] # roo troop

    self.special_tweeters = {"1447280926967304195":"rootroopnft", 
                             "1477912158730170370":"troopsales"}
    self.max_loops = 300 # limit == 30,000 likes, RTs (note, max 900 requests per 15 minutes
    self.continuously_scrape_sleep_time = 10 # seconds

    self.S_PER_MINUTE = 60
    self.S_PER_HOUR   = self.S_PER_MINUTE * 60
    self.S_PER_DAY    = self.S_PER_HOUR   * 24
    self.S_PER_MONTH  = self.S_PER_DAY    * 31
    self.S_PER_YEAR   = self.S_PER_MONTH  * 12

    self.URL = "https://cdn.discordapp.com/attachments/965394881067515914/980589091718586428/4431.png"

    TITLE = "__Help Menu__"
    DESCRIPTION = "Hi! I'm Twitteroo, developed by TheLunaLabs © 2022"
    DESCRIPTION += "\nBelow are my commands, which are case insensitive:"

    embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
    embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)#, color=discord.Color.blue())
    embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.add_field(name="**__!rtthelp__**", value="Display this help menu", inline=True)
    embedDpy.add_field(name="**__!rtthelp__**", value="Display this help menu", inline=True)
    embedInt.add_field(name="**__!rttlb__**", value="Display leaderboard (all data)\nTo see options for granular leaderboards, run command: **__!rtthelplb__**", inline=False)
    embedDpy.add_field(name="**__!rttlb__**", value="Display leaderboard (all data)\nTo see options for granular leaderboards, run command: **__!rtthelplb__**", inline=False)
    embedInt.add_field(name="**__!rttkeywords__**", value="Display keywords we use to find Tweets that count towards your rank", inline=False)
    embedDpy.add_field(name="**__!rttkeywords__**", value="Display keywords we use to find Tweets that count towards your rank", inline=False)
    embedDpy.add_field(name="**__!rttverify <url>,<username>__**", value="Verify if we've processed your interaction", inline=False)
    embedInt.add_field(name="**__!rttverify <url>,<username>__**", value="Verify if we've processed your interaction", inline=False)
    embedDpy.add_field(name="**__!rttstats <username>__**", value="Display user's points, likes, etc.", inline=False)
    embedInt.add_field(name="**__!rttstats <username>__**", value="Display user's points, likes, etc.", inline=False)
    embedDpy.add_field(name="**__!rttrank <username>__**", value="Display user's points, likes, etc.", inline=False)
    embedInt.add_field(name="**__!rttrank <username>__**", value="Display user's rank (all data). To see options for granular ranks, run command: **__!rtthelplb__**", inline=False)
    self.helpEmbedDpy = embedDpy
    self.helpEmbedInt = embedInt
    

    LB_HELP_TITLE = "__Leaderboard Help Menu__"
    LB_HELP_DESCRIPTION = "Hi! I'm Twitteroo, developed by TheLunaLabs © 2022"
    LB_HELP_DESCRIPTION += "\nThis is the help meun for querying the leaderboard.\nThe following commands are available:"

    embedDpy = discord.Embed(title=LB_HELP_TITLE, description=LB_HELP_DESCRIPTION, color=discord.Color.blue())
    embedInt = interactions.Embed(title=LB_HELP_TITLE, description=LB_HELP_DESCRIPTION)#, color=discord.Color.blue())
    embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.add_field(name="**__!rttlblikes__**", value="Displays the Likes leaderboard.", inline=True)
    embedDpy.add_field(name="**__!rttlblikes__**", value="Displays the Likes leaderboard.", inline=True)
    embedInt.add_field(name="**__!rttlbretweets__**", value="Displays the Retweets leaderboard.", inline=False)
    embedDpy.add_field(name="**__!rttlbretweets__**", value="Displays the Retweets leaderboard.", inline=False)
    embedInt.add_field(name="**__!rttlbreplies__**", value="Displays the Replies leaderboard.", inline=False)
    embedDpy.add_field(name="**__!rttlbreplies__**", value="Displays the Replies leaderboard.", inline=False)
    embedInt.add_field(name="**__!rttlbpoints__**", value="Displays the Points leaderboard.\n\n**__LEADERBOARD BY TIME RANGE__**\n\n\n\n\n", inline=False)
    embedDpy.add_field(name="**__!rttlbpoints__**", value="Displays the Points leaderboard.\n\n**__LEADERBOARD BY TIME RANGE__**\n\n\n\n\n", inline=False)
    embedInt.add_field(name="\n**__!rttlbtoday__**", value="Past 24 hours (time-zone agnostic)", inline=False)
    embedDpy.add_field(name="\n**__!rttlbtoday__**", value="Past 24 hours (time-zone agnostic)", inline=False)
    embedInt.add_field(name="**__!rttlbq1__**", value="Data from January 1st, 2022 - April 1st, 2022", inline=False)
    embedDpy.add_field(name="**__!rttlbq1__**", value="Data from January 1st, 2022 - April 1st, 2022", inline=False)
    embedInt.add_field(name="**__!rttlbq2__**", value="Data from April 1st, 2022 - July 1st, 2022", inline=False)
    embedDpy.add_field(name="**__!rttlbq2__**", value="Data from April 1st, 2022 - July 1st, 2022", inline=False)
    embedInt.add_field(name="**__!rttlblastyear__**", value="Data from January 1st, 2021 - January 1st, 2022", inline=False)
    embedDpy.add_field(name="**__!rttlblastyear__**", value="Data from January 1st, 2021 - January 1st, 2022", inline=False)
    embedInt.add_field(name="**__!rttlblastmonth__**", value="Data from the last month.", inline=False)
    embedDpy.add_field(name="**__!rttlblastmonth__**", value="Data from the last month.", inline=False)
    embedInt.add_field(name="**__!rttlb <month>__**", value="Data from the specified month.", inline=False)
    embedDpy.add_field(name="**__!rttlb <month>__**", value="Data from the specified month.", inline=False)
    embedInt.add_field(name="**__!rttlb start: <month day, year, time>, end: <month day, year, time>__**", value="Data from the specified timeframe. **Must fit expected style and spaces matter!**\nExample: !rttlb start: January 5, 2022, 17:07:39, end: January 6, 2022, 01:00:00\n\n**NOTE:** leaderboard type & time range options can be combined!\nExample:", inline=False)
    embedDpy.add_field(name="**__!rttlb start: <month day, year, time>, end: <month day, year, time>__**", value="Data from the specified timeframe. **Must fit expected style and spaces matter!**\nExample: !rttlb start: January 5, 2022, 17:07:39, end: January 6, 2022, 01:00:00\n\n**NOTE:** leaderboard type & time range options can be combined!\nExample:", inline=False)
    embedInt.add_field(name="**__!rttlblikesfebruary__**", value="Displays the Likes leaderboard for February tweets.", inline=False)
    embedDpy.add_field(name="**__!rttlblikesfebruary__**", value="Displays the Likes leaderboard for February tweets.", inline=False)
    self.lbHelpEmbedDpy = embedDpy
    self.lbHelpEmbedInt = embedInt

    self.keyword_query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
    self.keyword_query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
    self.keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"

    self.mo_to_num = {"january"   : "01",
                      "february"  : "02",
                      "march"     : "03",
                      "april"     : "04",
                      "may"       : "05",
                      "june"      : "06",
                      "july"      : "07",
                      "august"    : "08",
                      "september" : "09",
                      "october"   : "10",
                      "november"  : "11",
                      "december"  : "12"}

    self.tab = 4*" "
    tab = self.tab

    msg2 = "Hi! These are the keywords I use to scrape for tweets:\n\n"
    for keyword in self.keyword_query.split("OR"):
      keyword = keyword.replace(")","")
      keyword = keyword.replace("("," ")
      msg2 += 2*tab + keyword + "\n"
    # end for
    self.help_keywords = msg2

    TITLE = "__Keywords__"
    DESCRIPTION = msg2

    embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
    embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)#, color=discord.Color.blue())
    embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    self.keyEmbedDpy = embedDpy
    self.keyEmbedInt = embedInt

    help_msg_base = ">>> Hi! I'm Twitteroo, developed by TheLunaLabs © 2022\n"
    self.help     = help_msg_base + \
                    "Below are my commands, "         + \
                    "which are case insensitive:\n\n" + \
                    "**__!rtthelp__**\n" + tab       + \
                    "Display this help menu\n\n"      + \
                    "**__!rttlb__**\n" + tab         + \
                    "Display leaderboard (all data)\n" + tab + \
                    "To see options for granular leaderboards, run command:\n**__!rtthelplb__**\n\n" + \
                    "**__!rttkeywords__**\n" + tab + \
                    "Display keywords we use to find Tweets that count towards your rank\n\n" + \
                    "**__!rttverify <url>, <username>__**\n" + tab  + \
                    "Verify if we've processed your interaction\n\n" + \
                    "**__!rttstats <username>__**\n" + tab + \
                    "Display user's points, likes, etc.\n"

    self.help_lb  = help_msg_base + \
                    "This is the help menu for querying the leaderboard." + \
                    " The following commands are available:\n\n" + \
                    "**__LEADERBOARD TYPES__**\n\n"             + \
                    "**__!rttlblikes__**\n" + tab             + \
                    "Displays the Likes leaderboard.\n\n"       + \
                    "**__!rttlbretweets__**\n" + tab          + \
                    "Displays the Retweets leaderboard.\n\n"    + \
                    "**__!rttlbreplies__**\n" + tab           + \
                    "Displays the Replies leaderboard.\n\n"     + \
                    "**__!rttlbpoints__**\n" + tab            + \
                    "Displays the Points leaderboard.\n\n"      + \
                    "**__LEADERBOARD BY TIME RANGE__**\n\n"     + \
                    "**__!rttlbtoday__**\n" + tab             + \
                    "Past 24 hours (time-zone agnostic)\n\n"    + \
                    "**__!rttlbq1__**\n" + tab                + \
                    "Data from January 1st, 2022 - April 1st, 2022\n\n" + \
                    "**__!rttlbq2__**\n" + tab                        + \
                    "Data from April 1st, 2022 - July 1st, 2022\n\n"    + \
                    "**__!rttlblastyear__**\n" + tab                 + \
                    "Data from January 1st, 2021 - January 1st, 2022\n\n" + \
                    "**__!rttlblastmonth__**\n" + tab                  + \
                    "Data from the last month.\n\n"                       + \
                    "**__!rttlb <month>__**\n" + tab                     + \
                    "Data from the specified month.\n\n"                  + \
                    "**__!rttlb start: <month day,year; time>, end: <month, day, year, time>__**\n" + tab + \
                    "Data from the specified timeframe. **Must fit expected style and spaces matter!**\n" + tab + \
                    "Example: !rttlb start: January 5, 2022; 17:07:39, end: January 6, 2022; 01:00:00\n\n" + \
                    "**NOTE**: leaderboard type & time range options can be combined! \nExample:\n" + \
                    "**__!rttlblikesfebruary__**\n" + tab + \
                    "Displays the Likes leaderboard for February tweets.\n"

    ## 900 requests per 15 minutes max but likes/retweets lookup is 75 (total or each so total is 150? unclear)
    self.api_calls_struct = {"time_limit_s": 15*self.S_PER_MINUTE, 
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
      self.user_dict["discordId_to_username"] = {}
    # end if

    if "discordId_to_username" not in self.user_dict.keys():
      self.user_dict["discordId_to_username"] = {}
    # end if

    with open("discord_data/linked_1.json", "r") as fid:
      line = ast.literal_eval(fid.read())
      self.linked_usernames = []
      self.linked_userIds = []
      self.linked_discordIds = []
      for el in line:
        self.linked_usernames.append(str(el["handle"]))
        self.linked_userIds.append(str(el["id_str"]))
        self.linked_discordIds.append(str(el["user"]))

        self.user_dict["userId_to_username"][str(el["id_str"])] = str(el["handle"])
        self.user_dict["username_to_userId"][str(el["handle"])] = str(el["id"])
        self.user_dict["discordId_to_username"][str(el["user"])] = str(el["handle"])
      # end for line
    # end with open
    for ii in range(len(self.user_dict["discordId_to_username"])):
      tun = list(self.user_dict["username_to_userId"])[ii]
      uid = list(self.user_dict["userId_to_username"])[ii]
      did = list(self.user_dict["discordId_to_username"])[ii]
      if tun not in self.linked_usernames:
        self.linked_usernames.append(tun)
        self.linked_userIds.append(uid)
        self.linked_discordIds.append(did)
      # end if
    # end for ii
    self.safe_save(self.fname_user_info, self.user_dict)
    print("loaded linked_usernames!")

    self.init_auth()

    #self.activity_by_user  = self.safe_load(self.fname_activity)
    #self.safe_save_abu("junk1", "junk2")
    self.activity_by_user = self.safe_load_abu()
    #self.clean_abu()
    #self.safe_save_abu("junk1", "junk2")
    #self.safe_save(self.fname_activity, self.activity_by_user)
    #print("abu == abu2: ", self.activity_by_user == self.activity_by_user2)

    #self.activity_by_linked_users = {}
    #for userid in self.activity_by_user:
    #  if userid in self.linked_userIds:
    #    self.activity_by_linked_users[userid] = self.activity_by_user[userid]
      # end if
    # end for
    #self.safe_save(self.data_dir + "/activity_by_linked_users.json", self.activity_by_linked_users)
    #self.fetch_user_leaderboard()
    #sys.exit()
  # end __init__

  def clean_abu(self):
    abu = self.activity_by_user
    for uid in abu:
      if uid[0].isdigit():
        tweet_ids = []
        tweet_contents = []
        tweet_times = []
        num_keyword_replies = 0
        num_keyword_retweets = 0
        num_loops = min(len(abu[uid]["tweet_creation_times"]), 
                        len(abu[uid]["tweet_contents"]))
        for ii in range(num_loops):
          if abu[uid]["tweet_creation_times"][ii] in tweet_times:
            continue
          # end if
          tweet_ids.append(abu[uid]["tweet_ids"][ii])
          tweet_times.append(abu[uid]["tweet_creation_times"][ii])
          content = abu[uid]["tweet_contents"][ii]
          if "RT " == content[:3]:
            num_keyword_retweets += 1
          else:
            num_keyword_replies += 1
          # end if/else
          tweet_contents.append(content)
        # end for
        abu[uid]["tweet_ids"] = tweet_ids
        abu[uid]["tweet_creation_times"] = tweet_times
        abu[uid]["tweet_contents"] = tweet_contents
        abu[uid]["num_keyword_replies"] = num_keyword_replies
        abu[uid]["num_keyword_retweets"] = num_keyword_retweets
      # end if
    # end for
  # end clean_abu





  def safe_load_abu(self):
    abu = {}
    os.chdir(self.data_dir + "/user_data3")
    fs = glob.glob("*.json")
    for fn in fs:
      with open(fn, "r") as fid:
        if fn[0].isdigit():
          abu[fn.replace(".json","")] =  ast.literal_eval(fid.read())
        else:
          if "latest_tweet_time_s.json" == fn:
            abu[fn.replace(".json","")] =  float(fid.read())
          else:
            abu[fn.replace(".json","")] =  str(fid.read())
      # end with
    # end for
    os.chdir("../..")
    return abu
  # end safe_load_abu

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
    tweet_time_s = float(yy)*self.S_PER_YEAR   + float(mo)*self.S_PER_MONTH + \
                   float(dd)*self.S_PER_DAY    + float(hh)*self.S_PER_HOUR  + \
                   float(mi)*self.S_PER_MINUTE + float(ss)
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
          if time.time() - self.api_calls_struct["call_times"][key][ii+offset] > 15*self.S_PER_MINUTE:
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
                "' --connect-timeout 30 --max-time 30 >> " + fname)
      
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

    for dtype in ["Likes"]:#self.dtypes:
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

    for dtype in ["Likes"]:#self.dtypes:
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
        num_days = 30
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
        await self.process_url_activity()

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
          "/tweets?tweet.fields=created_at&max_results=10"

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
          "/tweets?tweet.fields=created_at&max_results=10"
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

  async def process_url_activity(self):
    print("begin process_url_activity")

    fs = glob.glob(self.data_dir + "/activity_*.txt")
    for fname in fs:
      asyncio.sleep(0.01)
      with open(fname, "r") as fid:
        for line in fid:
          pass
        # end for line
      # end with open
      activity_by_url = ast.literal_eval(line)
      tweet_id = list(activity_by_url.keys())[0]
      tweet_creation_time = activity_by_url[tweet_id]["tweet_created_at"]

      for dtype in ["Likes"]:#self.dtypes:
        asyncio.sleep(0.01)
        data = activity_by_url[tweet_id][dtype]
        for ii,user_id in enumerate(data["ids"]):
          asyncio.sleep(0.001)
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

    self.safe_save_abu(self.fname_activity, self.activity_by_user)

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

          if latest_tweet_s < self.activity_by_user["latest_tweet_time_s"] and self.force_update == False:
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

    self.safe_save_abu(self.fname_activity, self.activity_by_user)

    print("ukd executed in (s): ", time.time() - start)
    print("success update_keyword_data")
  # end update_keyword_data

  #=====================================================
  #=====================================================
  #=====================================================

  def safe_save_abu(self, junk1, junk2):
    os.chdir(self.data_dir + "/user_data3")
    for key in self.activity_by_user:
      with open(key + ".json", "w") as fid:
        fid.write(str(self.activity_by_user[key]))
      # end with open
    # end for key
    os.chdir("../..")
  # end safe_save_abu

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
        if "data" not in line[ii].keys():
          print("data not in line ii keys: ")
          print("we'll wait for user input")
          input(">>")
          continue
        # end if
        for jj in range(len(line[ii]["data"])):
          tweet_time = self.get_tweet_time_s(line[ii]["data"][jj]["created_at"])
          latest_tweet_s = max(latest_tweet_s, tweet_time)
        # end for
      # end for
      await asyncio.sleep(0.02)

      if self.activity_by_user["latest_tweet_time_s"] >= latest_tweet_s and self.force_update == False:
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

      self.safe_save_abu(self.fname_activity, self.activity_by_user)
      os.system("rm " + fname)
    # end for fnames

    print("pkd executed in (s): ", time.time() - start)
    print("success process_keyword_data")
  # end process_keyword_data

  #=====================================================
  #=====================================================
  #=====================================================
  #=====================================================

  async def fetch_rank(self, username, start_time="2020-05-04T23:59:59.000Z", 
    end_time="4022-05-04T23:59:59.000Z", method="Points", sharded=True, time_str="all"):
    print("begin fetch_rank")
    tstart = time.time()

    await asyncio.sleep(0.1)

    TITLE = method + " Rank for " + time_str + " data range"
    DESCRIPTION = "username: " + username
    embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
    embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION,)#, color=discord.Color.blue())
    embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)

    print("start_time: ", start_time)
    print("end_time: ", end_time)
    start_time_s = self.get_tweet_time_s(start_time)
    end_time_s   = self.get_tweet_time_s(end_time)
    print("start_time_s: ", start_time_s)
    print("end_time_s: ", end_time_s)

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
      #print("user: ", user)
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
      replies_cnt = 0
      retweets_cnt = 0
      tweet_contents = []
      tweet_times = []
      #print("len tct: ", len(self.activity_by_user[user]["tweet_creation_times"]))
      #print("len tc: ", len(self.activity_by_user[user]["tweet_contents"]))
      num_loops = min(len(self.activity_by_user[user]["tweet_creation_times"]),
                      len(self.activity_by_user[user]["tweet_contents"]))
      for ii in range(num_loops):
        ## avoiding double counting via looking at the tweet_ids from Likes etc
        ## currently won't work since at the root level tweet_ids contains all tweet_ids
        ## not just the ones from keyword stuff :(
        ## so either I gotta live with double counting or kind of start over.
        #if self.activity_by_user[user]["tweet_ids"][ii] in tweet_ids:
          #continue
        tweet_content = self.activity_by_user[user]["tweet_contents"][ii]
        tweet_time = self.activity_by_user[user]["tweet_creation_times"][ii]
        #if tweet_content in tweet_contents:
        if tweet_time in tweet_times:
          continue
        # end if
        tweet_times.append(tweet_time)
        tweet_contents.append(tweet_content)
        tweet_content = tweet_content.lower()

        ## below if statement to exclude LuckyRooToken tweets...or we
        ## could just check for whitelisted users???
        if "#luckyroo" in tweet_content or "@luckyr" in tweet_content or \
           "#saita" in tweet_content or "@saita" in tweet_content or \
           "promote it on" in tweet_content: # last one to filter out spam bots
          continue
        # end if

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
      #print("abu uns fr: ", self.activity_by_user[user]["usernames"])
      #print("abu uns fr -1: ", self.activity_by_user[user]["usernames"][-1])
      usernames.append(self.activity_by_user[user]["usernames"][-1].lower())
      for content in list(self.activity_by_user[user]["tweet_contents"]):
        contents.append(content)
      # end for
      if self.user_dict["userId_to_username"][user] == "morganstoneee":
        print("hi")
        print()
        print("keyword_replies: ", keyword_replies[-1])
        print("keyword_retweets: ", keyword_retweets[-1])
        print("num_Likes: ", num_dict["num_Likes"][-1])
        print("num_Retweets: ", num_dict["num_Retweets"][-1])
        print("num_Replies: ", num_dict["num_Replies"][-1])
        print("num_QuoteTweets: ", num_dict["num_QuoteTweets"][-1])
    # end for
    print("uns fr after loop: ", usernames)

    keyword_replies = np.array(keyword_replies)
    keyword_retweets = np.array(keyword_retweets)
    num_Likes = np.array(num_dict["num_Likes"])
    num_Retweets = np.array(num_dict["num_Retweets"])
    num_QuoteTweets = np.array(num_dict["num_QuoteTweets"])
    num_Replies = np.array(num_dict["num_Replies"])

    num_Retweets = num_Retweets + keyword_retweets + num_QuoteTweets
    num_Replies  = num_Replies  + keyword_replies  + num_QuoteTweets

    points = num_Likes*1 + num_Retweets*2 + num_Replies*3

    usernames = np.array(usernames)
    #print("1672 uns fr after loop: ", usernames)

    if   method == "Points":
      inds = np.argsort(points)[::-1]
      val = points
    elif method == "Likes":
      inds = np.argsort(num_Likes)[::-1]
      val = num_Likes
    elif method == "Retweets":
      inds = np.argsort(num_Retweets)[::-1]
      val = num_Retweets
    #elif method == "QuoteTweets":
    #  inds = np.argsort(num_QuoteTweets)[::-1]
    #  val = num_QuoteTweets
    elif method == "Replies":
      inds = np.argsort(num_Replies)[::-1]
      val = num_Replies
    #elif method == "keyword_replies":
    #  inds = np.argsort(keyword_replies)[::-1]
    #  val = keyword_replies
    #elif method == "keyword_retweets":
    #  inds = np.argsort(keyword_retweets)[::-1]
    #  val = keyword_retweets
    # end if/elifs

    username = username.lower()
    print(" 1698 un fr passed in: ", username)
    try:
      ind = np.where(usernames[inds] == username)[0][0]
    except:
      ind = np.where(usernames[inds] == username)
    # end try/except
    print("useranme; ", username)
    print("u ind: ", usernames[inds][ind])

    embedDpy.add_field(name="Rank", value=str(ind), inline=False)
    embedInt.add_field(name="Rank", value=str(ind), inline=False)
    self.rankEmbedDpy = embedDpy
    self.rankEmbedInt = embedInt

    print("fr executed in (s): ", time.time() - tstart)
    print("success fetch_rank")
  # end def fetch_rank

  #=====================================================
  #=====================================================
  #=====================================================
  #=====================================================

  async def fetch_user_leaderboard(self, start_time="2020-05-04T23:59:59.000Z", 
    end_time="4022-05-04T23:59:59.000Z", method="Points", sharded=True, time_str="all"):
    print("begin fetch_user_leaderboard")
    tstart = time.time()

    await asyncio.sleep(0.1)

    TITLE = method + " Leaderboard for " + time_str + " data range"
    DESCRIPTION = "\u200b"
    embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
    embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION,)#, color=discord.Color.blue())
    embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)

    print("start_time: ", start_time)
    print("end_time: ", end_time)
    start_time_s = self.get_tweet_time_s(start_time)
    end_time_s   = self.get_tweet_time_s(end_time)
    print("start_time_s: ", start_time_s)
    print("end_time_s: ", end_time_s)

    keyword_replies  = []
    keyword_retweets = []
    usernames = []
    contents  = []
    tweet_ids = []

    num_dict = {"num_Likes":[],
                "num_Retweets":[],
                "num_QuoteTweets":[],
                "num_Replies":[]}

    #print("fuls line 1692 (s): ", time.time() - tstart)
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
      #print("user: ", user)
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
      #print("fuls line 1692 (s): ", time.time() - tstart)
      #print(self.activity_by_user[user])
      if "Gio3272" in self.activity_by_user[user]["usernames"]:
        print("Gio lb rt: ", self.activity_by_user[user]["Retweets"]["num_Retweets"])
      replies_cnt = 0
      retweets_cnt = 0
      tweet_times = []
      #print("len tct: ", len(self.activity_by_user[user]["tweet_creation_times"]))
      #print("len tc: ", len(self.activity_by_user[user]["tweet_contents"]))
      num_loops = min(len(self.activity_by_user[user]["tweet_creation_times"]),
                      len(self.activity_by_user[user]["tweet_contents"]))
      for ii in range(num_loops):
        ## avoiding double counting via looking at the tweet_ids from Likes etc
        ## currently won't work since at the root level tweet_ids contains all tweet_ids
        ## not just the ones from keyword stuff :(
        ## so either I gotta live with double counting or kind of start over.
        #if self.activity_by_user[user]["tweet_ids"][ii] in tweet_ids:
          #continue
        tweet_content = self.activity_by_user[user]["tweet_contents"][ii]
        tweet_time = self.activity_by_user[user]["tweet_creation_times"][ii]
        #if tweet_content in tweet_contents:
        if tweet_time in tweet_times:
          continue
        # end if
        tweet_times.append(tweet_time)
        tweet_content = tweet_content.lower()

        ## below if statement to exclude LuckyRooToken tweets...or we
        ## could just check for whitelisted users???
        if "#luckyroo" in tweet_content or "@luckyr" in tweet_content or \
           "#saita" in tweet_content or "@saita" in tweet_content or \
           "promote it on" in tweet_content: # last one to filter out spam bots
          continue
        # end if

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
      if self.user_dict["userId_to_username"][user] == "morganstoneee":
        print("hi")
        print()
        print("un: ", self.user_dict["userId_to_username"][user])
        print("keyword_replies: ", keyword_replies[-1])
        print("keyword_retweets: ", keyword_retweets[-1])
        print("num_Likes: ", num_dict["num_Likes"][-1])
        print("num_Retweets: ", num_dict["num_Retweets"][-1])
        print("num_Replies: ", num_dict["num_Replies"][-1])
        print("num_QuoteTweets: ", num_dict["num_QuoteTweets"][-1])
      if self.user_dict["userId_to_username"][user].lower() == "gio3272":
        print("hi")
        print()
        print("un: ", self.user_dict["userId_to_username"][user])
        print("keyword_replies: ", keyword_replies[-1])
        print("keyword_retweets: ", keyword_retweets[-1])
        print("num_Likes: ", num_dict["num_Likes"][-1])
        print("num_Retweets: ", num_dict["num_Retweets"][-1])
        print("num_Replies: ", num_dict["num_Replies"][-1])
        print("num_QuoteTweets: ", num_dict["num_QuoteTweets"][-1])
    # end for
    #print("fuls line 1787 (s): ", time.time() - tstart)

    keyword_replies = np.array(keyword_replies)
    keyword_retweets = np.array(keyword_retweets)
    num_Likes = np.array(num_dict["num_Likes"])
    num_Retweets = np.array(num_dict["num_Retweets"])
    num_QuoteTweets = np.array(num_dict["num_QuoteTweets"])
    num_Replies = np.array(num_dict["num_Replies"])

    num_Retweets = num_Retweets + keyword_retweets + num_QuoteTweets
    num_Replies  = num_Replies  + keyword_replies  + num_QuoteTweets

    points = num_Likes*1 + num_Retweets*2 + num_Replies*3

    usernames = np.array(usernames)

    inds = np.argsort(points)[::-1]
    self.points_usernames = usernames[inds]

    if   method == "Points":
      inds = np.argsort(points)[::-1]
      val = points
    elif method == "Likes":
      inds = np.argsort(num_Likes)[::-1]
      val = num_Likes
    elif method == "Retweets":
      inds = np.argsort(num_Retweets)[::-1]
      val = num_Retweets
    #elif method == "QuoteTweets":
    #  inds = np.argsort(num_QuoteTweets)[::-1]
    #  val = num_QuoteTweets
    elif method == "Replies":
      inds = np.argsort(num_Replies)[::-1]
      val = num_Replies
    #elif method == "keyword_replies":
    #  inds = np.argsort(keyword_replies)[::-1]
    #  val = keyword_replies
    #elif method == "keyword_retweets":
    #  inds = np.argsort(keyword_retweets)[::-1]
    #  val = keyword_retweets
    # end if/elifs

    vpp = 20 # vals per page
    num_pages = int(np.ceil(len(usernames)/vpp))
    leaderboards      = []
    leaderboardsEmbed = []
    self.lbEmbedDpys = []
    self.lbEmbedInts = []
    #print("fuls line 1834 (s): ", time.time() - tstart)
    for jj in range(num_pages):
      start = jj*vpp
      end = (jj+1)*vpp
      if start > len(inds):
        continue
      if end > len(inds):
        end = len(inds)
      indsp = inds[start:end]

      usernamesp = usernames[indsp]
      valp       = val[indsp]

      max_name_len = 0
      max_val_len  = 0
      for ii in range(len(indsp)):
        max_name_len = max(max_name_len, len(usernamesp[ii]))
        max_val_len  = max(max_val_len,  len(str(valp[ii])))
      # end for ii

      leaderboards.append(">>> ```")
      leaderboardsEmbed.append("```")
      for ii in range(len(indsp)):
        line = str(jj*vpp+ii).rjust(2) + ") " + \
          (usernamesp[ii] + ":").ljust(max_name_len+1) + " " + \
            str(valp[ii]).rjust(max_val_len) + "\n"
        leaderboards[-1] += line
        leaderboardsEmbed[-1] += line
      # end for ii
      leaderboards[-1] += "```"
      leaderboardsEmbed[-1] += "```"

      curEmbedDpy = copy.deepcopy(embedDpy)
      curEmbedInt = copy.deepcopy(embedInt)

      curEmbedDpy.add_field(value=leaderboardsEmbed[-1], name="\u200b", inline=False)
      curEmbedInt.add_field(value=leaderboardsEmbed[-1], name="\u200b", inline=False)

      self.lbEmbedDpys.append(curEmbedDpy)
      self.lbEmbedInts.append(curEmbedInt)
    # end for
    #print("fuls line 1874 (s): ", time.time() - tstart)
    leaderboard = leaderboards[0]

    await asyncio.sleep(0.03)
    lb_str = "leaderboard"
    if sharded == True:
      lb_str += "Sharded"
    # end if
    fname = self.data_dir + "/" + lb_str + "_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
    tnow = datetime.datetime.now()
    tnow = tnow.strftime("%Y-%m-%d_%H:%M:%S")
    #print("fuls line 1885 (s): ", time.time() - tstart)
    with open(fname, "w") as fid:
      fid.write("last updated: " + tnow + "\n")
      fid.write(leaderboard)
    # end with

    self.lbEmbedDpy = embedDpy
    self.lbEmbedInt = embedInt

    print("fuls executed in (s): ", time.time() - tstart)
    print("success fetch_user_leaderboard")
    print("lb: ", leaderboard)
    print("type lb: ", type(leaderboard))
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
        
    #print("ud twids: ", user_data["tweet_ids"])
    #print("self_tweet_id: ", self_tweet_id)
    #print("ud un0: ", user_data["usernames"][0])

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
    message = ">>> Hmm, I don't see any interaction from the specified user on this Tweet. Are you sure there was a keyword or that the user did indeed interact? If so, please reach out to Ryan so he can look into it!"

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
      return [False, "error! username not found :(```"]
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
      return [False, "error! username not found :(```"]
    # end try/except
  # def fetch_user_data

  #=====================================================
  #=====================================================
  #=====================================================

  def fetch_user_points(self, user_data):
    ## uses result of fetch_user_data above

    TITLE = "Username: " + user_data["usernames"][-1]
    DESCRIPTION = "--"
    embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
    embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION,)#, color=discord.Color.blue())
    embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                    icon_url=self.URL)
    #embedDpy.set_author(name=user_data["usernames"][-1], 
    #  icon_url="https://pbs.twimg.com/profile_images/1327036716226646017/ZuaMDdtm_400x400.jpg")
    #embedInt.set_author(name=user_data["usernames"][-1], 
    #  icon_url="https://pbs.twimg.com/profile_images/1327036716226646017/ZuaMDdtm_400x400.jpg")

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
    tweet_times = []
    num_loops = min(len(user_data["tweet_creation_times"]),
                    len(user_data["tweet_contents"]))
    for ii in range(num_loops):
      tweet_content = user_data["tweet_contents"][ii]
    #for ii,tweet_content in enumerate(user_data["tweet_contents"]):
      #if user_data["tweet_ids"][ii] in tweet_ids:
      #  continue
      # end if
      ## the above is to avoid double counting from the interactions with the keyword
      ## stuff. No need to append to tweet_ids :)
      ## But it doesn't work currently, see note in fetch_user_leaderboard... :*(

      tweet_time = user_data["tweet_creation_times"][ii]
      #if tweet_content in tweet_contents:
      if tweet_time in tweet_times:
        continue
      # end if
      tweet_times.append(tweet_time)
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
           + num_dict["num_QuoteTweets"]*5 + num_dict["num_Replies"]*3   

    try:
      ind = np.where(self.points_usernames == user_data["usernames"][-1])[0][0]
    except:
      ind = "?"
    vals = {
      "Rank":             ind,
      "Points":           points,
      "Likes":            num_dict["num_Likes"],
      "Retweets":         num_dict["num_Retweets"] + num_dict["num_keyword_retweets"] + num_dict["num_QuoteTweets"],
      "Replies":          num_dict["num_Replies"] + num_dict["num_keyword_replies"] + num_dict["num_QuoteTweets"]
    }

    max_str    = 0
    max_digits = 0
    for key in vals.keys():
      max_str = max(max_str, len(key))
      max_digits = max(max_digits, len(str(vals[key])))
    # end for keys
    print("max_str: ", max_str)
    print("max_digits: ", max_digits)

    #message    = ">>> ```"
    message = ""
    for key in vals.keys():
      embedDpy.add_field(name=key, value=str(vals[key]), inline=False)
      embedInt.add_field(name=key, value=str(vals[key]), inline=False)
      message += key + ":" + (max_str-len(key))*" " + 4*" " + \
        (max_digits - len(str(vals[key])))*" " + str(vals[key]) + "\n"
    # end for
    message += "```"
    print(message)
    #sys.exit()
    self.statEmbedDpy = embedDpy
    self.statEmbedInt = embedInt

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

  async def convert_tweet_times_special_tweeters(self):
    for user_id in list(self.special_tweeters.keys()):
      username = self.special_tweeters[user_id]
      fname = self.data_dir + "/activity_" + username + ".json"
      activity = self.safe_load(fname)
      print("type(activity): ", type(activity))
      print("len(activity): ", len(activity))
      tweet_ids   = np.zeros(len(activity))
      tweet_times = np.zeros(len(activity))
      cnt = -1
      for tweetid_dict in activity:
        for tweetid in tweetid_dict:
          cnt += 1
          tweet_info = tweetid_dict[tweetid]
          tweet_time = tweet_info["tweet_created_at"]
          #print("tweet_time: ", tweet_time)
          tweet_times[cnt] = self.get_tweet_time_s(tweet_time)
          tweet_ids[cnt] = tweetid
          #print("datetime.datetime.now: ", str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")))
          #print("tnow_s: ", tnow_s)
          #print("tt cnt: ", tweet_times[cnt])
          #sys.exit()
        # end for
      # end for
      inds = np.argsort(tweet_times)[::-1]
      tweet_times = tweet_times[inds]
      tweet_ids = tweet_ids[inds]
      np.savetxt(self.data_dir + "/sorted_tweets_by_" + username + ".txt", [inds,tweet_ids,tweet_times])

      tnow = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
      tnow_s = self.get_tweet_time_s(tnow)
      inds = np.where(tweet_times > tnow_s - self.S_PER_DAY)
      print("len(inds): ", len(inds))
    # end for special_tweeters

    sys.exit()
  # end convert_tweet_times_special_tweeters

  async def continuously_scrape(self):
    print("BEGIN cont scrape")
    await asyncio.sleep(0.1)
    cs_start = time.time()

    #for cs_user_id in list(self.special_tweeters.keys()):
    #  await self.process_all_tweets_by_user(cs_user_id, update=True)
    #sys.exit()
    #await self.convert_tweet_times_special_tweeters()

    await asyncio.sleep(0.1)
    keyword_update_start = time.time()
    await self.update_keyword_data()
    await asyncio.sleep(0.1)
    await self.process_keyword_data()

    msg1 = "keyword update executed in: " + str(time.time() - keyword_update_start)
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

    os.system("python3 stream.py &")
    wcnt = 0
    while True:
      await asyncio.sleep(0.2)
      wcnt += 1
      #if wcnt % 100000 == 0:
      #  await self.process_all_tweets_by_user(cs_user_id, update=False)
      #  print("done processing all tweets by user!!!")
      
      fs = np.sort(glob.glob("stream_data?.txt"))
      #print("fs: ", fs)
      for fn in fs:
        #print("fn: ", fn)
        await asyncio.sleep(0.02)
        with open(fn, "r") as fid:
          for line in fid:
            await asyncio.sleep(0.02)
            try:
              line = ast.literal_eval(line)
            except:
              continue
            # end try/except
            if "matching_rules" not in line:
              continue
            # end if
            flag = "keyword"
            for matching_rule in line["matching_rules"]:
              if   matching_rule["tag"] == "retweetstag":
                flag = "retweet"
              elif matching_rule["tag"] == "quotestag":
                flag = "quotetweet"
              # end if/elif
            # end for
            author_id = line["data"]["author_id"]

            if author_id not in list(self.activity_by_user.keys()):
              self.activity_by_user[author_id] = \
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
            tweet_id = line["data"]["id"]
            if tweet_id in self.activity_by_user[author_id]["tweet_ids"]:
              #print("twid in abu?")
              continue
            # end if
            self.activity_by_user[author_id]["tweet_ids"].append(tweet_id)

            if flag == "retweet":
              self.activity_by_user[author_id]["num_keyword_retweets"] += 1
            elif flag == "quotetweet":
              self.activity_by_user[author_id]["num_keyword_retweets"] += 1
              self.activity_by_user[author_id]["num_keyword_replies" ] += 1
            else:
              self.activity_by_user[author_id]["num_keyword_replies"] += 1
            # end if/else

            for user in line["includes"]["users"]:
              await asyncio.sleep(0.003)
              if user["id"] == author_id:
                username = user["username"]
                break
              # end if
            # end for
            usernames = list(set(self.activity_by_user[author_id]["usernames"] + [username]))
            self.activity_by_user[author_id]["usernames"] = usernames
            self.activity_by_user[author_id]["tweet_contents"].append(line["data"]["text"])
            self.activity_by_user[author_id]["tweet_creation_times"].append(line["data"]["created_at"])

            if username not in list(self.user_dict["username_to_userId"].keys()):
              self.user_dict["userId_to_username"][author_id] = username
              self.user_dict["username_to_userId"][username ] = author_id
              await asyncio.sleep(0.02)
              self.safe_save(self.fname_user_info, self.user_dict)
            # end if
          # end for line
        # end with open
      # end for fs
      await asyncio.sleep(0.02)
      #self.safe_save_abu(self.fname_activity, self.activity_by_user)
      #await self.get_activity_by_linked_users()
      ## next, check for users to add to linked_1.json
    # end while
  # end def continuously_scrape

  async def get_activity_by_linked_users(self):
    activity_by_linked_users = {}
    for userid in self.activity_by_user:
      await asyncio.sleep(0.1)
      if userid in self.linked_userIds:
        activity_by_linked_users[userid] = self.activity_by_user[userid]
      # end if
    # end for
    self.activity_by_linked_users = activity_by_linked_users
  # end def

  def convert_time(self, human_time):
    ## convert the strings to a form twitter likes
    print("start convert_time")
    print("human_time: ", human_time)
    p1,p2,p3 = human_time.split(",")
    print("p1,p2,p3: ", p1,  p2, p3)
    p1 = p1.replace(",","")
    if p1[0] != " ":
      p1 = " " + p1
    # end if
    print("p1: ", p1)

    junk,month,day = p1.split(" ")
    year = p2
    year = year.replace(" ", "")
    if month not in self.mo_to_num.keys():
      msg2 = ">>> sorry we couldn't parse the month."
      return [False, msg2]
    # end if
    month = self.mo_to_num[month]
    print("month: ", month)

    p2 = p3
    hours,minutes,seconds = p2.split(":")
    hours   = hours.replace(" ","")
    minutes = minutes.replace(" ","")
    seconds = seconds.replace(" ","")
    hours = hours[:2]
    minutes = minutes[:2]
    seconds = seconds[:2]
    print("seconds: ", seconds)

    machine_time = year + "-" + month + "-" + day + "T" + \
                   hours + ":" + minutes + ":" + seconds + ".000Z"
    return [True, machine_time]
  # end convert_time

  #=====================================================
  #=====================================================
  #=====================================================

  async def embed_helper(self, pages, client, channel):
    xemoji = "🇽"

    async def post_page(page):
      message = await channel.send(embed=page)
      if len(pages) > 1:
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')
      # end if
      await message.add_reaction(xemoji)
      return message
    # end post_page
    message = await post_page(pages[0])
    self.pages[str(message.id)] = {"pnum":0, "pages":pages}
    return

    '''
    print("CACHED SLOTS: ", message._CACHED_SLOTS)
    print("HANDLERS: ", message._HANDLERS)
    print("add reaction: ", message._add_reaction)
    print("clear emoji: ", message._clear_emoji)
    #print("cs channel mentions: ", message._cs_channel_mentions)
    print("cs clean content: ", message._cs_clean_content)
    print("cs guild: ", message._cs_guild)
    print("cs raw channel mentions: ", message._cs_raw_channel_mentions)
    print("cs raw mentions: ", message._cs_raw_mentions)
    print("cs raw role mentions: ", message._cs_raw_role_mentions)
    print("cs system content: ", message._cs_system_content)
    print("edited timestamp: ", message._edited_timestamp)
    print("handle activity: ", message._handle_activity)
    print("handle application: ", message._handle_application)
    print("handle attachments: ", message._handle_attachments)
    print("handle author: ", message._handle_author)
    print(message._handle_call)
    print(message._handle_content)
    print(message._handle_edited_timestamp)
    print(message._handle_embeds)
    print(message._handle_flags)
    print(message._handle_member)
    print(message._handle_mention_everyone)
    print(message._handle_mention_roles)
    print(message._handle_mentions)
    print(message._handle_nonce)
    print(message._handle_pinned)
    print(message._handle_tts)
    print(message._handle_type)
    print(message._rebind_channel_reference)
    print(message._remove_reaction)
    print(message._state)
    print(message._try_patch)
    print(message._update)
    print(message.ack)
    print(message.activity)
    print(message.add_reaction)
    print(message.application)
    print(message.attachments)
    print(message.author)
    print(message.call)
    print(message.channel)
    print(message.channel_mentions)
    print(message.clean_content)
    print(message.clear_reaction)
    print(message.clear_reactions)
    print(message.content)
    print(message.created_at)
    print(message.delete)
    print(message.edit)
    print(message.edited_at)
    print(message.embeds)
    print(message.flags)
    print(message.guild)
    print(message.id)
    print(message.is_system)
    print(message.jump_url)
    print(message.mention_everyone)
    print(message.mentions)
    print(message.nonce)
    print(message.pin)
    print(message.pinned)
    print(message.publish)
    print(message.raw_channel_mentions)
    print(message.raw_mentions)
    print(message.raw_role_mentions)
    print(message.raw_reactions)
    print(message.refrence)
    print(message.remove_reaction)
    print(message.reply)
    print(message.role_mentions)
    print(message.stickers)
    print(message.system_content)
    print(message.to_message_reference_dict)
    print(message.to_reference)
    print(message.tts)
    print(message.type)
    print(message.unpin)
    print(message.webhook_id)

    for el in dir(message):
      print("el: ", el)
      print("eval el: ", ast.literal_eval(str("message." + el)))
    '''
    #rxn = discord.utils.get(message.reactions, emoji=xemoji)
    #print("message.reactions: ", message.reactions)
    #print("smtg: ", smtg)
    #sys.exit()

    def check(reaction, user):
      print("reaction: ", reaction)
      print("type reaction: ", type(reaction))
      print("dir reaction: ", dir(reaction))
      print("reaction.message.author: ", reaction.message.author)
      if "Tweeteroo#4024" in reaction.message.author:
        return False
      else:
        return True
      # end if/else
    # end check

    ii = 0
    reaction = None

    while True:
      io = ii
      await asyncio.sleep(0.2)
      
      try:
        reaction = await client.wait_for("reaction_add", timeout=30.0)#, check=check)
      except Exception as err:
        print("error")
        print(err)
        print("s react: ", str(reaction))
        if "Tweeteroo#4024" in str(reaction):
          continue
        break
      # end try/except
      print("hi")
      print("ii b4: ", ii)
      print(reaction)
      print(str(reaction))
      print(str(reaction).split("=")[1].split()[0])
      reaction = str(reaction).split("=")[1].split()[0].replace("'","")
      if str(reaction) == '⏮':
        print("to beginning")
        ii = 0
      elif str(reaction) == '◀':
        print("back one")
        if ii > 0:
          ii -= 1
      elif str(reaction) == '▶':
        print("fwd one")
        if ii < len(pages)-1:
          ii += 1
      elif str(reaction) == '⏭':
        print("to end")
        ii = len(pages)-1
      #elif str(reaction) == xemoji:
      #  print("xemoji reacted so breaking")
      #  break
      else:
        print("none of those")
      # end if/elifs
      print("ii after: ", ii)
      print("hi2")

      if ii != io:
        print("updating!")
        #await message.delete()
        await message.clear_reactions()
        message = await post_page(pages[ii])
      # end if
    # end while
    print("hi gonna delete")
    await message.delete()
    print("hi deleted")
    # end wait
  # end help_menu

  #=====================================================
  #=====================================================
  #=====================================================

  def discord_bot(self):
    print("begin discord_bot")
    secret = os.environ.get("rttBotPass")
    intBot = interactions.Client(secret)
    print("clientInteractions loaded")
    client = discord.Client()
    print("client loaded")

    @intBot.event
    async def on_ready():
      user = await get.get(intBot, interactions.User, user_id=int(intBot.me.id))
      print("We have logged in as {0.username}#{1.discriminator}".format(user,user))

      for BOT_COMMANDS_CID in self.BOT_COMMANDS_CIDS:
        channel = await get.get(intBot, interactions.Channel, channel_id=BOT_COMMANDS_CID)
        await channel.send("I AM ALIVE! MWAHAHAHA")
        break
      # end for
    # end on_ready

    @intBot.command(
      name="rtt",
      description="Tweeteroo commaands",
      scope=self.GUILDS,
      options=[
        interactions.Option(
          name="help",
          description="General help menu",
          type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
          name="helplb",
          description="Leaderboard help menu",
          type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
          name="keywords",
          description="List keywords we scrape",
          type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
          name="stats",
          description="User's twitter stats",
          type=interactions.OptionType.SUB_COMMAND,
          options=[
            interactions.Option(
              name="username",
              description="Your twitter username",
              type=interactions.OptionType.STRING,
              required=False,
            ),
          ],
        ),
        interactions.Option(
          name="verify",
          description="Verify if tweet has been processed",
          type=interactions.OptionType.SUB_COMMAND,
          options=[
            interactions.Option(
              name="url",
              description="Tweet URL",
              type=interactions.OptionType.STRING,
              required=True,
            ),
            interactions.Option(
              name="username",
              description="Your twitter username",
              type=interactions.OptionType.STRING,
              required=False,
            ),
          ],
        ),
        interactions.Option(
          name="lb",
          description="Twitter Leaderboard",
          type=interactions.OptionType.SUB_COMMAND,
          options=[
            interactions.Option(
              name="method",
              description="Leaderboard Type",
              type=interactions.OptionType.STRING,
              required=False,
            ),
            interactions.Option(
              name="timerange",
              description="Leaderboard Time Range",
              type=interactions.OptionType.STRING,
              required=False,
            ),
          ],
        ),
        interactions.Option(
          name="rank",
          description="Twitter Rank",
          type=interactions.OptionType.SUB_COMMAND,
          options=[
            interactions.Option(
              name="username",
              description="Twitter Username",
              type=interactions.OptionType.STRING,
              required=False,
            ),
            interactions.Option(
              name="method",
              description="Rank Type",
              type=interactions.OptionType.STRING,
              required=False,
            ),
            interactions.Option(
              name="timerange",
              description="Rank Time Range",
              type=interactions.OptionType.STRING,
              required=False,
            ),
          ],
        ),
      ],
    )
    async def cmd(ctx: interactions.CommandContext, sub_command: str,
                  username: str = None, method: str = None,
                  timerange: str = None, url: str = None):
      tab = self.tab
      if   sub_command in ["help", "halp", "hlp"]:
        await ctx.send(embeds=self.helpEmbedInt, ephemeral=True)

      elif sub_command in ["helplb","halplb","hlplb", 
                         "lbhelp","lbhalp","lbhlp"]:
        await ctx.send(embeds=self.lbHelpEmbedInt, ephemeral=True)
        #await ctx.send(self.help_lb, ephemeral=True)

      elif sub_command in ["keywords"]:
        await ctx.send(embeds=self.keyEmbedInt, ephemeral=True)

      elif sub_command in ["stats","stat"]:
        if username != None:
          username = username.lower()
          username = username.replace("@","")
          username = username.replace(" ","")

          print(">>> fetching user data")
          try:
            msg2 = ">>> ```Username: " + username + "\n"
            msg2 += "--\n"
          
            status, user_data = self.fetch_user_data(username)
            if status == False:
              msg2 += user_data
            else:
              print(">>> and now I'm computing user points")
              msg2 += self.fetch_user_points(user_data)
              #self.statEmbedInt.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
              await ctx.send(embeds=self.statEmbedInt, ephemeral=True)
              return
            # end if/else
          except:
            msg2  = ">>> sorry, I couldn't parse that. I'm loooking for smtg like\n"
            msg2 += 2*tab + "*!rtt stats username:TheLunaLabs*"
          # end try/except
          await ctx.send(msg2, ephemeral=True)
        else:
          if True:
            print(ctx)
            print()
            print(dir(ctx))
            print()
            print(dir(ctx.author))
            print()
            print(ctx.author)
            print()
            discord_id = str(ctx.author.id)
            try:
              username = self.user_dict["discordId_to_username"][discord_id]
            except:
              msg2 = "```>>> Danggg. Looks like I don't know your twitter username. Unpack this rage against the machine by slapping a seal ;)```"
              await ctx.send(msg2, ephemeral=True)
              return
              ## check if they have it linked, if so, slap a seal, say sorry
              ## and ask for them to enter it again
              ## if they haven't linked it, then just ask them for it
              return
            # end try/except
          # end if/else
          print("username: ", username)
          print("len username: ", len(username))
          print("u != '': ", username != "")
          msg2 = ">>> ```Username: " + username + "\n"
          msg2 += "--\n"
          if True:
            print(">>> fetching user data")
            status, user_data = self.fetch_user_data(username)
            if status == False:
              print("user_data: ", user_data)
              msg2 += user_data
              print("msg2: ", msg2)
            else:
              #print(user_data)
              print(">>> and now I'm computing user points")
              msg2 += self.fetch_user_points(user_data)
              #self.statEmbedInt.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
              await ctx.send(embeds=self.statEmbedInt, ephemeral=True)
              return
              print("msg2: ", msg2)
            # end if/else
          # end if True
          await ctx.send(msg2, ephemeral=True)
        # end if/elif username option used

      elif sub_command in ["verify"]:
        try:
          tweet_url = url.lower()
          if type(username) == type(str):
            print("username: ", username)
          # end if
          tweet_url = tweet_url.replace(",", "").replace(" ", "")
          if "?" in tweet_url:
            tweet_url = tweet_url.split("?")[0]
          # end if
        except:
          msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
          msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
          await ctx.send(msg2, ephemeral=True)
          return
        # end try/except
        if "https://twitter.com/" not in tweet_url:
          msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
          msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
          await ctx.send(msg2, ephemeral=True)
          return
        else:
          await ctx.send(">>> okay! will verify if we processed that tweet for that user yet or not", ephemeral=True)
          print("tweet_url: ", tweet_url)
          if username == None:
            discord_id = str(ctx.author.id)
            try:
              username = self.user_dict["discordId_to_username"][discord_id]
            except:
              msg2 = "```>>> Danggg. Looks like I don't know your twitter username. Unpack this rage against the machine by slapping a seal ;)```"
              await ctx.send(msg2, ephemeral=True)
              return
            # end try/except
          else:
            try:
              username = username.lower()
              useranme = username.replace(" ", "").replace(",","")
            except:
              msg2  = ">>> sorry, I couldn't parse that username. I'm loooking for something like\n"
              msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
              await ctx.send(msg2, ephemeral=True)
              return
            # end try/except
          # end if/else
          try:
            print("tweet_url: ", tweet_url)
            print("username: ", username)
            msg2,status = self.verify_processed_tweet(tweet_url, username)
            await ctx.send(msg2, ephemeral=True)
            return
          except Exception as err:
            print(err)
            msg2 = ">>> an error occurred."
            await ctx.send(msg2, ephemeral=True)
            status = False
            return
          # end try/except

      elif sub_command in ["leaderboard", "lb"]:
        if True:
          if method == None:
            method = "Points"
          # end if
          method = method.lower()
          method = method.replace(" ","")
          #method = "Points"
          if "like" in method:
            method = "Likes"
          elif "rt" in method[3:] or "retweet" in method:
            method = "Retweets"
          elif "repl" in method:
            method = "Replies"
          #elif "qt" in method[3:] or "quotetweet" in method or "quote tweet" in method:
          #  method = "QuoteTweets"
          else:
            method = "Points"
          # end if/elifs

          start_time = "2020-05-04T23:59:59.000Z"
          end_time   = "4022-05-04T23:59:59.000Z"
          tnow = datetime.datetime.now()
          tstr = "%Y-%m-%dT%H:%M:%S.000Z"
          time_str = "all"
          msg = timerange
          if msg == None:
            msg = ""
          # end if
          msg = msg.lower()
          print("msg: ", msg)
          print("start: in msg: ", "start:" in msg)
          print(",end: in msg: ", ",end:" in msg)
          print("msg: ", msg)
          if "start:" in msg and "end:" in msg:
            print("custom time range!")
            time_str = "user defined"
            try:
              start_time = msg.split("start:")[1].split(", end:")[0]
              end_time = msg.split("end:")[1]

              print("start_time: ", start_time)
              status,start_time = self.convert_time(start_time)
              if status == False:
                await ctx.send(start_time, ephemeral=True)
                return
              # end if

              print("end_time: ", end_time)
              status,end_time   = self.convert_time(end_time)
              if status == False:
                await ctx.send(end_time, ephemeral=True)
                return
              # end if

            except Exception as err:
              print(err)
              msg2 = ">>> sorry we couldn't parse that. Try ***__rtthelplb__** for an example of the syntax we're looking for."
              await ctx.send(msg2, ephemeral=True)
              return
            # end try/except

          elif "today" in msg or "24h" in msg:
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
          elif "last year" in msg or "2021" in msg or "lastyear" in msg:
            print("last year or 2021 in msg")
            start_time = "2021-01-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "2021"
          elif "year" in msg or "2022" in msg:
            print("year or 2022 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
          elif "last month" in msg or "may" in msg:
            print("last month or april in msg")
            start_time = "2022-05-01T00:00:00.000Z"
            end_time   = "2022-06-01T00:00:00.000Z"
            time_str = "May 2022"
          elif "april" in msg:
            print("last month or april in msg")
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-05-01T00:00:00.000Z"
            time_str = "April 2022"
          elif "month" in msg or "june" in msg:
            print("month or may in msg")
            start_time = "2022-06-01T00:00:00.000Z"
            end_time   = "2022-07-01T00:00:00.000Z"
            time_str = "June 2022"
          elif "dec" in msg:
            print("dec in msg")
            start_time = "2021-12-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "Dec 2021"
          elif "nov" in msg:
            print("nov in msg")
            start_time = "2021-11-01T00:00:00.000Z"
            end_time   = "2021-12-01T00:00:00.000Z"
            time_str = "Nov 2021"
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
          # end if/elifs

          fname = self.data_dir + "/leaderboard_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
          if "rtt lbAll".lower() in msg:
            fname = fname.replace("/leaderboard_", "/leaderboardSharded_")
          # end if

          if os.path.exists(fname) and os.stat(fname).st_size != 0:
            msg2  = ">>> Okay, grabbing the updated " + method + " leaderboard for "
            msg2 += time_str + " data range."
            await ctx.send(msg2, ephemeral=True)

          else:
            msg2  = ">>> Okay, grabbing the " + method + " leaderboard for "
            msg2 += time_str + " data range."
            await ctx.send(msg2, ephemeral=True)
          # end if/else

          print("msg: ", msg)
          if "rtt lbAll".lower() in msg or "rttlbAll".lower() in msg or "ALLDATA".lower() in msg:
            print("in lbAll")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time,
                   end_time=end_time, method=method, sharded=False, time_str=time_str)
          else:
            print("in reg lb")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time, 
                   end_time=end_time, method=method, sharded=True, time_str=time_str)
          # end if/elf
          print("discord bot hi here's the " + method + " leaderboard")
          print(msg2)
          timerange = ""
          #await ctx.send(embeds=self.lbEmbedInt, ephemeral=True)

          beginning_button = interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label="⏮ ",
            custom_id="beginning",
          )
          backwards_button = interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label="◀",
            custom_id="backwards",
          )
          forwards_button = interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label="▶",
            custom_id="forwards",
          )
          ending_button = interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label="⏭ ",
            custom_id="ending",
          )
          self.buttons_row = interactions.ActionRow(
            components=[
              beginning_button,
              backwards_button,
              forwards_button,
              ending_button,
            ]
          )
          self.lbPageNum = 0
          ijk = self.lbPageNum
          self.lbEmbedMsg = await ctx.send(embeds=self.lbEmbedInts[ijk], 
              components=[self.buttons_row], ephemeral=True)

          #await ctx.send(msg2, ephemeral=True)
          return
        # end if True (legacy indentation)

      elif sub_command in ["rank"]:
        if username == None:
          discord_id = str(ctx.author.id)
          try:
            username = self.user_dict["discordId_to_username"][discord_id]
          except:
            msg2 = "```>>> Danggg. Looks like I don't know your twitter username. Unpack this rage against the machine by slapping a seal ;)```"
            await ctx.send(msg2, ephemeral=True)
            return
          # end try/except
        # end if

        if True:
          if method == None:
            method = "Points"
          # end if
          method = method.lower()
          method = method.replace(" ","")
          #method = "Points"
          if "like" in method:
            method = "Likes"
          elif "rt" in method[3:] or "retweet" in method:
            method = "Retweets"
          elif "repl" in method:
            method = "Replies"
          #elif "qt" in method[3:] or "quotetweet" in method or "quote tweet" in method:
          #  method = "QuoteTweets"
          else:
            method = "Points"
          # end if/elifs

          start_time = "2020-05-04T23:59:59.000Z"
          end_time   = "4022-05-04T23:59:59.000Z"
          tnow = datetime.datetime.now()
          tstr = "%Y-%m-%dT%H:%M:%S.000Z"
          time_str = "all"
          msg = timerange
          if msg == None:
            msg = ""
          # end if
          msg = msg.lower()
          print("msg: ", msg)
          print("start: in msg: ", "start:" in msg)
          print(",end: in msg: ", ",end:" in msg)
          print("msg: ", msg)
          if "start:" in msg and "end:" in msg:
            print("custom time range!")
            time_str = "user defined"
            try:
              start_time = msg.split("start:")[1].split(", end:")[0]
              end_time = msg.split("end:")[1]

              print("start_time: ", start_time)
              status,start_time = self.convert_time(start_time)
              if status == False:
                await ctx.send(start_time, ephemeral=True)
                return
              # end if

              print("end_time: ", end_time)
              status,end_time   = self.convert_time(end_time)
              if status == False:
                await ctx.send(end_time, ephemeral=True)
                return
              # end if

            except Exception as err:
              print(err)
              msg2 = ">>> sorry we couldn't parse that user defined time range. Try ***__rtthelplb__** for an example of the syntax we're looking for."
              await ctx.send(msg2, ephemeral=True)
              return
            # end try/except

          elif "today" in msg or "24h" in msg:
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
          elif "last year" in msg or "2021" in msg or "lastyear" in msg:
            print("last year or 2021 in msg")
            start_time = "2021-01-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "2021"
          elif "year" in msg or "2022" in msg:
            print("year or 2022 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
          elif "last month" in msg or "may" in msg:
            print("last month or april in msg")
            start_time = "2022-05-01T00:00:00.000Z"
            end_time   = "2022-06-01T00:00:00.000Z"
            time_str = "May 2022"
          elif "april" in msg:
            print("last month or april in msg")
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-05-01T00:00:00.000Z"
            time_str = "April 2022"
          elif "month" in msg or "june" in msg:
            print("month or may in msg")
            start_time = "2022-06-01T00:00:00.000Z"
            end_time   = "2022-07-01T00:00:00.000Z"
            time_str = "June 2022"
          elif "dec" in msg:
            print("dec in msg")
            start_time = "2021-12-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "Dec 2021"
          elif "nov" in msg:
            print("nov in msg")
            start_time = "2021-11-01T00:00:00.000Z"
            end_time   = "2021-12-01T00:00:00.000Z"
            time_str = "Nov 2021"
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
          # end if/elifs

          fname = self.data_dir + "/leaderboard_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
          if "rtt lbAll".lower() in msg:
            fname = fname.replace("/leaderboard_", "/leaderboardSharded_")
          # end if

          if os.path.exists(fname) and os.stat(fname).st_size != 0:
            msg2  = ">>> Okay, grabbing the updated " + method + " rank for "
            msg2 += time_str + " data range."
            await ctx.send(msg2, ephemeral=True)

          else:
            msg2  = ">>> Okay, grabbing the " + method + " rank for "
            msg2 += time_str + " data range."
            await ctx.send(msg2, ephemeral=True)
          # end if/else

          print("msg: ", msg)
          if "rtt lbAll".lower() in msg or "rttlbAll".lower() in msg or "ALLDATA".lower() in msg:
            print("in lbAll")
            print("slash rank all un: ", username)
            msg2 = await self.fetch_rank(username, start_time=start_time,
                   end_time=end_time, method=method, sharded=False, time_str=time_str)
          else:
            print("in reg lb")
            print("slash rank reg un: ", username)
            msg2 = await self.fetch_rank(username, start_time=start_time, 
                   end_time=end_time, method=method, sharded=True, time_str=time_str)
          # end if/elf
          print("discord bot hi here's the " + method + " rank")
          print(msg2)
          timerange = ""
          await ctx.send(embeds=self.rankEmbedInt, ephemeral=True)
          return
        # end if True (legacy indentation)
      # end if/elifs
    # end def cmd

    @intBot.component("beginning")
    async def done_component(ctx: interactions.ComponentContext):
      self.lbPageNum = 0
      ijk = self.lbPageNum
      await ctx.send(embeds=self.lbEmbedInts[ijk], components=[self.buttons_row], ephemeral=True)
    # end def

    @intBot.component("backwards")
    async def done_component(ctx: interactions.ComponentContext):
      self.lbPageNum -= 1
      self.lbPageNum = max(self.lbPageNum,0)
      ijk = self.lbPageNum
      await ctx.send(embeds=self.lbEmbedInts[ijk], components=[self.buttons_row], ephemeral=True)
    # end def

    @intBot.component("forwards")
    async def done_component(ctx: interactions.ComponentContext):
      self.lbPageNum += 1
      self.lbPageNum = min(self.lbPageNum,len(self.lbEmbedInts)-1)
      ijk = self.lbPageNum
      await ctx.send(embeds=self.lbEmbedInts[ijk], components=[self.buttons_row], ephemeral=True)
    # end def

    @intBot.component("ending")
    async def done_component(ctx: interactions.ComponentContext):
      self.lbPageNum = len(self.lbEmbedInts)-1
      ijk = self.lbPageNum
      await ctx.send(embeds=self.lbEmbedInts[ijk], components=[self.buttons_row], ephemeral=True)
    # end def

    @client.event
    async def on_ready():
      print("We have logged in as {0.user}".format(client))

      print("0xraspberry in self.linked_usernames: ", "0xraspberry" in self.linked_usernames)

      channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
      await channel.send("I AM ALIVE! MWAHAHAHA")

      channel = client.get_channel(982340728980140122)
      messages = await channel.history(limit=100).flatten()
      for message in messages:
        print("message: ", message)
        print("message.content: ", message.content)
        twid = message.content.split("Twitter ID: ")[1].split("\n")[0]
        twid = twid.replace(" ","").replace("\n","")
        print("twid: ", twid)
        did = message.content.split("Discord ID: ")[1].split("\n")[0]
        did = did.replace(" ","").replace("\n","")
        print("did: ", did)
        tun = message.content.split("Twitter Handle: ")[1].split("\n")[0]
        tun = tun.replace(" ","").replace("\n","")
        print("tun: ", tun)

        if str(tun) not in self.linked_usernames:
          print("hi")
          self.linked_usernames.append(str(tun))
          self.linked_userIds.append(str(twid))
          self.linked_discordIds.append(str(did))

          self.user_dict["userId_to_username"][str(twid)] = str(tun)
          print("tun: ", str(tun))
          self.user_dict["username_to_userId"][str(tun)] = str(twid)
          self.user_dict["discordId_to_username"][str(did)] = str(tun)
          self.safe_save(self.fname_user_info, self.user_dict)
          print("hi2")
        # end if
      # end if
      await self.continuously_scrape()
    # end on_ready

    @client.event
    async def on_raw_reaction_add(payload):
      xemoji = "🇽"
      if payload.channel_id in self.BOT_COMMANDS_CIDS:
        if   payload.emoji.name == "🇽":
          channel = client.get_channel(payload.channel_id)
          message = await channel.fetch_message(payload.message_id)
          reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
          if reaction and reaction.count > 1:
            await message.delete()
        elif payload.emoji.name == '⏮':
          channel = client.get_channel(payload.channel_id)
          message = await channel.fetch_message(payload.message_id)
          reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
          if reaction and reaction.count > 1:
            self.pages[str(message.id)]["pnum"] = 0
            await message.edit(embed=self.pages[str(message.id)]["pages"][0])
            await message.clear_reactions()
            await message.add_reaction('⏮')
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            await message.add_reaction('⏭')
            await message.add_reaction(xemoji)
        elif payload.emoji.name == '◀':
          channel = client.get_channel(payload.channel_id)
          message = await channel.fetch_message(payload.message_id)
          reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
          if reaction and reaction.count > 1:
            self.pages[str(message.id)]["pnum"] = self.pages[str(message.id)]["pnum"]-1
            pnum = self.pages[str(message.id)]["pnum"]
            await message.edit(embed=self.pages[str(message.id)]["pages"][pnum])
            await message.clear_reactions()
            await message.add_reaction('⏮')
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            await message.add_reaction('⏭')
            await message.add_reaction(xemoji)
        elif payload.emoji.name == '▶':
          channel = client.get_channel(payload.channel_id)
          message = await channel.fetch_message(payload.message_id)
          reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
          if reaction and reaction.count > 1:
            self.pages[str(message.id)]["pnum"] = self.pages[str(message.id)]["pnum"]+1
            pnum = self.pages[str(message.id)]["pnum"]
            await message.edit(embed=self.pages[str(message.id)]["pages"][pnum])
            await message.clear_reactions()
            await message.add_reaction('⏮')
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            await message.add_reaction('⏭')
            await message.add_reaction(xemoji)
        elif payload.emoji.name == '⏭':
          channel = client.get_channel(payload.channel_id)
          message = await channel.fetch_message(payload.message_id)
          reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
          if reaction and reaction.count > 1:
            self.pages[str(message.id)]["pnum"] = len(self.pages[str(message.id)]["pages"])-1
            await message.edit(embed=self.pages[str(message.id)]["pages"][-1])
            await message.clear_reactions()
            await message.add_reaction('⏮')
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            await message.add_reaction('⏭')
            await message.add_reaction(xemoji)

    @client.event
    async def on_message(message):
      if message.author == client.user:
        return
      # end if

      channel = client.get_channel(message.channel.id)
      if message.channel.id == 982340728980140122:
        print("message: ", message)
        print("message.content: ", message.content)
        twid = message.content.split("Twitter ID:")[1]
        twid = twid.replace(" ","").replace("\n","")
        print("twid: ", twid)
        did = message.content.split("Discord ID:")[1]
        did = twid.replace(" ","").replace("\n","")
        print("did: ", did)
        tun = message.content.split("Twitter Handle:")[1]
        tun = twid.replace(" ","").replace("\n","")
        print("tun: ", tun)

        self.linked_usernames.append(str(tun))
        self.linked_userIds.append(str(twid))
        self.linked_discordIds.append(str(did))
      
        self.user_dict["userId_to_username"][str(twid)] = str(tun)
        self.user_dict["username_to_userId"][str(tun)] = str(twid)
        self.user_dict["discordId_to_username"][str(did)] = str(tun)
        self.safe_save(self.fname_user_info, self.user_dict)
        return

      elif message.channel.id not in self.BOT_COMMANDS_CIDS:
        return
      # end if

      msg = message.content.lower()
      message.content = message.content.lower().replace(" ","")

      tab = self.tab
      temp_msg = msg.replace("start","")
      if msg.startswith("rtt") or msg.startswith("!rtt") or \
         msg.startswith("/rtt"):
        msg = msg.replace("@","")

        max_len = len("!rtt help lb")
        if "lb" in msg[:max_len] and "help" in msg[:max_len]:
          #msg2 = self.help_lb
          #await channel.send(msg2)
          await self.embed_helper([self.lbHelpEmbedDpy], client, channel)
          #await channel.send(embed=self.lbHelpEmbedDpy)
          return
        # end if

        max_len = len("!rtt help")
        if "help" in msg[:max_len]:
          await self.embed_helper([self.helpEmbedDpy], client, channel)
          #await channel.send(embed=self.helpEmbedDpy)
          #await client.say( embed=self.helpEmbedDpy)
          return

        elif msg.startswith("!rttstats") or msg.startswith("!rtt stats") or \
           msg.startswith( "rttstats") or msg.startswith( "rtt stats") or \
           msg.startswith("/!rttstats") or msg.startswith("/!rtt stats") or \
           msg.startswith( "/rttstats") or msg.startswith( "/rtt stats"):
          if "username" in msg:
            username = ""
            try:
              username  = msg.split("username:")[1].replace(" ","")
            except:
              try:
                username  = msg.split("username=")[1].replace(" ","")
              except:
                msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
                msg2 += 2*tab + "*!rtt stats username:TheLunaLabs*"
                await channel.send(msg2)
                return
              # end try/except
            # end try/except
            if username == "":
              msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
              msg2 += 2*tab + "*!rtt stats username:TheLunaLabs*"
              await channel.send(msg2)
              return
          else:
            discord_id = str(message.author.id)
            try:
              username = self.user_dict["discordId_to_username"][discord_id]
            except:
              msg2 = ">>> Danggg. Looks like I don't know your twitter username. Slap a seal/Rubiks for me"
              ## check if they have it linked, if so, slap a seal, say sorry
              ## and ask for them to enter it again
              ## if they haven't linked it, then just ask them for it
              await channel.send(msg2)
              return
            # end try/except
          # end if/else
          print("username: ", username)
          print("len username: ", len(username))
          print("u != '': ", username != "")
          msg2 = ">>> ```Username: " + username + "\n"
          msg2 += "--\n"
          if True:
            print(">>> fetching user data")
            status, user_data = self.fetch_user_data(username)
            if status == False:
              print("user_data: ", user_data)
              msg2 += user_data
              print("msg2: ", msg2)
            else:
              #print(user_data)
              print(">>> and now I'm computing user points")
              msg2 += self.fetch_user_points(user_data)
              #self.statEmbedDpy.set_author(name=message.author, icon_url=message.author.avatar_url)
              await self.embed_helper([self.statEmbedDpy], client,channel)
              #await channel.send(embed=self.statEmbedDpy)
              return
              print("msg2: ", msg2)
            # end if/else
          # end if

        elif "verify" in msg:
          if "username" in msg:
            username = ""
            try:
              username  = msg.split("username:")[1].replace(" ","")
            except:
              try:
                username  = msg.split("username=")[1].replace(" ","")
              except:
                msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
                msg2 += 2*tab + "*!rtt stats username:TheLunaLabs*"
                await channel.send(msg2)
                return
              # end try/except
            # end try/except
            if username == "":
              msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
              msg2 += 2*tab + "*!rtt stats username:TheLunaLabs*"
              await channel.send(msg2)
              return
          else:
            discord_id = str(message.author.id)
            try:
              username = self.user_dict["discordId_to_username"][discord_id]
            except:
              msg2 = ">>> Danggg. Looks like I don't know your twitter username. Slap a seal/Rubiks for me"
              ## check if they have it linked, if so, slap a seal, say sorry
              ## and ask for them to enter it again
              ## if they haven't linked it, then just ask them for it
              await channel.send(msg2)
              return
            # end try/except
          # end if/else

          try:
            tweet_url = msg.split("url:")[1]
            print("username: ", username)
            tweet_url = tweet_url.replace(",", "").replace(" ", "")
            if "?" in tweet_url:
              tweet_url = tweet_url.split("?")[0]
            # end if
          except:
            msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
            msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
            await channel.send(msg2)
            return
          # end try/except
          if "https://twitter.com/" not in tweet_url:
            msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
            msg2 += tab + "*rtt verify url: https://twitter.com/RooTroopNFT/status/1499858580568109058, \nusername:TheLunaLabs*"
          else:
            await channel.send(">>> okay! will verify if we processed that tweet for that user yet or not")
            print("tweet_url: ", tweet_url)
            try:
              print("tweet_url: ", tweet_url)
              print("username: ", username)
              msg2,status = self.verify_processed_tweet(tweet_url, username)
            except Exception as err:
              print(err)
              msg2 = ">>> an error occurred."
              status = False
            # end try/except
          # end if/else

        elif "lb" in msg or "leaderboard" in msg:
          method = "Points"
          if "like" in msg:
            method = "Likes"
          elif "rt" in temp_msg[3:] or "retweet" in msg:
            method = "Retweets"
          elif "repl" in msg:
            method = "Replies"
          #elif "qt" in temp_msg[3:] or "quotetweet" in msg or "quote tweet" in msg:
          #  method = "QuoteTweets"
          # end if/elifs

          start_time = "2020-05-04T23:59:59.000Z"
          end_time   = "4022-05-04T23:59:59.000Z"
          tnow = datetime.datetime.now()
          tstr = "%Y-%m-%dT%H:%M:%S.000Z"
          time_str = "all"
          print("msg: ", msg)
          print("start: in msg: ", "start:" in msg)
          print(",end: in msg: ", ",end:" in msg)
          if "start:" in msg and "end:" in msg:
            print("custom time range!")
            time_str = "user defined"
            try:
              start_time = msg.split("start:")[1].split(", end:")[0]
              end_time = msg.split("end:")[1]

              print("start_time: ", start_time)
              status,start_time = self.convert_time(start_time)
              if status == False:
                await channel.send(start_time)
                return
              # end if

              print("end_time: ", end_time)
              status,end_time   = self.convert_time(end_time)
              if status == False:
                await channel.send(end_time)
                return
              # end if

            except Exception as err:
              print(err)
              msg2 = ">>> sorry we couldn't parse that. Try ***__rtthelplb__** for an example of the syntax we're looking for."
              await channel.send(msg2)
              return
            # end try/except

          elif "today" in msg or "24h" in msg:
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
          elif "last year" in msg or "2021" in msg or "lastyear" in msg:
            print("last year or 2021 in msg")
            start_time = "2021-01-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "2021"
          elif "year" in msg or "2022" in msg:
            print("year or 2022 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
          elif "last month" in msg or "may" in msg:
            print("last month or april in msg")
            start_time = "2022-05-01T00:00:00.000Z"
            end_time   = "2022-06-01T00:00:00.000Z"
            time_str = "May 2022"
          elif "month" in msg or "june" in msg:
            print("month or may in msg")
            start_time = "2022-06-01T00:00:00.000Z"
            end_time   = "2022-07-01T00:00:00.000Z"
            time_str = "June 2022"
          elif "dec" in msg:
            print("dec in msg")
            start_time = "2021-12-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "Dec 2021"
          elif "nov" in msg:
            print("nov in msg")
            start_time = "2021-11-01T00:00:00.000Z"
            end_time   = "2021-12-01T00:00:00.000Z"
            time_str = "Nov 2021"
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
          elif "april" in msg:
            print("last month or april in msg")
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-05-01T00:00:00.000Z"
            time_str = "April 2022"
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

          else:
            msg2  = ">>> Okay, grabbing the " + method + " leaderboard for "
            msg2 += time_str + " data range."
            await channel.send(msg2)
          # end if/else

          print("msg: ", msg)
          if "rtt lbAll".lower() in msg or "rttlbAll".lower() in msg or "ALLDATA".lower() in msg:
            print("in lbAll")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time,
                   end_time=end_time, method=method, sharded=False, time_str=time_str)
            await self.embed_helper(self.lbEmbedDpys, client,channel)
            #await channel.send(embed=self.lbEmbedDpy)
            return
          else:
            print("in reg lb")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time, 
                   end_time=end_time, method=method, sharded=True, time_str=time_str)
            await self.embed_helper(self.lbEmbedDpys, client,channel)
            #await channel.send(embed=self.lbEmbedDpy)
            return
          print("discord bot hi here's the " + method + " leaderboard")
          print(msg2)

        elif "rank" in msg:
          if "username" in msg:
            username = msg.split("username")[1][1:].replace(" ","")
          else:
            print("no un in msg")
            discord_id = str(message.author.id)
            print("did")
            try:
              username = self.user_dict["discordId_to_username"][discord_id]
              print("un from did: ", username)
            except:
              msg2 = ">>> Danggg. Looks like I don't know your twitter username. Slap a seal/Rubiks for me"
              await channel.send(msg2)
              return
            # end try/except
          # end if/else
          method = "Points"
          if "like" in msg:
            method = "Likes"
          elif "rt" in temp_msg[3:] or "retweet" in msg:
            method = "Retweets"
          elif "repl" in msg:
            method = "Replies"
          #elif "qt" in temp_msg[3:] or "quotetweet" in msg or "quote tweet" in msg:
          #  method = "QuoteTweets"
          # end if/elifs
          print("method rank: ", method)

          start_time = "2020-05-04T23:59:59.000Z"
          end_time   = "4022-05-04T23:59:59.000Z"
          tnow = datetime.datetime.now()
          tstr = "%Y-%m-%dT%H:%M:%S.000Z"
          time_str = "all"
          print("msg: ", msg)
          print("start: in msg: ", "start:" in msg)
          print(",end: in msg: ", ",end:" in msg)
          if "start:" in msg and "end:" in msg:
            print("custom time range!")
            time_str = "user defined"
            try:
              start_time = msg.split("start:")[1].split(", end:")[0]
              end_time = msg.split("end:")[1]

              print("start_time: ", start_time)
              status,start_time = self.convert_time(start_time)
              if status == False:
                await channel.send(start_time)
                return
              # end if

              print("end_time: ", end_time)
              status,end_time   = self.convert_time(end_time)
              if status == False:
                await channel.send(end_time)
                return
              # end if

            except Exception as err:
              print(err)
              msg2 = ">>> sorry we couldn't parse that. Try ***__rtthelplb__** for an example of the syntax we're looking for."
              await channel.send(msg2)
              return
            # end try/except

          elif "today" in msg or "24h" in msg:
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
          elif "last year" in msg or "2021" in msg or "lastyear" in msg:
            print("last year or 2021 in msg")
            start_time = "2021-01-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "2021"
          elif "year" in msg or "2022" in msg:
            print("year or 2022 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
          elif "last month" in msg or "may" in msg:
            print("last month or april in msg")
            start_time = "2022-05-01T00:00:00.000Z"
            end_time   = "2022-06-01T00:00:00.000Z"
            time_str = "May 2022"
          elif "month" in msg or "june" in msg:
            print("month or may in msg")
            start_time = "2022-06-01T00:00:00.000Z"
            end_time   = "2022-07-01T00:00:00.000Z"
            time_str = "June 2022"
          elif "dec" in msg:
            print("dec in msg")
            start_time = "2021-12-01T00:00:00.000Z"
            end_time   = "2022-01-01T00:00:00.000Z"
            time_str = "Dec 2021"
          elif "nov" in msg:
            print("nov in msg")
            start_time = "2021-11-01T00:00:00.000Z"
            end_time   = "2021-12-01T00:00:00.000Z"
            time_str = "Nov 2021"
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
          elif "april" in msg:
            print("last month or april in msg")
            start_time = "2022-04-01T00:00:00.000Z"
            end_time   = "2022-05-01T00:00:00.000Z"
            time_str = "April 2022"
          # end if/elifs
          print("st, et, ts: ", start_time, end_time, time_str)

          fname = self.data_dir + "/leaderboard_" + method + "_start" + \
            start_time + "_" + end_time + ".txt"
          if "rtt lbAll".lower() in msg:
            fname = fname.replace("/leaderboard_", "/leaderboardSharded_")
          # end if
          print("fname: ", fname)

          if os.path.exists(fname) and os.stat(fname).st_size != 0:
            msg2  = ">>> Okay, grabbing the updated " + method + " rank for "
            msg2 += time_str + " data range."
            await channel.send(msg2)
          else:
            msg2  = ">>> Okay, grabbing the " + method + " rank for "
            msg2 += time_str + " data range."
            await channel.send(msg2)
          # end if/else

          print("msg b4 rtlbALL check: ", msg)
          if "rtt lbAll".lower() in msg or "rttlbAll".lower() in msg or "ALLDATA".lower() in msg:
            print("in lbAll")
            msg2 = await self.fetch_rank(username, start_time=start_time,
                   end_time=end_time, method=method, sharded=False, time_str=time_str)
            await self.embed_helper([self.rankEmbedDpy], client,channel)
            return
          else:
            #await channel.send(embed=self.lbEmbedDpy)
            print("in reg lb")
            msg2 = await self.fetch_rank(username, start_time=start_time, 
                   end_time=end_time, method=method, sharded=True, time_str=time_str)
            await self.embed_helper([self.rankEmbedDpy], client,channel)
            #await channel.send(embed=self.lbEmbedDpy)
            return
          print("discord bot hi here's the " + method + " rank")
          print(msg2)

        elif "key" in msg:
          await self.embed_helper([self.keyEmbedDpy], client,channel)
          #await channel.send(embed=self.keyEmbedDpy)
          return

        else:
          msg2  = "sorry! I didn't understand that command. Try 'rtt help(?)'\n"
          msg2 += "without the quotes..."
        # end if/elif/else
        await channel.send(msg2)
      # end if rtt
    # end async

    loop = asyncio.get_event_loop()

    task2 = loop.create_task(client.start(secret))
    task1 = loop.create_task(intBot._ready())

    gathered = asyncio.gather(task1, task2, loop=loop)
    loop.run_until_complete(gathered)
    #client.start()
  # end discord_bot
# end class ScrapeTweets

if __name__ == "__main__":
  tweet_scrape_instance = ScrapeTweets()
  tweet_scrape_instance.discord_bot()

print("execution rate: ", time.time() - start)
print("SUCCESS ScrapeTweets")
## end ScrapeTweets.py
