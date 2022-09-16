import os
import discord
from discord import app_commands

GID = 931482273440751638
class client(discord.Client):
    def __init__(self):
        super().__init__()
        self.synced = False # we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=GID))
            self.synced = True
        print(f"We have logged in as {self.user}.")
    
aclient = client()
tree = app_commands.CommandTree(aclient)

# guild specific slash command
@tree.command(guild = discord.Object(id=GID), name="tester", description="testing")
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am working! I was made with Discord.py", ephemeral=True)

aclient.run(os.environ.get("habitsNestBotPass"))