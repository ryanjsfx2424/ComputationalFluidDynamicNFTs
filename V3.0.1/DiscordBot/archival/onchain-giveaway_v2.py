## onchain-giveaway.py
"""
This is a discord bot. The first version just grabbed activity
and can roll dice.

Next I'm going to query for addresses of who owns V1, V2 NFTs.
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
channels = {
            "general": 931482273973420034,
            "apod"   : 940983047157854248,
            "xkcd"   : 940985070460760094
           }
BOT_COMMANDS_CID = 932056137518444594
GIVEAWAY_CID     = 938548088270880878
SLEEP_TIME = 0.2

ABI_PATHS = [
             "abi_v1-0-0.json",
             "abi_v2-0-0.json",
             "abi_v3-0-0.json"
            ]
cfd_nft_holders = [[] for ii in range(len(ABI_PATHS))]

CONTRACT_ADDRESSES = [
                      "0x60369C62eF43521D95ac78bA18D111604a2A3C82", #V1
                      "0x34bD2c9D7568b9d659221f83Fd044fB94C08805d", #V2
                      "0xd3eF9a40806AcfE42a5E99257cd8774Cd25d525f"  #V3
                     ]
MY_ADDRESSES = [
                "0x65AAf6d3fAe0E3BC43bB7cd48f4bb1B105Ab2b7E",
                "0x64F1E48cb75825c384B8eB6134c959c3C8BBC11A"
               ]
KNOWN_ADDRESSES = {
                   "0xd4b7315fE51081f829cA1F6486E97C44BEFb688b": "BreadedCrab",
                   "0x8e8395F9BEf1c1E2472986B9A181ccf33BD56b94": "Thicctor",
                   "0x89B88287e2905003551f06eD77c3491bE360DE8D": "NBSea",
                   "0x71bAb317A63dFD6fa948D3b0d599b080a09E3d6C": "Alsa_eth",
                   "0x7690f3D66B410628C173d3564B6a5b451249D249": "aier",
                   "0x5dE0F9eF517976CDDF2a7DC737766A448123A38F": "NosOmnesAnates",
                   "0x53d2984aBf5a7ebb53aF92098D57671ef6A20D58": "PrettyPonies",
                   "0x2f683b8Ef03DF165bd7C4d9b81bB51c78b6E3848": "RebeL-_-",
                   "0x275381048C9D6b9CDE3375815466F9aE14736a86": "_Furuta_",
                   "0xB822d34051167DBD07130dd8de66D41C95E5bb6B": "EbyssLabs",
                   "0xF24a4BA4C3c87F3E097bC06e7625aa02D5dB8D0f": "Bonsai-Fox"
                  }

ALCHEMY_API_KEY = os.environ["ALCHEMY_API_KEY"]
ALCHEMY_URL = "https://polygon-mainnet.g.alchemy.com/v2/" + ALCHEMY_API_KEY

## web3 stuff
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

contracts = []
totalSupplies = []
for ii in range(len(ABI_PATHS)):
  abi_path = ABI_PATHS[ii]
  contract_address = CONTRACT_ADDRESSES[ii]

  with open(abi_path, "r") as fid:
    rl = "".join(fid.readlines())
    abi = json.loads(rl)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    contracts.append(contract)
  # end with open
  totalSupplies.append(contract.functions.totalSupply().call())
  for jj in range(totalSupplies[-1]):
    token = contract.functions.tokenByIndex(jj).call()
    cfd_nft_holders[ii].append(contract.functions.ownerOf(token).call())
    time.sleep(SLEEP_TIME)
  # end for jj
# end for ii

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

          if int(float(messages[-1].created_at.day)) > 25:
            LIMIT *= 2
          else:
            break
        # end while True

        for message in messages:
          msg_day = message.created_at.day
          msg_mo = message.created_at.month


          if (msg_day >= 26 and msg_mo == 3) or (msg_day <= 1 and msg_mo == 4):
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

      text = "ROLL: " + \
             str(random.randrange(0,len(ppl)))
      msg = await channel.send(text)
      for ii in range(5):
        await asyncio.sleep(SLEEP_TIME)
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
