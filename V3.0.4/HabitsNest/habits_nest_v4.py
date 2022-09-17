## invite link: https://discord.com/api/oauth2/authorize?client_id=1019966201008488488&permissions=3072&scope=bot
## above uses scopes (1): 1) bot
## above uses perms (2): 1) read messages/view channels & 2) send messages
import os
import io
import sys
import json
import shutil
import socket
import requests
import asyncio
import gspread
import datetime
from pytz import timezone

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

if socket.gethostname() == "MB-145.local":
#   sys.path.append("/Users/ryanjsfx/Documents/interactions-ryanjsfx")
  gname = "/Users/ryanjsfx/.config/gspread/HabitsNest/service_account.json"
else:
#   sys.path.append("/root/ToServer/interactions-ryanjsfx")
  gname = "/root/.config/gspread/HabitsNest/service_account.json"
# end if/else
# sys.path.insert(0,"/Users/ryanjsfx/Documents/interactions-ryanjsfx")

import interactions
#from interactions.ext.files.files import command_send

class HabitsNest(object):
    def __init__(self):
        TTM_GID = 931482273440751638
        RT_GID = 993961827799158925 # roo tech
        self.GIDS = [TTM_GID, RT_GID]
        self.LOG_CHANNEL = 932056137518444594
        self.TEST_CHANNEL = 1020438647302000731
        self.init_stuff()
        self.gsheet_name = "habits-nest-prompts"
        self.airtable_url = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/Table%201"
        self.rows_handled = []
        self.MODE = "airtable" # or "gdrive"
    # end __init__

    def init_stuff(self):
        self.gc = gspread.service_account(filename=gname)

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

    def initialize_drive(self):
        """
        Initializes a drive service object.

        Returns: An authorized drive service object.
        """
        # credentials = ServiceAccountCredentials.from_json_keyfile_name("client_secrets.json", ['https://www.googleapis.com/auth/drive'])

        # # Build the service object.
        # service = build("drive", "v3", credentials=credentials)
        # return service

        credentials = service_account.Credentials.from_service_account_file(
                        gname)

        scopes = ['https://www.googleapis.com/auth/drive']
        scoped_credentials = credentials.with_scopes(scopes)
        # Build the service object.
        service = build("drive", "v3", credentials=scoped_credentials)

        return service
    # end initialize_drive

    def download_gdrive_file(self, image_name):
        if ".jpg" in image_name.lower() or ".jpeg" in image_name.lower():
            mimeType = "image/jpeg"
        elif ".png" in image_name.lower():
            mimeType = "image/png"
        elif "svg" in image_name.lower():
            mimeType = "image/svg+xml"
        elif "pdf" in image_name.lower():
            mimeType = "application/pdf"
        else:
            print("invalid image extension! Received: ", image_name)
            return False
        # end if/elifs/else

        try:
            service = self.initialize_drive()

            results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get("files", [])

            if not items:
                print("No files found.")
                return False
            # end if

            fid = ""
            for item in items:
                if item["name"] == image_name:
                    print("image_name: ", image_name)
                    fid = item["id"]
                    break
                # end if
            # end for
            if fid == "":
                print("Requested image not found")
                return False
            # end if

            request = service.files().get_media(fileId=fid)#, mimeType=mimeType)
            #request = service.files().export_media(fileId=fid, mimeType=mimeType)
            my_file = io.BytesIO()
            downloader = MediaIoBaseDownload(my_file, request)
            finished = False

            while finished is False:
                status, finished = downloader.next_chunk()
                print(F"Download {int(status.progress() * 100)}.")
            # end while

            my_file.seek(0)

            with open(image_name, "wb") as fid:
                fid.write(my_file.read())
            # end with open
            print("done with open!")

        except HttpError as error:
            print(F"An error occurred: {error}")
            my_file = None
        # end try/except

        #print("my_file.getvalue(): ", my_file.getvalue())
        return my_file.getvalue()
    # end download_gdrive_file

    def process_time(self, time_to_send):
        print("time_to_send (st process_time): ", time_to_send)

        yy,mm,dd = time_to_send.split("-")
        dd,hh,apm = dd.split()
        HH,MM = hh.split(":")
        
        yy = int(yy); mm = int(mm); dd = int(dd)
        HH = int(HH); MM = int(MM)
        print("pm in apm.lower(): ", "pm" in apm.lower())
        print("apm.lower(): ", apm.lower())

        if "pm" in apm.lower() and HH != 12:
            print("added 12!")
            HH += 12
        # end if

        now = datetime.datetime.now(timezone("US/Eastern"))
        print("now: ", now)
        print("HH: ", HH)
        print("now.year,   int(yy), now.year   >= int(yy): ", now.year,   int(yy), now.year   >= int(yy))
        print("now.month,  int(mm), now.month  >= int(mm): ", now.month,  int(mm), now.month  >= int(mm))    
        print("now.day,    int(dd), now.day    >= int(dd): ", now.day,    int(dd), now.day    >= int(dd))
        print("now.hour,   int(HH), now.hour   > int(HH): ", now.hour,    int(HH), now.hour   >= int(HH)) 
        print("now.minute, int(MM), now.minute > int(MM): ", now.minute,  int(MM), now.minute >= int(MM))   
        #input(">>")
        
        result = False
        if   now.year  > yy:
            result = True
        elif now.year == yy:
            if now.month > mm:
                result = True
            elif now.month == mm:
                if now.day > dd:
                    result = True
                elif now.day == dd:
                    if now.hour > HH:
                        result = True
                    elif now.hour == HH:
                        if now.minute >= MM:
                            result = True
                        # end if
                    # end if/elif
                # end if/elif
            # end if/elif
        # end if/elif
        return result
    # end process_time

    async def gdrive_stuff(self, client):
        sh = self.gc.open(self.gsheet_name)
        worksheet = sh.get_worksheet(0)
        print("got worksheet!")
        gsheet = worksheet.get_all_values()
        for jj,row in enumerate(gsheet[1:]): # first row is header
            if row in self.rows_handled:
                continue
            # end if
            time_to_send = row[0]

            good_to_send = self.process_time(time_to_send)
            if not good_to_send:
                print("too early!")
                continue
            # end if

            image_name   = row[1]
            button_text  = row[2]
            message_text = row[3]
            modal_title  = row[4]
            prompts      = row[5:]

            print("time to send it hurray!")

            ## first, download the image file
            self.download_gdrive_file(image_name)
            for channel in self.channels:
                image_file = interactions.File(filename=image_name)
                await channel.send(files=image_file)
            #input(">>")

            button = interactions.Button(style=1, label=button_text, custom_id="button")

            modal_components = []
            for ii in range(len(prompts)):
                modal_components.append(interactions.TextInput(
                    style=interactions.TextStyleType.PARAGRAPH,
                    label=prompts[ii],
                    custom_id="text-input-" + str(ii),
                ))
            # end for ii
            self.modal = interactions.Modal(
                            title="Modal Title",
                            custom_id="modal",
                            components=modal_components
                        )
            for channel in self.channels:
                await channel.send(message_text.replace("\\n", "\n"), components=button)
            self.rows_handled.append(row)
        # end for rows
    # end gdrive_stuff

    async def airtable_stuff(self, client):
        headers = {"Content-Type":"json", "Authorization":"Bearer " + os.environ["airTable"]}
        req = requests.get(self.airtable_url, headers=headers)
        print("airtable_stuff req.status_code: ", req.status_code)
        
        if str(req.status_code)[0] != "2":
            print("not 2XX??")
        # end if
        
        result = req.json()
        with open("debug_airtable.json", "w") as fid:
            json.dump(result, fid)
        # end with

        for record in result["records"]:
            if str(record) in self.rows_handled:
                continue
            # end if
            fields = record["fields"]

            if len(fields) < 5:
                print("too few fields? wanted 5. received len(fields): ", len(fields))
                print("fields: ", fields)
                print("skipping")
                continue
            # end if

            time_to_send = fields["TimeToSendEST"]

            good_to_send = self.process_time(time_to_send)
            if not good_to_send:
                print("too early! airtable")
                continue
            # end if

            attachments  = fields["Attachments"] # list, index with ['url']
            button_text  = fields["ButtonText"]
            message_text = fields["Discord Message"]

            num_prompts = 0
            prompts = []
            for field in fields:
                if "Prompt" in field:
                    num_prompts += 1
                    prompts.append("")
                # end if
            # end for

            for field in fields:
                if "Prompt" in field:
                    ind = int(field.replace("Prompt",""))-1
                    prompts[ind] = fields[field]
                # end if
            # end for
            
            button = interactions.Button(style=1, label=button_text, custom_id="button")

            modal_components = []
            for ii in range(len(prompts)):
                modal_components.append(interactions.TextInput(
                    style=interactions.TextStyleType.PARAGRAPH,
                    label=prompts[ii],
                    custom_id="text-input-" + str(ii),
                ))
            # end for ii
            self.modal = interactions.Modal(
                            title="Modal Title",
                            custom_id="modal",
                            components=modal_components
                        )
            parts = message_text.split("@(")
            message_text = parts[0]
            for part in parts[1:]:
                part.split()
                message_text += "<@&"
            for channel in self.channels:
                await channel.send(message_text.replace("\\n", "\n"), components=button)
            self.rows_handled.append(str(record))

            print("prompts: ", prompts)
            for attachment in attachments:
                image_url = attachment["url"]
                image_name = image_url.split("/")[-1]
                r = requests.get(image_url, stream=True)
                print("r.status_code: ", r.status_code)
                r.raw.decode_content = True

                with open(image_name, "wb") as fid:
                    shutil.copyfileobj(r.raw, fid)
                # end with
                print("Image downloaded!")

                for channel in self.channels:
                    image_file = interactions.File(filename=image_name)
                    await channel.send(files=image_file)
                # end for
            # end for attachments
        # end records
    # end airtable_stuff


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

            channel_test = await interactions.get(client, interactions.Channel, object_id=self.TEST_CHANNEL)
            channel_log = await interactions.get(client, interactions.Channel, object_id=self.LOG_CHANNEL)
            self.channels = [channel_log]#, channel_test]
            # channel_log = interactions.Channel(**await client.http.get_channel(self.LOG_CHANNEL), _client=client._http)
            for channel in self.channels:
                await channel.send("I am reborn from my ashes.")
            #await channel_log.send("Click the button below to send a modal!", components=self.button)
            while True:
                if self.MODE == "gdrive":
                    await self.gdrive_stuff(client)
                elif self.MODE == "airtable":
                    await self.airtable_stuff(client)
                else:
                    print("error! Mode not supported. self.MODE: ", self.MODE)
                # end if/elif/else

                await asyncio.sleep(5.0)
            # end while True
        # end on_ready

        client.start()
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()
