import os
import sys
import ast
import random
import discord
import asyncio

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions.client import get

class BountifulDiscordBot(object):
    def __init__(self):
        self.LOG_CID = 932056137518444594 ## TTB Bot-commands
        self.BOT_CIDS = [1002314445382484058] # bountiful bot-commands
        self.RUL_CID = 1002246080353808496 # bountiful rules
        self.GIDS = [931482273440751638, # toTheMoons
                     1002246079493980221] # Bountiful

        self.approved_users = [855616810525917215, # me
                               890926940083589161, # Horst
                               426687223467868172] # Zoro

        self.msg_timer = 0

        self.URL = "https://cdn.discordapp.com/attachments/1000331210557497364/1002224083561357462/Profile_Imaage_0-00-00-00.jpg"
    # end __init__

    def discord_bot(self):
        client = discord.Client()
        secret = os.environ.get("fracBotPass")
        intBot = interactions.Client(secret)

        @client.event
        async def on_ready():
           print("ready!")
           channel = client.get_channel(self.LOG_CID)
           await channel.send("Bountiful!")
        # end on_ready

        ## modify this!!
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

            channel_log = client.get_channel(self.LOG_CID)
            if message.channel.id not in self.BOT_CIDS:
                if time.time() - self.msg_timer > 3600:
                    self.msg_timer = time.time()
                    await channel_log.send("channel id not in BOT_CIDS!")
                    await channel_log.send("msg channel id: " + str(message.channel.id))
                    await channel_log.send("self.BOT_CIDS: " + str(self.BOT_CIDS))
                # end if
                return
            # end if
        # end on_message

        loop = asyncio.get_event_loop()

        task2 = loop.create_task(client.start(os.environ.get("fracBotPass")))
        task1 = loop.create_task(intBot._ready())

        gathered = asyncio.gather(task1, task2, loop=loop)
        loop.run_until_complete(gathered)
    # end discord_bot
# end FractalzDiscordBot

if __name__ == "__main__":
    frac = FractalzDiscordBot()
    frac.discord_bot()
## end fractalz.py
