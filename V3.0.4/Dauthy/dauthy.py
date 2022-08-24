## dauthy.py by @TheLunaLabs (Twitter) Copyright 2022
## url invite link set up:
## scopes: bot, application.commands, guilds.members.read
## redirect url: https://www.rootroop.com/
## permissions: 1) read/view messages, 2) send messages, 3) embed links, 
## 4) attach files, 5) manage roles, 6) read message history
## https://discord.com/api/oauth2/authorize?client_id=979391724734521354&permissions=268553216&scope=bot%20applications.commands
import os
import sys
import ast
import time
import pyotp
import qrcode
import socket
import asyncio
from PIL import Image
from cryptography.fernet import Fernet


if socket.gethostname() == "MB-145.local":
  sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
  gname = "/Users/ryanjsfx/.config/gspread/origo/service_account.json"
else:
  sys.path.append("/root/ToServer/interactions-ryanjsfx")
  gname = "/root/.config/gspread/origo/service_account.json"

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions.client import get
from interactions.ext.files import command_send

class AuthenticationDiscordBot(object):
  def __init__(self):
    self.BOT_NAME = "Dauthy"
    self.FOOTER   = "Built for Roo Tech, Powered by Roo Tech"
    self.CMD_PREFIX = ""

    self.SLEEP_TIME = 3.2

    self.fname = "DauthyData.txt"

    success = self.load_data()
    if not success:
      self.first_time()
      print("first_time done")
    # end if
    print("self.APPROVED_USERS: ", [self.APPROVED_USERS])

    self.init_embeds()
  # end __init__


  def first_time(self):
    self.key = pyotp.random_base32()
    self.totp = pyotp.TOTP(self.key)

    TTM_GID = 931482273440751638
    ROO_TECH_GID = 993961827799158925
    self.GIDS = [TTM_GID, ROO_TECH_GID]

    self.ME = 855616810525917215

    self.APPROVED_USERS = {}
    self.MODERATOR_IDS  = {}
    self.AUTHENTD_IDS   = {}
    self.RESET_TIMES    = {}
    self.MOD_PASSWORDS  = {}
    self.AUTHENTD_TIMES = {}
  # end first_time

  def init_embeds(self):
    self.URL = "https://cdn.discordapp.com/icons/993961827799158925/9832210ac7bd13033037b865b1622c68.webp?size=160"

    TITLE = "__Help Menu__"
    DESCRIPTION = "Hi! I am " + self.BOT_NAME + " developed by @TheLunaLabs © 2022"
    DESCRIPTION += ".\n Below are my commands which are case insensitive: "

    embedInt = interactions.Embed(title=TITLE, description=DESCRIPTION)
    embedInt.set_footer(text = self.FOOTER, icon_url=self.URL)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "help**", value="(Access: Everyone) Displays this help menu", inline=True)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "add_approved_user**", value="(Access: Creator) Adds user that can manage Dauthy settings for their guild.", inline=False)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "add_role_ids**", value="(Access: Approved Users) Adds 'authenticated' role id for given guild and roles ('moderators') which may authenticate.", inline=False)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "authentication_reset_timer**", value="(Access: Approved Users) Modifies time 'authenticated' role is granted before it is revoked.", inline=False)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "init_password**", value="(Access: 'Moderator' Role(s)) Initializes dauthy password for given user.", inline=False)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "generate_qr_code**", value="(Access: 'Moderator' Role(s)) Generates QR code for given user to initialize passcode generation with their 2FA app.", inline=False)
    embedInt.add_field(name="**/" + self.CMD_PREFIX + "authenticate**", value="(Access: 'Moderator' Role(s)) Grants users that pass the 2FA challenge an 'authenticated' role, granting access to secured channels (e.g., announcements), if they pass the 2FA challenge.", inline=False)

    self.helpEmbedInt = embedInt
  # end init_embeds

  def load_data(self):
    print("BEGIN load_data")
    if os.path.exists(self.fname) and os.stat(self.fname).st_size != 0:
      print("in if")
      fernet = Fernet(os.environ["dauthyFern1"] + os.environ["dauthyFern2"] + os.environ["dauthyFern3"])
      with open(self.fname, "rb") as fid:
        lines = fid.readlines()
        for ii in range(len(lines)):
          lines[ii] = fernet.decrypt(lines[ii])
        # end for
        self.key = lines[0].replace("\n","")
        self.totp = pyotp.TOTP(self.key)

        self.GIDS = lines[1].replace("[","").replace("]","").replace("\n","").split(", ")
        for ii in range(len(self.GIDS)):
          self.GIDS[ii] = int(self.GIDS[ii])
        # end for

        self.ME = int(lines[2].replace("\n",""))
        self.APPROVED_USERS = ast.literal_eval(lines[3])
        print("AU after eval: ", self.APPROVED_USERS)
        self.MODERATOR_IDS  = ast.literal_eval(lines[4])
        self.AUTHENTD_IDS   = ast.literal_eval(lines[5])
        self.RESET_TIMES    = ast.literal_eval(lines[6])
        self.MOD_PASSWORDS  = ast.literal_eval(lines[7])
        try:
          self.AUTHENTD_TIMES = ast.literal_eval(lines[8])
        except:
          self.AUTHENTD_TIMES = {993961827799158925:{}}
        return True
      # end with
    else:
      print("didn't find data to load!")
      return False
    # end if
  # end load_data

  def save_data(self):
    to_save = [self.key, self.GIDS, self.ME, self.APPROVED_USERS, 
               self.MODERATOR_IDS, self.AUTHENTD_IDS, self.RESET_TIMES,
               self.MOD_PASSWORDS, self.AUTHENTD_TIMES]
    fernet = Fernet(os.environ["dauthyFern1"] + os.environ["dauthyFern2"] + os.environ["dauthyFern3"])
    with open(self.fname, "wb") as fid:
      for el in to_save:
        fid.write(fernet.encrypt( (str(el) + "\n").encode("utf-8") ))
    # end with open
  # end save_data

  async def remove_authentication_from_all_users(self, client):
    for guild in client.guilds:
      gid = int(guild.id)
      print("gid, guild.id: ", gid, guild.id)

      if gid not in self.AUTHENTD_IDS:
        print("Note, gid for guild not in AUTHENTD_IDS: ", gid, guild)
        continue
      # end if

      members = await guild.get_all_members()
      print("guild.get_all_members: ",members)
      for member in members:
        print("125 member: ", member)
        for aid in self.AUTHENTD_IDS[gid]:
          print("member.roles: ", member.roles)
          print("aid: ", aid)
          #input(">>")
          if aid in member.roles:
            print("aid in roles")
            await member.remove_role(aid, guild_id=gid)
            print("removed role")
          # end if
        # end for
      # end for
    # end for
  # end remove_authentication_from_all_users

  async def remove_authenticated_users(self):
    for gid in list(self.AUTHENTD_TIMES.keys()):
      reset_time = self.RESET_TIMES[gid]

      for did in list(self.AUTHENTD_TIMES[gid].keys()):
        print("126 did: ", did)
        arr = self.AUTHENTD_TIMES[gid][did]

        member     = arr[0]
        aid        = arr[1]
        time_added = arr[2]

        if time.time() - time_added > reset_time:
          try:
            await member.remove_role(aid, guild_id=gid)
            del self.AUTHENTD_TIMES[gid][did]
            self.save_data()
            print("removed role!")
          except Exception as err:
            print("already removed role?")
            print("68 err: ", err)
            print("69 err.ags: ", err.args[:])
          # end try/except
        # end if
      # end for did
    # end for gid
  # end remove_authenticated_users

  def discord_bot(self):
    client = interactions.Client(token=os.environ["dauthyBotPass"], intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)

    @client.command(
      name="help",
      description="Displays the help menu",
      scope=self.GIDS,
    )
    async def help(ctx: interactions.CommandContext):
      await ctx.send(embeds=self.helpEmbedInt, ephemeral=True)
    # end help

    @client.command(
      name="add_guild",
      description="Adds guild id to gids",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="gid",
          description="guild id",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def add_guild(ctx: interactions.CommandContext, 
                          gid: str):
      if int(ctx.author.id) != self.ME:
        await ctx.send("ERROR only botfather can add guilds", ephemeral=True)
        return
      # end if

      try:
        gid = int(gid)
      except:
        await ctx.send("Error, didn't pass in guild id parseable as int")
        return
      # end try/except
      if gid in self.GIDS and gid in self.APPROVED_USERS:
        print("68 err, gid: ", gid, " self.GIDS: ", self.GIDS)
        await ctx.send("Note, guild id already known", ephemeral=True)
        return
      # end if
      self.APPROVED_USERS[gid] = []
      self.MODERATOR_IDS[ gid] = []
      self.AUTHENTD_IDS[  gid] = []
      self.RESET_TIMES[   gid] = 10.0
      self.MOD_PASSWORDS[ gid] = {}
      self.AUTHENTD_TIMES[gid] = {}
      if gid not in self.GIDS:
        self.GIDS.append(gid)
      # end if
      print("added gid: ", gid, " to self.GIDS")
      self.save_data()
      await ctx.send("Added guild id!", ephemeral=True)
      return
    # end add_guild

    @client.command(
      name="add_approved_user",
      description="Adds approved user for a given guild",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="gid",
          description="guild id",
          type=interactions.OptionType.STRING,
          required=True,
        ),
        interactions.Option(
          name="did",
          description="discord id",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def add_approved_user(ctx: interactions.CommandContext, 
                                gid: str, did: str):
      if int(ctx.author.id) != self.ME:
        await ctx.send("ERROR only botfather can add approved users", ephemeral=True)
        return
      # end if

      try:
        gid = int(gid)
      except:
        await ctx.send("Error, didn't pass in guild id parseable as int", ephemeral=True)
        return
      # end try/except

      try:
        did = int(did)
      except:
        await ctx.send("Error, didn't pass in discord id parseable as int", ephemeral=True)
        return
      # end try/except

      if did in self.APPROVED_USERS[gid]:
        await ctx.send("Note, discord id passed is already an approved user for this guild id", ephemeral=True)
      # end if
      self.APPROVED_USERS[gid].append(did)
      self.save_data()
      await ctx.send("Successfully added discord id to approved users for given guild id!", ephemeral=True)
      return
    # end add_approved_user

    @client.command(
      name="add_role_ids",
      description="Add mod and authenticated role ids for the given guild",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="guild_id",
          description="guild id",
          type=interactions.OptionType.STRING,
          required=True,
        ),
        interactions.Option(
          name="mod_id",
          description="moderator role id",
          type=interactions.OptionType.STRING,
          required=True,
        ),
        interactions.Option(
          name="authd_id",
          description="'authenticated' role id",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def add_role_ids(ctx: interactions.CommandContext, 
                              guild_id: str, mod_id: str, authd_id: str):
      did = int(ctx.author.id)
      gid = guild_id
      mid = mod_id
      aid = authd_id
      try:
        gid = int(gid)
      except:
        await ctx.send("Error, didn't pass in guild id parseable as int. Try again.", ephemeral=True)
        return
      # end try/except

      try:
        mid = int(mid)
      except:
        await ctx.send("Error, didn't pass in moderator role id parseable as int. Try again.", ephemeral=True)
        return
      # end try/except

      try:
        aid = int(aid)
      except:
        await ctx.send("Error, didn't pass in 'authenticated' role id parseable as int. Try again.", ephemeral=True)
        return
      # end try/except

      free_pass = did != self.ME

      if free_pass and gid not in self.APPROVED_USERS:
        await ctx.send("Error, guild id not yet added. Please contact the developer.", ephemeral=True)
        return
      # end if

      if free_pass and did not in self.APPROVED_USERS[gid]:
        await ctx.send("Error, only approved users can add the moderator id.", ephemeral=True)
      # end if

      self.MODERATOR_IDS[gid].append(mid)
      self.AUTHENTD_IDS[ gid].append(aid)
      self.save_data()
      await ctx.send("Successfully added moderator and 'authenticated' role ids for given guild id!", ephemeral=True)
      return
    # end add_mod_role_id

    @client.command(
      name="authentication_reset_time",
      description="Assigns the timer a user is 'authenticated' for.",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="seconds",
          description="Time a user is authenticated for in seconds. (<= 300)",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def authentication_reset_time(ctx: interactions.CommandContext, 
                                        seconds: str):
      did = int(ctx.author.id)
      gid = int(ctx.guild_id)

      try:
        seconds = float(seconds)
      except:
        await ctx.send("Error, couldn't parse 'seconds' as a decimal.", ephemeral=True)
      # end try/except

      free_pass = did != self.ME

      if free_pass and gid not in self.APPROVED_USERS:
        await ctx.send("Error, guild id not yet added. Please contact the developer.", ephemeral=True)
        return
      # end if

      if free_pass and did not in self.APPROVED_USERS[gid]:
        await ctx.send("Error, only approved users can modify the reset timer.", ephemeral=True)
        return
      # end if

      if seconds > 300:
        await ctx.send("Error, tried to set the reset time to > 300 seconds", ephemeral=True)
        return
      # end if

      self.RESET_TIMES[gid] = seconds
      self.save_data()
      await ctx.send(f"Updated authentication reset timer. Authentication currently invalidates after {seconds} seconds", ephemeral=True)
      return
    # end authentication_reset_time

    @client.command(
      name="init_password",
      description="Initializes password for given user.",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="password",
          description="Mod's password. Must be >= 16 characters and contain at least one number and symbol.",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def init_password(ctx: interactions.CommandContext, 
                           password: str):
      gid = int(ctx.guild_id)

      did = int(ctx.author.id)
      if did in self.MOD_PASSWORDS[gid]:
        await ctx.send("Error, you've already set your password. If you forgot, you'll have to contact the developer. And he'll taunt you a second time ;)", ephemeral=True)
        return
      # end if

      mod_roles = self.MODERATOR_IDS[gid]
      has_mod_role = False
      for mod_role in mod_roles:
        if mod_role in ctx.author.roles:
          has_mod_role = True
        # end if
      # end for

      if not has_mod_role:
        await ctx.send("Error, user does not have moderator role.", ephemeral=True)
        return
      # end if

      if len(password) < 16:
        await ctx.send("Error, your password was shorter than 16 characters bozo. Try again.", ephemeral=True)
        return
      # end if

      num_in_password = False
      for num in "1234567890":
        if num in password:
          num_in_password = True
        # end if
      # end for
      if not num_in_password:
        await ctx.send("Error, your password didn't have a number in it bozo. Try again.", ephemeral=True)
        return
      # end if

      sym_in_password = False
      for sym in "!@#$%^&*()`~-_=+[{]}\|'\";:/?.>,<":
        if sym in password:
          sym_in_password = True
        # end if
      # end for
      if not sym_in_password:
        await ctx.send("Error, your password didn't have a symbol in it bozo. Try again.", ephemeral=True)
        return
      # end if

      self.MOD_PASSWORDS[gid][did] = password
      self.save_data()
      await ctx.send("Successfully added your password: " + password + "\nNow don't forget it!", ephemeral=True)
      return
    # end init_password

    @client.command(
      name="generate_qr_code",
      description="Generates QR code for authenticator app (e.g., Google Authentcator) for given user.",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="password",
          description="Mod's password.",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def generate_qr_code(ctx: interactions.CommandContext,
                               password: str):
      did = int(ctx.author.id)
      gid = int(ctx.guild_id)

      if gid not in self.MOD_PASSWORDS:
        await ctx.send("Error, guild id not yet added. Please contact the developer.", ephemeral=True)
        return
      # end if

      if did not in self.MOD_PASSWORDS[gid]:
        await ctx.send("Error, user hasn't set a password yet.", ephemeral=True)
        return
      # end if

      if password != self.MOD_PASSWORDS[gid][did]:
        await ctx.send("Error, wrong password.", ephemeral=True)
        return
      # end if

      name = "gid" + str(gid) + "did" + str(did)
      auth_str = self.totp.provisioning_uri(name=name,
                                            issuer_name="Dauthy")
      img = qrcode.make(auth_str)
      img.save(name + ".png")
      #await ctx.send(file=name + ".png", ephemeral=True)
      file = interactions.File(filename=name + ".png")
      await command_send(ctx, files=file, ephemeral=True)
      os.system("rm " + name + ".png")
      return
      # send image somehow. Doesn't have to be an embed. Should be ephemeral tho
    # end generate_qr_code

    @client.command(
      name="authenticate",
      description="Assigns 'authenticated' role to user for 60s.",
      scope=self.GIDS,
      options = [
        interactions.Option(
          name="password",
          description="mod's password",
          type=interactions.OptionType.STRING,
          required=True,
        ),
        interactions.Option(
          name="authentication_token",
          description="mod's authentication token",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def authenticate(ctx: interactions.CommandContext, 
                           password: str, authentication_token: str):
      print("BEGIN authenticate")
      did = int(ctx.author.id)
      gid = int(ctx.guild_id)

      if gid not in self.MOD_PASSWORDS:
        await ctx.send("Error, guild id not yet added. Please contact the developer.", ephemeral=True)
        return
      # end if

      if did not in self.MOD_PASSWORDS[gid]:
        await ctx.send("Error, user hasn't set a password yet.", ephemeral=True)
        return
      # end if

      if password != self.MOD_PASSWORDS[gid][did]:
        await ctx.send("Error, wrong password.", ephemeral=True)
        return
      # end if

      if authentication_token != self.totp.now():
        await ctx.send("Error, wrong authentication token.", ephemeral=True)
        return
      # end if

      aids = self.AUTHENTD_IDS[gid]
      for aid in aids:
        print("540 aid")
        if aid not in ctx.author.roles:
          print("542 aid not in roles")
          await ctx.author.add_role(aid, guild_id = gid)

          if did not in self.AUTHENTD_TIMES[gid]:
            self.AUTHENTD_TIMES[gid][did] = [ctx.author, aid, time.time()]
          else:
            self.AUTHENTD_TIMES[gid][did].append([ctx.author, aid, time.time()])
          # end if/else
        else:
          await ctx.send("Note, user already has authenticated role.", ephemeral=True)
          return
        # end if/else
      # end for
      self.save_data()
      await ctx.send("Authenticated successfully.", ephemeral=True)
    # end authenticate

    @client.event
    async def on_ready():
      print("Dauthy on_ready!")
      await self.remove_authentication_from_all_users(client)
      #for BOT_COMMANDS_CID in self.BOT_COMMANDS_CIDS:
      #  channel = client.get_channel(BOT_COMMANDS_CID)
      #  await channel.send("URL Police bot is on patrol.")
      # end for
      while True:
        await asyncio.sleep(self.SLEEP_TIME)
        await self.remove_authenticated_users()
      # end while
    # end on_ready

    client.start()
  # end discord_bot
# end AuthenticationDiscordBot

if __name__ == "__main__":
  bot = AuthenticationDiscordBot()
  bot.discord_bot()
# end if
## end dauthy.py
