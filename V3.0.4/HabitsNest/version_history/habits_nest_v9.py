## invite link: https://discord.com/api/oauth2/authorize?client_id=1019966201008488488&permissions=3072&scope=bot
## above uses scopes (1): 1) bot
## above uses perms (2): 1) read messages/view channels & 2) send messages
import os
import io
import sys
import math
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
        self.response_dict = {}

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
        print("time to send?: ", result)
        return result
    # end process_time

    async def airtable_stuff(self, client):
        if "airTable" not in os.environ:
            print("err, forgot to export airTable environment variable.")
            sys.exit()
        # end if
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

            if len(fields) < 4:
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

            if "Discord Message" not in fields:
                print("Discord Message not filled out yet!")
                continue
            #if "ChannelId" not in fields:
            #    print("ChannelId not filled out yet!")
            #    continue
            
            message_text = fields["Discord Message"]
            channel_id   = fields["Button Channel Id"]
            rchannel_id   = fields["Button Channel Id"]
            print("message_text 189: ", message_text)

            try:
                channel_id = int(channel_id)
                rchannel_id = int(rchannel_id)

            except Exception as err:
                print("couldn't cast (r)channel_id to int")
                print("181 err: ", err)
                print("182 err.args: ", err.args[:])
                continue
            # end try/except

            try:
                channel = await interactions.get(client, interactions.Channel, object_id=channel_id)
                rchannel = await interactions.get(client, interactions.Channel, object_id=rchannel_id)
            except Exception as err:
                print("couldn't get channel for channel_id: ", channel_id)
                print("191 err: ", err)
                print("192 err.args: ", err.args[:])
                continue
            # end try/except
            print("got channel!")

            dropdowns  = []
            textinputs = []
            num_dropdowns  = []
            num_textinputs = []
            for field in fields:
                if len(fields[field]) == 0:
                    continue
                # end if

                if "TextInput" in field:
                    arr = num_textinputs
                    arr2 = textinputs

                elif "DropDown" in field:
                    arr = num_dropdowns
                    arr2 = dropdowns

                else:
                    continue
                # end if/else

                if "_" in field:
                    field = field.split("_")[0]
                    num = field[-1]

                    if num.isdigit():
                        if num not in arr:
                            arr.append(num)
                            arr2.append([""])

                        else:
                            ind = arr.index(num)
                            arr2[ind].append("")
                        # end if
                    # end if
                # end if

                if "TextInput" in field:
                    num_textinputs = arr
                    textinputs = arr2
                elif "DropDown" in field:
                    num_dropdowns = arr
                    dropdowns = arr2
                # end if/else
            # end for

            for field in fields:
                if len(fields[field]) == 0:
                    continue
                # end if

                if "DropDown" in field:
                    var = "DropDown"
                    arr = dropdowns

                elif "TextInput" in field:
                    var = "TextInput"
                    arr = textinputs

                else:
                    continue
                # end if/elif

                ind1 = int(field.replace(var, "").split("_")[0])-1
                ind2 = int(field.split("_")[1][-1])-1

                val = fields[field]
                if len(val) > 45:
                    val = val[:40]
                    val = " ".join(val.split()[:-1]) + "..."
                arr[ind1][ind2] = val
            # end for
            print("dropdowns: ", dropdowns)
            print("textinputs: ", textinputs)

            buttons = []
            button_texts = []
            select_menus = []
            labels = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣".split()
            
            cnt2 = -1
            ii = 0
            for ii in range(len(dropdowns)):
                cnt2 += 1
                label = labels[ii]
                button_texts.append(label)
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
                cnt2 += 1
                label = labels[cnt2]

                button_texts.append(label)
                buttons.append(interactions.Button(style=1, label=label,
                                custom_id="button" + str(cnt2)))

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
                            custom_id="modal" + str(cnt2),
                            components=modal_components
                ))
            # end for

            row = interactions.ActionRow(components=buttons)
            self.modals = modals
            self.button_texts = button_texts
            self.select_menus = select_menus
            self.message_text = message_text.replace("\\n", "\n").replace("\*", "*")
            self.response_channel = rchannel
            self.response_channel_id = rchannel_id

            print("self.channels: ", self.channels)
            print("message_text: ", self.message_text)
            print("button_texts: ", button_texts)
            print("select_menus: ", self.select_menus)
            print("modals: ", self.modals)

            if len(self.message_text) > 2000:
                msg_remaining = self.message_text + ""
                
                cnt3 = -1
                while len(msg_remaining) > 0:
                    cnt3 += 1

                    print("[] msg_remanining: ", [msg_remaining])
                    print("len msg_remaining: ", len(msg_remaining))

                    msg = msg_remaining[:2000]
                    lines = msg.split("\n")
                    
                    for ii,line in enumerate(lines[::-1]):
                        if len(line) == 0:
                            break
                        # end if
                    # end for

                    ind = len(lines) - (ii+1)
                    msg_to_send = "\n".join(lines[:ind])
                    if cnt3 > 0:
                        msg_to_send = "\u200b" + msg_to_send

                    print("msg_to_send: ", [msg_to_send])
                    try:
                        await channel.send(msg_to_send)
                    except:
                        continue
                    msg_remaining = msg_remaining[len(msg_to_send):]
                # end while
                
                #num_chunks = int(math.ceil( len(self.message_text)/2000.0 ))
                #for ijk in range(num_chunks):
                #    msg = self.message_text[ijk*2000:(ijk+1)*2000]
                #    await channel.send(msg.replace("\\n", "\n"))
            else:
                try:
                    await channel.send(self.message_text.replace("\\n", "\n"))
                except:
                    continue
                print("sent message!")
            # end if/else

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
            print("done with attachments")

            await channel.send("\u200b", components=row)
            print("sent components!")

            self.rows_handled.append(str(record))
            print("row added")
            self.save_arr()
            print("saved arr")
        # end records
    # end airtable_stuff

    def discord_bot(self):
        client = interactions.Client(token=os.environ["habitsNestBotPass"])#, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)

        async def button_func(ctx: interactions.ComponentContext):
            ii = int(ctx.data.custom_id.replace("button", ""))

            if ii < len(self.select_menus):
                print("ii, self.select_menus[ii]: ", ii, self.select_menus[ii])
                await ctx.send(components=self.select_menus[ii], ephemeral=True)
            else:
                jj = len(self.select_menus) - ii
                print("ii, jj, self.modals[jj]: ", ii, jj, self.modals[jj])
                await ctx.popup(self.modals[jj])
            # end if/else
        # end def

        async def menu_response(ctx: interactions.CommandContext, response: str):
            gid = int(ctx.guild.id)
            aid = int(ctx.author.id)
            cid = int(ctx.channel_id)

            custom_id = ctx.data.custom_id
            num = int(custom_id.replace("menu","").replace("modal",""))

            #print("response: ", response)
            #print("[r]: ", [response])
            print("gid, custom_id, num: ", gid, custom_id, num)

            if type(response) == type([]):
                response = response[0]
            # end if

            print("num, self.button_texts: ", num, self.button_texts)
            print("response, self.button_texts[ii]: ", response, self.button_texts[num])
            print("type response: ", type(response))

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}

            print("modal response author id: ", ctx.author.id)

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("self.message_text: ", self.message_text)
            data = {
                "records": [
                            {
                                "fields": {
                                    "TimeEST": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "FromGuildId": str(gid),
                                    "Button Channel Id": str(cid),
                                    "Response Channel Id": str(self.response_channel_id),
                                    "FromDiscordId": str(aid),
                                    "DiscordMessage": self.message_text,
                                    "ButtonType": "DropDown" + str(num+1),
                                    "Response1": response
                                }
                            }
                           ]
                    }

            url = (self.airtable_base + self.time_text.replace(":", "%3A") + " " + str(cid) + " DropDown" + str(num+1)).replace(" ", "%20")
            print("url: ", url)
            req = requests.post(url, headers=headers, json=data)
            print("req.status_code: ", req.status_code)
            msg = f"Your response to {self.button_texts[num]}: {response}"
            print("msg: msg")

            labels = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣".split()

