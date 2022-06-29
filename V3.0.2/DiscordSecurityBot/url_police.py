## url_police.py by TheLunaLabs Copyright 2022
"""
The purpose of this script is to implement a URL allowlist bot
that only permits URLs if they're in the allowlist. URL (pattern)
can be set depending on the channel.

Additional features to add
1) auto-ban users impersonating staff (look at ascii representation
   and assume the worst for lots of unicode, except for accents maybe

## url to invite bot (see ScreenshotUrlGenerator.jpeg for the perms)
https://discord.com/api/oauth2/authorize?client_id=979391724734521354&permissions=76800&scope=bot%20applications.commands
"""
import os
import sys
import time
import asyncio
import hashlib
from cryptography.fernet import Fernet

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions.client import get

class AuthenticationDiscordBot(object):
  def __init__(self):
    self.TTM_GID = 931482273440751638
    self.ROLES = {"Authenticated":979452786355867679,
                            "Mod":948657215143817286}
    self.RESET_TIME = 60 # seconds
    self.authenticated_members = {"obj":[], "time_added":[]}
    self.BOT_COMMANDS_CIDS = [932056137518444594]
    self.SLEEP_TIME = 0.2
    self.APPROVED_USERS = [855616810525917215]
    self.fern = Fernet(os.environ["dwEncKey"])
    self.authentication_token = self.get_random()
  # end __init__

  def get_random(self):
    seed = bytes(str(time.time()).encode("utf-8"))

    h = hashlib.new("sha256")
    h.update(seed)
    token = h.hexdigest()

    with open("authentication_token.enc", "wb") as fid:
      fid.write(self.fern.encrypt(token.encode("utf-8")))
    # end with open
    self.last_change = time.time()

    return h.hexdigest()
  # end get random()

  async def remove_authenticated_users(self):
    ams = self.authenticated_members
    members_still_authenticated = []
    times_og_added = []
    for ii in range(len(ams["obj"])):
      await asyncio.sleep(self.SLEEP_TIME)
      if time.time() - ams["time_added"][ii] > self.RESET_TIME:
        await ams["obj"][ii].remove_role(self.ROLES["Authenticated"], 
                                         guild_id=self.TTM_GID)
        print("removed role!")
      else:
        members_still_authenticated.append(ams["obj"][ii])
        times_og_added.append(ams["time_added"][ii])
      # end if/else
    # end for
    ams["obj"]        = members_still_authenticated
    ams["time_added"] = times_og_added
    #print("rau ams: ", self.authenticated_members)
  # end remove_authenticated_users

  def discord_bot(self):
    client = interactions.Client(token=os.environ["secBotPass"])

    @client.command(
      name="authenticate",
      description="Assigns 'authenticated' role to user for 60s.",
      scope=self.TTM_GID,
      options = [
        interactions.Option(
          name="authentication_token",
          description="authentication token",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def authenticate(ctx: interactions.CommandContext, 
                           authentication_token: str):
      if authentication_token != self.authentication_token:
        print("recvd: ", authentication_token)
        print("token: ", self.authentication_token)
        await ctx.send("Error, bad authentication token")
      else:
        member = ctx.author

        ams = self.authenticated_members
        ams["obj"].append(member)
        ams["time_added"].append(time.time())

        role = self.ROLES["Authenticated"]
        if role not in member.roles:
          await member.add_role(role, guild_id=self.TTM_GID)
          print("added role")
          await ctx.send("Authenticated successfully.")
        else:
          await ctx.send("User is already authenticated.")
        # end if
      # end if/else
      #print("ams: ", self.authenticated_members)
    # end authenticate

    @client.event
    async def on_ready():
      print("We have logged in as url police")
      #for BOT_COMMANDS_CID in self.BOT_COMMANDS_CIDS:
      #  channel = client.get_channel(BOT_COMMANDS_CID)
      #  await channel.send("URL Police bot is on patrol.")
      # end for
      while True:
        await asyncio.sleep(self.SLEEP_TIME)
        await self.remove_authenticated_users()

        if time.time() - self.last_change > self.RESET_TIME:
          self.authentication_token = self.get_random()
        # end if
      # end while
    # end on_ready

    @client.command(
      name="authentication_reset_time",
      description="Assigns the timer a user is 'authenticated' for.",
      scope=self.TTM_GID,
      options = [
        interactions.Option(
          name="seconds",
          description="Time a user is authenticated for.",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def authentication_reset_time(ctx: interactions.CommandContext, 
                           seconds: str):
      mid = ctx.member.id
      print("mid: ", mid)
      if mid in self.APPROVED_USERS:
        self.RESET_TIME = float(seconds)
        await ctx.send(f"Updated authentication reset timer. Authentication currently invalidates after {seconds} seconds", ephemeral=True)
      else:
        await ctx.send("Error! Unapproved user attempted to modify the authentication reset timer!")
      # end if/else
    # end authentication_reset_time

    @client.command(
      name="authentication_add_moderator",
      description="Assigns user the moderator role.",
      scope=self.TTM_GID,
      options = [
        interactions.Option(
          name="userid",
          description="Adds a user to the moderation team.",
          type=interactions.OptionType.STRING,
          required=True,
        ),
      ],
    )
    async def authentication_add_moderator(ctx: interactions.CommandContext, 
                                           userid: str):
      user   = await get.get(client, interactions.User, user_id=int(userid))
      member = await get.get(client, interactions.Member, 
                             member_id=int(userid),
                             guild_id=self.TTM_GID)
      role = self.ROLES["Mod"]
      await member.add_role(role, guild_id=self.TTM_GID)
      print("added role in mod cmd")
      await ctx.send("Added " + user.username + " as a moderator.")
    # end def authentication_add_moderator

    client.start()
  # end discord_bot
# end AuthenticationDiscordBot

if __name__ == "__main__":
  bot = AuthenticationDiscordBot()
  bot.discord_bot()
# end if
## end url_police.py
