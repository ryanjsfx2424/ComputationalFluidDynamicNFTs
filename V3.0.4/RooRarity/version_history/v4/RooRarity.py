## DisplayRoos.py
"""
The purpose of this script is to display roos by their rarity
"""
import os
import sys
import ast
import copy

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
print("Begin DisplayRoos")

class DisplayRoos(object):
  def __init__(self):
    self.TTM_GID = 931482273440751638
    self.BOT_COMMANDS_CIDS = [932056137518444594]
    frare = "rarities_rarity-tools_roo-troop.txt"

    with open(frare, "r") as fid:
      self.rarities = fid.read()
    # end with
    self.rarities = ast.literal_eval(self.rarities)

    self.URL = "https://cdn.discordapp.com/attachments/965394881067515914/980589091718586428/4431.png"


    self.super_roo_url = "https://cc_nftstore.mypinata.cloud/ipfs/QmX2Jf52HcRBoGEP6i6xptdHCF1Caa6iM6X3Zi1jSTvPHb"
    self.base_roo_url = "https://cc_nftstore.mypinata.cloud/ipfs/QmPZXdpP1sZj67GgevEr2W93bB1D7XcmySLKrMmNDGL4FP/"

  # end __init__

  def discord_bot(self):
    client = interactions.Client(token=os.environ["displayBotPass"])
    client.load("interactions.ext.files")

    @client.command(
      name="roorarity",
      description="Displays roo of a given rarity",
      scope=self.TTM_GID,
      options = [
        interactions.Option(
          name="rank",
          description="roo rank to display",
          type=interactions.OptionType.STRING,
          required=False,
        ),
        interactions.Option(
          name="name",
          description="roo name to display the rank of",
          type=interactions.OptionType.STRING,
          required=False,
        ),
      ],
    )
    async def roorarity(ctx: interactions.CommandContext,
                        rank: str = None, name: str = None):

      if   rank != None and name != None:
        await ctx.send("error! can only accept rank or name, not both",
                       ephemeral=True)
      elif rank != None:
        print("rank: ", rank)
        rank = int(float(rank))
        
        if rank < 1 or rank > 5501:
          await ctx.send("error! rank must be >= only accept rank or name, not both",
                       ephemeral=True)
          return
        # end if
        if str(rank)[-1] == "1":
          end = "st"
        if str(rank)[-1] == "2":
          end = "nd"
        if str(rank)[-1] == "3":
          end = "rd"
        else:
          end = "th"
        title = "**__ranked " + str(rank) + end + " => " + \
                self.rarities[rank-1]+ "__**"
        description = "\u200b"

        if rank == 1:
          fname = "5501.png"
        else:
          num = self.rarities[rank-1].split("#")[1]
          fname = str(num).zfill(5) + ".webp"
        # end if/else

        embed = interactions.Embed(title=title, description=description,)
        embed.set_footer(text = "Built for Roo Troop, Powered by @TheLunaLabs",
                         icon_url=self.URL)

        os.chdir("IMAGES/root/")
        file = interactions.File(fname)
        embed.set_image(url="attachment://" + fname)
        await ctx.send(files=file, embeds=embed, ephemeral=True)
        os.chdir("../..")
      elif name != None:
        print("name: ", name)
        num = name.split("#")[1]
        name1 = "Roo #" + num
        name2 = "Roo Troop #" + num
        
        if "super" in name.lower():
          name = "Super Roo #1 - Jungle Roo"
        else:
          name = name1
        # end if

        for ii in range(len(self.rarities)):
          if   name1 == self.rarities[ii] or \
               name2 == self.rarities[ii] or \
               name  == self.rarities[ii]:
            title = "**__rank of " + name + "=> " + str(ii+1) + "__**"
            description = "\u200b"
            print(self.rarities[ii])


            if "super" in name.lower():
              image_url = self.super_roo_url
              fname = "5501.png"
            else:
              image_url = self.base_roo_url + num + ".webp"
              fname = str(num).zfill(5) + ".webp"
            # end if/else

            embed = interactions.Embed(title=title, description=description,)
            embed.set_footer(text = "Built for Roo Troop, Powered by @TheLunaLabs",
                    icon_url=self.URL)
            os.chdir("IMAGES/root/")
            file = interactions.File(fname)
            embed.set_image(url="attachment://" + fname)
            await ctx.send(files=file, embeds=embed, ephemeral=True)
            os.chdir("../..")
            return
          # end if
        # end for
      # end if/elifs
    # end roorarity

    client.start()
  # end discord_bot
# end DisplayRoos

if __name__ == "__main__":
  bot = DisplayRoos()
  bot.discord_bot()
# end if
print("Success DisplayRoos")
