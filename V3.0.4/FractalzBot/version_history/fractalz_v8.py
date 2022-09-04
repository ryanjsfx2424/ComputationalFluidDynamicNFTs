import os
import sys
import ast
import random
import socket
import discord
import asyncio
import gspread

if socket.gethostname() == "MB-145.local":
  sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
else:
  sys.path.append("/root/ToServer/interactions-ryanjsfx")
# end if/else
import interactions
from interactions.client import get

class FractalzDiscordBot(object):
    def __init__(self):
        self.LOG_CID = 932056137518444594
        self.BOT_CIDS = [932056137518444594]
        self.GIDS = [931482273440751638, # toTheMoons
                     902886970383040512] # FRACTALZ

        self.paused = True

        self.approved_users = [855616810525917215, # me
                               399985291135549442] # liamptd

        self.QS = 0.01

        self.fname_settings = "settings_fractalz.txt"

        self.cmd_names = ["?repair"]
        self.cmd_msgs = [["Success - you've repaired the module, role 'Authenticated' granted", "Failure to fix space station modules"]]
        self.success_rates = [[0.1, 1.0]]
        self.roles_awarded = [[979452786355867679, ""]]
        self.roles_removed = [["",""]]

        #self.init_gsheet()
        self.init_settings()
    # end __init__

    def init_gsheet(self):
        gc = gspread.service_account(filename="/Users/ryanjsfx/.config/gspread/fractalz/service_account.json")
        sh = gc.open("fractalz-atlas-settings")
    # end init_gsheet

    async def get_settings(self):
        ## maximum 100 commands atm
        for ii in range(100):
            try:
                worksheet = sh.get_worksheet(ii)
            except:
                break
            # end try/except

            gsheet = worksheet.get_all_values()

            cmd_msgs = []
            success_rates = []
            roles_awarded = []
            roles_removed = []
            for row in gsheet:
                cmd_msgs.append(     row[1])
                success_rates.append(row[2])
                roles_awarded.append(row[3])
                roles_removed.append(row[4])
            # end for
            self.cmd_names.append(worksheet.title)
            self.cmd_msgs.append(cmd_msgs)
            self.success_rates.append(success_rates)
            self.roles_awarded.append(roles_awarded)
            self.roles_removed.append(roles_removed)
        # end for ii

        self.settings = settings
    # end get_settings

    def init_settings(self):
        if os.path.exists(self.fname_settings) and os.stat(self.fname_settings).st_size != 0:
            with open(self.fname_settings, "r") as fid:
                lines = fid.readlines()
                self.cmd_names     = ast.literal_eval(lines[0])
                self.cmd_msgs      = ast.literal_eval(lines[1])
                self.success_rates = ast.literal_eval(lines[2])
                self.roles_awarded = ast.literal_eval(lines[3])

                if "," in lines[4]:
                    self.roles_removed = ast.literal_eval(lines[4])
                else:
                    self.roles_removed = ast.literal_eval(lines[3])
                    for ii in range(len(self.roles_removed)):
                        for jj in range(len(self.roles_removed[ii])):
                            self.roles_removed[ii][jj] = ""
                        # end for
                    # end for
                # end if/else

                if "True" in lines[-1]:
                    self.paused = True
                else:
                    self.paused = False
                # end if/else
            # end with open
        # end if
    # end init_settings

    def discord_bot(self):
        client = discord.Client()
        secret = os.environ.get("fracBotPass")
        intBot = interactions.Client(secret)

        @client.event
        async def on_ready():
           print("ready!")
           pfp_path = "atlas_pfp.png"
           with open(pfp_path, "rb") as pfp:
               await client.user.edit(password=secret, avatar=pfp.read())
           # end with open
           channel = client.get_channel(self.LOG_CID)
           self.channel_log = channel
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
                print("ii: ", ii)
                msg = message.content.replace(" ","")
                if msg == cmd_name:
                    roll = random.random()
                    print("roll: ", roll)
                    for jj in range(len(self.cmd_msgs[ii])):
                        await asyncio.sleep(self.QS)
                        print("jj: ", jj)
                        if roll <= self.success_rates[ii][jj]:
                            if self.roles_awarded[ii][jj] != "":
                                member = message.author
                                guild = client.get_guild(message.guild.id)
                                role  = guild.get_role(self.roles_awarded[ii][jj])
                                if role not in member.roles:
                                    await member.add_roles(role)
                                # end if
                            # end if
                            await channel.send(self.cmd_msgs[ii][jj])
                            
                            #embedDpy = discord.Embed(title=TITLE, description=DESCRIPTION, color=discord.Color.blue())
                            #embedDpy.set_footer(text = "Built for FRACTALZ, Powered by @TheLunaLabs",
                            #                icon_url=self.URL)
                            #embedDpy.add_field(name="**__!rttrank <username>__**", value="Display user's points, likes, etc.", inline=False)
                            return
                        else:
                            if self.roles_removed[ii][jj] != "":
                                member = message.author
                                guild = client.get_guild(message.guild.id)
                                role  = guild.get_role(self.roles_awarded[ii][jj])
                                if role in member.roles:
                                    await member.remove_roles(role)
                                # end if
                    # end for
                    await asyncio.sleep(0.1)
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
            print("begin activate command")
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
                    name="msgs",
                    description="Message(s) issued when users 'succeed'",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="roles_awarded",
                    description="Role(s) awarded when users 'succeed'",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="roles_removed",
                    description="Role(s) removed when users 'succeed'",
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
                            name:    str = None,
                            msgs:    str = None,
                            roles_awarded: str = None,
                            roles_removed: str = None,
                            rates:   str = None,
                            ):
            print("begin command command")
            if ( oldname  == None and \
                    name  == None and \
                    msgs  == None and \
                    roles_awarded == None and \
                    roles_removed == None and \
                    rates == None):
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
                    self.cmd_msgs.append([])
                    self.roles_awarded.append([])
                    self.success_rates.append([])
                    await ctx.send("Added command name: " + self.cmd_names[-1] + "\n\n", ephemeral=True)
                else:
                    self.cmd_names[index] = name
                    await ctx.send("Updated command name to: " + self.cmd_names[index] + "\n\n", ephemeral=True)
                # end if/else

            if msgs != None:
                if "; " in msgs:
                    msgs = msgs.split("; ")
                else:
                    msgs = [msgs]
                # end if/else

                if oldname == None:
                    self.cmd_msgs[-1] = msgs
                    await ctx.send("Added success message(s) to: " + str(self.cmd_msgs[-1]) + "\n\n", ephemeral=True)
                else:
                    self.cmd_msgs[index] = msgs
                    await ctx.send("Updated success message(s) to: " + str(self.cmd_msgs[index]) + "\n\n", ephemeral=True)
                # end if/else
                
            if roles_awarded != None:
                if "; " in roles_awarded:
                    roles_awarded = roles_awarded.split("; ")
                else:
                    roles_awarded = [roles_awarded]
                # end if/else

                roles_arr = []
                flag = True
                for role in roles_awarded:
                    await asyncio.sleep(self.QS)
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

                if flag:
                    if oldname == None:
                        self.roles_awarded[-1] = roles_arr
                        await ctx.send("Added the following role(s) to award on command success: " + str(self.roles_awarded[-1]) + "\n\n", ephemeral=True)
                    else:
                        self.roles_awarded[index] = roles_arr
                        await ctx.send("Updated the following role(s) to award on command success: " + str(self.roles_awarded[index]) + "\n\n", ephemeral=True)
                    # end if/else
                # end if

            if roles_removed != None:
                if "; " in roles_removed:
                    roles_removed = roles_removed.split("; ")
                else:
                    roles_removed = [roles_removed]
                # end if/else

                roles_arr = []
                flag = True
                for role in roles_removed:
                    await asyncio.sleep(self.QS)
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

                if flag:
                    if oldname == None:
                        self.roles_removed[-1] = roles_arr
                        await ctx.send("Added the following role(s) to award on command success: " + str(self.roles_removed[-1]) + "\n\n", ephemeral=True)
                    else:
                        self.roles_removed[index] = roles_arr
                        await ctx.send("Updated the following role(s) to award on command success: " + str(self.roles_removed[index]) + "\n\n", ephemeral=True)
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
                    await asyncio.sleep(self.QS)
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
                        try:
                          self.success_rates[index] = rates_arr
                        except Exception as err:
                          print("330 err: ", err)
                          print("331 err.args: ", err.args[:])
                          print("Traceback")
                          await ctx.send("Index out of bounds error assigning rates to the success_rates.")
                          return
                        await ctx.send("Updated the following success rate(s) to issue command success: " + str(self.success_rates[index]) + "\n\n", ephemeral=True)
                    # end if/else
                # end if
            # end if

            bad_iis = []
            for ii in range(len(self.cmd_names)):
                await asyncio.sleep(self.QS)
                mask = (len(self.cmd_msgs[ii]) == len(self.success_rates[ii])) and \
                       (len(self.cmd_msgs[ii]) == len(self.roles_awarded[ii])) and \
                       (len(self.cmd_msgs[ii]) == len(self.roles_removed[ii]))
                if not mask:
                    bad_iis.append(ii)
                # end if
            # end for ii

            for ii in bad_iis[::-1]:
                await asyncio.sleep(self.QS)
                msg = "Sorry, the number of successmsgs, failmsgs, rates, and roles did not match.\n\n"
                msg += "This was the command: " + str(self.cmd_names[ii]) + "\n\n"
                msg += "msgs: " + str(self.cmd_msgs[ii]) + "\n\n"
                msg += "rates: " + str(self.success_rates[ii]) + "\n\n"
                msg += "rolesA: " + str(self.roles_awarded[ii]) + "\n\n"
                msg += "rolesR: " + str(self.roles_removed[ii]) + "\n\n"
                await ctx.send(msg)

                del self.cmd_names[ii]
                del self.cmd_msgs[ ii]
                del self.success_rates[ii]
                del self.roles_awarded[ii]
                del self.roles_removed[ii]
            # end for ii

            with open(self.fname_settings, "w") as fid:
                fid.write(str(self.cmd_names)     + "\n")
                fid.write(str(self.cmd_msgs )     + "\n")
                fid.write(str(self.success_rates) + "\n")
                fid.write(str(self.roles_awarded) + "\n")
                fid.write(str(self.roles_removed) + "\n")
                print(str(self.roles_removed) + "\n")
                fid.write(str(self.paused))
            # end with open

            return
        # end command

        @intBot.command(
            name="remove_command",
            description="remove text command",
            scope=self.GIDS,
            options = [
                interactions.Option(
                    name="name",
                    description="Existing command name to delete",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
            ]
        )
        async def command(ctx: interactions.CommandContext, 
                          name: str):
            if ctx.author.id not in self.approved_users:
                await ctx.send("WARNING! Non-approved user tried to activate me.")
                return
            # end if

            index = -11
            for ii in range(len(self.cmd_names)):
                await asyncio.sleep(self.QS)
                if name == self.cmd_names[ii]:
                    index = ii
                # end if
            # end for
            if index == -11:
                msg = "Sorry, I couldn't find 'name' in the list of existing commands.\n\n"
                msg += "This is what I received: " + name + "\n\n"
                msg += "And these are the commands I know about: " + str(self.cmd_names)
                await ctx.send(msg, ephemeral=True)
            # end if
            try:
                del self.cmd_names[    index]
                del self.cmd_msgs[     index]
                del self.success_rates[index]
                del self.roles_awarded[index]
                del self.roles_removed[index]
            except Exception as err:
                print("417 err: ", err)
                print("418 err.args: ", err.args[:])
                print("419 Traceback, error deleting a command for index: ", index)
                print("and name: ", name)
                await ctx.send("An error occurred wile trying to delete that command. Plz contact the dev.")
            # end try/excpet
            await ctx.send("Successfully removed command: ", name)
            return
        # end remove_command

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

