## invite link: https://discord.com/api/oauth2/authorize?client_id=1019966201008488488&permissions=3072&scope=bot
## above uses scopes (1): 1) bot
## above uses perms (2): 1) read messages/view channels & 2) send messages
import os
import discord

class HabitsNest(object):
    def __init__(self):
        self.LOG_CHANNEL = 932056137518444594
    # end __init__

    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_ready():
            print("ready!")
            channel_log = client.get_channel(self.LOG_CHANNEL)
            await channel_log.send("I am reborn from my ashes.")
        # end on_ready

        client.run(os.environ.get("habitsNestBotPass"))
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()