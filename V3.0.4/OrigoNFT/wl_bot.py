## NOTE: use env-old-discord on MB-145.local
import os
import sys
import socket
import discord
import asyncio
import gspread

# mehhh actually use interactions since idk how to do slash commands
# with discord2.0 yet...
if socket.gethostname() == "MB-145.local":
  sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
else:
  sys.path.append("/root/ToServer/interactions-ryanjsfx")
# end if/else
import interactions
from interactions.client import get

## bot invite link
## scopes: bot + application.commands
## bot permissions: 1) read messages/view channels, 2) send messages, 3) embed links, 4) read message history
## https://discord.com/api/oauth2/authorize?client_id=1011037304778928129&permissions=84992&scope=bot%20applications.commands

class OrigoDiscordBot(object):
    def __init__(self):
        self.GIDS = [931482273440751638] # ToTheMoonsNFT

        self.LOG_CID = 932056137518444594 # ToTheMoonsNFT Bot-CIDs

        self.QS = 0.01

        self.BOT_NAME = "Origo Bot (WILL NEVER DM YOU)"
        self.FOOTER   = "Built for Origo, powered by @TheLunaLabs"
        self.CMD_PREFIX = "origo"

        self.init_gsheet()
        self.init_embeds()
    # end __init__

    def init_gsheet(self):
        gc = gspread.service_account(filename="/Users/ryanjsfx/.config/gspread/origo/service_account.json")
        sh = gc.open("origo-wl-check")
        self.worksheet = sh.get_worksheet(0)
    # end init_gsheet

    def init_embeds(self):
        self.URL = "https://cdn.discordapp.com/icons/949922677521522778/7924d7e3c272fd29119df7e613bdae5e.webp?size=160"

        TITLE = "__Help Menu__"
        DESCRIPTION = "Hi! I am " + self.BOT_NAME + " developed by @TheLunaLabs © 2022"
        DESCRIPTION += ".\n Below are my commands which are case insensitive: "

        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedInt.set_footer(text = self.FOOTER, icon_url=self.URL)

        embedInt.add_field(name="**/" + self.CMD_PREFIX + " help**", 
                           value="Display this help menu", inline=True)
        embedInt.add_field(name="**/" + self.CMD_PREFIX + " wallet_check**", 
                           value="Check if your Ethereum wallet address is in our records", 
                           inline=False)
        self.helpEmbedInt = embedInt

        embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
        embedInt.set_footer(text = self.FOOTER, icon_url=self.URL)
    # end init_embeds

    async def get_addresses(self):
        print("BEGIN get_addresses")
        try:
            gsheet = self.worksheet.get_all_values()
        except Exception as err:
            print("30 err: ", err)
            print("31 err.args: ", err.args[:])
            msg = "32 err_arg: error getting gsheet!"

            print(msg)
            await self.channel_log.send(msg)
            return False
        # end try/except

        addresses = []
        for row in gsheet:
            addresses.append(row[0])
        # end for

        self.addresses = addresses
        print("SUCCESS get_addresses")
        return True
    # end get_addresses

    def discord_bot(self):
        client = discord.Client()
        secret = os.environ.get("origoBotPass")
        intBot = interactions.Client(secret)

        @client.event
        async def on_ready():
            print("ready!")

            self.channel_log = client.get_channel(self.LOG_CID)

            await self.channel_log.send("ready!")
            await self.get_addresses()
        # end on_ready

        @intBot.command(
            name="origo",
            description="Origo WL Bot Commands",
            scope=self.GIDS,
            options = [
                interactions.Option(
                    name="help",
                    description="Displays help menu",
                    type=interactions.OptionType.SUB_COMMAND,
                ),
                interactions.Option(
                    name="refresh",
                    description="Fetches latest list of wallets from our records",
                    type=interactions.OptionType.SUB_COMMAND,
                ),
                interactions.Option(
                    name="check_wallet",
                    description="Checks if wallet is in our records",
                    type=interactions.OptionType.SUB_COMMAND,
                    options=[
                        interactions.Option(
                            name="wallet_address",
                            description="Ethereum wallet address to check if it is in our database",
                            type=interactions.OptionType.STRING,
                            required=True,
                        ),
                    ],
                ),
            ],
        )
        async def cmd(ctx: interactions.CommandContext, sub_command: str,
                      wallet_address: str=None):
            print("begin cmd for sub_command: ", sub_command)

            if sub_command == "help":
                await ctx.send(embeds=self.helpEmbedInt, ephemeral=True)

            elif sub_command == "refresh":
                await ctx.send("fetching latest list of wallets from our database, this can take up to 30 seconds", ephemeral=True)
                result = await self.get_addresses()

                if result:
                    await ctx.send("succeeded fetching addresses!", ephemeral=True)

                else:
                    await ctx.send("error fetching addresses, please try again in a moment.\nIf you tried a few times already, please contact the developer @TheLunaLabs", ephemeral=True)
                # end if/else

            elif sub_command == "check_wallet":
                if wallet_address in self.addresses:
                    await ctx.send("SUCCESS!\n" + wallet_address + " **is** in our records!", ephemeral=True)

                else:
                    await ctx.send("WARNING!\n" + wallet_address + " **not** in our records!", ephemeral=True)
                # end if/else
            # end if/elif

            return
        # end cmd
        loop = asyncio.get_event_loop()

        task2 = loop.create_task(client.start(secret))
        task1 = loop.create_task(intBot._ready())

        gathered = asyncio.gather(task1, task2, loop=loop)
        loop.run_until_complete(gathered)
    # end discord_bot
# end FractalzDiscordBot

if __name__ == "__main__":
    origo = OrigoDiscordBot()
    origo.discord_bot()
## end fractalz.py

