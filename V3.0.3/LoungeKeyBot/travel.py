## v1 gets latest data working
## v2 did pretty embeds
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
    self.errs  = {"texts": [], "images": [], "urls": []}
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

  def get_error_fares(self):
    ErrorFares = self.html.split("Latest Error Fares")[1].split("Popular Departure Cities")[0]
    imgs = ErrorFares.split('<img ')[1:]
    
    images = []
    for image in imgs:
      image = image.split('src="')[1].split('"')[0]
      if "EXPIRED" not in image:
        images.append(image)
      # end if
    # end for

    ErrorFares = ErrorFares.split(self.h3str)
    print("len ErrorFares: ", len(ErrorFares))
    print("len images: ", len(images))
    for ii,err in enumerate(ErrorFares[1:]):
      url   = err.split(  '<a href="')[1].split(" ")[ 0]
      err   = err.split(    'title="')[1].split('" ')[0]
      image = images[ii]

      if err not in self.errs["texts"]:
        print("errFare: ", err)
        self.errs["urls"  ].append(url  )
        self.errs["texts" ].append(err  )
        self.errs["images"].append(image)
    # end for

    with open("errFares.txt", "w") as fid:
      fid.write(str(self.errs))
    # end with open
  # end get_error_fares

  def get_latest_deals(self):
    LatestDeals = self.html.split("Latest Deals")[1].split("As seen on")[0]
    images = LatestDeals.split('<img ')[1:]

#    for image in images:
#      image = image.split('src="')[1].split('"')[0]
#      self.deals["images"].append(image)
#    # end for images

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
    client = discord.Client()

    @client.event
    async def on_ready():
      channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
      while True:
        old_deals = [] + self.deals["texts"]
        old_errs  = [] + self.errs[ "texts"]
        self.get_html()
        self.get_latest_deals()
        self.get_error_fares()

        for ii,deal in enumerate(self.deals["texts"]):
          if deal not in old_deals:
            print("new deal!")

            title       = deal
            description = deal
            if len(deal) > 50:
              title = deal[:50] + "..."
            # end if

            embed = discord.Embed(title=title, description=description, 
                    color=discord.Color.blue(), url=self.deals["urls"][ii])
            img = self.deals["images"][ii]
            embed.set_image(url=img)
            embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                             icon_url=self.icon_url)
            await channel.send(embed=embed)
          # end if
        # end for

        for ii,err in enumerate(self.errs["texts"]):
          if err not in old_errs:
            print("new err fare!")

            title = err
            description = err
            if len(err) > 50:
              title = err[:50] + "..."
            # end if

            embed = discord.Embed(title=title, description=description[:-1] + " (Error Fare)", 
                    color=discord.Color.blue(), url=self.errs["urls"][ii])
            img = self.errs["images"][ii]
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