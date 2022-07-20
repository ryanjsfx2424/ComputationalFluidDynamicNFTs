import os
import sys
import random
import discord
import asyncio

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions.client import get

class FractalzDiscordBot(object):
    def __init__(self):
        self.LOG_CID = 932056137518444594
        self.BOT_CIDS = [932056137518444594]
        self.ROLE = 0
        self.GIDS = [931482273440751638]#, # toTheMoons
                     #902886970383040512] # FRACTALZ

        self.paused = True

        self.approved_users = [855616810525917215, # me
                               399985291135549442] # liamptd

        self.cmd_name = "?repair"
        self.cmd_success = "Success - you've repaired the module, role 'Authenticated' granted"
        self.cmd_fail = "Failure to fix space station modules"
        self.success_rate = 0.1
    # end __init__

    def discord_bot(self):
        client = discord.Client()
        secret = os.environ.get("fracBotPass")
        intBot = interactions.Client(secret)

        @client.event
        async def on_ready():
           print("ready!")
           channel = client.get_channel(self.LOG_CID)
           await channel.send("Greetings, FRACTALZ!")

        @client.event
        async def on_message(message):
            channel_log = client.get_channel(self.LOG_CID)
            if message.channel.id not in self.BOT_CIDS:
               await channel_log.send("channel id not in BOT_CIDS!")
               await channel_log.send("msg channel id: " + str(message.channel.id))
               await channel_log.send("self.BOT_CIDS: " + str(self.BOT_CIDS)) 
            # end if

            if message.author == client.user:
                return
            # end if

            if self.paused:
                await channel_log.send("we are paused!" + str(self.paused))
                return
            # end if
            if message.content.startswith(self.cmd_name):
                channel = client.get_channel(message.channel.id)
                
                roll = random.random()
                if roll < self.success_rate:
                    member = message.author
                    guild = client.get_guild(self.GID)
                    role  = guild.get_role(self.ROLE)
                    if role not in member.roles:
                        await member.add_roles(role)
                    await channel.send(self.cmd_success)
                else:
                    await channel.send(self.cmd_fail)
                # end if/else
            # end if
        # end on_message

        @intBot.command(
            name="activate",
            description="Activates the bot for a given channel",
            scope=self.GIDS,
            options = [
                interactions.Option(
                name="channel",
                description="channel id for bot commands",
                type=interactions.OptionType.STRING,
                required=True,
                ),
            ],
        )
        async def activate(ctx: interactions.CommandContext, 
                               channel: str):
      
            if ctx.author.id not in self.approved_users:
                await ctx.send("WARNING! Non-approved user tried to activate me.")
                return
            # end if

            try:
                channel = int(float(channel))
            except Exception as err:
                print("83 err: ", err)
                print("84 err.args: ", err.args[:])
                await ctx.send("Sorry, I couldn't parse the 'channel' as an integer. Use 'copy id' when right clicking the channel to get it's id :)",
                ephemeral=True)
            # end try/except

            if channel in self.BOT_CIDS:
                self.paused = False
                await ctx.send("I am already activated for that channel :)", ephemeral=True)
                return
            # end if
            try:
                await ctx.send("I am now activated in channel: " + str(channel))
                self.BOT_CIDS.append(channel)
                self.paused = False
            except Exception as err:
                print("98 err: ", err)
                print("99 err.args: ", err.args[:])
                await ctx.send("Sorry, I can't find the channel you passed.  Use 'copy id' when right clicking the channel to get it's id :)",
                    ephemeral=True)
            # end try/except
            return
        # end authenticate

        @intBot.command(
            name="command",
            description="Modify repair command",
            scope=self.GIDS,
            options = [
                interactions.Option(
                    name="name",
                    description="Command that users type",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="success",
                    description="Message issued when users succeed",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="fail",
                    description="Message issued when users fail",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="role",
                    description="Role awarded when users succeed",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="rate",
                    description="Rate user succeeds at task",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
            ],
        )
        async def command(ctx: interactions.CommandContext, 
                            name: str = None,
                            success: str = None,
                            fail: str = None,
                            role: str = None,
                            rate: str = None,
                            ):
            if (    name == None and \
                 success == None and \
                    fail == None and \
                    role == None and \
                    rate == None):
                await ctx.send("Sorry, I didn't notice the use of any options. Try again using one of the options.", ephmeral=True)
                return
            # end if
      
            if ctx.author.id not in self.approved_users:
                await ctx.send("WARNING! Non-approved user tried to activate me.")
                return
            # end if

            msg = ""
            if name != None:
                self.cmd_name = name
                await ctx.send("Updated command name to: " + self.cmd_name + "\n\n", ephemeral=True)
            if success != None:
                self.cmd_success = success
                await ctx.send("Updated success to: " + self.cmd_success + "\n\n", ephemeral=True)
            if fail != None:
                self.cmd_fail = fail
                await ctx.send("Updated fail to: " + self.cmd_fail + "\n\n", ephemeral=True)
            if role != None:
                try:
                    self.ROLE = int(float(role))
                    await ctx.send("Updated role awarded to <@&" + str(self.ROLE) + ">", ephemeral=True)
                except Exception as err:
                    print("181 err: ", err)
                    print("182 err.args: ", err.args[:])
                    await ctx.send("Sorry, I couldn't parse the 'role' option as an integer", ephemeral=True)
                # end try/except
            if rate != None:
                try:
                    self.success_rate = float(rate)
                    await ctx.send("Updated success rate to " + str(self.success_rate) + "", ephemeral=True)
                except Exception as err:
                    print("192 err: ", err)
                    print("193 err.args: ", err.args[:])
                    await ctx.send("Sorry, I couldn't parse the 'rate' option as a decimal.", ephemeral=True)
                # end try/except
            # end if
            return
        # end authenticate

        loop = asyncio.get_event_loop()

        task2 = loop.create_task(client.start(os.environ.get("fracBotPass")))
        task1 = loop.create_task(intBot._ready())

        gathered = asyncio.gather(task1, task2, loop=loop)
        loop.run_until_complete(gathered)
    # end discord_bot
# end FractalzDiscordBot

if __name__ == "__main__":
    frac = FractalzDiscordBot()
    frac.discord_bot()
## end fractalz.py