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
import dateutil.parser as dt
import numpy as np
from pymongo import MongoClient

class AbeBot(object):
    def __init__(self):
        self.FOOTER = "ABE A.I. powered by EILabs.AI Visit our website for more. Not financial advice."
        self.ICON_URL = "https://cdn.discordapp.com/icons/952352992626114622/39bd07c3ccd0d708f20e47b3dc7cb140.webp?size=160"

        self.LOG_CID = 932056137518444594 # TTB bot-commands

        self.embed_rgb = [21, 77, 255]# main color EI Labs brandKit v2

        os.system("mkdir -p data_big")

        self.rating_map = {"A": "alpha-plus", "B": "alpha", "P": "aptos", "S": "solana", "D": "daos", "T": "nft-tools", "DailyEth": "daily", "Highlight":"highlight", "Artist":"artist", "C": "might-be-something", "VC": "vc-firms", "Daily": "daily", "V": "vc-firms"}

        ## note, toTheMoons paid for 1 month, standard
        ## note, test paid for 1 month, standard
        ## this is in seconds
        self.trial_map = {
                            "952352992626114622": 1e50, # ABE
                            "922678240798187550": 5 # sketches by gabo
                        }
        self.premium_ratings = ["aptos", "artist", "daos", "nft-tools", "premint", "vc-firms"]

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

        ## if not an expected rating, skip.
        #if payload["rating"].lower() == "highlight":
        #    return False

        embed = discord.Embed(title=title, description=description,
            color=discord.Color.from_rgb(self.embed_rgb[0], self.embed_rgb[1], self.embed_rgb[2]), url=url)
        embed.set_thumbnail(url=payload["profile_image_url"])
        embed.set_footer(text = self.FOOTER, icon_url=self.ICON_URL)

        description = payload["description"]
        if description == "":
            description = "\u200b"
        if len(description) > 1024:
            wcnt = 0
            while len(description) > 0:
                wcnt += 1
                chunk = description[:1024]
                if "\n" in chunk:
                    chunk2 = "\n".join(chunk.split("\n")[:-1])
                description = description[len(chunk2):]
                if "\n" not in chunk:
                  chunk2 += "-"
                chunk = chunk2
                embed.add_field(name="**Description (" + str(wcnt) + ")**", value=chunk, inline=False)
        else:
            embed.add_field(name="**Description**",           value=payload["description"],  inline=False)
        embed.add_field(name="**Influential Followers**", value=payload["influential_followers"], inline=False)
        embed.add_field(name="**Rating**",                value=payload["rating"],       inline=False)
        embed.add_field(name="**Followers**",             value=payload["followers"],    inline=False)
        embed.add_field(name="**Created Date**",          value=payload["created_date"], inline=False)
        embed.add_field(name="**Found Date**",            value=payload["found_date"], inline=False)
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

    def update_in(self, guild, abe_guild):
        if "in" not in abe_guild or abe_guild["in"] == False:
            self.mongoDB["abe-guilds-data"].find_one_and_update({
                "guild_id":str(int(guild.id))},
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

    async def get_abe_guild(self, abe_guilds_data_db, guild):
        sub_inds  = []
        sub_dates = []
        subscribed = False

        for ii,abe_guild in enumerate(abe_guilds_data_db):
            if "guild_id" in abe_guild and int(guild.id) == int(abe_guild["guild_id"]):
                subscribed = True
                sub_inds.append(ii)
                sub_dates.append(abe_guild["date"])

        if not subscribed:
            await guild.leave()
            print("left guild")
            return None
        # end if

        sub_inds = np.array(sub_inds)
        if len(sub_inds) == 1:
            abe_guild = abe_guilds_data_db[sub_inds[0]]
        else:
            inds = np.argsort(sub_dates)
            ind  = int(np.array(sub_inds)[inds][-1])
            abe_guild = abe_guilds_data_db[ind]
        # end if/else
        return abe_guild
    # def get_abe_guild

    async def update_guilds_data(self, guilds):
        abe_guilds_data_db = self.get_guild_data()

        for guild in guilds:
            print("guild.name; ", guild.name)

            abe_guild = await self.get_abe_guild(abe_guilds_data_db, guild)
            print("got abe_guild")
            #print("\n\nabe_guild: ", abe_guild)
            
            if abe_guild == None:
                continue
            # end if

            guild_id = int(guild.id)
            self.update_in(      guild, abe_guild)
            self.update_channels(guild, abe_guild)
            self.update_roles(   guild, abe_guild)
            print("done with update in, channels, roles")
        # end for
    # end update_guilds_data

    async def send_payload(self, payload, rating, guilds):
        print("rating: ", rating)
        abe_guilds_data_db = self.get_guild_data()

        for guild in guilds:
            print("guild.name in send_payload: ", guild.name)

            abe_guild = await self.get_abe_guild(abe_guilds_data_db, guild)
            print("got abe_guild (send_payload")
            #print("\n\nabe_guild: ", abe_guild)
            
            if abe_guild == None:
                continue
            # end if

            if "subscribed_channel_feed_map" not in abe_guild:
                continue

            if rating not in abe_guild["subscribed_channel_feed_map"]:
                continue
            
            channel_name = abe_guild["subscribed_channel_feed_map"][rating]

            if abe_guild["num_months"] == 0:
                if abe_guild["guild_id"] not in self.trial_map:
                    print("trial but not in trial map? Fatal")
                    raise
                
                duration = self.trial_map[abe_guild["guild_id"]]
            else:
                duration = abe_guild["num_months"]*30*24*3600
            
            start = abe_guild["date"]
            start = start.split("(")[0]
            start = dt.parse(start)
            start = time.mktime(start.timetuple())

            premium_rating = rating in self.premium_ratings
            has_premium = abe_guild["name"] == "premium"

            role_to_ping = ""
            rold_id = None
            if "subscribed_role_feed_map" in abe_guild and rating in abe_guild["subscribed_role_feed_map"]:
                role_to_ping = abe_guild["subscribed_role_feed_map"][rating]
                for role in guild.roles:
                    if role.name == role_to_ping:
                        role_id = str(int(role.id))
            # end if
            print("role_id: ", role_id)
            print("channel_name: ", channel_name)

            if rating != "premint":
                embed = await self.build_embed(payload)

            sent = False
            for channel in guild.channels:
                if channel.category == None:
                    continue

                if channel.name != channel_name:
                    continue

                #'''
                if time.time() - (start+duration) > 0:
                    try:
                        await channel.send("Uh oh! We had new alpha to send but your subscription expired. \nDon't miss out! Renew your subscription today: \nhttps://www.alwaysbeearly.io")
                    except Exception as err:
                        print("272 err: ", err)
                        print("272 err.args: ", err.args[:])
                    sent = True
                    break

                if premium_rating and has_premium == False:
                    try:
                        await channel.send("Uh oh! We had premium alpha to send but you don't have a premium subscription. \nDon't miss out! Upgrade your subscription today: \nhttps://www.alwaysbeearly.io")
                    except Exception as err:
                        print("281 err: ", err)
                        print("282 err.args: ", err.args[:])
                    sent = True
                    break
                #'''

                if rating == "premint":
                    if role_to_ping == "@everyone":
                        print("role_to_ping == @everyone")
                        try:
                            await channel.send(payload)
                            await channel.send("@everyone")
                        except Exception as err:
                            print("294 err: ", err)
                            print("295 err.args: ", err.args[:])
                    else:
                        if role_id != None:
                            print("role_id: ", role_id)
                            try:
                                await channel.send(payload + "^ <@&" + role_id + ">")
                            except Exception as err:
                                print("302 err: ", err)
                                print("303 err.args: ", err.args[:])
                        else:
                            try:
                                await channel.send(payload)
                            except Exception as err:
                                print("308 err: ", err)
                                print("309 err.args: ", err.args[:])
                        # end if/else
                    # end if/else

                    sent = True
                    break
                else:
                    print("286 payload: ", payload)
                    try:
                        await channel.send(embed=embed)
                    except Exception as err:
                        print("320 err: ", err)
                        print("321 err.args: ", err.args[:])
                    if role_to_ping == "@everyone":
                        try:
                            await channel.send("^ @everyone")
                        except Exception as err:
                            print("320 err: ", err)
                            print("321 err.args: ", err.args[:])
                    else:
                        try:
                            await channel.send("^ <@&" + role_id + ">")
                        except Exception as err:
                            print("320 err: ", err)
                            print("321 err.args: ", err.args[:])
                    # end if/else

                    sent = True
                    break
            # end for channels

            #if not sent and ("moons" in guild.name or "Moons" in guild.name):
            #    print("\n\nTraceback: ============= didn't send =====================\n\n")
            #    sys.exit()
        # end for guilds
    # end send_payload

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
            print("on_ready")
            wcnt = 0
            last = time.time() - 10*60
            premint_per_hour = False

            while True:
                wcnt += 1
                print("wcnt: ", wcnt)
                if wcnt > 1:
                    print("sleeping a minute")
                    print("now: ", datetime.datetime.now())
                    #sys.exit()
                    await asyncio.sleep(60.0)

                #'''
                now = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
                print("now: ", now)

                await self.update_guilds_data(client.guilds)
                #continue

                # once every 6 minutes
                if time.time() - last < 6*60:
                    continue
                last = time.time()

                minute = datetime.datetime.now().minute
                if minute < 45 and premint_per_hour:
                    premint_per_hour = False
                if not premint_per_hour and minute >= 45:
                    premint_per_hour = True
                    
                    #'''
                    result = await self.query_gcp(premint=True)
                    parsed = True
                    try:
                        print("result.text: ", result.text)

                    except Exception as err:
                        print("352 err: ", err)
                        print("353 err.args: ", err.args[:])
                        parsed = False
                    # end try/except

                    if parsed:
                        with open("data_big/premint_" + now + ".txt", "w") as fid:
                            fid.write(str(result.text))
                        #end with
                
                    try:
                        print("result.json: ", result.json())
                        result = result.json()
                    except Exception as err:
                        print("375 err: ", err)
                        print("376 err.args: ", err.args[:])
                        parsed = False
                    # end try/except
     
                    '''
                    with open("data_big/premint_22-11-05_18-47-40.txt", "r") as fid:
                        result = json.load(fid)
                    # end with open
                    #'''

                    if parsed:
                        if "links_count" in result and "newly_found_links" in result:
                            message = ""
                            for link in result["newly_found_links"]:
                                message += link + "\n"
                            await self.send_payload(message, "premint", client.guilds)
                            ## loop over subscribing guilds and send to their premint channel, if any
                        # end if
                # end if premint stuff

                #'''
                result = await self.query_gcp()
                print("result.text: ", result.text)
                with open("data_big/" + now + ".txt", "w") as fid:
                   fid.write(str(result.text))
                #end with

                try:
                    print("result.json: ", result.json())
                    result = result.json()

                except Exception as err:
                    print("303 err: ", err)
                    print("304 err.args: ", err.args[:])
                    continue
                # end try/except
                #'''

                '''
                with open("data_big/22-11-07_14-03-36.txt", "r") as fid:
                    result = json.load(fid)
                # end with open
                #'''
                print("query_gcp done!")

                fields = [
                            "handle", "rating", "profile_image_url", 
                            "description", "influential_followers", "followers",
                            "created_date", "found_date"
                        ]
                skip = False
                for field in fields:
                    if field not in result:
                        print(field + " not in payload so we're skipping!")
                        skip = True
                        break
                if skip:
                    continue
                
                rating = result["rating"]
                if rating not in self.rating_map:
                    print("\n\nTraceback: unrecognized rating!\n\n")
                    continue
                
                rating = self.rating_map[rating]

                print("rating: ", rating)
                await self.send_payload(result, rating, client.guilds)
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
