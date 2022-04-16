import os
import numpy as np
import random
import asyncio
import discord

client = discord.Client()
channels = {"general":931482273973420034,
            "apod":940983047157854248,
            "xkcd":940985070460760094,
           }
BOT_COMMANDS_CID = 932056137518444594
GIVEAWAY_CID     = 938548088270880878
sleep_time = 0.2

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if 'test' in message.content:
        channel = client.get_channel(BOT_COMMANDS_CID) # bot-commands

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        channel = client.get_channel(BOT_COMMANDS_CID) # bot-commands
        await channel.send('Hello, World!')

    if message.channel.id == GIVEAWAY_CID and \
       message.content.startswith('$cfd-v1-giveaway') or \
       message.content.startswith('$cfd-v2-giveaway'):
      
      if "v1" in message.content:
        num = 15
      else: 
        num = 31
      # end if/else

      channel = client.get_channel(GIVEAWAY_CID) # bot-commands
      
      msg = await channel.send("rolling between 0 and " + str(num) + ", inclusive")
      text = "ROLL: " + \
             str(random.randrange(0,num+1))
      msg = await channel.send(text)
      for ii in range(5):
        await asyncio.sleep(sleep_time)
        text = "ROLL: " + \
               str(random.randrange(0,num+1))
        await msg.edit(content=text)
      # end for ii

      text = "WINNER: " + \
             str(random.randrange(0,num+1))
      await msg.edit(content=text)
      

    if message.channel.id == GIVEAWAY_CID and \
       message.content.startswith('$activity-giveaway'):

      channel = client.get_channel(GIVEAWAY_CID) # bot-commands
      await channel.send('Getting activity, this may take a moment.')
      ppl = []
      for channel_key in channels.keys():
        print(channel_key)
        channel = client.get_channel(channels[channel_key])

        LIMIT = 200
        while True:
          messages = await channel.history(limit=LIMIT).flatten()
          #messages = await message.channel.history(limit=LIMIT).flatten()

          if int(float(messages[-1].created_at.day)) > 20:
            LIMIT *= 2
          else:
            break
        # end while True

        for message in messages:
          msg_day = message.created_at.day
          msg_mo = message.created_at.month


          if msg_day >= 20 and msg_day <= 24 and msg_mo == 3:
            name = message.author.name
            if name == "ryanjsfx.eth|ToTheMoonsNFT|Luna":
              continue
            if "apod" in channel_key:
              if not message.attachments:
                continue
            ppl.append(message.author.name)
          # end if
        # end for
      # end for channels
      print(ppl)
      print("len(ppl): ", len(ppl))
      channel = client.get_channel(GIVEAWAY_CID) # bot-commands
      await channel.send('Got activity, let\'s roll!')
      await channel.send('entrants:')
      text = ""
      for pp in range(len(ppl)):
        text += str(pp) + ": " + ppl[pp] + "\n"
      await channel.send(text)
      # end for
      await channel.send('(THIS IS A TEST)')

      text = "ROLL: " + \
             str(random.randrange(0,len(ppl)))
      msg = await channel.send(text)
      for ii in range(5):
        await asyncio.sleep(sleep_time)
        text = "ROLL: " + \
               str(random.randrange(0,len(ppl)))
        await msg.edit(content=text)
      # end for ii

      text = "WINNER: " + \
             str(random.randrange(0,len(ppl)))
      await msg.edit(content=text)


      print("SUCCESS scan!")
    # end if command == scan
    print("SUCCESS!")  

secret = os.environ.get("ocgBotPass")
client.run(secret)
