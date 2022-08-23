import os
import sys

sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
import interactions
from interactions.client import get

def dauthy_commands(client, GIDS):
    @client.command(
        name="help",
        description="Displays the help menu",
        scope=GIDS,
    )
    async def help(ctx: interactions.CommandContext):
        await ctx.send(embeds=self.helpEmbedInt, ephemeral=True)
    # end help

    @client.command(
        name="add_guild",
        description="Adds guild id to gids",
        scope=GIDS,
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
        if ctx.author.id != self.ME:
            await ctx.send("ERROR only botfather can add guilds", ephemeral=True)
        return
        # end if

        try:
            gid = int(gid)
        except:
            await ctx.send("Error, didn't pass in guild id parseable as int")
            return
        # end try/except
        if gid in GIDS:
            print("68 err, gid: ", gid, " GIDS: ", GIDS)
            await ctx.send("Error, gid already in ALL_GIDS", ephemeral=True)
            return
        # end if
        self.APPROVED_USERS[gid] = []
        self.MODERATOR_IDS[ gid] = []
        self.AUTHENTD_IDS[  gid] = []
        self.RESET_TIMES[   gid] = 60.0
        self.MOD_PASSWORDS[ gid] = {}
        self.AUTHENTD_TIMES[gid] = {}
        GIDS.append(gid)

        print("added gid: ", gid, " to GIDS")
        await ctx.send("Added guild id!", ephemeral=True)
        return
    # end add_guild

    @client.command(
        name="add_approved_user",
        description="Adds approved user for a given guild",
        scope=GIDS,
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
        if ctx.author.id != self.ME:
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

        self.APPROVED_USERS[gid].append(did)
        await ctx.send("Successfully added did to approved users for given gid!", ephemeral=True)
        return
    # end add_approved_user

    @client.command(
        name="add_role_ids",
        description="Add mod and authenticated role ids for the given guild",
        scope=GIDS,
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
        did = ctx.author.id
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
        await ctx.send("Successfully added moderator and 'authenticated' role ids for given guild id!", ephemeral=True)
        return
    # end add_mod_role_id

    @client.command(
        name="authentication_reset_time",
        description="Assigns the timer a user is 'authenticated' for.",
        scope=GIDS,
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
        did = ctx.author.id
        gid = ctx.guild.id

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
        await ctx.send(f"Updated authentication reset timer. Authentication currently invalidates after {seconds} seconds", ephemeral=True)
        return
    # end authentication_reset_time

    @client.command(
        name="init_password",
        description="Initializes password for given user.",
        scope=GIDS,
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
        print("dir(ctx): ", dir(ctx))
        print("ctx.guild: ", ctx.guild)
        print("ctx.guild.id: ", ctx.guild.id)
        gid = ctx.guild.id

        did = ctx.author.id
        if did in self.MOD_PASSWORDS[gid]:
            await ctx.send("Error, you've already set your password. If you forgot, you'll have to contact the developer. And he'll taunt you a second time ;)", ephemeral=True)
            return
        # end if

        mod_roles = self.MODERATOR_IDS[gid]
        has_mod_role = False
        for mod_role in mod_roles:
            if ctx.author.roles in mod_role:
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
        await ctx.send("Successfully added your password: " + password + "\nNow don't forget it!", ephemeral=True)
        return
    # end init_password

    @client.command(
        name="generate_qr_code",
        description="Generates QR code for authenticator app (e.g., Google Authentcator) for given user.",
        scope=GIDS,
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
        did = ctx.author.id
        gid = ctx.guild.id

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
        auth_str = self.totp.provisionning_uri(name=name,
                                                issuer_name="Dauthy")
        img = qrcode.make(auth_str)
        img.save(name + ".png")
        # send image somehow. Doesn't have to be an embed. Should be ephemeral tho
    # end generate_qr_code

    @client.command(
        name="authenticate",
        description="Assigns 'authenticated' role to user for 60s.",
        scope=GIDS,
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
        did = ctx.author.id
        gid = ctx.guild.id

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
            if aid not in ctx.author.roles:
                ctx.author.add_role(aid, guild_id = gid)

                if did not in self.AUTHENTD_TIMES[gid]:
                    self.AUTHENTD_TIMES[gid][did] = [ctx.author, aid, time.time()]
                else:
                    self.AUTHENTD_TIMES[gid][did].append([ctx.author, aid, time.time()])
            # end if/else
        # end for
        await ctx.send("Authenticated successfully.", ephemeral=True)
    # end authenticate
# end dauthy_commands