import os
import discord
import asyncio
from travel import TravelBot

class TravelDiscordBot(TravelBot):
    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_ready():
            while True:
                old_fares = []

                if self.fares != {}:
                    old_fares += self.fares["texts"]
                # end if

                self.get_html()
                self.get_fares("err")
                self.get_fares("deals")

                for ii,fare in enumerate(self.fares["texts"]):
                    if fare in old_fares:
                        continue
                    # end if
                    title = fare
                    description = ", ".join(self.fares["hashtags"][ii])

                    embed = discord.Embed(title=title, description=description,
                        color=discord.Color.blue(), url=self.fares["urls"][ii])
                    embed.set_thumbnail(url=self.fares["images"][ii])
                    embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                        icon_url=self.icon_url)
                    for hashtag in self.fares["hashtags"][ii]:
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
                        channel = client.get_channel(did)
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