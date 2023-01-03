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
        self.client = client

        @client.event
        async def on_message(message):
            if message.channel.id != self.BOT_COMMANDS_CIDS[0]:
                return
            # end if
            if message.author.id != 855616810525917215:
                return
            else:
                pass
                #print([message.content])
                #print([message.author.id])
                #print([message.channel.id])
            if message.content.startswith("!lk update pfp="):
                img = message.content.replace("!lk update pfp=","")
                with open(img, "rb") as fid:
                    #await client.edit_profile(avatar=fid.read()) re-write/2.0
                    await client.user.edit(avatar=fid.read()) # 1.7.3
                # end with open

        @client.event
        async def on_ready():
            last_sf_update = time.time() - 7200
            last_nd_update = time.time() - 7200
            print("on_ready")

            if self.TESTING:
                test_channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
            # end if

            business_channel = client.get_channel(self.BUSINESS_CID)
            first_class_channel = client.get_channel(self.FIRST_CLASS_CID)

            wcnt = 0
            while True:
                wcnt += 1
                print("wcnt: ", wcnt)

                if time.time() - last_sf_update > 60.1:
                    last_sf_update = time.time()
                    if not self.SCOTTS:
                        self.get_html()
                        self.get_fares("err")
                        self.get_fares("deals")
                # end if

                if time.time() - last_nd_update > 3600:
                    print("now: ", datetime.datetime.now())
                    last_nd_update = time.time()
                    if not self.SCOTTS:
                        await self.get_html_nd()
                # end if

                #if time.time() - self.last_scotts_update > 24.5*3600 or 
                if self.SCOTTS and self.first_time:
                    self.first_time = False
                    print("now: ", datetime.datetime.now())
                    self.last_scotts_update = time.time()
                    print("scotts")
                    asyncio.create_task(self.get_fares_scotts())
                    await asyncio.sleep(3600*24*365)
                # end if
                if self.SCOTTS:
                    sys.exit()

                with open(self.fname_fares, "w") as fid:
                    fid.write(str(self.fares))
                # end with open

                # with open(self.fname_fares_scotts, "w") as fid:
                #     fid.write(str(self.fares_scotts))
                # # end with open

                fares = []
                hashtags = []
                urls = []
                images = []
                if self.fares != {}:
                    fares    += self.fares[   "texts"]
                    hashtags += self.fares["hashtags"]
                    urls     += self.fares[    "urls"]
                    images   += self.fares[  "images"]

                # if self.fares_scotts != {} and \
                #         len(self.fares_scotts["texts"]) == \
                #         len(self.fares_scotts["hashtags"]) == \
                #         len(self.fares_scotts["urls"]) == \
                #         len(self.fares_scotts["images"]):
                #     print("adding scotts fares!")

                    # fares    += self.fares_scotts["texts"]
                    # hashtags += self.fares_scotts["hashtags"]
                    # urls     += self.fares_scotts["urls"]
                    # images   += self.fares_scotts["images"]

                    # print("fares inc. scotts: ", fares)
                # end if

                roles_mentioned = []
                for ii,fare in enumerate(fares):
                    if fare in self.old_fares:
                        #print("fare was in old_fares")
                        #print("ii: ", ii)
                        #print("fare: ", fare)
                        #print("old_fares: ", self.old_fares)
                        #input(">>")
                        continue
                    # end if
                    title = fare
                    description = ""

                    ports = []; roles = []; channels = []
                    for jj,hashtag in enumerate(hashtags[ii]):
                        description += hashtag + ", "
                        if "_from" in hashtag:
                            if "usa" in hashtag:
                                print("usa in hashtag")
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
                            color=discord.Color.blue(), url=urls[ii])
                        embed.set_thumbnail(url=images[ii])
                        embed.set_footer(text = "Built for Solana Vegas Tour, Powered by @TheLunaLabs",
                          icon_url=self.icon_url)
                        try:
                            print("going to get LV channel, now: ", datetime.datetime.now())
                            channel = client.get_channel(self.CID_VEGAS)
                            print("got LV channel, now: ", datetime.datetime.now())
                            if not self.TESTING:
                                await channel.send(embed=embed)
                            print("LV sent embed, now: ", datetime.datetime.now())
                        except Exception as err:
                            print("error LV, now: ", datetime.datetime.now())
                            print("111 tdb err: ", err)
                            print("112 tdb err: ", err.args[:])
                        # end try/except
                    # end if

                    embed = discord.Embed(title=title, description=description,
                        color=discord.Color.blue(), url=urls[ii])
                    embed.set_thumbnail(url=images[ii])
                    embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                        icon_url=self.icon_url)
                    #embed.add_field(name="Hey @Authenticated", value="\u200b")

                    #channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
                    for jj,role in enumerate(roles):
                        channel = channels[jj]
                        if role not in roles_mentioned:
                            try:
                                if not self.TESTING:
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
                                print("hashtags: ", hashtags[ii])
                            # end try/except
                            roles_mentioned.append(role)
                        # end if
                        try:
                            if not self.TESTING:
                                await channel.send(embed=embed)
                                
                            else:
                                await test_channel.send(embed=embed)
                            
                            self.old_fares.append(fare)

                        except Exception as err:
                            print("129 err: ", err)
                            print("130 err_args: ", err.args[:])
                            print("channel: ", channel)
                        # end try/except

                        if "business" in title.lower():
                            await business_channel.send(embed=embed)
                        
                        if "first class" in title.lower():
                            await first_class_channel.send(embed=embed)
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
