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
  # end __init__

  def discord_bot(self):
    client = interactions.Client(token=os.environ["displayBotPass"])

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
        title = "**__rank " + str(rank) + ":__**"
        description = self.rarities[rank-1]

        embed = interactions.Embed(title=title, description=description,)
        embed.set_footer(text = "Built for Roo Troop, Powered by @TheLunaLabs",
                         icon_url=self.URL)

        await ctx.send(embeds=embed, ephemeral=True)
      elif name != None:
        print("name: ", name)
        name1 = "Roo #" + name.split("#")[1]
        name2 = "Roo Troop #" + name.split("#")[1]
        for ii in range(len(self.rarities)):
          if name1 == self.rarities[ii] or name2 == self.rarities[ii]:
            title = "**__rank of " + name + "__**"
            description = str(ii+1)
            print(self.rarities[ii])

            embed = interactions.Embed(title=title, description=description,)
            embed.set_footer(text = "Built for Roo Troop, Powered by @TheLunaLabs",
                    icon_url=self.URL)
            await ctx.send(embeds=embed, ephemeral=True)
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
