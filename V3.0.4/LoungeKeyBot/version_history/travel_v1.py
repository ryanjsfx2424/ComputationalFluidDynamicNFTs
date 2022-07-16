import os
import requests
import asyncio
import discord

class TravelBot(object):
  def __init__(self):
    self.url = "https://secretflying.com"
    self.h3str = '<h3 class="entry-title">'
    self.deals = []
    self.BOT_COMMANDS_CIDS = [932056137518444594]
    self.sleep_time = 60.1

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
    LatestDeals = LatestDeals.split(self.h3str)
    for deal in LatestDeals[1:]:
      deal = deal.split('title="')[1].split('" ')[0]
      if deal not in self.deals:
        print("deal: ", deal)
        self.deals.append(deal)
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
        await asyncio.sleep(self.sleep_time)
        old_deals = [] + self.deals
        self.get_latest_deals()

        for deal in self.deals:
          if deal not in old_deals:
            await channel.send(deal)
          # end if
        # end for
      # end while
    # end on_ready
    client.run(os.environ.get("lkBotPass"))
  # end def discord_bot
# end TravelBot

if __name__ == "__main__":
  tb = TravelBot()
  tb.discord_bot()
# end if