#            self.response_dict[aid] = labels[num] + " " + response

            await self.response_channel.send(msg)
        # end menu_response

        async def modal_response(ctx: interactions.CommandContext, 
                                response1: str, 
                                response2: str = None,
                                response3: str = None,
                                response4: str = None,
                                response5: str = None,
                                response6: str = None,
                                response7: str = None,
                                response8: str = None,
                                response9: str = None):
            gid = int(ctx.guild.id)
            aid = int(ctx.author.id)
            cid = int(ctx.channel_id)

            custom_id = ctx.data.custom_id
            num = int(custom_id.replace("menu","").replace("modal",""))
            print("gid, custom_id, num: ", gid, custom_id, num)

            responses = []
            rs = [response1, response2, response3, response4, response5,
                  response6, response7, response8, response9]
            for r in rs:
                if r is not None:
                    responses.append(r)
                # end if
            # end for
            print("responses: ", responses)

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            fields = {
                        "TimeEST": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "FromGuildId": str(gid),
                        "Button Channel Id": str(cid),
                        "Response Channel Id": str(self.response_channel_id),
                        "FromDiscordId": str(aid),
                        "Discord Message": self.message_text,
                        "ButtonType": "TextInput" + str(num-len(self.select_menus)+1)
                    }
            for ii in range(len(responses)):
                fields["Response" + str(ii+1)] = responses[ii]
            # end for

            data = {
                "records": [
                            {
                                "fields": fields
                            }
                           ]
                    }

            url = (self.airtable_base + self.time_text.replace(":", "%3A") + " " + str(cid) + " TextInput" + str(num+1 - len(self.select_menus))).replace(" ", "%20")
            print("url: ", url)
            req = requests.post(url, headers=headers, json=data)
            print("req.status_code: ", req.status_code)
            msg = f"Your responses to {self.button_texts[num]}: {responses}"
            print("msg: msg")

            payload = labels[num] + " " + response
            if gid not in self.response_dict:
                self.response_dict[gid] = {}
            if aid not in self.response_dict[gid]:
                self.response_dict[gid][aid] = []
            
            self.response_dict[gid][aid].append(payload)

            if len(self.response_dict) == len(self.button_texts):
                # first, build the embed
                print("dir ctx author: ", dir(ctx.author))
                avatar_url = ctx.author.display_avatar.url
                print("avatar_url: ", avatar_url)
                print("type avatar_url: ", type(avatar_url))
                handle = ctx.author.display_name
                print("handle: ", handle)
                print("type handle: ", type(handle))
                embed = discord.Embed(title=handle, description="\u200b", image_url=avatar_url)
                emebd.set_footer(text = "Built for Habit Nest, powered by Roo Tech", icon_url = "https://cdn.discordapp.com/icons/864029910507323392/e2eb644133171506b6f22e55fb3daed1.webp")
                embed.add_field()
                for response in self.response_dict[gid][aid]:
                    embed.add_field(name="\u200b", value=response, inline=True)
                # end for
                await self.response_channel.send(embed=embed)
                self.response_dict[gid][aid] = []
            # end if
        # end modal_response

        for ii in range(self.max_menus):
            client.component("button" + str(ii))(button_func)
            client.component("menu"   + str(ii))(menu_response)
            client.modal(    "modal"  + str(ii))(modal_response)
        # end for ii

        @client.event
        async def on_ready():
            print("ready!")

            channel_test = await interactions.get(client, interactions.Channel, object_id=self.TEST_CHANNEL)
            channel_log = await interactions.get(client, interactions.Channel, object_id=self.LOG_CHANNEL)
            self.channels = [channel_log]#, channel_test]

            #for channel in self.channels:
            #    await channel.send("I am reborn from my ashes.")
            # end for

            #await self.airtable_stuff(client)

            #'''
            while True:
                await self.airtable_stuff(client)
                await asyncio.sleep(5.0)
            # end while True
            #'''
        # end on_ready

        client.start()
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()
