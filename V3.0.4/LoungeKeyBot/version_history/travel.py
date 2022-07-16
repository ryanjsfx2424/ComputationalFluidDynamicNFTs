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
    self.deals = {"texts": [], "images": [], "urls": [], 
                  "regions_from":[], "regions_to":[]}
    self.errs  = {"texts": [], "images": [], "urls": [], 
                  "regions_from":[], "regions_to":[]}
    self.BOT_COMMANDS_CIDS = [932056137518444594]
    self.CIDS = {
                 "usa"                 : 985734292867006464,
                 "canada"              : 985734339360878592,
                 "c-america-carribean" : 985734367869558825,
                 "south-america"       : 985734405823799306,
                 "europe"              : 985734428598874142,
                 "me-and-north-africa" : 985734538632232960,
                 "africa"              : 985734740118237195,
                 "c-and-s-asia"        : 985734786112954388,
                 "east-asia"           : 985734816861392896,
                 "oceania"             : 985734839107981332,
                 "uk-and-ireland"      : 985745362335694918,
                 "error-fares"         : 991451387068158063
                }
    self.CIDS_USA = {
                     #"Test" : 992569174901665942,
                     "North West"  : 992564988642340937,
                     "South West"  : 992565083613966426,
                     "Mid West"    : 992565190736482344,
                     "South"       : 992565252401156097,
                     "Great Lakes" : 992565351713865749,
                     "South East"  : 992565426754162708,
                     "New England" : 992565535181111366
                    }
    self.sleep_time = 60.1

    self.icon_url = "https://cdn.discordapp.com/attachments/932056137518444594/991364877467783279/Screenshot_2022-06-28_at_13.56.21.png"
    
    self.states = []
    with open("states.txt", "r") as fid:
      for line in fid:
        self.states.append(line.split()[-1].strip(" \n").lower())
      # end for
    # end with

    ## note I used this list of countries for caribbean, central am + south am
    ## http://lanic.utexas.edu/subject/countries/
    self.ca_carribean = []
    with open("carribean.txt", "r") as fid:
      for line in fid:
        self.ca_carribean.append(line.replace(" ","").replace("\n","").lower())
      # end for
    # end with

    with open("central_america.txt", "r") as fid:
      for line in fid:
        self.ca_carribean.append(line.replace(" ","").replace("\n","").lower())
      # end for
    # end with

    self.samerica = []
    with open("south_america.txt", "r") as fid:
      for line in fid:
        self.samerica.append(line.replace(" ","").replace("\n","").lower())
      # end for
    # end with

    ## grabbed from wikipedia
    self.europe = []
    with open("europe.txt", "r") as fid:
      for line in fid:
        self.europe.append(line.split()[1].replace("*","").replace("\n","").lower())
      # end for
    # end with

    ## grabbed from https://www.investopedia.com/terms/m/middle-east-and-north-africa-mena.asp
    self.mena = []
    with open("middle_east.txt") as fid:
      line = fid.read()
      countries = line.split(", ")
      for country in countries:
        self.mena.append(country.replace(" ", "").replace("\n","").lower())
      # end for
    # end with open

    with open("north_africa.txt") as fid:
      line = fid.read()
      countries = line.split(", ")
      for country in countries:
        self.mena.append(country.replace(" ", "").replace("\n","").lower())
      # end for
    # end with open

    self.africa = []
    with open("west_africa.txt") as fid:
      for line in fid:
        self.africa.append(line.split()[0].lower())
      # end for
    # end with open

    with open("central_africa.txt") as fid:
      for line in fid:
        self.africa.append(line.split()[0].lower())
      # end for
    # end with open

    with open("south_africa.txt") as fid:
      for line in fid:
        self.africa.append(line.split()[0].lower())
      # end for
    # end with open

    ## grabbed from: https://ustr.gov/countries-regions/south-central-asia
    self.cs_asia = []
    with open("central_asia.txt") as fid:
      line = fid.read()
      countries = line.split(", ")
      for country in countries:
        self.cs_asia.append(country.replace(" ", "").replace("\n","").lower())
      # end for
    # end with open

    self.cs_asia = []
    with open("south_asia.txt") as fid:
      line = fid.read()
      countries = line.split(", ")
      for country in countries:
        self.cs_asia.append(country.replace(" ", "").replace("\n","").lower())
      # end for
    # end with open

    ## grabbed from https://en.wikipedia.org/wiki/East_Asia
    ## and worldpopreview below
    self.e_asia = []
    with open("east_asia.txt") as fid:
      line = fid.read()
      countries = line.split(", ")
      for country in countries:
        self.e_asia.append(country.replace(" ", "").replace("\n","").lower())
      # end for
    # end with open

    ## grabbed from https://worldpopulationreview.com/country-rankings/countries-in-oceania
    self.oceania = []
    with open("oceania.txt") as fid:
      for line in fid:
        self.oceania.append(line.split()[1].lower())
      # end for
    # end with open

    self.southwest = []
    with open("southwest.txt") as fid:
      for line in fid:
        self.southwest.append(line.replace("\n",""))
      # end for
    # end with

    self.northwest = []
    with open("northwest.txt") as fid:
      for line in fid:
        self.northwest.append(line.replace("\n",""))
      # end for
    # end with

    self.midwest = []
    with open("midwest.txt") as fid:
      for line in fid:
        self.midwest.append(line.replace("\n",""))
      # end for
    # end with

    self.south = []
    with open("south.txt") as fid:
      for line in fid:
        self.south.append(line.replace("\n",""))
      # end for
    # end with

    self.greatlakes = []
    with open("greatlakes.txt") as fid:
      for line in fid:
        self.greatlakes.append(line.replace("\n",""))
      # end for
    # end with

    self.southeast = []
    with open("southeast.txt") as fid:
      for line in fid:
        self.southeast.append(line.replace("\n",""))
      # end for
    # end with

    self.newengland = []
    with open("newengland.txt") as fid:
      for line in fid:
        self.newenglad.append(line.replace("\n",""))
      # end for
    # end with
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
      url   = err.split(  '<a href="')[2].split(" ")[ 0].split('"')[0]
      err   = err.split(    'title="')[1].split('" ')[0]
      image = images[ii]

      if err not in self.errs["texts"]:
        print("errFare: ", err)
        self.errs["urls"  ].append(url  )
        self.errs["texts" ].append(err  )
        self.errs["images"].append(image)
        self.get_regions(err, "err")
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
      url   = deal.split(  '<a href="')[2].split(" ")[ 0].split('"')[0]
      deal  = deal.split(    'title="')[1].split('" ')[0]
      image = images[ii].split('src="')[1].split('"')[ 0]
      if "Hotel" in deal:
        continue
      # end if

      if deal not in self.deals["texts"]:
        print("deal: ", deal)
        self.deals["urls"  ].append(url  )
        self.deals["texts" ].append(deal )
        self.deals["images"].append(image)
        self.get_regions(deal, "deal")
      # end if
    # end for

    with open("deals.txt", "w") as fid:
      fid.write(str(self.deals))
    # end with open
  # end get_latest_deals

  def get_regions(self, fare, err_or_deal):
    if err_or_deal == "err":
      fares = self.errs
    elif err_or_deal == "deal":
      fares = self.deals
    else:
      print("expected err or deal")
      raise
    # end if/elif/else

    print("fare: ", fare)
    dest,port = fare.split(" to ")
    if " for only " in port:
      port = port.split(" for only ")[0]
    elif " from only " in port:
      port = port.split(" from only ")[0]
    else:
      print("error! Neither ' for only ' nor ' from only ' in port!")
      raise
    if "," not in dest:
      fares["regions_to"].append("usa")

                     "North West"  : 992564988642340937,
                     "South West"  : 992565083613966426,
                     "Mid West"    : 992565190736482344,
                     "South"       : 992565252401156097,
                     "Great Lakes" : 992565351713865749,
                     "South East"  : 992565426754162708,
                     "New England" : 992565535181111366

      if " or " in dest:
        for dest in dest.split(" or "):
          if "chicago" in dest.lower():
            fares["regions_to"].append("Mid West")
          elif "fort lauderdale" in dest.lower() or \
               "miami"           in dest.lower():
            fares["regions_to"].append("South East")
          elif "boston"   in dest.lower() or \
               "new york" in dest.lower() or \
               "buffalo"  in dest.lower():
            fares["regions_to"].append("New England")
          elif "san francisco" in dest.lower() or \
               "los angeles"   in dest.lower():
            fares["regions_to"].append("South West")
          elif "washington dc" in dest.lower():
            fares["regions_to"].append("Great Lakes")
          elif "minneapolis" in dest.lower() or \
               "st. louis"   in dest.lower():
            fares["regions_to"].append("Mid West")
          # end if/elifs
        

    else:
      city,country = dest.split(", ")
      city = city.replace("Non-stop from ", "").replace(" ","").lower()
      country = country.replace(" ", "").lower()

      if country in self.states:
        fares["regions_to"].append("usa")

        if country in self.south:
          fares["regions_to"].append("South")
        elif country in self.greatlakes:
          fares["regions_to"].append("Great Lakes")
        elif country in self.southeast:
          fares["regions_to"].append("South East")
        elif country in self.southwest:
          fares["regions_to"].append("South West")
        elif country in self.northwest:
          fares["regions_to"].append("North West")
        elif country in self.midwest:
          fares["regions_to"].append("Mid West")
        elif country in self.newenglad:
          fares["regions_to"].append("New Englad")

        fares

      elif country == "usa":
        fares["regions_to"].append("usa")
      elif country == "canada":
        fares["regions_to"].append("canada")
      elif country in self.ca_carribean:
        fares["regions_to"].append("c-america-carribean")
      elif country in self.samerica:
        fares["regions_to"].append("south-america")
      elif country in ["uk","ireland"]:
        fares["regions_to"].append("uk-and-ireland")
      elif country in self.europe:
        fares["regions_to"].append("europe")
      elif country in self.mena:
        fares["regions_to"].append("me-and-north-africa")
      elif country in self.africa:
        fares["regions_to"].append("africa")
      elif country in self.cs_asia:
        fares["regions_to"].append("c-and-s-asia")
      elif country in self.e_asia:
        fares["regions_to"].append("east-asia")
      elif country in self.oceania:
        fares["regions_to"].append("oceania")
      else:
        print("error getting regions_to")
        print("port: ", dest)
        print("city: ", city)
        print("country: ", country)
        raise
      # end if/elifs
    # end if/else

    if "," not in port:
      fares["regions_from"] = "usa"
    else:
      city,country = port.split(", ")
      city = city.replace("Non-stop from ", "").replace(" ","").lower()
      country = country.replace(" ", "").lower()

      if country in self.states:
        fares["regions_from"].append("usa")
      elif country == "usa":
        fares["regions_from"].append("usa")
      elif country == "canada":
        fares["regions_from"].append("canada")
      elif country in self.ca_carribean:
        fares["regions_from"].append("c-america-carribean")
      elif country in self.samerica:
        fares["regions_from"].append("south-america")
      elif country in ["uk","ireland"]:
        fares["regions_from"].append("uk-and-ireland")
      elif country in self.europe:
        fares["regions_from"].append("europe")
      elif country in self.mena:
        fares["regions_from"].append("me-and-north-africa")
      elif country in self.africa:
        fares["regions_from"].append("africa")
      elif country in self.cs_asia:
        fares["regions_from"].append("c-and-s-asia")
      elif country in self.e_asia:
        fares["regions_from"].append("east-asia")
      elif country in self.oceania:
        fares["regions_from"].append("oceania")
      else:
        print("error getting regions_from")
        print("port: ", port)
        print("city: ", city)
        print("country: ", country)
        raise
      # end if/elifs
    # end if/else
  # end get_regions


  def discord_bot(self):
    client = discord.Client(intents=None)

    @client.event
    async def on_ready():
      channel0 = client.get_channel(self.BOT_COMMANDS_CIDS[0])
      await channel0.send("channel msg test") # succeeds
      thread = channel0.get_thread(992569174901665942)
      await thread.send("thread msg test") # succeeds!

      '''
      channel_usa = client.get_channel(self.CIDS["usa"])
      #thread = channel_usa.get_thread(992564988642340937)
      #await thread.send("thread msg test") # succeeds!
      #sys.exit()
      '''

      while True:
        old_deals = [] + self.deals["texts"]
        old_errs  = [] + self.errs[ "texts"]
        self.get_html()
        self.get_latest_deals()
        self.get_error_fares()

        for ii,deal in enumerate(self.deals["texts"]):
          if deal not in old_deals:
            print("new deal!")

            title = deal
            try:
              description = "#" + self.deals["regions_to"][  ii] + \
                           " #" + self.deals["regions_from"][ii]
            except Exception as err:
              print("err 348: ", err)
              print("err args: ", err.args[:])
              print("len deals regs to: ",   self.deals["regions_to"  ][ii])
              print("len deals regs from: ", self.deals["regions_from"][ii]) 
            # end try/except

            embed = discord.Embed(title=title, description=description, 
                    color=discord.Color.blue(), url=self.deals["urls"][ii])
            img = self.deals["images"][ii]
            #embed.set_image(url=img)
            embed.set_thumbnail(url=img)
            embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                             icon_url=self.icon_url)
            cid_to   = self.CIDS[self.deals["regions_to"][  ii]]
            cid_from = self.CIDS[self.deals["regions_from"][ii]]
            print("cid_to: ", cid_to)
            print("cid_from: ", cid_from)
            channel_to   = client.get_channel(cid_to  )
            channel_from = client.get_channel(cid_from)
            #await channel_to.send(  embed=embed)
            #await channel_from.send(embed=embed)
            await channel0.send(    embed=embed)
          # end if
        # end for

        for ii,err in enumerate(self.errs["texts"]):
          if err not in old_errs:
            print("new err fare!")

            title = err
            description = err
            description = "#" + self.errs["regions_to"][  ii] + \
                         " #" + self.errs["regions_from"][ii]
            #if len(err) > 50:
            #  title = err[:50] + "..."
            # end if

            print("self.errs['urls'][ii]: ", self.errs['urls'][ii])
            embed = discord.Embed(title=title, description=description + " #error-fare", 
                    color=discord.Color.blue(), url=self.errs["urls"][ii])
            img = self.errs["images"][ii]
            print("img: ", img)
            #embed.set_image(url=img)
            embed.set_thumbnail(url=img)
            embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                             icon_url=self.icon_url)
            cid_to   = self.CIDS[self.errs["regions_to"][  ii]]
            cid_from = self.CIDS[self.errs["regions_from"][ii]]
            channel_to   = client.get_channel(cid_to  )
            channel_from = client.get_channel(cid_from)
            channel_err = client.get_channel(self.CIDS["error-fares"])
            print("cid_to: ", cid_to)
            print("cid_from: ", cid_from)
            print("cid_err: ", self.CIDS["error-fares"])
            #await channel_err.send( embed=embed)
            #await channel_to.send(  embed=embed)
            #await channel_from.send(embed=embed)
            await channel0.send(    embed=embed)
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
