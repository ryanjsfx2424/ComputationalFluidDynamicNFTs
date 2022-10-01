import os
import sys
import time
import discord
import asyncio
import datetime
from travel import TravelBot

class TravelDiscordBot(TravelBot):
    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_message(message):
            if message.channel.id != self.BOT_COMMANDS_CIDS[0]:
                return
            # end if
            if message.author.id != 855616810525917215:
                return
            else:
                print([message.content])
                print([message.author.id])
                print([message.channel.id])
            if message.content.startswith("!lk update pfp="):
                img = message.content.replace("!lk update pfp=","")
                with open(img, "rb") as fid:
                    #await client.edit_profile(avatar=fid.read()) re-write/2.0
                    await client.user.edit(avatar=fid.read()) # 1.7.3
                # end with open

        @client.event
        async def on_ready():
            last_nd_update = time.time() - 7200
            print("on_ready")

            #channel = client.get_channel(self.CID_VEGAS)
            #await channel.send("test")
            #print("sent test")

            wcnt = 0
            while True:
                wcnt += 1
                print("wcnt: ", wcnt)

                old_fares = []
                if self.fares != {}:
                    old_fares += self.fares["texts"]
                # end if

                self.get_html()
                self.get_fares("err")
                self.get_fares("deals")

                if time.time() - last_nd_update > 3600:
                    print(datetime.datetime.now())
                    last_nd_update = time.time()
                    self.get_html_nd()
                # end if

                with open(self.fname_fares, "w") as fid:
                    fid.write(str(self.fares))
                # end with open

                roles_mentioned = []
                for ii,fare in enumerate(self.fares["texts"]):
                    if fare in old_fares:
                        continue
                    # end if
                    title = fare
                    description = ""

                    ports = []; roles = []; channels = []
                    for jj,hashtag in enumerate(self.fares["hashtags"][ii]):
                        description += hashtag + ", "
                        if "_from" in hashtag:
                            if "usa" in hashtag:
                                continue
                            # end if
                            hashtag = hashtag.replace("_from","")
                            if "#mena" in hashtag:
                              hashtag = "#me-and-north-africa"
                            # end if
                            roles.append(self.roles[hashtag[1:]])
                            ports.append(jj)
                            if   hashtag[1:] in self.CIDS:
                                did = self.CIDS[hashtag[1:]]
                            elif hashtag[1:] in self.TIDS_USA:
                                did = self.TIDS_USA[hashtag[1:]]
                            else:
                                print("34 err hashtag not in CIDS, TIDS_USA")
                                print("hashtag: ", hashtag)
                                print("hashtag[1:]: ", hashtag[1:])
                                print("CIDS keys: ", self.CIDS.keys())
                                print("TIDS_USA keys: ", self.TIDS_USA.keys())
                                raise
                            # end if/elif
                            channels.append(client.get_channel(did))
                        # end if
                        if "error-fares" in hashtag:
                            ports.append(jj)
                            roles.append(self.roles["error-fares"])
                            channels.append(client.get_channel(self.CIDS["error-fares"]))
                        # end if
                    # end for
                    description = description[:-2]
                    description = description.replace("_from","")
                    #description = ", ".join(self.fares["hashtags"][ii])

                    if "to Las Vegas" in title:
                        print("Las vegas in title, now: ", datetime.datetime.now())

                        embed = discord.Embed(title=title, description=title,
                            color=discord.Color.blue(), url=self.fares["urls"][ii])
                        embed.set_thumbnail(url=self.fares["images"][ii])
                        embed.set_footer(text = "Built for Solana Vegas Tour, Powered by @TheLunaLabs",
                          icon_url=self.icon_url)
                        try:
                            print("going to get LV channel, now: ", datetime.datetime.now())
                            channel = client.get_channel(self.CID_VEGAS)
                            print("got LV channel, now: ", datetime.datetime.now())
                            await channel.send(embed=embed)
                            print("LV sent embed, now: ", datetime.datetime.now())
                        except Exception as err:
                            print("error LV, now: ", datetime.datetime.now())
                            print("111 tdb err: ", err)
                            print("112 tdb err: ", err.args[:])
                        # end try/except
                    # end if

                    embed = discord.Embed(title=title, description=description,
                        color=discord.Color.blue(), url=self.fares["urls"][ii])
                    embed.set_thumbnail(url=self.fares["images"][ii])
                    embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                        icon_url=self.icon_url)
                    #embed.add_field(name="Hey @Authenticated", value="\u200b")

                    #channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
                    for jj,role in enumerate(roles):
                        channel = channels[jj]
                        if role not in roles_mentioned:
                            try:
                                await channel.send("Hey <@&" + role + ">")
                            except Exception as err:
                                print("112 err: ", err)
                                print("113 err_args: ", err.args[:])
                                print("channel: ", channel)
                                print("jj: ", jj)
                                print("role: ", role)
                                print("channels: ", channels)
                                print("title: ", title)
                                print("description: ", description)
                                print("hashtags: ", self.fares["hashtags"][ii])
                            # end try/except
                            roles_mentioned.append(role)
                        # end if
                        try:
                            await channel.send(embed=embed)
                        except Exception as err:
                            print("129 err: ", err)
                            print("130 err_args: ", err.args[:])
                            print("channel: ", channel)
                        # end try/except
                    # end for
                # end for
                print("119 tdb going to sleep for " + str(self.sleep_time)+"s")
                await asyncio.sleep(self.sleep_time)
            # end while
        # end on_ready
        client.run(os.environ.get("lkBotPass"))
    # end discord_bot
# end TravelDiscordBot

if __name__ == "__main__":
    tdb = TravelDiscordBot()
    tdb.discord_bot()
# end if
## end travel_discord_bot.py
