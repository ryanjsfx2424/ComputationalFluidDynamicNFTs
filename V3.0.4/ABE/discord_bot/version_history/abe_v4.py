## invite link: https://discord.com/api/oauth2/authorize?client_id=1014177171008409660&permissions=19456&scope=bot
## ^That's for scopes = bot; permissions = 1) read messages/view channels, 2) send messages, 3) embed links

## invite link: https://discord.com/api/oauth2/authorize?client_id=1014177171008409660&permissions=183296&scope=bot
## ^That's for scopes(1) = bot; permissions (5) = 1) read messages/view channels, 2) send messages, 3) embed links, 4) attach files, 5) mention everyone

## to do
# 1) switch to HTTPClient (I guess would need to switch to interactions for this...will defer)
# 2) have bot say 'hi' in all channels it's subscribed to 
#    (if this errors, I need to give the bot more perms on-invite; maybe manage channels?)
# 3) generate regular data embed on-the-fly
# 4) generate premint embed-on-the-fly
# 5) mention roles it's supposed to mention (think this has to happen outside the embeds)
## need to store result.json's to make sure I skip if payload is the same

import os
import time
import json
import urllib
import requests
import asyncio
import discord
import datetime
import numpy as np
from pymongo import MongoClient

class AbeBot(object):
    def __init__(self):
        self.LS = 3600.0

        self.FOOTER = "Please visit AlwaysBeEarly.AI for full terms and conditions. Not Financial Advice."
        self.ICON_URL = "https://cdn.discordapp.com/icons/952352992626114622/39bd07c3ccd0d708f20e47b3dc7cb140.webp?size=160"

        self.LOG_CID = 932056137518444594 # TTB bot-commands

        self.embed_rgb = [21, 77, 255]# main color EI Labs brandKit v2

        os.system("mkdir -p data_big")

        self.init_gcp()
        self.init_mongodb()
    # end __init__

    def init_gcp(self):
        psk = os.environ["abe1"] + os.environ["abe2"]
        self.gcp_url = "https://us-central1-alphaintel.cloudfunctions.net/abe_get_data"
        self.gcp_url_premint = "https://us-central1-alphaintel.cloudfunctions.net/abe_get_premint"
        self.gcp = {"psk": psk, "key": "Y"}
    # end init_gcp

    async def query_gcp(self, premint=False):
        if premint:
            return requests.post(self.gcp_url_premint, json=self.gcp)
        else:
            return requests.post(self.gcp_url, json=self.gcp)
    # end query_gcp

    async def build_embed(self, payload):
        title = "Twitter: @" + payload["handle"]
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

    def update_in(self, guild_id, abe_guild):
        if "in" not in abe_guild or abe_guild["in"] == False:
            self.mongoDB["abe-guilds-data"].find_one_and_update({
                "guild_id":str(guild_id)},
                {"$set": {"in": True}}
            )
            print("set 'in' True!")
        # end if

    def update_channels(self, guild, abe_guild):
        channels = []
        for channel in guild.channels:
            if channel.category == None:
                continue

            ## filter channels for perms
            perms = channel.permissions_for(channel.guild.me)
            if perms.view_channel and perms.send_messages and perms.embed_links and perms.attach_files and perms.mention_everyone:
                channels.append(channel.name)
            # end if
        # end for
        channels = list(np.sort(channels))

        if "channels" not in abe_guild or abe_guild["channels"] != channels:
            self.mongoDB["abe-guilds-data"].find_one_and_update({
                "guild_id":str(int(guild.id))},
                {"$set": {"channels": channels}}
            )
            print("set channels!")
        # end if

    def update_roles(self, guild, abe_guild):
        roles = []
        for role in guild.roles:
            roles.append(role.name)
        # end for

        if "roles" not in abe_guild or abe_guild["roles"] != roles:
            self.mongoDB["abe-guilds-data"].find_one_and_update({
                "guild_id":str(int(guild.id))},
                {"$set": {"roles": roles}}
            )
            print("set roles!")
        # end if

    async def update_guilds_data(self, guilds):
        abe_guilds_data_db = self.get_guild_data()

        for guild in guilds:
            print("guild.name; ", guild.name)
            subscribed = False
            for ii,abe_guild in enumerate(abe_guilds_data_db):
                if "guild_id" in abe_guild and int(guild.id) == int(abe_guild["guild_id"]):
                    subscribed = True
                    break

            if not subscribed:
                await guild.leave()
                print("left guild")
                continue
            # end if

            self.update_in(      guild_id, abe_guild)
            self.update_channels(guild,    abe_guild)
            self.update_roles(   guild,    abe_guild)

            print("staying in guild")
        # end for
    # end leave_unsubscribed_guilds

    def discord_bot(self):
        intents = discord.Intents.default()
        intents.guilds = True
        client = discord.Client(intents=intents)
        print("client.user: ", client.user)

        @client.event
        async def on_guild_join(guild):
            print("guild joined!")
            await self.update_guilds_data([guild])

        @client.event
        async def on_ready():
            print("dir client: ", dir(client))
            print("\n\ndir client.user: ", dir(client.user))
            print("client.user: ", client.user)
            print("on_ready")
            wcnt = 0
            last = time.time()

            while True:
                wcnt += 1
                print("wcnt: ", wcnt)
                if wcnt > 1:
                    print("sleeping a minute")
                    await asyncio.sleep(60.0)

                #'''
                now = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
                print("now: ", now)

                await self.update_guilds_data(client.guilds)
                continue


                result = await self.query_gcp()
                print("result.text: ", result.text)
                with open("data_big/" + now + ".txt", "w") as fid:
                   fid.write(str(result.text))
                #end with
                print("result.json: ", result.json())
                result = result.json()
                #'''
                
                #with open("test.txt", "r") as fid:
                #    result = json.load(fid)
                
                ## note, A rating -> abe-alpha-plus
                ## B rating -> abe-alpha
                ## P -> aptos
                ## S -> Solana
                ## Daily -> Daily
                ## D: daos
                ## T: tools

                print("query_gcp done!")
                #result = {'profile_image_url': 'https://pbs.twimg.com/profile_images/1551744305961701376/fKV6-Mne_400x400.jpg', 
                #          'handle': 'W3NationNFT', 
                #          'description': 'The Birth Of A New Nation🔫 | 7,777', 'influential_followers': 'WhySo4488, NFTNate_, NFTBuffet, Pants_shh, ', 
                #          'rating': 'A', 
                #          'followers': 10133, 
                #          'created_date': '2022-07-18', 
                #          'found_date': '2022-08-25 13:49PT'}

                #if result.status_code == 200:
                    #embed = await self.build_embed(result.json())
                if True:
                    embed = await self.build_embed(result)
                    await channel_log.send(embed=embed)
                    print("sent embed!")
                    sys.exit()
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
