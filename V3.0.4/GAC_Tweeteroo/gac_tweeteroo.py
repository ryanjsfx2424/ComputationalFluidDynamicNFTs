import sys
import discord

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions import Button, ButtonStyle, ActionRow
from interactions.client import get

from init_fetch_likes_tweet_activity import *
from init_fetch_retweets_tweet_activity import *
from init_fetch_quotes_tweet_activity import *
from update_fetch_likes_tweet_activity import *
from update_fetch_retweets_tweet_activity import *
from update_fetch_quotes_tweet_activity import *

class GacTweeteroo(object):
    def __init__(self):
        self.CID_LOG = 998218831036170301 # roo tech, tweeteroo gac demo room
        self.CID_MSG = 998218831036170301
        self.GUILDS = [993961827799158925] # roo tech guild id

        self.CMD_PREFIX = "rtt"
        self.CMD_DESCRIPTION = "Tweeteroo commands"
        self.tab = 4*" "

        query  = "("
        query += "gac"
        query += " OR lfgac"
        query += " OR lfgaccc"
        query += " OR gaming ape club"
        query += " OR gacattack"
        query += " OR gacgang"
        query += " OR gacsales"
        query += " OR gacfollowgac"
        self.keywords_help = query + ""
        self.keywords_query = query.replace(" ", "%20")

        self.init_embeds()
    # end __init__

    def init_embeds(self):
        self.URL = "https://cdn.discordapp.com/attachments/965394881067515914/980589091718586428/4431.png"

        TITLE = "__Help Menu__"
        DESCRIPTION = "Hi! I'm Twitteroo, developed by @TheLunaLabs © 2022"
        DESCRIPTION += "\nBelow are my commands, which are case insensitive:"

        embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION)
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
        embedDpy.add_field(name="**__!rttverify <url>,<twitter username>__**", value="Verify if we've processed your interaction", inline=False)
        embedInt.add_field(name="**__!rttverify <url>,<twitter username>__**", value="Verify if we've processed your interaction", inline=False)
        embedDpy.add_field(name="**__!rttstats <twitter username>__**", value="Display user's points, likes, etc.", inline=False)
        embedInt.add_field(name="**__!rttstats <twitter username>__**", value="Display user's points, likes, etc.", inline=False)
        embedDpy.add_field(name="**__!rttrank <twitter username>__**", value="Display user's points, likes, etc.", inline=False)
        embedInt.add_field(name="**__!rttrank <twitter username>__**", value="Display user's rank (all data). To see options for granular ranks, run command: **__!rtthelplb__**", inline=False)
        self.helpEmbedDpy = embedDpy
        self.helpEmbedInt = embedInt

        LB_HELP_TITLE = "__Leaderboard Help Menu__"
        LB_HELP_DESCRIPTION = "Hi! I'm Twitteroo, developed by @TheLunaLabs © 2022"
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

        TITLE = "__Keywords__"
        DESCRIPTION = "Hi! These are the keywords I use to scrape for tweets:\n\n"
        for keyword in self.keywords_help.split("OR"):
            keyword = keyword.replace(")","")
            keyword = keyword.replace("("," ")
            DESCRIPTION += 2*self.tab + keyword + "\n"
        # end for

        embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)#, color=discord.Color.blue())
        embedDpy.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                        icon_url=self.URL)
        embedInt.set_footer(text = "Built for Roo Troop, Powered by TheLunaLabs",
                        icon_url=self.URL)
        self.keyEmbedDpy = embedDpy
        self.keyEmbedInt = embedInt
    # end init_embeds

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
                channel = await get.get(intBot, interactions.Channel, channel_id=self.CID_LOG)
                await channel.send("I AM ALIVE! MWAHAHAHA")
                break
            # end for
        # end on_ready

        @intBot.command(
      name=self.CMD_PREFIX,
      description=self.CMD_DESCRIPTION,
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
                        msg2 = "```>>> Danggg. Looks like that twitter username isn't linked in my database. Unpack this rage against the machine by slapping a seal ;)```"
                        await ctx.send(msg2, ephemeral=True)
                        return
                    # end if
                    username = self.user_dict["discordId_to_username"][discord_id]

                elif username != None:
                    username = username.lower()
                    username = username.replace("@","")
                    username = username.replace(" ","")

                else:
                    msg2 = ">>> Something went very wrong fetching the username. Error Coe 273"
                    await ctx.send(msg2, ephemeral=True)
                    return
                # end if/elif/else

                msg2 = ">>> ```Username: " + username + "\n"
                msg2 += "--\n"

                print("281: ", msg2)
                self.embed_user_stats(ctx, username)

            elif sub_command in ["verify"]:
                tweet_url = url.lower()
                tweet_url = tweet_url.replace(",", "").replace(" ", "")
                if "?" in tweet_url:
                    tweet_url = tweet_url.split("?")[0]
                # end if

                if ("https://twitter.com/" not in tweet_url) and ("https://mobile.twitter.com/") not in tweet_url:
                    msg2  = ">>> sorry, I couldn't parse that. I'm loooking for something like\n"
                    msg2 += tab + "*!rttverify https://twitter.com/RooTroopNFT/status/1499858580568109058, TheLunaLabs*"
                    await ctx.send(msg2, ephemeral=True)
                    return
                # end if
          
                if username == None:
                    discord_id = str(ctx.author.id)
                    if discord_id not in self.user_dict["discordId_to_username"]:
                        msg2 = "```>>> Danggg. Looks like that twitter username isn't linked in my database. Unpack this rage against the machine by slapping a seal ;)```"
                        await ctx.send(msg2, ephemeral=True)
                        return
                    # end if
                    username = self.user_dict["discordId_to_username"][discord_id]

                elif username != None:
                    username = username.lower()
                    username = username.replace("@","")
                    username = username.replace(" ","")
                # end if/elif
                msg2 = ">>> okay! will verify if we processed that weet for `" + username + "` yet or not"
                await ctx.send(msg2, ephemeral=True)
                self.verify_processed_tweet(ctx, tweet_url, username)

            elif sub_command in ["leaderboard", "lb"]:
                if method == None:
                    method = "Points"
                # end if
                method = method.lower()
                method = method.replace(" ","")
                if "like" in method:
                    method = "Likes"
                elif "rt" in method[3:] or "retweet" in method:
                    method = "Retweets"
                elif "repl" in method:
                    method = "Replies"
                elif "keyword" in method:
                    method = "Custom_" + method.split("keyword")[1].lower()
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

                if "start:" in msg and "end:" in msg:
                    print("custom time range!")
                    time_str = "user defined"
                    start_time = msg.split("start:")[1]
                    start_time = start_time.replace(",", " ").replace(" ", "")
                    start_time = start_time.split(", end:")[0]
                    end_time = msg.split("end:")[1]
                    end_time = end_time.replace(" ", "")

                    status, start_time = self.convert_time(start_time)
                    status2, end_time   = self.convert_time(end_time)

                    if status == False or status2 == False:

                # end if

              #print("end_time: ", end_time)
              status,end_time   = self.convert_time(end_time)
              if status == False:
                await ctx.send(end_time, ephemeral=True)
                return
              # end if

            except Exception as err:
              print("3104 err: ", err)
              print("3105 err args: ", err.args[:])
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

          #print("msg: ", msg)
          if "rtt lbAll".lower() in msg or "rttlbAll".lower() in msg or "ALLDATA".lower() in msg:
            #print("in lbAll")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time,
                   end_time=end_time, method=method, sharded=False, time_str=time_str)
          else:
            #print("in reg lb")
            msg2 = await self.fetch_user_leaderboard(start_time=start_time, 
                   end_time=end_time, method=method, sharded=True, time_str=time_str)
          # end if/elf
          #print("discord bot hi here's the " + method + " leaderboard")
          #print(msg2)
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
          elif "keyword" in method:
            method = "Custom_" + method.split("keyword")[1].lower()
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
          #print("msg: ", msg)
          #print("start: in msg: ", "start:" in msg)
          #print(",end: in msg: ", ",end:" in msg)
          #print("msg: ", msg)
          if "start:" in msg and "end:" in msg:
            print("custom time range!")
            time_str = "user defined"
            try:
              start_time = msg.split("start:")[1].split(", end:")[0]
              end_time = msg.split("end:")[1]

              #print("start_time: ", start_time)
              status,start_time = self.convert_time(start_time)
              if status == False:
                await ctx.send(start_time, ephemeral=True)
                return
              # end if

              #print("end_time: ", end_time)
              status,end_time   = self.convert_time(end_time)
              if status == False:
                await ctx.send(end_time, ephemeral=True)
                return
              # end if

            except Exception as err:
              print("3315 err: ", err)
              print("3316 err args: ", err.args[:])
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
            #print("slash rank all un: ", username)
            msg2 = await self.fetch_rank(username, start_time=start_time,
                   end_time=end_time, method=method, sharded=False, time_str=time_str)
          else:
            print("in reg lb")
            #print("slash rank reg un: ", username)
            msg2 = await self.fetch_rank(username, start_time=start_time, 
                   end_time=end_time, method=method, sharded=True, time_str=time_str)
          # end if/elf
          print("discord bot hi here's the " + method + " rank")
          #print(msg2)
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
        #print("message: ", message)
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
          #print("hi")
          self.linked_usernames.append(str(tun))
          self.linked_userIds.append(str(twid))
          self.linked_discordIds.append(str(did))

          self.user_dict["userId_to_username"][str(twid)] = str(tun)
          print("3496 tun: ", str(tun))
          self.user_dict["username_to_userId"][str(tun)] = str(twid)
          self.user_dict["discordId_to_username"][str(did)] = str(tun)
          self.safe_save(self.fname_user_info, self.user_dict)
          #print("hi2")
        # end if
      # end if
      if not self.dev_mode:
        await self.continuously_scrape()
      # end if
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
            try:
              self.pages[str(message.id)]["pnum"] = self.pages[str(message.id)]["pnum"]+1
            except Exception as err:
              print("3568 page deleted probly")
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


        @client.event
        async def on_ready():
            self.channel_log = client.get_channel(self.CID_LOG)
            self.channel_msg = client.get_channel(self.CID_MSG)
    # end discord_bot
# end GacTweeteroo

if __name__ == "__main__":
    gt = GacTweeteroo()
    gt.discord_bot()
# end if