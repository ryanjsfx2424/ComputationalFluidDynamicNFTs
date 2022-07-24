import os
import re
import sys
import time
import glob
import copy
import asyncio
import datetime
import numpy as np
import discord
np.set_printoptions(threshold = sys.maxsize)

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions import Button, ButtonStyle, ActionRow
from interactions.client import get

from init_fetch_likes_ezu_tweet_activity import *
from init_fetch_retweets_ezu_tweet_activity import *
from init_fetch_quotes_ezu_tweet_activity import *
from update_fetch_likes_ezu_tweet_activity import *
from update_fetch_retweets_ezu_tweet_activity import *
from update_fetch_quotes_ezu_tweet_activity import *

DEFAULT_METHOD = "Points"
DEFAULT_STARTT = "2020-05-04T23:59:59.000Z"
DEFAULT_ENDT   = "4022-05-04T23:59:59.000Z"
DEFAULT_TIMEST = "all"

class EzuTweeteroo(object):
    def __init__(self):
        self.CID_LOG = 999617660155334766 # test server, secret channel
        self.CID_MSG = 999617660155334766
        self.BOT_COMMANDS_CIDS = [self.CID_MSG,self.CID_LOG]
        self.GUILDS = [999414546496229498] # 'test' guild id

        self.CMD_PREFIX = "ezu"
        self.BOT_NAME   = "tweetlist by ezu"
        self.FOOTER = "-- built for ezu, powered by [redacted] --"

        self.init_keywords() # prob edit these!

        self.VERIFY1 = "https://twitter.com/BAYC2745/status/1546309756255862784"
        self.VERIFY2 = "!ezuverify https://twitter.com/ezu_xyz/status/1544884799676231680, @pa4677"

        self.LB_VPP = 20 # values per page

        self.UNKNOWN_USERNAME = "```>>> Looks like that twitter username isn't linked in my database. Please use the 'linktwitter' command.```"
        self.TAB = 4*" "
        self.VERIFY_ERROR = "```>>> sorry, I couldn't parse that. I'm looking for something like\n" \
                            + 2*self.TAB + "!" + self.CMD_PREFIX + "verify " + self.VERIFY1 + " \nOR\n" \
                            + 2*self.TAB + "!" + self.CMD_PREFIX + "verify " + self.VERIFY2 + "```"
        self.VERIFY_SUCCESS = "```>>> SUCCESS! Your tweet was already processed :)```"
        self.STATS_ERROR = "```>>> error fetching user's stats```"
        self.RANK_ERROR = "```>>> error fetching user's rank```"
        self.LB_ERROR = "```>>> error fetching the leaderboard```"

        self.twitter_api_base = "https://api.twitter.com/2/tweets/"
        self.curl_base = "curl --request GET --url '"
        self.curl_header = "' --header 'Authorization: Bearer "

        self.QS = 1e-6
        self.SS = 0.02
        self.MS = 0.2

        self.FLAG_KEY = "keywords"
        self.FLAG_RTS = "retweets"
        self.FLAG_QTS = "quotes"

        self.fname_stream = "data_big/stream_data.txt"
        self.pages = {}; self.points_usernames = []
        self.init_times()
        self.init_auth()
        self.init_embeds()
        self.load_data()
        self.user_dict = {"discordId_to_username":[]}
    # end __init__

    def init_keywords(self):
        self.PROJECT_TWITTER = "ezu_xyz"
        query = "@" + self.PROJECT_TWITTER
        self.keywords_help = query + ""
        self.keywords_query = query.replace(" ", "%20")
    # end init_keywords

    def init_times(self):
        self.S_PER_MINUTE = 60
        self.S_PER_HOUR   = self.S_PER_MINUTE * 60
        self.S_PER_DAY    = self.S_PER_HOUR   * 24
        self.S_PER_MONTH  = self.S_PER_DAY    * 31
        self.S_PER_YEAR   = self.S_PER_MONTH  * 12
    # end define_times

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

    def init_embeds(self):
        self.URL = "https://cdn.discordapp.com/attachments/999617660155334766/999620697951326269/tPWW2u9T_400x400.jpeg"

        TITLE = "__Help Menu__"
        DESCRIPTION = "greetings i am -- " + self.BOT_NAME + " -- developed by [redacted] © 2022"
        DESCRIPTION += "\n-- below are my commands which are case insensitive --"

        embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION)
        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedDpy.set_footer(text = self.FOOTER,
                            icon_url=self.URL)
        embedInt.set_footer(text = self.FOOTER,
                            icon_url=self.URL)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "help__**", value="Display this help menu", inline=True)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "help__**", value="Display this help menu", inline=True)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lb__**", value="Display leaderboard (all data)\nTo see options for granular leaderboards, run command: **__!" + self.CMD_PREFIX + "helplb__**", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lb__**", value="Display leaderboard (all data)\nTo see options for granular leaderboards, run command: **__!" + self.CMD_PREFIX + "helplb__**", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "keywords__**", value="Display keywords we use to find Tweets that count towards your rank", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "keywords__**", value="Display keywords we use to find Tweets that count towards your rank", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "verify <url>,<twitter username>__**", value="Verify if we've processed your interaction", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "verify <url>,<twitter username>__**", value="Verify if we've processed your interaction", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "stats <twitter username>__**", value="Display user's points, likes, etc.", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "stats <twitter username>__**", value="Display user's points, likes, etc.", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "rank <twitter username>__**",  value="Display user's rank (all data). To see options for granular ranks, run command: **__!" + self.CMD_PREFIX + "helplb__**", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "rank <twitter username>__**",  value="Display user's rank (all data). To see options for granular ranks, run command: **__!" + self.CMD_PREFIX + "helplb__**", inline=False)
        self.helpEmbedDpy = embedDpy
        self.helpEmbedInt = embedInt

        LB_HELP_TITLE = "__Leaderboard Help Menu__"
        LB_HELP_DESCRIPTION = "greetings i am -- " + self.BOT_NAME + " -- developed by [redacted] © 2022"
        LB_HELP_DESCRIPTION += "\n-- this is the help meun for querying the leaderboard --\n-- the following commands are available --"

        embedDpy = discord.Embed(title=LB_HELP_TITLE, description=LB_HELP_DESCRIPTION)
        embedInt = interactions.Embed(title=LB_HELP_TITLE, description=LB_HELP_DESCRIPTION)
        embedDpy.set_footer(text = self.FOOTER,
                        icon_url=self.URL)
        embedInt.set_footer(text = self.FOOTER,
                        icon_url=self.URL)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lblikes__**", value="Displays the Likes leaderboard.", inline=True)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lblikes__**", value="Displays the Likes leaderboard.", inline=True)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lbretweets__**", value="Displays the Retweets leaderboard.", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lbretweets__**", value="Displays the Retweets leaderboard.", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lbtweets__**", value="Displays the Tweets leaderboard.", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lbtweets__**", value="Displays the Tweets leaderboard.", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lbpoints__**", value="Displays the Points leaderboard.\n\n**__LEADERBOARD BY TIME RANGE__**\n\n\n\n\n", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lbpoints__**", value="Displays the Points leaderboard.\n\n**__LEADERBOARD BY TIME RANGE__**\n\n\n\n\n", inline=False)
        embedInt.add_field(name="\n**__!" + self.CMD_PREFIX + "lbtoday__**", value="Past 24 hours (time-zone agnostic)", inline=False)
        embedDpy.add_field(name="\n**__!" + self.CMD_PREFIX + "lbtoday__**", value="Past 24 hours (time-zone agnostic)", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lbq1__**", value="Data from January 1st, 2022 - April 1st, 2022", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lbq1__**", value="Data from January 1st, 2022 - April 1st, 2022", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lbq2__**", value="Data from April 1st, 2022 - July 1st, 2022", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lbq2__**", value="Data from April 1st, 2022 - July 1st, 2022", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lblastyear__**", value="Data from January 1st, 2021 - January 1st, 2022", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lblastyear__**", value="Data from January 1st, 2021 - January 1st, 2022", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lblastmonth__**", value="Data from the last month.", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lblastmonth__**", value="Data from the last month.", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lb <month>__**", value="Data from the specified month.", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lb <month>__**", value="Data from the specified month.", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lb start: <month day, year, time>, end: <month day, year, time>__**", value="Data from the specified timeframe. **Must fit expected style and spaces matter!**\nExample: !" + self.CMD_PREFIX + "lb start: January 5, 2022, 17:07:39, end: January 6, 2022, 01:00:00\n\n**NOTE:** leaderboard type & time range options can be combined!\nExample:", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lb start: <month day, year, time>, end: <month day, year, time>__**", value="Data from the specified timeframe. **Must fit expected style and spaces matter!**\nExample: !" + self.CMD_PREFIX + "lb start: January 5, 2022, 17:07:39, end: January 6, 2022, 01:00:00\n\n**NOTE:** leaderboard type & time range options can be combined!\nExample:", inline=False)
        embedInt.add_field(name="**__!" + self.CMD_PREFIX + "lblikesfebruary__**", value="Displays the Likes leaderboard for February tweets.", inline=False)
        embedDpy.add_field(name="**__!" + self.CMD_PREFIX + "lblikesfebruary__**", value="Displays the Likes leaderboard for February tweets.", inline=False)
        self.lbHelpEmbedDpy = embedDpy
        self.lbHelpEmbedInt = embedInt

        TITLE = "__Keywords__"
        DESCRIPTION = "-- greetings these are the keywords I use to scrape for tweets --\n\n"
        if "OR" in self.keywords_help:
            keywords = self.keywords_help.split("OR")
        else:
            keywords = [self.keywords_help]
        # end if/else
        for keyword in keywords:
            keyword = keyword.replace(")","")
            keyword = keyword.replace("("," ")
            DESCRIPTION += 2*self.TAB + keyword + "\n"
        # end for

        embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION)
        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedDpy.set_footer(text = self.FOOTER,
                        icon_url=self.URL)
        embedInt.set_footer(text = self.FOOTER,
                        icon_url=self.URL)
        self.keyEmbedDpy = embedDpy
        self.keyEmbedInt = embedInt
    # end init_embeds

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
    # end embed_helper

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
            msg2 = "```>>> sorry we couldn't parse the month.```"
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

    def load_data(self):
        start = time.time()
        self.load_keywords()
        print("loaded keywords in: ", time.time() - start)

        start = time.time()
        self.load_engagement()
        print("loaded engagement in: ", time.time() - start)

        self.load_stream_data()

        self.load_latest_tweet_time_s()
    # end load_data

    def load_keywords(self):
        fname_data = "data_big/at_ezu_xyz"
        with open(fname_data, "r") as fid:
            line = fid.read()
        # end with open
        dates = line.split("date=datetime.datetime(")[1:]
        tweets = line.split("Tweet(")[1:]

        dates = []
        dates_s = []
        tweet_ids = []
        tuids = []
        usernames = []
        contents = []
        for tweet in tweets:
            date = tweet.split("date=datetime.datetime(")[1].split(", tzinfo=")[0]
            if len(date.split(",")) == 6:
                yy,mm,dd,HH,MM,SS = date.split(", ")
            else:
                yy,mm,dd,HH,MM = date.split(", ")
                SS = "00"
            # end if/else
            dates.append(yy + "-" + mm.zfill(2) + "-" + dd.zfill(2) + "T" + HH.zfill(2) + ":" + MM.zfill(2) + ":" + SS.zfill(2) + ".000Z")
            dates_s.append(str(self.get_tweet_time_s(dates[-1])))

            tweet_ids.append(tweet.split("/status/")[1].split("'")[0])

            tuids.append(tweet.split("user=User(")[1].split("id=")[1].split(",")[0])
            usernames.append(tweet.split("user=User(")[1].split("username='")[1].split(",")[0][:-1])
            contents.append(tweet.split("content=")[1][1:].split(",")[0][:-1])
        # end for tweets
        self.keywords_data = {
            "dates": np.array(dates),
            "dates_s": np.array(dates_s),
            "tweet_ids": np.array(tweet_ids),
            "tuids": np.array(tuids),
            "usernames": np.char.lower(np.array(usernames)),
            "contents": np.char.lower(np.array(contents))
        }
    # end load_data

    def load_engagement(self):
        self.engagement = {}
        for etype in ["likes", "retweets", "replies", "quotes"]:
            fnames = np.sort(glob.glob("data_big/" + etype + "/activity_*.txt"))
            tuids = []
            usernames = []
            tweet_ids = []
            
            for fname in fnames:
                usernames_f = []
                print("fname: ", fname)
                with open(fname, "r") as fid:
                    for line in fid:
                        if "next_token: " in line and "None" not in line:
                            next_token = line.split("next_token: ")[1]
                        elif "twitter_ids: " in line and "[]" not in line:
                            tuids_line = line.replace("'", "").replace("[", "").replace("]","").replace("\n","").split("twitter_ids: ")[1]
                            if ", " in tuids_line:
                                tuids += tuids_line.split(", ")
                            else:
                                tuids += [tuids_line]
                            # end if/else
                        elif "twitter_usernames: " in line and "[]" not in line:
                            usernames_line = line.replace("'", "").replace("[", "").replace("]","").replace("\n","").split("twitter_usernames: ")[1]
                            if ", " in usernames_line:
                                usernames += usernames_line.split(", ")
                                usernames_f += usernames_line.split(", ")
                            else:
                                usernames   += [usernames_line]
                                usernames_f += [usernames_line]
                            # end if/else
                        # end if/elifs
                    # end for line in fid
                # end with open
                if len(usernames) != len(tuids):
                    print("usernames != tweet_ids ???")
                    print("len usernames: ", len(usernames))
                    print("len tuids: ", len(tuids))
                    raise
                # end if
                tweet_id = int(fname.split("activity_ezu_xyz_")[1].split(".txt")[0])
                tweet_ids += len(usernames_f)*[tweet_id]

                if len(usernames) != len(tuids):
                    print("usernames != tweet_ids ???")
                    print("len usernames: ", len(usernames))
                    print("len tuids: ", len(tuids))
                    raise
                # end if

            # end for fnames

            usernames = np.array(usernames)
            if len(usernames) != 0:
                usernames = np.char.lower(usernames)

            self.engagement[etype] = {
                "tweet_ids": np.array(tweet_ids),
                "tuids": np.array(tuids),
                "usernames": usernames
            }
        # end for etypes
    # end load_engagement

    def load_stream_data(self):
        self.stream_data = {
            "tweet_ids": np.array([]),
            "tuids": np.array([]),
            "usernames": np.array([]),
            "dates": np.array([]),
            "dates_s": np.array([]),
            "etypes": np.array([]),
            "texts": np.array([])
        }

        result = self.safe_load(self.fname_stream)
        if result != {}:
            self.stream_data = {
                "tweet_ids": np.array(result["tweet_ids"]),
                    "tuids": np.array(result[    "tuids"]),
                "usernames": np.array(result["usernames"]),
                    "dates": np.array(result[    "dates"]),
                  "dates_s": np.array(result[  "dates_s"]),
                   "etypes": np.array(result[   "etypes"]),
                    "texts": np.array(result[    "texts"])
            }
        # end if
    # end load_stream_data

    def load_latest_tweet_time_s(self):
        self.latest_tweet_time_s = 0.0

        if len(self.stream_data["dates_s"]) != 0:
            self.latest_tweet_time_s = np.max(self.stream_data["dates_s"].astype(float))
        # end if
        self.latest_tweet_time_s = max(np.max(self.keywords_data["dates_s"].astype(float)),
                                       self.latest_tweet_time_s)        

        #for etype in ["likes", "retweets", "replies", "quotes"]:
        #    self.latest_tweet_time_s = max(self.latest_tweet_time_s, np.max(self.engagement[etype]["dates_s"]))
        # end for etype
    # end load_latest_tweet_time_s

    def safe_load(self, fname):
        result = {}
        if os.path.exists(fname) and \
            os.stat(fname).st_size != 0:
            try:
                with open(fname, "r") as fid:
                    result = ast.literal_eval(fid.read())
                # end with
            except:
                print("420 exception triggered when trying to load `" + fname + "` in safe load")
                print("421 now we're trying to load the backup.")
                #result = np.loadtxt(fname + "_backup")
                with open(fname + "_backup", "r") as fid:
                    result = ast.literal_eval(fid.read())
                # end with
                print("425 we loaded the backup (sl) so now we'll re-set the file with the backup2")
                os.system("cp " + fname + "_backup " + fname)
            # end try/except
        # end if
        return result
    # end safe_load

    def get_time_str(self, msg):
        start_time = DEFAULT_STARTT
        end_time   = DEFAULT_ENDT
        time_str   = DEFAULT_TIMEST
        
        tnow = datetime.datetime.now()
        tstr = "%Y-%m-%dT%H:%M:%S.000Z"
        yr,mo = tnow.strftime(tstr).split("-")[:2]

        if msg == None:
            return [start_time, end_time, time_str, True, ""]
        # end if

        msg = msg.lower()
        if "start:" in msg and "end:" in msg:
            print("custom time range!")
            time_str = "user defined"

            try:
                start_time = msg.split("start:")[1].split(", end:")[0]
                end_time = msg.split("end:")[1]

                status, start_time = self.convert_time(start_time)
                if status == False:
                    return ["start_foo", "end_foo" "time_foo", False, start_time]
                # end if

                status, end_time   = self.convert_time(end_time)
                if status == False:
                    return ["start_foo", "end_foo" "time_foo", False, end_time]
                # end if

            except Exception as err:
                print("371 get_time_str err: ", err)
                print("372 get_time_str err.args: ", err.args[:])
                err_msg = "```>>> sorry we couldn't parse that. Try ***__" + self.CMD_PREFIX + "helplb__** for an example of the syntax we're looking for.```"
                return ["start_foo", "end_foo" "time_foo", False, err_msg]
            # end try/except

        elif "today" in msg or "24h" in msg:
            print("today or 24H in msg")
            ## to be time-zone agnostic we start 24H ago and end now
            start_time = (tnow - datetime.timedelta(days=1)).strftime(tstr)
            end_time = tnow.strftime(tstr)
            time_str = "past 24 hours"
        elif "q1" in msg:
            print("Q1 in msg")
            start_time = yr + "-01-01T00:00:00.000Z"
            end_time   = yr + "-04-01T00:00:00.000Z"
            time_str   = "Q1 (" + yr + ")"
        elif "q2" in msg:
            print("Q2 in msg")
            start_time = yr + "-04-01T00:00:00.000Z"
            end_time   = yr + "-07-01T00:00:00.000Z"
            time_str   = "Q2 (" + yr + ")"
        elif "q3" in msg:
            print("Q3 in msg")
            start_time = yr + "-07-01T00:00:00.000Z"
            end_time   = yr + "-10-01T00:00:00.000Z"
            time_str   = "Q3 (" + yr + ")"
        elif "2021" in msg:
            print("2021 in msg")
            start_time = "2021-07-01T00:00:00.000Z"
            end_time   = "2021-10-01T00:00:00.000Z"
            time_str   = "2021"
        elif "2022" in msg:
            print("year or 2022 in msg")
            start_time = "2022-01-01T00:00:00.000Z"
            end_time   = "2023-01-01T00:00:00.000Z"
            time_str = "2022"
        elif "2023" in msg:
            print("year or 2023 in msg")
            start_time = "2023-01-01T00:00:00.000Z"
            end_time   = "2024-01-01T00:00:00.000Z"
            time_str = "2023"
        elif "last year" in msg or "lastyear" in msg:
            print("last year or lastyear in msg")
            start_time = str(int(yr)-1) + "-01-01T00:00:00.000Z"
            end_time   =             yr + "-01-01T00:00:00.000Z"
            time_str = "last year"
        elif "year" in msg:
            print("year in msg")
            start_time =             yr + "-01-01T00:00:00.000Z"
            end_time   = str(int(yr)+1) + "-01-01T00:00:00.000Z"
            time_str = "year"
        elif "jan" in msg:
            print("jan in msg")
            start_time = yr + "-01-01T00:00:00.000Z"
            end_time   = yr + "-02-01T00:00:00.000Z"
            time_str = "Jan " + yr
        elif "feb" in msg:
            print("feb in msg")
            start_time = yr + "-02-01T00:00:00.000Z"
            end_time   = yr + "-03-01T00:00:00.000Z"
            time_str = "Feb " + yr
        elif "mar" in msg:
            print("mar in msg")
            start_time = yr + "-03-01T00:00:00.000Z"
            end_time   = yr + "-04-01T00:00:00.000Z"
            time_str = "Mar " + yr
        elif "april" in msg:
            print("april in msg")
            start_time = yr + "-04-01T00:00:00.000Z"
            end_time   = yr + "-05-01T00:00:00.000Z"
            time_str = "April " + yr
        elif "may" in msg:
            print("may in msg")
            start_time = yr + "-05-01T00:00:00.000Z"
            end_time   = yr + "-06-01T00:00:00.000Z"
            time_str = "May " + yr
        elif "june" in msg:
            print("june in msg")
            start_time = yr + "-06-01T00:00:00.000Z"
            end_time   = yr + "-07-01T00:00:00.000Z"
            time_str = "June " + yr
        elif "july" in msg:
            print("month or july in msg")
            start_time = yr + "-07-01T00:00:00.000Z"
            end_time   = yr + "-08-01T00:00:00.000Z"
            time_str = "July " + yr
        elif "aug" in msg:
            print("aug in msg")
            start_time = yr + "-08-01T00:00:00.000Z"
            end_time   = yr + "-09-01T00:00:00.000Z"
            time_str = "Aug " + yr
        elif "sep" in msg:
            print("sep in msg")
            start_time = yr + "-08-01T00:00:00.000Z"
            end_time   = yr + "-09-01T00:00:00.000Z"
            time_str = "Sep " + yr
        elif "oct" in msg:
            print("oct in msg")
            start_time = yr + "-08-01T00:00:00.000Z"
            end_time   = yr + "-09-01T00:00:00.000Z"
            time_str = "Oct " + yr
        elif "nov" in msg:
            print("nov in msg")
            start_time = yr + "-11-01T00:00:00.000Z"
            end_time   = yr + "-12-01T00:00:00.000Z"
            time_str = "Nov " + yr
        elif "dec" in msg:
            print("dec in msg")
            start_time = yr + "-12-01T00:00:00.000Z"
            end_time   = yr + "-01-01T00:00:00.000Z"
            time_str = "Dec " + yr
        elif "last month" in msg or "lastmonth" in msg:
            print("last month in msg")
            start_time = yr + str(int(mo)-1) + "-01T00:00:00.000Z"
            end_time   = yr +             mo + "-01T00:00:00.000Z"
            time_str = "last month"
        elif "month" in msg:
            print("month in msg")
            start_time = yr +             mo + "-01T00:00:00.000Z"
            end_time   = yr + str(int(mo)+1) + "-01T00:00:00.000Z"
            time_str = "last month"
        # end if/elifs

        return [start_time, end_time, time_str, True, ""]
    # end get_time_str

    def get_method(self, method):
        if method == None:
            method = "Points"
        # end if
        method = method.lower()
        method = method.replace(" ","")
        if "like" in method:
            method = "Likes"
        elif "retweet" in method:
            method = "Retweets"
        elif "tweet" in method:
            method = "Tweets"
        elif "keyword" in method:
            method = "Custom_" + method.split("keyword")[1].lower()
        else:
            method = "Points"
        # end if/elifs
        return method
    # end get_method

    def get_user_stats(self, username):
        indsKE = np.where(         self.keywords_data["usernames"] == username)
        indsLI = np.where(self.engagement["likes"   ]["usernames"] == username)
        indsRT = np.where(self.engagement["retweets"]["usernames"] == username)
        indsRP = np.where(self.engagement["replies" ]["usernames"] == username)
        indsQT = np.where(self.engagement["quotes"  ]["usernames"] == username)

        indsST = np.where(self.stream_data["usernames"] == username)

        indsSK = np.where(self.stream_data["etypes"][indsST] == self.FLAG_KEY)
        indsSR = np.where(self.stream_data["etypes"][indsST] == self.FLAG_RTS)
        indsSQ = np.where(self.stream_data["etypes"][indsST] == self.FLAG_QTS)

        lenKE = len(         self.keywords_data["usernames"][indsKE])
        lenLI = len(self.engagement[   "likes"]["usernames"][indsLI])
        lenRT = len(self.engagement["retweets"]["usernames"][indsRT])
        lenRP = len(self.engagement[ "replies"]["usernames"][indsRP])
        lenQT = len(self.engagement[  "quotes"]["usernames"][indsQT])

        lenKE += len(self.stream_data["usernames"][indsST][indsSK])
        lenRT += len(self.stream_data["usernames"][indsST][indsSR])
        lenQT += len(self.stream_data["usernames"][indsST][indsSQ])

        TITLE = "Username: " + username
        DESCRIPTION = "--"
        embedDpy =      discord.Embed(title=TITLE, description=DESCRIPTION)
        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedDpy.set_footer(text = self.FOOTER, icon_url=self.URL)
        embedInt.set_footer(text = self.FOOTER, icon_url=self.URL)

        try:
            rank = np.where(self.points_usernames == username)[0][0]
        except:
            rank = "?"
        # end try/except

        vals = {
            "Rank":     rank,
            "Points":   lenLI + 2*lenRT + 2*lenQT + 3*lenRP + 3*lenQT + 3*lenKE,
            "Likes":    lenLI,
            "Retweets": lenRT + lenQT,
            "Tweets":   lenKE + lenRP + lenQT
        }

        max_str    = 0
        max_digits = 0
        for key in vals.keys():
            max_str = max(max_str, len(key))
            max_digits = max(max_digits, len(str(vals[key])))
        # end for keys

        for key in vals.keys():
            embedDpy.add_field(name=key, value=str(vals[key]), inline=False)
            embedInt.add_field(name=key, value=str(vals[key]), inline=False)
        # end for

        self.statEmbedDpy = embedDpy
        self.statEmbedInt = embedInt
    # end get_user_stats

    def verify_processed_tweet(self, tweet_url, username):
        try:
            tweet_id = int(tweet_url.split("/status/")[1].replace(" ","").replace("\n",""))
        except:
            error_msg = "```>>> error! Malformed tweet_url. Could not find /status/```"
            return [error_msg, False]
        # end try/except

        if "ezu_xyz" in tweet_url:
            print("in if")
            if username == "":
                error_msg  = "```>>> error! Didn't supply username and we were asked to verify"
                error_msg += " interaction with @ezu_xyz```"
                return [error_msg, False]
            # end if
            for etype in ["likes","retweets"]:
                inds = np.where(self.engagement[etype]["tweet_ids"] == tweet_id)
                if len(inds) != 0:
                    print("696 inds: ", inds)
                    if username in self.engagement[etype]["usernames"][inds]:
                        return [self.VERIFY_SUCCESS, True]
                    # end if
                # end if
                if etype == "retweets":
                    inds = np.where(self.stream_data["etypes"] == self.FLAG_RTS)
                    inds = np.where(self.stream_data["tweet_ids"][inds] == tweet_id)
                    if len(inds) != 0:
                        print("705 inds: ", inds)
                        if username in self.stream_data["usernames"][inds]:
                            return [self.VERIFY_SUCCESS, True]
                        # end if
                    # end if
                # end if
            # end for
        else:
            print("in else")
            inds = np.where(self.keywords_data["tweet_ids"] == tweet_id)
            if len(inds) != 0:
                if username in self.keywords_data["usernames"][inds]:
                    return [self.VERIFY_SUCCESS, True]
                # end if
            # end if
            for etype in ["quotes", "replies"]:
                inds = np.where(self.engagement[etype]["tweet_ids"] == tweet_id)
                if len(inds) != 0:
                    print("723 inds: ", inds)
                    if username in self.engagement[etype]["usernames"][inds]:
                        return [self.VERIFY_SUCCESS, True]
                    # end if
                # end if
            # end for
            inds = np.where(self.stream_data["etypes"] == self.FLAG_QTS)
            inds = np.where(self.stream_data["tweet_ids"][inds] == tweet_id)
            if len(inds) != 0:
                print("732 inds: ", inds)
                if username in self.stream_data["usernames"][inds]:
                    return [self.VERIFY_SUCCESS, True]
                # end if
            # end if
            inds = np.where(self.stream_data["etypes"] == self.FLAG_KEY)
            inds = np.where(self.stream_data["tweet_ids"][inds] == tweet_id)
            if len(inds) != 0:
                print("740 inds: ", inds)
                if username in self.stream_data["usernames"][inds]:
                    return [self.VERIFY_SUCCESS, True]
                # end if
            # end if
        # end if/else

        url = self.twitter_api_base[:-1] + "?ids=" + str(tweet_id) \
            + "&tweet.fields=created_at"

        os.system(self.curl_base + url + self.curl_header + self.auth + 
                  "' > " + "delete_me.txt")

        with open("delete_me.txt", "r") as fid:
            line = fid.read()
        # end with open

        tweet_time = line.split('"created_at":"')[1].split('"')[0]
        tweet_time_s = self.get_tweet_time_s(tweet_time)

        if self.latest_tweet_time_s < tweet_time_s:
            message = "This tweet created after last query was made"
            print(message)
            return [message,False]
        # end if
        message = "```>>> Hmm, I don't see any interaction from the specified user on this Tweet. Are you sure there was a keyword or that the user did indeed interact? If so, please reach out to [redacted] so [] can look into it!```"

        print(message)
        return [message,False]
    # end verify_processed_tweet

    async def get_rankings(self, method = DEFAULT_METHOD,
                             start_time = DEFAULT_STARTT, 
                             end_time   = DEFAULT_ENDT, 
                             time_str   = DEFAULT_TIMEST):
        print("begin get_rankins")

        if method in ["Likes", "Retweets"]:
            etype = method.lower()

            inds = np.where(self.stream_data["etypes"] == etype)
            tuids = np.unqiue(
                        np.concatenate([
                            self.engagement[etype]["tuids"],
                            self.stream_data["tuids"][inds]
                        ])
            )
            ees = np.zeros(len(tuids))
            usernames = []
            for ii,tuid in enumerate(tuids):
                await asyncio.sleep(self.QS)
                indsEE = np.where(self.engagement[etype]["tuids"] == tuid)
                indsST = np.where(self.stream_data["tuids"][inds] == tuid)

                lenEE  = len(self.engagement[etype]["usernames"][indsEE])
                lenEE += len(      self.stream_data["usernames"][inds][indsST])

                ees[ii] = lenEE
                if len(self.engagement[etype]["usernames"][indsEE]) != 0:
                    usernames.append(self.engagement[etype]["usernames"][indsEE][0])
                elif len(self.stream_data["usernames"][inds][indsST]) != 0:
                    usernames.append(self.stream_data["usernames"][inds][indsST])
                # end if/elifs
            # end for
            inds = np.argsort(ees)[::-1]
            vals = ees[inds]
            usernames = np.array(usernames)[inds]

        elif method == "Tweets":
            tuids =  np.unique(
                    np.concatenate([
                                 self.keywords_data["tuids"],
                        self.engagement[ "replies"]["tuids"],
                        self.engagement[  "quotes"]["tuids"],
                        self.stream_data["tuids"]
                    ])
                )
            tweets = np.zeros(len(tuids))
            usernames = []
            print("len tuids: ", len(tuids))
            for ii,tuid in enumerate(tuids):
                #if ii % 100 == 0:
                #    print("ii, tuid: ", ii, tuid)
                # end if

                await asyncio.sleep(self.QS)
                indsKE = np.where(        self.keywords_data["tuids"] == tuid)
                indsRP = np.where(self.engagement["replies" ]["tuids"] == tuid)
                indsQT = np.where(self.engagement["quotes"  ]["tuids"] == tuid)

                indsST = np.where(self.stream_data["tuids"] == tuid)

                indsSK = np.where(self.stream_data["etypes"][indsST] == self.FLAG_KEY)
                indsSQ = np.where(self.stream_data["etypes"][indsST] == self.FLAG_QTS)

                lenKE = len(         self.keywords_data["usernames"][indsKE])
                lenRP = len(self.engagement[ "replies"]["usernames"][indsRP])
                lenQT = len(self.engagement[  "quotes"]["usernames"][indsQT])

                lenKE += len(self.stream_data["usernames"][indsST][indsSK])
                lenQT += len(self.stream_data["usernames"][indsST][indsSQ])

                tweets[ii] = lenQT + lenRP + lenKE
                if   len(self.keywords_data["usernames"][indsKE]) != 0:
                    usernames.append(         self.keywords_data["usernames"][indsKE][0])
                elif len(self.engagement[ "replies"]["usernames"][indsRP]) != 0:
                    usernames.append(self.engagement[ "replies"]["usernames"][indsRP][0])
                elif len(self.engagement[  "quotes"]["usernames"][indsQT]) != 0:
                    usernames.append(self.engagement[  "quotes"]["usernames"][indsQT][0])
                elif len(self.stream_data["usernames"][indsST][indsSK]) != 0:
                    usernames.append(self.stream_data["usernames"][indsST][indsSK])
                elif len(self.stream_data["usernames"][indsST][indsSQ]) != 0:
                    usernames.append(self.stream_data["usernames"][indsST][indsSQ])
                # end if/elifs
            # end for
            inds = np.argsort(tweets)[::-1]
            vals = tweets[inds]
            usernames = np.array(usernames)[inds]

        elif method == "Points":
            ## first get all unique IDs
            tuids =  np.unique(
                    np.concatenate([
                                 np.unique(self.keywords_data["tuids"]),
                        np.unique(self.engagement[   "likes"]["tuids"]),
                        np.unique(self.engagement["retweets"]["tuids"]),
                        np.unique(self.engagement[ "replies"]["tuids"]),
                        np.unique(self.engagement[  "quotes"]["tuids"]),
                        np.unique(self.stream_data["tuids"])
                    ])
                )
            points = np.zeros(len(tuids))
            usernames = []
            print("len tuids: ", len(tuids))
            for ii,tuid in enumerate(tuids):
                '''
                print("tuids: ", [tuids])
                input(">>")
                print("tuid: ", [tuid])
                input(">>")
                print("kdids: ", [self.keywords_data["tuids"]])
                input(">>")
                print("liids: ", [self.engagement["likes"]["tuids"]])
                input(">>")
                print("rtids: ", [self.engagement["retweets"]["tuids"]])
                input(">>")
                print("rpids: ", [self.engagement["replies"]["tuids"]])
                input(">>")
                print("qtids: ", [self.engagement["quotes"]["tuids"]])
                input(">>")
                print("stids: ", [self.stream_data["tuids"]])
                input(">>")
                '''
                if ii % 100 == 0:
                    print("ii, tuid: ", ii, tuid)
                # end if
                await asyncio.sleep(self.QS)
                indsKE = np.where(         self.keywords_data["tuids"] == tuid)
                indsLI = np.where(self.engagement["likes"   ]["tuids"] == tuid)
                indsRT = np.where(self.engagement["retweets"]["tuids"] == tuid)
                indsRP = np.where(self.engagement["replies" ]["tuids"] == tuid)
                indsQT = np.where(self.engagement["quotes"  ]["tuids"] == tuid)

                indsST = np.where(self.stream_data["tuids"] == tuid)

                indsSK = np.where(self.stream_data["etypes"][indsST] == self.FLAG_KEY)
                indsSR = np.where(self.stream_data["etypes"][indsST] == self.FLAG_RTS)
                indsSQ = np.where(self.stream_data["etypes"][indsST] == self.FLAG_QTS)

                lenKE = len(         self.keywords_data["usernames"][indsKE])
                lenLI = len(self.engagement[   "likes"]["usernames"][indsLI])
                lenRT = len(self.engagement["retweets"]["usernames"][indsRT])
                lenRP = len(self.engagement[ "replies"]["usernames"][indsRP])
                lenQT = len(self.engagement[  "quotes"]["usernames"][indsQT])

                lenKE += len(self.stream_data["usernames"][indsST][indsSK])
                lenRT += len(self.stream_data["usernames"][indsST][indsSR])
                lenQT += len(self.stream_data["usernames"][indsST][indsSQ])

                points[ii] = lenLI + 2*lenRT + 2*lenQT + 3*lenRP + 3*lenQT + 3*lenKE

                '''
                print("type tuid: ", type(tuid))
                iii = np.where(np.concatenate([
                                 self.keywords_data["tuids"],
                        self.engagement[   "likes"]["tuids"],
                        self.engagement["retweets"]["tuids"],
                        self.engagement[ "replies"]["tuids"],
                        self.engagement[  "quotes"]["tuids"],
                        self.stream_data["tuids"]
                    ]) == tuid)
                print("iii", iii)

                ikd  = np.where(self.keywords_data["tuids"] == tuid)
                ieli = np.where(self.engagement["likes"]["tuids"] == tuid)
                iert = np.where(self.engagement["retweets"]["tuids"] == tuid)
                ierp = np.where(self.engagement["replies"]["tuids"] == tuid)
                ieqt = np.where(self.engagement["quotes"]["tuids"] == tuid)
                istr = np.where(self.stream_data["tuids"] == tuid)

                
                print("ikd: ",  ikd)
                print("ieli: ", ieli)
                print("iert: ", iert)
                print("ierp: ", ierp)
                print("ieqt: ", ieqt)
                print("istr: ", istr)

                print("kd: ", tuid in self.keywords_data["tuids"].tolist())
                print("eli: ", tuid in self.engagement["likes"]["tuids"].tolist())
                print("ert: ", tuid in self.engagement["retweets"]["tuids"].tolist())
                print("erp: ", tuid in self.engagement["replies"]["tuids"].tolist())
                print("equ: ", tuid in self.engagement["quotes"]["tuids"].tolist())
                print("str: ", tuid in self.stream_data["tuids"].tolist())
                '''

                ## this is to grab a/the username corresponding to the tuid (so yes if/elifs)
                if   len(self.keywords_data["usernames"][indsKE]) != 0:
                    usernames.append(         self.keywords_data["usernames"][indsKE][0])
                elif len(self.engagement[   "likes"]["usernames"][indsLI]) != 0:
                    usernames.append(self.engagement[   "likes"]["usernames"][indsLI][0])
                elif len(self.engagement["retweets"]["usernames"][indsRT]) != 0:
                    usernames.append(self.engagement["retweets"]["usernames"][indsRT][0])
                elif len(self.engagement[ "replies"]["usernames"][indsRP]) != 0:
                    usernames.append(self.engagement[ "replies"]["usernames"][indsRP][0])
                elif len(self.engagement[  "quotes"]["usernames"][indsQT]) != 0:
                    usernames.append(self.engagement[  "quotes"]["usernames"][indsQT][0])
                elif len(self.stream_data["usernames"][indsST][indsSK]) != 0:
                    usernames.append(self.stream_data["usernames"][indsST][indsSK])
                elif len(self.stream_data["usernames"][indsST][indsSR]) != 0:
                    usernames.append(self.stream_data["usernames"][indsST][indsSR])
                elif len(self.stream_data["usernames"][indsST][indsSQ]) != 0:
                    usernames.append(self.stream_data["usernames"][indsST][indsSQ])
                else:
                    print("couldn't find username")
                    raise
                # end if/elifs
            # end for
            inds = np.argsort(points)[::-1]
            vals = points[inds]
            usernames = np.array(usernames)[inds]
            self.points_usernames = usernames
        #elif method == Tweets, and then custom, but I also need to handle date ranges..
        print("finished with get_rankings")
        return [vals, usernames]
    # end get_rankings

    async def get_leaderboard(self, method     = DEFAULT_METHOD,
                                    start_time = DEFAULT_STARTT, 
                                    end_time   = DEFAULT_ENDT, 
                                    time_str   = DEFAULT_TIMEST):
        start_lb = time.time()

        vals, usernames = await self.get_rankings(method=method, start_time=start_time, end_time=end_time, time_str=time_str)
        print("vals[:20]: ", vals[:20])

        # now that we have vals, usernames - let's bdl the leaderboard!

        TITLE = method + " Leaderboard for " + time_str + " data range"
        DESCRIPTION = "\u200b"
        embedDpy =      discord.Embed(title=TITLE, description=DESCRIPTION)
        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedDpy.set_footer(text = self.FOOTER, icon_url=self.URL)
        embedInt.set_footer(text = self.FOOTER, icon_url=self.URL)

        num_pages = int(np.ceil(len(usernames)/self.LB_VPP))
        leaderboards      = []
        leaderboardsEmbed = []
        self.lbEmbedDpys  = []
        self.lbEmbedInts  = []
        vpp = int(self.LB_VPP)
        for jj in range(num_pages):
            start = jj*vpp
            end = (jj+1)*vpp
            if start > len(vals):
                continue
            if end > len(vals):
                end = len(vals)
            # end if

            usernamesp = usernames[start:end]
            valp       = vals[start:end]

            max_name_len = 0
            max_val_len  = 0
            for ii in range(len(valp)):
                max_name_len = max(max_name_len, len(usernamesp[ii]))
                max_val_len  = max(max_val_len,  len(str(int(valp[ii]))))
            # end for ii

            leaderboards.append(">>> ```")
            leaderboardsEmbed.append("```")
            for ii in range(len(valp)):
                line = str(jj*vpp+ii).rjust(2) + ") " + \
                (usernamesp[ii] + ":").ljust(max_name_len+1) + " " + \
                    str(int(valp[ii])).rjust(max_val_len) + "\n"
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
        # end for jj in num_pages
        print("get_leaderboard executed in (s): ", time.time() - start_lb)
    # end get_leaderboard

    async def get_rank(self, username, method     = DEFAULT_METHOD,
                                       start_time = DEFAULT_STARTT, 
                                       end_time   = DEFAULT_ENDT, 
                                       time_str   = DEFAULT_TIMEST):

        vals, usernames = await self.get_rankings(method=method, start_time=start_time, end_time=end_time, time_str=time_str)
        ind = np.where(usernames == username)
        print("805 gr ind: ", ind)
        ind = ind[0][0]

        custom = ""
        if "Custom_" in method:
            custom += method
            method = method.split("Custom_")[1]
        # end if

        TITLE = method + " Rank for " + time_str + " data range"
        DESCRIPTION = "username: " + username
        embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION)
        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedDpy.set_footer(text = self.FOOTER, icon_url=self.URL)
        embedInt.set_footer(text = self.FOOTER, icon_url=self.URL)
        
        embedDpy.add_field(name="Rank", value=str(ind), inline=False)
        embedInt.add_field(name="Rank", value=str(ind), inline=False)
        self.rankEmbedDpy = embedDpy
        self.rankEmbedInt = embedInt
    # end get_rank

    async def tweeteroo_stream(self):
        print("begin tweeteroo_stream")
        #os.system("python3 stream.py &")

        wcnt = 0
        while True:
            await asyncio.sleep(self.MS)
            wcnt += 1

            fs = np.sort(glob.glob("stream_data?.txt"))
            for fn in fs:
                await asyncio.sleep(self.SS)
                with open(fn, "r") as fid:
                    for line in fid:
                        await asyncio.sleep(self.SS)
                        try:
                            line = ast.literal_eval(line)
                        except:
                            continue
                        # end try/except
                        
                        if "matching_rules" not in line:
                            continue
                        # end if

                        if not ("data" in line and    
                                 (        "id" in line["data"] and 
                                        "text" in line["data"] and 
                                  "created_at" in line["data"])) or \
                           not (    "includes" in line and "users" in line["includes"]):
                            continue
                        # end if
                        tweet_id = line["data"]["id"]
                        tuid     = line["data"]["author_id"]
                        text     = line["data"]["text"]
                        date     = line["data"]["created_at"]
                        date_s   = str(self.get_tweet_time_s(date))

                        flag = "keywords"
                        flag = self.FLAG_KEY
                        for matching_rule in line["matching_rules"]:
                            if "retweetstag" in matching_rule["tag"]:
                                flag = self.FLAG_RTS
                                text = text[:2]
                            elif "quotestag" in matching_rule["tag"]:
                                flag = self.FLAG_QTS
                            # end if/elif
                        # end for

                        for user in line["includes"]["users"]:
                            await asyncio.sleep(self.QS)
                            if user["id"] == tuid:
                                username = user["username"]
                                break
                            # end if
                        # end for
                        self.stream_data["tweet_ids"  ] = np.append(self.stream_data["tweet_ids"  ], tweet_id)
                        self.stream_data[    "tuids"  ] = np.append(self.stream_data[    "tuids"  ], tuid)
                        self.stream_data["usernames"  ] = np.append(self.stream_data["usernames"  ], username)
                        self.stream_data[    "dates"  ] = np.append(self.stream_data[    "dates"  ], date)
                        self.stream_data[    "dates_s"] = np.append(self.stream_data[    "dates_s"], date_s)
                        self.stream_data[   "etypes"  ] = np.append(self.stream_data[   "etypes"  ], flag)
                        self.stream_data[    "texts"  ] = np.append(self.stream_data[    "texts"  ], text)
                        stream_data_to_save = {
                            "tweet_ids": self.stream_data["tweet_ids"  ].tolist(),
                                "tuids": self.stream_data[    "tuids"  ].tolist(),
                            "usernames": self.stream_data["usernames"  ].tolist(),
                            "dates"    : self.stream_data[    "dates"  ].tolist(),
                            "dates_s"  : self.stream_data[    "dates_s"].tolist(),
                            "etypes"   : self.stream_data[   "etypes"  ].tolist(),
                            "texts"    : self.stream_data[    "texts"  ].tolist()
                        }

                        self.safe_save(self.fname_stream, stream_data_to_save)
                    # end for line in fid
                # end with open
            # end for fs
        # end while True
        print("end tweeteroo_stream")
    # end tweeteroo_stream

    def safe_save(self, fname, data):
        fname_temp   = fname + "_temp"
        fname_backup = fname + "_backup"

        os.system("cp " + fname + " " + fname_backup)
        #np.savetxt(fname_temp, np.array(data))
        with open(fname_temp, "w") as fid:
            fid.write(str(data))
        # end with open
        os.system("cp " + fname_temp + " " + fname)
    # end safe_save

    def discord_bot(self):
        print("begin discord_bot")
        secret = os.environ.get(self.CMD_PREFIX + "BotPass")
        intBot = interactions.Client(secret)
        print("clientInteractions loaded")
        client = discord.Client()
        print("client loaded")

        @intBot.event
        async def on_ready():
            user = await get.get(intBot, interactions.User, user_id=int(intBot.me.id))
            print("We have logged in as {0.username}#{1.discriminator}".format(user,user))

            channel = await get.get(intBot, interactions.Channel, channel_id=self.CID_LOG)
            await channel.send("I AM ALIVE! MWAHAHAHA")
        # end on_ready

        @intBot.command(
            name=self.CMD_PREFIX,
            description=self.BOT_NAME + " commands",
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

            if   sub_command in ["help", "halp", "hlp"]:
                await ctx.send(embeds=self.helpEmbedInt, ephemeral=True)

            elif sub_command in ["helplb","halplb","hlplb", 
                                "lbhelp","lbhalp","lbhlp"]:
                await ctx.send(embeds=self.lbHelpEmbedInt, ephemeral=True)
        
            elif sub_command in ["keywords"]:
                await ctx.send(embeds=self.keyEmbedInt, ephemeral=True)

            elif sub_command in ["stats","stat"]:
                if username == None:
                    discord_id = str(ctx.author.id)
                    if discord_id not in self.user_dict["discordId_to_username"]:
                        await ctx.send(self.UNKNOWN_USERNAME, ephemeral=True)
                        return
                    # end if
                    username = self.user_dict["discordId_to_username"][discord_id]

                elif username != None:
                    username = username.lower()
                    username = username.replace("@","")
                    username = username.replace(" ","")

                else:
                    msg2 = "```>>> Something went very wrong fetching the username. Error Code 273```"
                    await ctx.send(msg2, ephemeral=True)
                    return
                # end if/elif/else

                msg2 = ">>> ```Username: " + username + "\n"
                msg2 += "--\n"

                print("281: ", msg2)
                try:
                    self.get_user_stats(username)
                except Exception as err:
                    print("833 get_user_stats err: ", err)
                    print("834 get_user_stats err.ags: ", err.args[:])
                    await channel.send(self.STATS_ERROR)
                    return
                # end try/except
                await ctx.send(embeds=self.statEmbedInt, ephemeral=True)
                return


            elif sub_command in ["verify"]:
                tweet_url = url.lower()
                tweet_url = tweet_url.replace(",", "").replace(" ", "")
                if "?" in tweet_url:
                    tweet_url = tweet_url.split("?")[0]
                # end if

                if ("https://twitter.com/" not in tweet_url) and ("https://mobile.twitter.com/") not in tweet_url:
                    await ctx.send(self.VERIFY_ERROR, ephemeral=True)
                    return
                # end if
          
                if username == None:
                    discord_id = str(ctx.author.id)
                    if discord_id not in self.user_dict["discordId_to_username"]:
                        await ctx.send(msg2, ephemeral=True)
                        return
                    # end if
                    username = self.user_dict["discordId_to_username"][discord_id]

                elif username != None:
                    username = username.lower()
                    username = username.replace("@","")
                    username = username.replace(" ","")
                # end if/elif
                msg2 = "```>>> okay! will verify if we processed that tweet for '" + username + "' yet or not```"
                await ctx.send(msg2, ephemeral=True)

                try:
                    msg2,status = self.verify_processed_tweet(tweet_url, username)
                except Exception as err:
                    print("873 verify_processed_tweet err: ", err)
                    print("874 vpt err.ags: ", err.args[:])
                    await channel.send(self.VERIFY_ERROR, ephemeral=True)
                    return
                # end try/except
                if status == False:
                    print("879 vptF error")
                    await channel.send(self.VERIFY_ERROR, ephemeral=True)
                    return
                # end if
                await ctx.send(msg2, ephemeral=True)

            elif sub_command in ["leaderboard", "lb"]:
                method = self.get_method(method)

                start_time, end_time, time_str, status, err_msg = self.get_time_str(timerange)
                if status == False:
                    await ctx.send(err_msg, ephemeral=True)
                    return
                # end if

                msg2  = "```>>> Okay, grabbing the " + method + " leaderboard for the "
                msg2 += time_str + " data time range.```"
                await ctx.send(msg2, ephemeral=True)

                try:
                    await self.get_leaderboard(start_time=start_time,
                            end_time=end_time, method=method, time_str=time_str)
                except Exception as err:
                    print("914 get_lb err: ", err)
                    print("915 get_lb err.args: ", err.args[:])
                    await ctx.send(self.LB_ERROR)
                    return
                # end try/except
                timerange = ""

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
                print("going to send embed")
                print("self.lbEmbedInts[ijk]: ", self.lbEmbedInts[ijk])
                await ctx.send(embeds=self.lbEmbedInts[ijk], 
                    components=[self.buttons_row], ephemeral=True)
                print("sent embed!")
                return
            
            elif sub_command in ["rank"]:
                if username == None:
                    discord_id = str(ctx.author.id)
                    try:
                        username = self.user_dict["discordId_to_username"][discord_id]
                    except:
                        await ctx.send(self.UNKNOWN_USERNAME, ephemeral=True)
                        return
                    # end try/except
                # end if

                method = self.get_method(method)
                start_time, end_time, time_str, status, err_msg = self.get_time_str(timerange)
                if status == False:
                    await ctx.send(err_msg, ephemeral=True)
                    return
                # end if

                msg2  = "```>>> Okay, grabbing the " + method + " rank for the "
                msg2 += time_str + " data time range.```"
                await ctx.send(msg2, ephemeral=True)

                try:
                    await self.get_rank(username.lower(), start_time=start_time,
                            end_time=end_time, method=method, time_str=time_str)
                except Exception as err:
                    print("1075 get_rank err: ", err)
                    print("1076 gr cmd err.args: ", err.args[:])
                    await ctx.send(self.RANK_ERROR, ephemeral=True)
                # end try/except

                print("discord bot hi here's the " + method + " rank")
                timerange = ""
                try:
                    await ctx.send(embeds=self.rankEmbedInt, ephemeral=True)
                except:
                    pass
            # end if/elifs
            return
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
        async def on_raw_reaction_add(payload):
            xemoji = "🇽"
            if payload.channel_id not in self.BOT_COMMANDS_CIDS:
                return
            # end if

            try:
                if payload.emoji.name == "🇽":
                    channel = client.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    if reaction and reaction.count > 1:
                        try:
                            await message.delete()
                        except Exception as err:
                            print("1033 orra del err: ", err)
                            print("1034 orra del err.args: ", err.args[:])
                        # end try/except
                    # end if
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
                    # end if
                elif payload.emoji.name == '◀':
                    channel = client.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    if reaction and reaction.count > 1:
                        try:
                            self.pages[str(message.id)]["pnum"] = self.pages[str(message.id)]["pnum"]-1
                        except Exception as err:
                            print("1059 orra err: ", err)
                            print("1060 orra err.args: ", err.args[:])
                        # end try/except
                        pnum = self.pages[str(message.id)]["pnum"]
                        await message.edit(embed=self.pages[str(message.id)]["pages"][pnum])
                        await message.clear_reactions()
                        await message.add_reaction('⏮')
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')
                        await message.add_reaction('⏭')
                        await message.add_reaction(xemoji)
                    # end if
                elif payload.emoji.name == '▶':
                    channel = client.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    if reaction and reaction.count > 1:
                        try:
                            self.pages[str(message.id)]["pnum"] = self.pages[str(message.id)]["pnum"]+1
                        except Exception as err:
                            print("1079 orra err: ", err)
                            print("1080 orra err.args: ", err.args[:])
                            return
                        # end try/except
                        pnum = self.pages[str(message.id)]["pnum"]
                        await message.edit(embed=self.pages[str(message.id)]["pages"][pnum])
                        await message.clear_reactions()
                        await message.add_reaction('⏮')
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')
                        await message.add_reaction('⏭')
                        await message.add_reaction(xemoji)
                    # end if
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
                    # end if
                # end if/elifs
            except Exception as err:
                print("1108 orra err: ", err)
                print("1109 orra err.args: ", err.args[:])
                print("uncaught exception in on_raw_reaction_add")
                return
            # end try/except
        # end on_raw_reaction_add

        @client.event
        async def on_ready():
            print("We have logged in as {0.user}".format(client))

            channel = client.get_channel(self.CID_LOG)
            await channel.send("I AM ALIVE! MWAHAHAHA")
            await self.tweeteroo_stream()
        # end on_ready

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            # end if

            if message.channel.id not in self.BOT_COMMANDS_CIDS:
                return
            # end if

            channel = client.get_channel(message.channel.id)

            msg = message.content.lower()
            prefix_in_msg = msg.startswith(      self.CMD_PREFIX) or \
                            msg.startswith("!" + self.CMD_PREFIX) or \
                            msg.startswith("/" + self.CMD_PREFIX)
            if not prefix_in_msg:
                return
            # end if

            message.content = message.content.lower().replace(" ","")

            tab = self.TAB
            msg = msg.replace("@","")
            max_len_stats = len("!" + self.CMD_PREFIX + " stats ")

            max_len  = len("!" + self.CMD_PREFIX + " help lb")
            if "lb" in msg[:max_len] and "help" in msg[:max_len]:
                await self.embed_helper([self.lbHelpEmbedDpy], client, channel)
                return
            # end if

            max_len = len("!" + self.CMD_PREFIX + " help")
            if "help" in msg[:max_len]:
                await self.embed_helper([self.helpEmbedDpy], client, channel)
                return
            elif msg.startswith("!" + self.CMD_PREFIX + "stats") or msg.startswith("!" + self.CMD_PREFIX + " stats") or \
                 msg.startswith( "" + self.CMD_PREFIX + "stats") or msg.startswith( "" + self.CMD_PREFIX + " stats") or \
                 msg.startswith("/!" + self.CMD_PREFIX + "stats") or msg.startswith("/!" + self.CMD_PREFIX + " stats") or \
                 msg.startswith( "/" + self.CMD_PREFIX + "stats") or msg.startswith( "/" + self.CMD_PREFIX + " stats"):
                
                if "username" in msg or len(msg) > max_len_stats:
                    username = ""
                    try:
                        username  = msg.split("username:")[1].replace(" ","")
                    except:
                        try:
                            username  = msg.split("username=")[1].replace(" ","")
                        except:
                            try:
                                username = msg.split("stats ")[1].replace(" ","")
                            except:
                                await channel.send(self.VERIFY_ERROR)
                                return
                            # end try/except
                        # end try/except
                    # end try/except
                    if username == "":
                        await channel.send(self.VERIFY_ERROR)
                        return
                    # end if
                else:
                    discord_id = str(message.author.id)
                    try:
                        username = self.user_dict["discordId_to_username"][discord_id]
                    except:
                        await channel.send(self.UNKNOWN_USERNAME)
                        return
                    # end try/except
                # end if/else
                
                msg2 = ">>> ```Username: " + username + "\n"
                msg2 += "--\n"
                print(">>> fetching user data")
                try:
                    self.get_user_stats(username)
                except Exception as err:
                    print("1205 get_user_stats err: ", err)
                    print("1206 gus err.ags: ", err.args[:])
                    await channel.send(self.STATS_ERROR)
                    return
                # end try/except
                await self.embed_helper([self.statEmbedDpy], client,channel)
                return

            elif "verify" in msg:
                if (("https://twitter.com/" not in msg) and ("https://mobile.twitter.com/") not in msg) or "/status/" not in msg:
                    print("1361 malformed url in on_msg verify")
                    await channel.send(self.VERIFY_ERROR)
                    return
                # end if

                msg = msg.split("verify")
                if len(msg) > 2:
                    msg = "".join(msg[1:])
                else:
                    msg = msg[1]
                # end if/else
                msg = msg.replace(" ","").replace("\n","")
                msg = msg.replace(":","").replace("=","")
                msg = msg.replace("@","")
                msg = msg.replace("username","")
                if "ezu_xyz/status/" in msg:
                    if "," in msg:
                        tweet_url,username = msg.split(",")
                    else:
                        discord_id = str(message.author.id)
                        try:
                            username = self.user_dict["discordId_to_username"][discord_id]
                        except:
                            await channel.send(self.UNKNOWN_USERNAME)
                            await channel.send(self.VERIFY_ERROR)
                            return
                        # end try/except
                        tweet_url = msg
                    # end if/else
                else:
                    try:
                        username = msg.split("/status/")[0].split("/")[-1].replace(" ","").replace("\n","")
                    except Exception as err:
                        print("1370 on_msg verify username split err: ", err)
                        print("1371 omvusp err.args: ", err.args[:])
                        await channel.send(self.VERIFY_ERROR)
                        return
                    # end try/except

                    if "," in msg:
                        msg = msg.split(",")[0]
                    # end if
                    tweet_url = msg
                # end if/else
                if "?" in tweet_url:
                    tweet_url = tweet_url.split("?")[0]
                # end if
                print("1408 username: ", username)
                print("1409 tweet_url: ", tweet_url)

                await channel.send("```>>> okay! will verify if we processed that tweet for that user yet or not```")
                msg2,status = self.verify_processed_tweet(tweet_url, username)
                try:
                    msg2,status = self.verify_processed_tweet(tweet_url, username)
                except Exception as err:
                    print("1415 verify_processed_tweet err: ", err)
                    print("1416 vpt err.ags: ", err.args[:])
                    await channel.send(self.VERIFY_ERROR)
                    return
                # end try/except
                if status == False:
                    print("1421 error, msg2: ", msg2)
                    await channel.send(self.VERIFY_ERROR)
                    return
                # end if
                await channel.send(msg2)
                return

            elif "lb" in msg or "leaderboard" in msg:
                method = "Points"
                if "like" in msg:
                    method = "Likes"
                elif "retweet" in msg:
                    method = "Retweets"
                elif "repl" in msg:
                    method = "Replies"
                elif "keyword" in msg:
                    method = "Custom_" + msg.split("keyword")[1].lower()
                # end if/elifs
                method = self.get_method(msg)
                start_time, end_time, time_str, status, err_msg = self.get_time_str(msg)
                if status == False:
                    await channel.send(err_msg)
                    return
                # end if

                msg2  = "```>>> Okay, grabbing the " + method + " leaderboard for "
                msg2 += time_str + " data range.```"
                await channel.send(msg2)

                print("msg: ", msg)
                start_time = start_time.replace("st","")
                start_time = start_time.replace("nd","")
                start_time = start_time.replace("th","")
                end_time = end_time.replace("st","")
                end_time = end_time.replace("nd","")
                end_time = end_time.replace("th","")

                await self.get_leaderboard(start_time=start_time,
                            end_time=end_time, method=method, time_str=time_str)
                await self.embed_helper(self.lbEmbedDpys, client,channel)
                return
                try:
                    await self.get_leaderboard(start_time=start_time,
                            end_time=end_time, method=method, time_str=time_str)
                except Exception as err:
                    print("1324 lb on_msg err: ", err)
                    print("1325 lb on_msg err.args: ", err.args[:])
                    await channel.send(self.LB_ERROR)
                    return
                # end try/except
                await self.embed_helper(self.lbEmbedDpys, client,channel)
                return

            elif "rank" in msg:
                print("in rank")
                max_len_rank = len("!rtt rank ")
                if "username" in msg:
                    if "method" in msg or "timerange" in msg:
                        username = msg.split("username")[1][1:]
                        if username[0] == " ":
                            username = username[1:]
                        # end if
                        username = username.split()[0].replace(" ","")
                    else:
                        username = msg.split("username")[1][1:].replace(" ","")
                    # end if/else
                elif "keyword" in msg and len(msg.split("keyword")[0]) <= max_len_rank:
                    print("no un in msg")
                    discord_id = str(message.author.id)
                    print("did")
                    try:
                        username = self.user_dict["discordId_to_username"][discord_id]
                        print("un from did: ", username)
                    except:
                        await channel.send(self.UNKNOWN_USERNAME)
                        return
                    # end try/except
                elif len(msg) > max_len_rank:
                    username = msg.split("rank ")[1]
                    if "keyword" in username:
                        username = username.split("keyword")[0]
                    if "," in username:
                        username = username.split(",")[0]
                    # end if
                    useranme = username.replace(" ","")
                    useranme = username.replace("\n","")
                    useranme = username.replace("@","")
          
                else:
                    print("no un in msg")
                    discord_id = str(message.author.id)
                    print("did")
                    try:
                        username = self.user_dict["discordId_to_username"][discord_id]
                        print("un from did: ", username)
                    except:
                        await channel.send(self.UNKNOWN_USERNAME)
                        return
                    # end try/except
                # end if/else

                method = self.get_method(msg)
                start_time, end_time, time_str, status, err_msg = self.get_time_str(msg)
                if status == False:
                    await channel.send(err_msg)
                    return
                # end if
          
                msg2  = "```>>> Okay, grabbing the " + method + " rank for "
                msg2 += time_str + " data range.```"
                await channel.send(msg2)

                print("username: ", username)
                try:
                    await self.get_rank(username, start_time=start_time,
                                        end_time=end_time, method=method, time_str=time_str)
                except Exception as err:
                    print("1508 get_rank err: ", err)
                    print("1509 gr msg err.args: ", err.args[:])
                    await channel.send(self.RANK_ERROR)
                    return
                # end try/except
                await self.embed_helper([self.rankEmbedDpy], client,channel)
                return
            
            elif "key" in msg:
                await self.embed_helper([self.keyEmbedDpy], client,channel)
                return

            else:
                msg2  = "```sorry! I didn't understand that command. Try '" + self.CMD_PREFIX + "help(?)'\n"
                msg2 += "without the quotes...```"
            # end if/elif/else
            await channel.send(msg2)
        # end def on_message

        loop = asyncio.get_event_loop()

        task2 = loop.create_task(client.start(secret))
        task1 = loop.create_task(intBot._ready())

        gathered = asyncio.gather(task1, task2, loop=loop)
        loop.run_until_complete(gathered)
    # end discord_bot
# end EzuTweeteroo

if __name__ == "__main__":
    ezu = EzuTweeteroo()
    ezu.discord_bot()
# end if
