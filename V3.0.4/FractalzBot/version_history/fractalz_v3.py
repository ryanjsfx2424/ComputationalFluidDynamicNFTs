import os
import sys
import ast
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
        self.GIDS = [931482273440751638]#, # toTheMoons
                     #902886970383040512] # FRACTALZ

        self.paused = True

        self.approved_users = [855616810525917215, # me
                               399985291135549442] # liamptd

        self.fname_settings = "settings_fractalz.txt"

        self.cmd_names = ["?repair"]
        self.cmd_successes = [["Success - you've repaired the module, role 'Authenticated' granted"]]
        self.cmd_fails = [["Failure to fix space station modules"]]
        self.success_rates = [[0.1]]
        self.roles_awarded = [[979452786355867679]]

        if os.path.exists(self.fname_settings) and os.stat(self.fname_settings).st_size != 0:
            with open(self.fname_settings, "r") as fid:
                lines = fid.readlines()
                self.cmd_names     = ast.literal_eval(lines[0])
                self.cmd_successes = ast.literal_eval(lines[1])
                self.cmd_fails     = ast.literal_eval(lines[2])
                self.success_rates = ast.literal_eval(lines[3])
                self.roles_awarded = ast.literal_eval(lines[4])
                print("self.cmd_names: ", self.cmd_names)
                if "True" in lines[5]:
                    print("paused True")
                    self.paused = True
                else:
                    print("paused False")
                    self.paused = False
                # end if/else
            # end with open
        # end if
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
            channel = client.get_channel(message.channel.id)
            for ii,cmd_name in enumerate(self.cmd_names):
                msg = message.content.replace(" ","")
                if msg == cmd_name:
                    print("len cmd successes: ", len(self.cmd_successes))
                    for jj in range(len(self.cmd_successes[ii])):
                        roll = random.random()
                        print("roll: ", roll)
                        if roll < self.success_rates[ii][jj]:
                            if self.roles_awarded[ii][jj] != "":
                                member = message.author
                                guild = client.get_guild(message.guild.id)
                                print("ii,jj: ", ii,jj)
                                print("self.roles_awarded[ii][jj]: ", self.roles_awarded[ii][jj])
                                role  = guild.get_role(self.roles_awarded[ii][jj])
                                if role not in member.roles:
                                    print("role: ", role)
                                    print("role.id: ", role.id)
                                    await member.add_roles(role)
                                # end if
                            # end if
                            await channel.send(self.cmd_successes[ii][jj])
                        else:
                            await channel.send(self.cmd_fails[ii][jj])
                        # end if/else
                        await asyncio.sleep(0.1)
                    # end for
                # end if
            # end for
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
                await ctx.send("I am now activated in channel: " + str(channel), ephemeral=True)
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
            description="Add/Modify text command",
            scope=self.GIDS,
            options = [
                interactions.Option(
                    name="oldname",
                    description="Existing command name that users type",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="name",
                    description="New command that users will type",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="successmsgs",
                    description="Message(s) issued when users succeed",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="failmsgs",
                    description="Message(s) issued when users fail",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="roles",
                    description="Role(s) awarded when users succeed",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="rates",
                    description="Rate(s) user succeeds at task",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
            ],
        )
        async def command(ctx: interactions.CommandContext, 
                            oldname: str = None,
                            name: str = None,
                            successmsgs: str = None,
                            failmsgs: str = None,
                            roles: str = None,
                            rates: str = None,
                            ):
            if ( oldname     == None and \
                    name     == None and \
                 successmsgs == None and \
                    failmsgs == None and \
                    roles    == None and \
                    rates    == None):
                await ctx.send("Sorry, I didn't notice the use of any options. Try again using one of the options.", ephemeral=True)
                return
            # end if
      
            if ctx.author.id not in self.approved_users:
                await ctx.send("WARNING! Non-approved user tried to activate me.")
                return
            # end if

            if oldname != None:
                index = -11
                for ii in range(len(self.cmd_names)):
                    if oldname == self.cmd_names[ii]:
                        index = ii
                    # end if
                # end for
                if index == -11:
                    msg = "Sorry, I couldn't find 'oldname' in the list of existing commands.\n\n"
                    msg += "This is what I received: " + oldname + "\n\n"
                    msg += "And these are the commands I know about: " + str(self.cmd_names)
                    await ctx.send(msg, ephemeral=True)
                # end if
            # end if/else

            msg = ""
            if name != None:
                if oldname == None:
                    self.cmd_names.append(name)
                    self.cmd_successes.append([])
                    self.cmd_fails.append([])
                    self.roles_awarded.append([])
                    self.success_rates.append([])
                    await ctx.send("Added command name: " + self.cmd_names[-1] + "\n\n", ephemeral=True)
                else:
                    self.cmd_names[index] = name
                    await ctx.send("Updated command name to: " + self.cmd_names[index] + "\n\n", ephemeral=True)
                # end if/else
            if successmsgs != None:
                if "; " in successmsgs:
                    successmsgs = successmsgs.split("; ")
                else:
                    successmsgs = [successmsgs]
                # end if/else

                if oldname == None:
                    self.cmd_successes[-1] = successmsgs
                    await ctx.send("Added success message(s) to: " + str(self.cmd_successes[-1]) + "\n\n", ephemeral=True)
                else:
                    self.cmd_successes[index] = successmsgs
                    await ctx.send("Updated success message(s) to: " + str(self.cmd_successes[index]) + "\n\n", ephemeral=True)
                # end if/else
                
            if failmsgs != None:
                if "; " in failmsgs:
                    failmsgs = failmsgs.split("; ")
                else:
                    failmsgs = [failmsgs]
                # end if/else

                if oldname == None:
                    self.cmd_fails[-1] = failmsgs
                    await ctx.send("Added failure message(s) to: " + str(self.cmd_fails[-1]) + "\n\n", ephemeral=True)
                else:
                    self.cmd_fails[index] = failmsgs
                    await ctx.send("Updated failure message(s) to: " + str(self.cmd_fails[index]) + "\n\n", ephemeral=True)
                # end if/else
            if roles != None:
                if "; " in roles:
                    roles = roles.split("; ")
                else:
                    roles = [roles]
                # end if/else

                roles_arr = []
                flag = True
                for role in roles:
                    if role == "None":
                        roles_arr.append("")
                        continue
                    # end if

                    try:
                        roles_arr.append(int(role))
                    except Exception as err:
                        print("258 err: ", err)
                        print("2592 err.args: ", err.args[:])
                        await ctx.send("Sorry, I couldn't parse (one of) the 'role' option as an integer", ephemeral=True)
                        flag = False
                    # end try/except
                # end for
                print("roles_arr: ", roles_arr)
                if flag:
                    print('flag is true!')
                    if oldname == None:
                        self.roles_awarded[-1] = roles_arr
                        await ctx.send("Added the following role(s) to award on command success: " + str(self.roles_awarded[-1]) + "\n\n", ephemeral=True)
                    else:
                        self.roles_awarded[index] = roles_arr
                        await ctx.send("Updated the following role(s) to award on command success: " + str(self.roles_awarded[index]) + "\n\n", ephemeral=True)
                    # end if/else
                # end if
            if rates != None:
                if "; " in rates:
                    rates = rates.split("; ")
                else:
                    rates = [rates]
                # end if/else

                rates_arr = []
                flag = True
                for rate in rates:
                    try:
                        rates_arr.append(float(rate))
                    except Exception as err:
                        print("287 err: ", err)
                        print("288 err.args: ", err.args[:])
                        await ctx.send("Sorry, I couldn't parse (one of) the 'rates' option as a decimal", ephemeral=True)
                        flag = False
                    # end try/except
                # end for

                if flag:
                    if oldname == None:
                        self.success_rates[-1] = rates_arr
                        await ctx.send("Added the following success rate(s) to issue command success: " + str(self.success_rates[-1]) + "\n\n", ephemeral=True)
                    else:
                        self.success_rates[index] = rates_arr
                        await ctx.send("Updated the following success rate(s) to issue command success: " + str(self.success_rates[index]) + "\n\n", ephemeral=True)
                    # end if/else
                # end if
            # end if

            bad_iis = []
            for ii in range(len(self.cmd_names)):
                mask = (len(self.cmd_successes[ii]) == len(self.cmd_fails[ii])) and \
                       (len(self.cmd_successes[ii]) == len(self.success_rates[ii])) and \
                       (len(self.cmd_successes[ii]) == len(self.roles_awarded[ii]))
                if not mask:
                    bad_iis.append(ii)
                # end if
            # end for ii

            for ii in bad_iis[::-1]:
                msg = "Sorry, the number of successmsgs, failmsgs, rates, and roles did not match.\n\n"
                msg += "This was the command: " + str(self.cmd_names[ii]) + "\n\n"
                msg += "successmsgs: " + str(self.cmd_successes[ii]) + "\n\n"
                msg += "failmsgs: " + str(self.cmd_fails[ii]) + "\n\n"
                msg += "rates: " + str(self.rates[ii]) + "\n\n"
                msg += "roles: " + str(self.roles_awarded[ii]) + "\n\n"
                await ctx.send(msg)

                del self.cmd_names[ii]
                del self.cmd_successes[ii]
                del self.cmd_fails[ii]
                del self.success_rates[ii]
                del self.roles_awarded[ii]
            # end for ii

            with open(self.fname_settings, "w") as fid:
                fid.write(str(self.cmd_names)     + "\n")
                fid.write(str(self.cmd_successes) + "\n")
                fid.write(str(self.cmd_fails)     + "\n")
                fid.write(str(self.success_rates) + "\n")
                fid.write(str(self.roles_awarded) + "\n")
                print(str(self.roles_awarded) + "\n")
                fid.write(str(self.paused))
            # end with open

            return
        # end command

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
