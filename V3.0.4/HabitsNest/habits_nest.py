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
        
        self.max_menus = 10

        self.response_table_names = []

        self.GIDS = [TTM_GID, RT_GID]
        self.LOG_CHANNEL = 932056137518444594
        self.TEST_CHANNEL = 1020438647302000731

        self.gsheet_name = "habits-nest-prompts"
        self.airtable_url = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/AllTheDays"
        self.airtable_base = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/"

        self.fname = "data_big/rows_handled.json"
        os.system("mkdir -p data_big")
        self.rows_handled =  self.load_arr()
    # end __init__

    def save_arr(self):
        with open("data_big/temp.txt", "w") as fid:
            for row in self.rows_handled:
                fid.write(str(row))
            # end for
        # end with open
        os.system("cp data_big/temp.txt " + self.fname)
    # end save_arr

    def load_arr(self):
        arr = []
        if os.path.exists(self.fname) and os.stat(self.fname).st_size != 0:
            with open(self.fname, "r") as fid:
                lines = fid.readlines()
                for line in lines:
                    arr.append(line)
                # end for
            # end with
        # end if
        return arr
    # end load_arr


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

            time_to_send = fields["TimeEST"]
            self.time_text = time_to_send

            good_to_send = self.process_time(time_to_send)
            if not good_to_send:
                print("too early! airtable")
                continue
            # end if

            attachments = []
            if "Attachments" in fields:
                attachments  = fields["Attachments"] # list, index with ['url']
            # end if

            message_text = fields["Discord Message"]
            channel_id   = fields["Channel_Id"]

            try:
                channel_id = int(channel_id)
            except Exception as err:
                print("couldn't cast channel_id to int")
                print("181 err: ", err)
                print("182 err.args: ", err.args[:])
                continue
            # end try/except

            try:
                channel = await interactions.get(client, interactions.Channel, object_id=channel_id)
            except Exception as err:
                print("couldn't get channel for channel_id: ", channel_id)
                print("191 err: ", err)
                print("192 err.args: ", err.args[:])
                continue
            # end try/except

            dropdowns  = []
            textinputs = []
            num_dropdowns  = []
            num_textinputs = []
            for field in fields:
                if "TextInput" in field:
                    arr = num_textinputs
                    arr2 = textinputs
                elif "DropDown" in field:
                    arr = num_dropdowns
                    arr2 = dropdowns
                # end if/else

                if "_" in field:
                    field = field.split("_")
                    num = field[-1]
                    print("field, num: ", field, num)
                    if num.isdigit():
                        if num not in arr:
                            arr.append(num)
                            arr2.append([])
                            print("in if")
                        else:
                            print("else")
                            ind = arr.index(num)
                            arr2[ind].append("")
                        # end if
                        print("num is digit")
                    # end if
                # end if

                if "TextInput" in field:
                    num_textinputs = arr
                    textinputs = arr2
                elif "DropDown" in field:
                    num_dropdowns = arr
                    dropdowns = arr2
                # end if/else

                print("arr, arr2: ", arr, arr2)
            # end for

            print("dropdowns: ", dropdowns)
            print("textinputs: ", textinputs)
            for field in fields:
                if "DropDown" in field:
                    var = "DropDown"
                    arr = dropdowns
                    print("DD")
                elif "TextInput" in field:
                    var = "TextInput"
                    arr = textinputs
                    print("TI")
                # end if/elif
                ind1 = int(field.replace(var, "").split("_")[0])-1
                ind2 = int(field.replace(var, "").split("_")[1][1])-1
                print("ind1, ind2: ", ind1, ind2)
                arr[ind1][ind2] = fields[field]
            # end for

            buttons = []
            select_menus = []
            labels = "a b c d e f g h i j k l m n o".split()
            for ii in range(len(dropdowns)):
                label = ":regional_indicator_" + labels[ii] + ":"
                buttons.append(interactions.Button(style=1, label=label,
                                custom_id="button" + str(ii)))

                select_options = []
                for dropdown_option in dropdowns[ii]:
                    select_options.append(interactions.SelectOption(
                        label=dropdown_option, value=dropdown_option, description=dropdown_option))
                # end for
                
                select_menus.append(interactions.SelectMenu(
                    options=select_options,
                    placeholder=label,
                    custom_id="menu" + str(ii)
                ))
            # end for
            
            cnt = 0
            modals = []
            for jj in range(len(textinputs)):
                label = ":regional_indicator_" + labels[ii+jj+1] + ":"
                buttons.append(interactions.Button(style=1, label=label,
                                custom_id="button" + str(ii+jj+1)))

                modal_components = []
                for kk in range(len(textinputs[jj])):
                    cnt += 1
                    modal_components.append(interactions.TextInput(
                        style=interactions.TextStyleType.PARAGRAPH,
                        label=textinputs[jj][kk],
                        custom_id="text-input-" + str(cnt),
                    ))
                # end for

                modals.append(interactions.Modal(
                            title=label,
                            custom_id="modal" + str(ii+jj+1),
                            components=modal_components
                ))
            # end for

            row = interactions.ActionRow(components=buttons)
            self.select_menus = select_menus
            self.modals = modals
            self.message_text = message_text

            print("message_text: ", message_text)
            print("select_menus: ", self.select_menus)
            print("modals: ", self.modals)

            print("attachments: ", attachments)
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
                image_file = interactions.File(filename=image_name)

                await channel.send(files=image_file)
            # end for attachments
            for channel in self.channels:
                await channel.send(message_text.replace("\\n", "\n"), components=row)
            # end for
            self.rows_handled.append(str(record))
            self.save_arr()
        # end records
    # end airtable_stuff

    def discord_bot(self):
        client = interactions.Client(token=os.environ["habitsNestBotPass"])#, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)

        async def button_func(ctx: interactions.ComponentContext):
            ii = int(ctx.data.custom_id.replace("button", ""))

            if ii < len(self.select_menus):
                print("ii, self.select_menus[ii]: ", ii, self.select_menus[ii])
                await ctx.send(components=self.select_menus[ii])#, ephemeral=True)
            else:
                jj = len(self.select_menus) - ii
                print("ii, jj, self.modals[jj]: ", ii, jj, self.modals[jj])
                await ctx.popup(self.modals[jj])
            # end if/else
        # end def

        async def user_response(ctx: interactions.CommandContext, response: str):
            gid = int(ctx.guild.id)

            custom_id = ctx.data.custom_id
            num = int(custom_id.replace("menu","").replace("modal",""))

            print("response: ", response)
            print("[r]: ", [response])
            print("gid, custom_id, num: ", gid, custom_id, num)
            return

            if   "menu" in custom_id:
                pass
            elif "modal" in custom_id:
                pass
            if type(response) == type([]):
                response = response[0]
            # end if


            print("ii, response, self.button_texts[ii]: ", ii, response, self.button_texts[ii])
            print("type response: ", type(response))

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}

            print("modal response author id: ", ctx.author.id)

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "records": [
                            {
                                "fields": {
                                    "TimeEST": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Attachments": [],
                                    "Discord Message": self.message_text,
                                    "ButtonText" + str(ii+1): response,
                                    "FromDiscordID": str(int(ctx.author.id)),
                                    "FromGuildID": str(gid)
                                }
                            }
                           ]
                    }

            url = (self.airtable_base + self.time_text.replace(":", "%3A") + " " + self.button_texts[ii]).replace(" ", "%20")
            print("url: ", url)
            req = requests.post(url, headers=headers, json=data)
            print("req.status_code: ", req.status_code)
            msg = f"Your response to {self.button_texts[ii]}: {response}"
            print("msg: msg")
            await ctx.send(msg)#, ephemeral=True)
        # end modal_response

        for ii in range(self.max_menus):
            client.component("button" + str(ii))(button_func)
            client.component("menu"   + str(ii))(user_response)
            client.component("modal"  + str(ii))(user_response)
        # end for ii

        @client.event
        async def on_ready():
            print("ready!")

            channel_test = await interactions.get(client, interactions.Channel, object_id=self.TEST_CHANNEL)
            channel_log = await interactions.get(client, interactions.Channel, object_id=self.LOG_CHANNEL)
            self.channels = [channel_log]#, channel_test]

            for channel in self.channels:
                await channel.send("I am reborn from my ashes.")
            # end for

            await self.airtable_stuff(client)

            '''
            while True:
                await self.airtable_stuff(client)
                await asyncio.sleep(5.0)
            # end while True
            '''
        # end on_ready

        client.start()
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()
