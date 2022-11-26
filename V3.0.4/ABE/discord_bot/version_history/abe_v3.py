## invite link: https://discord.com/api/oauth2/authorize?client_id=1014177171008409660&permissions=19456&scope=bot
## ^That's for scopes = bot; permissions = 1) read messages/view channels, 2) send messages, 3) embed links

import os
import time
import urllib
import requests

import asyncio
import discord
from pymongo import MongoClient

class AbeBot(object):
    def __init__(self):
        self.LS = 3600.0

        self.FOOTER = "Please visit AlwaysBeEarly.AI for full terms and conditions. Not Financial Advice."
        self.ICON_URL = "https://cdn.discordapp.com/icons/952352992626114622/39bd07c3ccd0d708f20e47b3dc7cb140.webp?size=160"

        self.LOG_CID = 932056137518444594 # TTB bot-commands

        self.embed_rgb = [21, 77, 255]# main color EI Labs brandKit v2

        self.init_gcp()
        self.init_mongodb()
    # end __init__

    def init_gcp(self):
        psk = os.environ["abe1"] + os.environ["abe2"]
        self.gcp_url = "https://us-central1-alphaintel.cloudfunctions.net/abe_get_data"
        self.gcp_url = "https://us-central1-alphaintel.cloudfunctions.net/abe_get_premint"
        self.gcp = {"psk": psk, "key": "Y"}
    # end init_gcp

    async def query_gcp(self):
        return requests.post(self.gcp_url, json=self.gcp)
    # end query_gcp

    async def build_embed(self, payload):
        title = "@" + payload["handle"]
        description = "\u200b"
        url = "https://twitter.com/" + payload["handle"]

        embed = discord.Embed(title=title, description=description,
            color=discord.Color.from_rgb(self.embed_rgb[0], self.embed_rgb[1], self.embed_rgb[2]), url=url)
        embed.set_thumbnail(url=payload["profile_image_url"])
        embed.set_footer(text = self.FOOTER, icon_url=self.ICON_URL)        

        embed.add_field(name="**Description**",           value=payload["description"],  inline=False)
        embed.add_field(name="**Influential Followers**", value=payload["influential_followers"], inline=False)
        embed.add_field(name="**Rating**",                value=payload["rating"],       inline=False)
        embed.add_field(name="**Followers**",             value=payload["followers"],    inline=False)
        embed.add_field(name="**Created Date**",          value=payload["created_date"], inline=False)
        embed.add_field(name="**Found Date**",            value=payload["created_date"], inline=False)
        return embed
    # end build_embed

    def init_mongodb(self):
        user = urllib.parse.quote("pymongo-user")
        word = urllib.parse.quote(os.environ["atlP"])

        connection_string = "mongodb+srv://" + user + ":" + word \
                          + "@cluster0.pqg6c02.mongodb.net/" \
                          + "?retryWrites=true&w=majority"

        client = MongoClient(connection_string)
        self.mongoDB = client.get_database("abe")

    def get_guild_data(self):
        cursor = self.mongoDB["abe-guilds-data"].find({})
        abe_guilds_data_db = []
        for document in cursor:
            abe_guilds_data_db.append(document)
        return abe_guilds_data_db

    async def leave_unsubscribed_guilds(self, client):
        abe_guilds_data_db = self.get_guild_data()

        for guild in client.guilds:
            print("guild.name; ", guild.name)
            subscribed = False

            for ii,abe_guild in enumerate(abe_guilds_data_db):
                if "guild_id" in abe_guild:
                    if int(guild.id) == int(abe_guild["guild_id"]):
                        if "subscribed" in abe_guild and abe_guild["subscribed"] == True:
                            subscribed = True
                            break
            # end for

            if not subscribed:
                await guild.leave()
                print("left guild")
            else:
                if "in" not in abe_guild or abe_guild["in"] == False:
                    self.mongoDB["abe-guilds-data"].find_one_and_update({
                        "guild_id":str(int(guild.id))},
                        {"$set": {"in": True}}
                    )
                    print("set 'in' True!")
                # end if

                channels = []
                for channel in guild.channels:
                    channels.append(channel.name)
                
                if "channels" not in abe_guild or abe_guild["channels"] != channels:
                    self.mongoDB["abe-guilds-data"].find_one_and_update({
                        "guild_id":str(int(guild.id))},
                        {"$set": {"channels": channels}}
                    )
                    print("set channels!")

                print("staying in guild")
            # end if/else
        # end for
    # end leave_unsubscribed_guilds

    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_ready():
            print("on_ready")
            wcnt = 0
            last = time.time()

            for guild in client.guilds:
                print("guild.name: ", guild.name)
                print("guild.channels: ", guild.channels)
                for channel in guild.channels:
                    print("channel.id, channel.name: ", channel.id, channel.name)

            await self.leave_unsubscribed_guilds(client)
            sys.exit()

            channel_log = client.get_channel(self.LOG_CID)
            await channel_log.send("hi")
            sys.exit()
            while True:
                wcnt += 1
                print("wcnt: ", wcnt)

                await self.leave_unsubscribed_guilds(client)
                result = await self.query_gcp()
                print("result.text: ", result.text)
                print("result.json: ", result.json())
                with open("premint_test.txt", "w") as fid:
                    fid.write(str(result.text))
                # end with
                sys.exit()

                print("query_gcp done!")
                result = {'profile_image_url': 'https://pbs.twimg.com/profile_images/1551744305961701376/fKV6-Mne_400x400.jpg', 
                          'handle': 'W3NationNFT', 
                          'description': 'The Birth Of A New Nation🔫 | 7,777', 'influential_followers': 'WhySo4488, NFTNate_, NFTBuffet, Pants_shh, ', 
                          'rating': 'A', 
                          'followers': 10133, 
                          'created_date': '2022-07-18', 
                          'found_date': '2022-08-25 13:49PT'}

                #if result.status_code == 200:
                    #embed = await self.build_embed(result.json())
                if True:
                    embed = await self.build_embed(result)
                    await channel_log.send(embed=embed)
                # end if
                await asyncio.sleep(self.LS)
            # end while
        # end on_ready

        client.run(os.environ.get("abeBotPass"))
    # end discord_bot
# end AbeDiscordBot

if __name__ == "__main__":
    abe = AbeBot()
    abe.discord_bot()
# end if
## end abe.py
