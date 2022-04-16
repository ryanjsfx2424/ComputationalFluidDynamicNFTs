## fat-finger-detector.py
"""
This is a discord bot. It'll send messages when it detects
an OpenSea listing way below a threshold value for a given
collection.

Reason for being a discord bot is so ideally a user can
input collections they want to watch, thresholds, etc. And
maybe it can also email users interested in such as well.
"""
import os
import time
import json
import random
import asyncio
import discord
import numpy as np
from web3 import Web3

client = discord.Client()

BOT_COMMANDS_CID = 932056137518444594
SLEEP_TIME = 0.2

ABI_PATHS = [
             "abi_bayc.json"
            ]

CONTRACT_ADDRESSES = {
                      "bayc": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
                     }

ALCHEMY_API_KEY = os.environ["ALCHEMY_API_KEY_ETH"]
ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/" + ALCHEMY_API_KEY

## web3 stuff
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

contracts = []
totalSupplies = []
for ii in range(len(ABI_PATHS)):
  abi_path = ABI_PATHS[ii]
  key = list(CONTRACT_ADDRESSES.keys())[ii]
  contract_address = CONTRACT_ADDRESSES[key]

  with open(abi_path, "r") as fid:
    rl = "".join(fid.readlines())
    abi = json.loads(rl)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    contracts.append(contract)
  # end with open
  totalSupplies.append(contract.functions.totalSupply().call())
# end for ii
print("totalSupplies: ", totalSupplies)
sys.exit()

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
       message.content.startswith('$cfd-v2-giveaway') or \
       message.content.startswith('$cfd-v3-giveaway'):
      
      if "v1" in message.content:
        ind = 0
      elif "v2": 
        ind = 1
      elif "v3":
        ind = 2
      else:
        print("something went very wrong!")
        raise
      # end if/else
      num = len(cfd_nft_holders[ind])-1

      channel = client.get_channel(GIVEAWAY_CID) # bot-commands
      
      msg = await channel.send("rolling between 0 and " + str(num) + ", inclusive")
      text = "ROLL: " + \
             str(random.randrange(0,num+1))
      msg = await channel.send(text)
      for ii in range(5):
        await asyncio.sleep(SLEEP_TIME)
        text = "ROLL: " + \
               str(random.randrange(0,num+1))
        await msg.edit(content=text)
      # end for ii

      while True:
        winning_roll = random.randrange(0,num+1)
        winning_address = cfd_nft_holders[ind][winning_roll]
        if winning_address not in MY_ADDRESSES:
          break
        # end if
      # end while True
      
      text = "WINNER: " + str(winning_roll)
      if winning_address in KNOWN_ADDRESSES.keys():
        text += "\nwhich is: " + KNOWN_ADDRESSES[winning_address]
      else:
        text += "\nwhich is: " + winning_address
      # end if/else

      await msg.edit(content=text)
    # end if  

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
