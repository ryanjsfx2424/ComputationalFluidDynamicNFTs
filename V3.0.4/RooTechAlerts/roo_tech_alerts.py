# invite with this one to send messages: 
# https://discord.com/api/oauth2/authorize?client_id=993956538043617320&permissions=19456&scope=bot
import os
import discord

class RooTechAlerts(object):
    def __init__(self):
        self.TTM_BOT_COMMANDS = 932056137518444594

    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_ready():
            print("on_ready")
            channel = client.get_channel(self.TTM_BOT_COMMANDS)
            print("sending msg")
            await channel.send("Hello, World!")
            print("sent msg")
        # end on_ready

        client.run(os.environ.get("rtaBotPass"))
    # end discord_bot
# end RooTechAlerts

if __name__ == "__main__":
    rta = RooTechAlerts()
    rta.discord_bot()
# end if
## end roo_tech_alerts.py
