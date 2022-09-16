## invite link: https://discord.com/api/oauth2/authorize?client_id=1019966201008488488&permissions=3072&scope=bot
## above uses scopes (1): 1) bot
## above uses perms (2): 1) read messages/view channels & 2) send messages
import os
import sys
import socket

if socket.gethostname() == "MB-145.local":
  sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
else:
  sys.path.append("/root/ToServer/interactions-ryanjsfx")
# end if/else
sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")

import interactions
#print("interactions.__version__: ", interactions.__version__)
#print("interactions.__version__: ", interactions.version)

class HabitsNest(object):
    def __init__(self):
        TTM_GID = 931482273440751638
        self.GIDS = [TTM_GID]
        self.LOG_CHANNEL = 932056137518444594
        self.init_stuff()
    # end __init__

    def init_stuff(self):
        self.button = interactions.Button(style=1, label="Click for Modal", custom_id="button")

        self.modal = interactions.Modal(
                title="Modal Title",
                custom_id="modal",
                components=[
                    interactions.TextInput(
                        style=interactions.TextStyleType.SHORT,
                        label="Short text input",
                        custom_id="text-input-1"
                    ),
                    interactions.TextInput(
                        style=interactions.TextStyleType.PARAGRAPH,
                        label="Paragraph text input",
                        custom_id="text-input-2",
                    ),
                ],
            )

    def discord_bot(self):
        client = interactions.Client(token=os.environ["habitsNestBotPass"])#, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)

        @client.command(name="send-modal", description="Send a modal", scope=self.GIDS)
        async def send_modals(ctx: interactions.CommandContext):
            await ctx.popup(self.modal)

        @client.command(name="send-button", description="Send a button", scope=self.GIDS)
        async def send_button(ctx: interactions.CommandContext):
            await ctx.send("Click the button below to send a modal!", components=self.button)

        @client.component("button")
        async def button_func(ctx: interactions.ComponentContext):
            await ctx.popup(self.modal)

        @client.modal("modal")
        async def modal_response(ctx: interactions.CommandContext, short: str, paragraph: str):
            await ctx.send(f"Short text: {short}\nLong text: {paragraph}")

        @client.event
        async def on_ready():
            print("ready!")

            channel_log = await interactions.get(client, interactions.Channel, object_id=self.LOG_CHANNEL)
            # channel_log = interactions.Channel(**await client.http.get_channel(self.LOG_CHANNEL), _client=client._http)
            await channel_log.send("I am reborn from my ashes.")
            await channel_log.send("Click the button below to send a modal!", components=self.button)
        # end on_ready

        client.start()
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()