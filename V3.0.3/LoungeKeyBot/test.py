## v1 gets latest data working
## v2 will do pretty embeds
## v3 will get the error fares too

import os
import requests
import asyncio
import discord

class TravelBot(object):
  def __init__(self):
    self.url = "https://secretflying.com"
    self.h3str = '<h3 class="entry-title">'
    self.deals = {"texts": [], "images": [], "urls": []}
    self.BOT_COMMANDS_CIDS = [932056137518444594]
    self.sleep_time = 60.1

    self.icon_url = "https://cdn.discordapp.com/attachments/932056137518444594/991364877467783279/Screenshot_2022-06-28_at_13.56.21.png"
  # end __init__

  def get_html(self):
    resp = requests.get(self.url)
    print("resp: ", resp)
    self.html = resp.text

    with open("html.txt", "w") as fid:
      fid.write(self.html)
    # end with open
  # end get_html

  def get_latest_deals(self):
    self.get_html()
    LatestDeals = self.html.split("Latest Deals")[1].split("As seen on")[0]
    images = LatestDeals.split('<img ')[1:]

    for image in images:
      image = image.split('src="')[1].split('"')[0]
      self.deals["images"].append(image)
    # end for images

    LatestDeals = LatestDeals.split(self.h3str)
    for ii,deal in enumerate(LatestDeals[1:]):
      url   = deal.split(  '<a href="')[1].split(" ")[ 0]
      deal  = deal.split(    'title="')[1].split('" ')[0]
      image = images[ii].split('src="')[1].split('"')[ 0]

      if deal not in self.deals["texts"]:
        print("deal: ", deal)
        self.deals["urls"  ].append(url  )
        self.deals["texts" ].append(deal )
        self.deals["images"].append(image)
      # end if
    # end for

    with open("deals.txt", "w") as fid:
      fid.write(str(self.deals))
    # end with open
  # end get_latest_deals

  def discord_bot(self):
    client = discord.Client(intents=None)

    @client.event
    async def on_message(message):
      if message.author == client.user:
        return
      print("message.author: ", message.author)
      print("dir message.author: ", dir(message.author))
      print("client.user: ", client.user)
      if message.author.id == 855616810525917215:
        print("sup")
      #channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
      #if message.channel.id == self.BOT_COMMANDS_CIDS[0]:

    @client.event
    async def on_ready():
      return
      channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
      while True:
        old_deals = [] + self.deals["texts"]
        self.get_latest_deals()

        for ii,deal in enumerate(self.deals["texts"]):
          if deal not in old_deals:
            title, description = deal.split("(")
            embed = discord.Embed(title=title, description=description[:-1], 
                    color=discord.Color.blue(), url=self.deals["urls"][ii])
            img = self.deals["images"][ii]
            print("img: ", img)
            embed.set_image(url=img)
            embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                             icon_url=self.icon_url)
            await channel.send(embed=embed)
          # end if
        # end for
        await asyncio.sleep(self.sleep_time)
      # end while
    # end on_ready
    client.run(os.environ.get("lkBotPass"))
  # end def discord_bot
# end TravelBot

if __name__ == "__main__":
  tb = TravelBot()
  tb.discord_bot()
# end if
