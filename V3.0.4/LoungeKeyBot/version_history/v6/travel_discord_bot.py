import os
import discord
import asyncio
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
            print("on_ready")
            while True:
                old_fares = []

                if self.fares != {}:
                    old_fares += self.fares["texts"]
                # end if

                self.get_html()
                self.get_fares("err")
                self.get_fares("deals")

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
                            await channel.send("Hey <@&" + role + ">")
                            roles_mentioned.append(role)
                        # end if
                        await channel.send(embed=embed)
                    # end for
                # end for
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
