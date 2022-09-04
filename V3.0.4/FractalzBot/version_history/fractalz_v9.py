## invite link
## scopes (3): 1) guild.members.read, bot, application.commands
## perms (4): 1) manage roles, 2) read messages/view channels, 3) send messages, 4) read message history
## https://discord.com/api/oauth2/authorize?client_id=998319674632712283&permissions=268504064&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorized&response_type=code&scope=guilds.members.read%20bot%20applications.commands
## channel perms (3): 1) view channel, 2) send messages, 3) read message history
## use old-discord env on Mac; Fractalz on hostwinds

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
        self.BOT_CIDS = [932056137518444594, ] # TTM, Fractalz
        self.GIDS = [931482273440751638, # toTheMoons
                     902886970383040512] # FRACTALZ

        if socket.gethostname() == "MB-145.local":
            self.gc = gspread.service_account(filename="/Users/ryanjsfx/.config/gspread/fractalz/service_account.json")
        else:
            self.gc = gspread.service_account(filename="/root/.config/gspread/fractalz/service_account.json")
        # end if/else

        self.approved_users = [855616810525917215, # me
                               399985291135549442] # liamptd

        self.fname = "cids.txt"

        self.QS = 0.01
        self.LS = 60.1

        self.cmd_names = ["?repair"]
        self.cmd_msgs = [["Success - you've repaired the module, role 'Authenticated' granted", "Failure to fix space station modules"]]
        self.success_rates = [[0.1, 1.0]]
        self.roles_awarded = [[979452786355867679, ""]]
        self.roles_removed = [["",""]]

        self.init_cids()
    # end __init__

    def init_cids(self):
        if (not os.path.exists(self.fname)) or (os.stat(self.fname).st_size == 0):
            return
        # end if

        with open(self.fname, "r") as fid:
            lines = fid.read()
        # end with

        for line in lines:
            cid = int(line.replace("\n",""))
            if cid not in self.BOT_CIDS:
                self.BOT_CIDS.append(cid)
            # end if
        # end for lines
    # end init_cids

    def save_cids(self):
        with open("temp.txt", "w") as fid:
            for cid in self.BOT_CIDS:
                fid.write(str(cid) + "\n")
            # end for
        # end with
        os.system("cp temp.txt " + self.fname)
    # end save_cids

    async def get_settings(self):
        ## maximum 100 commands atm
        sh = self.gc.open("fractalz-atlas-settings")
        for ii in range(100):
            print("ii: ", ii)
            try:
                worksheet = sh.get_worksheet(ii)
            except:
                break
            # end try/except
            print("worksheet.title: ", worksheet.title)

            gsheet = worksheet.get_all_values()

            cmd_msgs      = []
            success_rates = []
            roles_awarded = []
            roles_removed = []
            for jj,row in enumerate(gsheet):
                if jj == 0:
                    continue ## header
                # end if

                if row[0] == "END":
                    break

                cmd_msg = row[1]
                awarded = row[2]
                removed = row[3]
                success_rate = float(row[4])

                if awarded != "":
                    awarded = int(awarded)
                if removed != "":
                    removed = int(removed)
                # end ifs

                try:
                    cmd_msg = row[1]
                    awarded = row[2]
                    removed = row[3]
                    success_rate = float(row[4])

                    if awarded != "":
                        awarded = int(awarded)
                    if removed != "":
                        removed = int(removed)
                    # end ifs
                except:
                    print("72 exception")
                    print("row: ", row)
                    input(">>")
                    continue
                # end try/except

                cmd_msgs.append(cmd_msg)
                success_rates.append(success_rate)
                roles_awarded.append(awarded)
                roles_removed.append(removed)
            # end for

            title = worksheet.title

            if title in self.cmd_names:
                ind = self.cmd_names.index(title)
                del self.cmd_names[ind]
                del self.cmd_msgs[ind]
                del self.success_rates[ind]
                del self.roles_awarded[ind]
                del self.roles_removed[ind]
            # end if

            self.cmd_names.append(worksheet.title)
            self.cmd_msgs.append(cmd_msgs)
            self.success_rates.append(success_rates)
            self.roles_awarded.append(roles_awarded)
            self.roles_removed.append(roles_removed)
        # end for ii
        print("SUCCESS get_settings!")
    # end get_settings

    def discord_bot(self):
        client = discord.Client()
        secret = os.environ.get("fracBotPass")
        intBot = interactions.Client(secret)

        @client.event
        async def on_ready():
            print("ready!")

            channel = client.get_channel(self.LOG_CID)
            self.channel_log = channel
            await channel.send("Greetings, FRACTALZ!")

            wcnt = 0
            while True:
                wcnt += 1; print("on_ready wcnt: ", wcnt)
                await self.get_settings()
                await asyncio.sleep(self.LS)
            # end while True
        # end on_ready

        @client.event
        async def on_message(message):
            channel_log = client.get_channel(self.LOG_CID)

            if message.channel.id not in self.BOT_CIDS:
                return
            # end if

            if message.author == client.user:
                return
            # end if

            channel = client.get_channel(message.channel.id)
            for ii,cmd_name in enumerate(self.cmd_names):
                print("ii: ", ii)
                await asyncio.sleep(self.QS)

                msg = message.content.replace(" ","").replace("\n","")
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

                                if hasattr(role, "id") == False:
                                    await self.channel_log.send("Error! Guild " + message.guild.name + ", does not have role id " 
                                        + str(self.roles_awarded[ii][jj]) + " from command: " + cmd_name)
                                else:
                                    if role not in member.roles:
                                        await member.add_roles(role)
                                    # end if
                                # end if/else
                            # end if

                            await channel.send(self.cmd_msgs[ii][jj])
                            return
                        else:
                            if self.roles_removed[ii][jj] != "":
                                member = message.author

                                guild = client.get_guild(message.guild.id)
                                role  = guild.get_role(self.roles_removed[ii][jj])

                                if hasattr(role, "id") == False:
                                    await self.channel_log.send("Error! Guild " + message.guild.name + ", does not have role id " 
                                        + str(self.roles_removed[ii][jj]) + " from command: " + cmd_name)
                                else:
                                    if role in member.roles:
                                        await member.remove_roles(role)
                                    # end if
                                # end if/else
                            # end if
                        # end if/else
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
                await ctx.send("I am already activated for that channel :)", ephemeral=True)
                return
            # end if

            self.BOT_CIDS.append(channel)
            self.save_cids()
            await ctx.send("I am now activated in channel: " + str(channel), ephemeral=True)
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