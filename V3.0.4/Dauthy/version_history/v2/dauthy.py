## dauthy.py by @TheLunaLabs (Twitter) Copyright 2022
## url invite link set up:
## scopes: bot, application.commands
## permissions: 1) read/view messages, 2) send messages, 3) embed links, 
## 4) attach files, 5) manage roles, 6) read message history
## https://discord.com/api/oauth2/authorize?client_id=979391724734521354&permissions=268553216&scope=bot%20applications.commands
import os
import sys
import imp
import time
import asyncio
import pyotp
import qrcode

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions.client import get

from commands import dauthy_commands

class AuthenticationDiscordBot(object):
  def __init__(self):
    self.BOT_NAME = "Dauthy"
    self.FOOTER   = "Built for Roo Tech, Powered by Roo Tech"
    self.CMD_PREFIX = ""

    success = self.load_data()
    if not success:
      self.first_time()
    # end if

    self.init_embeds()
  # end __init__

  def load_data(self):
    return False
  # end load_data

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

  def first_time(self):
    key = pyotp.random_base32()
    self.totp = pyotp.TOTP(key)

    TTM_GID = 931482273440751638
    self.GIDS = [TTM_GID]

    self.ME = 855616810525917215
    self.APPROVED_USERS = {TTM_GID: []}
    self.MODERATOR_IDS = {TTM_GID: []}

    self.ROLES = {"Authenticated":979452786355867679,
                            "Mod":948657215143817286}
    self.CIDS = [932056137518444594]
    self.SLEEP_TIME = 0.2

    self.APPROVED_USERS = {}
    self.MODERATOR_IDS  = {}
    self.AUTHENTD_IDS   = {}
    self.RESET_TIMES    = {}
    self.MOD_PASSWORDS  = {}
    self.AUTHENTD_TIMES = {}

    self.authenticated_members = {"obj":[], "time_added":[], "gid":[],
                                  "pass":[]}
    self.ams = self.authenticated_members
  # end __init__

  async def remove_authenticated_users(self):
    for gid in self.AUTHENTD_TIMES:
      reset_time = self.RESET_TIMES[gid]
      for did in self.AUTHENTD_TIMES[gid]:
        inds_to_del = []
        for ii,arr in enumerate(self.AUTHENTD_TIMES[gid][did]):

          member     = arr[0]
          aid        = arr[1]
          time_added = arr[2]

          if time.time() - time_added > reset_time:
            try:
              member.remove_role(aid, guild_id=gid)
              inds_to_del.append(ii)
              print("removed role!")
            except Exception as err:
              print("already removed role?")
              print("68 err: ", err)
              print("69 err.ags: ", err.args[:])
            # end try/except
          # end if
        # end for ii
        for ii in inds_to_del[::-1]:
          del self.AUTHENTD_TIMES[gid][did][ii]
        # end for ii
      # end for did
    # end for gid
  # end remove_authenticated_users

  def discord_bot(self):
    client = interactions.Client(token=os.environ["dauthyBotPass"])

    @client.event
    async def on_ready():
      print("Dauthy is ready!")
      dauthy_commands(client, self.GIDS)
      print("done with dauthy_commands")
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