## invite link: https://discord.com/api/oauth2/authorize?client_id=1019966201008488488&permissions=3072&scope=bot
## above uses scopes (1): 1) bot
## above uses perms (2): 1) read messages/view channels & 2) send messages
import os
import io
import sys
import math
import json
import shutil
import pickle
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
        self.max_menus = 10

        self.labels = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣".split()

        self.GUILDS = [864029910507323392, 993961827799158925]

        os.system("mkdir -p data_big")

        self.airtable_url = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/AllTheDays"
        self.airtable_base = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/"

        self.init_fnames()
        self.init_data()
    # end __init__

    def init_fnames(self):
        self.fname_times               = "data_big/times_handled.json"        
        self.fname                     = "data_big/rows_handled.json"
        self.fname_response_dict       = "data_big/response_dict.json"

        self.fname_time_text           = "data_big/time_text.pickle"
        self.fname_button_texts        = "data_big/button_texts.pickle"
        self.fname_modals              = "data_big/modals.pickle"
        self.fname_select_menus        = "data_big/select_menus.pickle"
        self.fname_message_text        = "data_big/message_text.pickle"
        self.fname_response_channel_id = "data_big/response_channel_id.pickle"
        self.fname_response_buttons    = "data_big/response_buttons.pickle"
        self.fname_special_button_messages = "data_big/special_button_messages.pickle"
    # end init_fnames

    def init_data(self):        
        self.rows_handled =  self.load_arr()
        self.response_dict = self.load_json(self.fname_response_dict, dtype = {})
        self.times_handled = self.load_pickle(self.fname_times, dtype = {
            str(1001020922423152691):
                [
                    "2024-10-04 1:00 PM", 
                    "2024-10-05 1:01 PM", 
                    "2024-10-05 1:01 PM",
                    "2022-10-07 1:01 PM",
                    "2022-10-17 11:40AM",
                    "2022-10-18 12:40PM",
                    "2022-10-19 10:00AM",
                    "2022-10-20 10:00AM",
                    "2022-10-21 10:00AM"
                ]
            }
        )

        self.time_text           = self.load_pickle(self.fname_time_text)
        self.button_texts        = self.load_pickle(self.fname_button_texts)
        self.modals              = self.load_pickle(self.fname_modals)
        self.select_menus        = self.load_pickle(self.fname_select_menus)
        self.message_text        = self.load_pickle(self.fname_message_text)
        self.response_channel_id = self.load_pickle(self.fname_response_channel_id)
        self.response_buttons    = self.load_pickle(self.fname_response_buttons)
        self.special_button_messages = self.load_pickle(self.fname_special_button_messages)
    # end init_data

    def save_pickles(self):
        self.save_pickle(self.fname_times,               self.times_handled)
        self.save_pickle(self.fname_time_text,           self.time_text)
        self.save_pickle(self.fname_button_texts,        self.button_texts)
        self.save_pickle(self.fname_modals,              self.modals)
        self.save_pickle(self.fname_select_menus,        self.select_menus)
        self.save_pickle(self.fname_message_text,        self.message_text)
        self.save_pickle(self.fname_response_channel_id, self.response_channel_id)
        self.save_pickle(self.fname_special_button_messages, self.special_button_messages)
    # end save_pickles

    def save_pickle(self, fname, obj):
        with open(fname, "wb") as fid:
            pickle.dump(obj, fid, pickle.HIGHEST_PROTOCOL)
        # end with
    # end save_pickle

    def load_pickle(self, fname, dtype={}):
        result = dtype
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "rb") as fid:
                result = pickle.load(fid)
            # end with
        # end if
        return result
    # end load_pickle

    def save_json(self, fname, obj):
        with open(fname, "w") as fid:
            json.dump(obj, fid)
        # end with
    # end save_json

    def load_json(self, fname, dtype = []):
        result = dtype
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "r") as fid:
                result = json.load(fid)
            # end with
        # end if
        return result
    # end load_json

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
        # print("time_to_send (st process_time): ", time_to_send)

        yy,mm,dd = time_to_send.split("-")
        if "pm" in dd.lower():
            apm = "PM"
        elif "am" in dd.lower():
            apm = "AM"
        else:
            return False
        dd = dd[:-2]
        #dd,hh,apm = dd.split()
        dd,hh = dd.split()
        HH,MM = hh.replace(" ","").split(":")
        print("[HH], [MM]: ", [HH], [MM])

        yy = int(yy); mm = int(mm); dd = int(dd)
        HH = int(HH); MM = int(MM)
        # print("pm in apm.lower(): ", "pm" in apm.lower())
        # print("apm.lower(): ", apm.lower())

        if "pm" in apm.lower() and HH != 12:
            # print("added 12!")
            HH += 12
        # end if

        now = datetime.datetime.now(timezone("US/Eastern"))
        # print("now: ", now)
        # print("HH: ", HH)
        # print("now.year,   int(yy), now.year   >= int(yy): ", now.year,   int(yy), now.year   >= int(yy))
        # print("now.month,  int(mm), now.month  >= int(mm): ", now.month,  int(mm), now.month  >= int(mm))    
        # print("now.day,    int(dd), now.day    >= int(dd): ", now.day,    int(dd), now.day    >= int(dd))
        # print("now.hour,   int(HH), now.hour   > int(HH): ", now.hour,    int(HH), now.hour   >= int(HH)) 
        # print("now.minute, int(MM), now.minute > int(MM): ", now.minute,  int(MM), now.minute >= int(MM))   
        
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
        # print("time to send?: ", result)
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
            return
        # end if
        
        try:
            result = req.json()
        except:
            print("214 err: ", err)
            print("214 err.args: ", err.args[:])
            return
        # end try/except

        with open("debug_airtable.json", "w") as fid:
            json.dump(result, fid)
        # end with

        for record in result["records"]:
            if str(record) in self.rows_handled:
                continue
            # end if
            fields = record["fields"]

            if len(fields) < 4:
                # print("too few fields? wanted 5. received len(fields): ", len(fields))
                # print("fields: ", fields)
                # print("skipping")
                continue
            # end if

            if "Discord Message" not in fields:
                print("Discord Message not filled out yet!")
                continue

            try:
                time_to_send = fields["TimeEST"]

            except Exception as err:
                print("couldn't get TimeEST from airtable (time to send message)")
                print("217 err: ", err)
                print("218 err.args: ", err.args[:])

            time_to_send = time_to_send.replace(" copy", "")


            good_to_send = self.process_time(time_to_send)
            if not good_to_send:
                #print("too early! airtable")
                continue
            # end if

            try:
                channel_id  = fields["Button Channel Id"]
                rchannel_id = fields["Response Channel Id"]

            except Exception as err:
                print("couldn't get button channel id or response channel id from airtable")
                print("182 err: ", err)
                print("183 err.args: ", err.args[:])
                continue
            # end try/except

            try:
                channel_id  = int( channel_id)
                rchannel_id = int(rchannel_id)

            except Exception as err:
                print("couldn't cast (r)channel_id to int")
                print("190 err: ", err)
                print("191 err.args: ", err.args[:])
                continue
            # end try/except

            try:
                channel  = await interactions.get(client, interactions.Channel, object_id=channel_id)
                rchannel = await interactions.get(client, interactions.Channel, object_id=rchannel_id)
            
            except Exception as err:
                print("couldn't get channel for channel_id: ", channel_id)
                print("205 err: ", err)
                print("206 err.args: ", err.args[:])
                continue
            # end try/except
            print("got channel!")

            cid = channel_id

            if str(cid) in self.times_handled and time_to_send in self.times_handled[str(cid)]:
                continue


            attachments = []
            if "Attachments" in fields:
                attachments  = fields["Attachments"] # list, index with ['url']
            # end if
            
            message_text = fields["Discord Message"]
            end = min(20, len(message_text))
            print("message_text[:20] 189: ", message_text[:end])
            
            messages = [message_text]
            special_button_names   = []
            special_button_messages = []

            if "<<<" in message_text and ">>>" in message_text and ":::" in message_text:
                starts = message_text.split("<<<")
                messages = [starts[0] + ""]
                starts = starts[1:]
                for ss,start in enumerate(starts):
                    print("in start ss: ", ss)
                    before,after = start.split(">>>")
                    if len(after.replace(" ","").replace("\n","")) == 0:
                        after = ""
                    # end if
                    name,msg = before.split(":::")
                    special_button_names.append(name)
                    special_button_messages.append(msg.replace("\\n","\n"))
                    messages.append(after)
                    #print("[after]: ", [after])
                    #print("len after: ", len(after))
                    #print("len after.replace(" ",""): ", len(after.replace(" ","")))
                    #print("len after.replace(' ','').replace('slashn',''): ", len(after.replace(" ","").replace("\n","")))
                # end for
            # end if
            print("special_button_names: ", special_button_names)
            print("special_button_messages: ", special_button_messages)

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

            cnt2 = -1
            ii = 0
            for ii in range(len(dropdowns)):
                cnt2 += 1
                label = self.labels[ii]
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
                label = self.labels[cnt2]

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

            #print("message_text1: ", message_text)

            self.time_text[cid] = time_to_send
            self.modals[cid] = modals
            self.button_texts[cid] = button_texts
            self.select_menus[cid] = select_menus
            self.message_text[cid] = message_text.replace("\\n", "\n").replace("\*", "*")
            self.response_channel_id[cid] = rchannel_id
            self.special_button_messages[cid] = special_button_messages
            self.response_buttons[cid] = buttons

            if cid not in self.times_handled:
                self.times_handled[cid] = []
            # end if
            self.times_handled[cid].append(time_to_send)

            self.save_pickles()

            # print("message_text2: ", self.message_text)
            # print("message_text[cid]: ", self.message_text[cid])
            # input(">>")
            # print("button_texts: ", button_texts)
            # print("select_menus: ", self.select_menus[cid])
            # print("modals: ", self.modals[cid])

            row_buttons = []
            print("len messages: ", len(messages))
            for mm, message in enumerate(messages):
                print("mm: ", mm)
                if len(message) > 2000:
                    msg_remaining = message + ""
                
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
                        # end try/except

                        msg_remaining = msg_remaining[len(msg_to_send):]
                    # end while
                else:
                    if len(message) == 0:
                        append_button_flag = True
                    else:
                        append_button_flag = False
                        if ((mm+1 < len(messages)) and len(messages[mm+1]) == 0):
                            append_button_flag = True
                        try:
                            await channel.send(message.replace("\\n", "\n"))
                        except:
                            continue
                        print("sent message!")
                    # end if/else
                # end if/else
                if mm < len(special_button_names):
                    button = interactions.Button(style=1, label=special_button_names[mm],
                                custom_id="special_button" + str(mm))
                    if append_button_flag:
                        row_buttons.append(button)
                    else:
                        if len(row_buttons) > 0:
                            row2 = interactions.ActionRow(components=row_buttons)
                            await channel.send("\u200b", components=row2)
                            row_buttons = []
                        else:
                            await channel.send("\u200b", components=button)
                        # end if/else
                    # end if/else
                # end if
            # end for messages
            if len(row_buttons) > 0:
                row2 = interactions.ActionRow(components=row_buttons)
                await channel.send("\u200b", components=row2)
            # end if

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

                print("channel_id: ", channel_id)
                await channel.send(files=image_file)
            # end for attachments
            print("done with attachments")

            #await channel.send("\u200b", components=row)
            #print("sent components!")

            self.rows_handled.append(str(record))
            print("row added")
            self.save_arr()
            print("saved arr")
        # end records
    # end airtable_stuff

    async def post_to_airtable(self, url, headers, data):
        req = requests.post(url, headers=headers, json=data)        
        print("req.status_code: ", req.status_code)

    def discord_bot(self):
        client = interactions.Client(token=os.environ["habitsNestBotPass"])#, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)

        @client.command(
            name="habit-nest-daily-challenge",
            description="Your response to a habit nest daily challenge!",
            scope=self.GUILDS,
            options=[
                interactions.Option(
                    name="prompt1",
                    description="Your response to the 1st prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
                interactions.Option(
                    name="prompt2",
                    description="Your response to the 2nd prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt3",
                    description="Your response to the 3rd prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt4",
                    description="Your response to the 4th prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt5",
                    description="Your response to the 5th prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt6",
                    description="Your response to the 6th prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt7",
                    description="Your response to the 7th prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt8",
                    description="Your response to the 8th prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="prompt9",
                    description="Your response to the 9th prompt of a daily challenge",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                interactions.Option(
                    name="days_old",
                    description="Number of days old. For example put 1 for yesterday",
                    type=interactions.OptionType.INTEGER,
                    required=False
                ),
                interactions.Option(
                    name="image_upload",
                    description="Upload an image in response to one of the daily challenge prompts",
                    type=interactions.OptionType.ATTACHMENT,
                    required=False,
                )
            ]
        )
        async def cmd(ctx: interactions.CommandContext, prompt1: str, days_old: int = None, 
                      image_upload: interactions.Attachment = None,
                      prompt2: str=None,
                      prompt3: str=None,
                      prompt4: str=None,
                      prompt5: str=None,
                      prompt6: str=None,
                      prompt7: str=None,
                      prompt8: str=None,
                      prompt9: str=None):
            aid = int(ctx.author.id)
            cid = int(ctx.channel_id)
            if aid != 855616810525917215:
                await ctx.send("still developing only developer can use this now", ephemeral=True)
            # end if

            image_url = ""
            if image_upload != None:
                await ctx.send("received something in image_upload", ephemeral=True)
                print("image_upload: ", image_upload)
                print("dir image_upload: ", dir(image_upload))
                print("image_upload.content_type: ", image_upload.content_type)
                print("image_upload.ephemeral: ", image_upload.ephemeral)
                print("image_upload.filename: ", image_upload.filename)
                print("image_upload.proxy_url: ", image_upload.proxy_url)
                print("image_upload.url: ", image_upload.url)
                #print("image_upload.keys: ", image_upload.keys())
                if "image" not in image_upload.content_type:
                    await ctx.send("we didn't recognize the uploaded file as an image :(", ephemeral=True)
                else:
                    image_url = image_upload.url
                # end if


            if days_old != None:
                await ctx.send("received days_old input, but not implemented yet :)", ephemeral=True)
            
            avatar_url = ctx.author.user.avatar_url
            print("dir ctx.author: ", dir(ctx.author))
            print("dir ctx.author.user: ", dir(ctx.author.user))
            print("ctx.author.user: ", ctx.author.user)
            print("ctx.author.user.discriminator: ", ctx.author.user.discriminator)
            # print("ctx.author.discriminator: ", ctx.author.discriminator)
            title = ctx.author.name + "#" + ctx.author.user.discriminator
            embed = interactions.Embed(title=title, description="\u200b", image_url=avatar_url)
            embed.set_footer(text = "Built for Habit Nest, powered by Roo Tech", icon_url = "https://cdn.discordapp.com/icons/864029910507323392/e2eb644133171506b6f22e55fb3daed1.webp")
            embed.set_thumbnail(url=avatar_url)

            prompts = [
                        prompt1,
                        prompt2,
                        prompt3,
                        prompt4,
                        prompt5,
                        prompt6,
                        prompt7,
                        prompt8,
                        prompt9
                        ]
            for ii,prompt in enumerate(prompts):
                if prompt != None:
                    embed.add_field(name="\u200b", value=self.labels[ii] + " " + prompt, inline=False)
            # end for

            rchannel = await interactions.get(client, interactions.Channel, object_id=self.response_channel_id[cid])
            await rchannel.send(embeds=embed)
            await ctx.send("We posted your response in <#" + str(self.response_channel_id[cid]) + ">\nGood work!", ephemeral=True)
            if image_url:
                await image_upload.download()
                await ctx.send("Downloaded!", ephemeral=True)
                #await rchannel.send("\u200b", attachments=[image_upload])
                #await ctx.send("And now we sent your uploaded iamge too :)", ephemeral=True)
            # end if

            return

        async def button_func(ctx: interactions.ComponentContext):
            cid = int(ctx.channel_id)

            custom_id = ctx.data.custom_id
            if "special_button" in custom_id:
                print("special_button in custom_id")
                ii = custom_id.replace("special_button", "")
                ii = int(ii)

                trues = 0
                for jj in range(len(self.response_buttons[cid])):
                    if self.labels[jj] in self.special_button_messages[cid][ii]:
                        trues += 1
                # end for

                if trues == len(self.response_buttons[cid]):
                    row = interactions.ActionRow(components=self.response_buttons[cid])
                    await ctx.send(self.special_button_messages[cid][ii], components=row, ephemeral=True)
                else:
                    await ctx.send(self.special_button_messages[cid][ii], ephemeral=True)
                # end if/else

                return
            # end if

            ii = int(custom_id.replace("button", ""))

            if ii < len(self.select_menus[cid]):
                print("ii, self.select_menus[ii]: ", ii, self.select_menus[cid][ii])
                await ctx.send(components=self.select_menus[cid][ii], ephemeral=True)
            else:
                jj = len(self.select_menus[cid]) - ii
                print("ii, jj, self.modals[jj]: ", ii, jj, self.modals[cid][jj])
                await ctx.popup(self.modals[cid][jj])
            # end if/else
            return
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

            print("num, self.button_texts: ", num, self.button_texts[cid])
            print("response, self.button_texts[ii]: ", response, self.button_texts[cid][num])
            print("type response: ", type(response))

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}

            print("modal response author id: ", ctx.author.id)

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print("self.message_text: ", self.message_text[cid])
            data = {
                "records": [
                            {
                                "fields": {
                                    "TimeEST": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "FromGuildId": str(gid),
                                    "Button Channel Id": str(cid),
                                    "Response Channel Id": str(self.response_channel_id[cid]),
                                    "FromDiscordId": str(aid),
                                    "DiscordMessage": self.message_text[cid],
                                    "ButtonType": "DropDown" + str(num+1),
                                    "Response1": response
                                }
                            }
                           ]
                    }

            url = (self.airtable_base + self.time_text[cid].replace(":", "%3A") + " " + str(cid) + " DropDown" + str(num+1)).replace(" ", "%20")
            print("url: ", url)
            asyncio.create_task(self.post_to_airtable)
            msg = f"Your response to {self.button_texts[cid][num]}: {response}"
            print("msg: msg")

            rchannel = await interactions.get(client, interactions.Channel, object_id=self.response_channel_id[cid])
            await rchannel.send(msg)
            return
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
                    responses.append(self.labels[num] + " " + r)
                # end if
            # end for
            print("responses: ", responses)

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            fields = {
                        "TimeEST": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "FromGuildId": str(gid),
                        "Button Channel Id": str(cid),
                        "Response Channel Id": str(self.response_channel_id[cid]),
                        "FromDiscordId": str(aid),
                        "Discord Message": self.message_text[cid],
                        "ButtonType": "TextInput" + str(num-len(self.select_menus[cid])+1)
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

            url = (self.airtable_base + self.time_text[cid].replace(":", "%3A") + " " + str(cid) + " TextInput" + str(num+1 - len(self.select_menus[cid]))).replace(" ", "%20")
            print("url: ", url)
            asyncio.create_task(self.post_to_airtable(url, headers, data))
            msg = f"Your responses to {self.button_texts[cid][num]}: {responses}"
            print("msg: msg")

            if cid not in self.response_dict:
                self.response_dict[cid] = {}
            if aid not in self.response_dict[cid]:
                self.response_dict[cid][aid] = []

            self.response_dict[cid][aid].append(responses)
            self.save_json(self.fname_response_dict, self.response_dict)

            if len(self.response_dict[cid][aid]) == len(self.button_texts[cid]):
                # first, build the embed
                print("dir ctx author: ", dir(ctx.author))
                print("ctx author user: ", ctx.author.user)
                print("dir ctx author user: ", dir(ctx.author.user))
                print("ctx.author.avatar: ", ctx.author.avatar)
                print("ctx.author.nick: ", ctx.author.nick)
                print("ctx.author.name: ", ctx.author.name)
                print("ctx.author.avatar_url: ", ctx.author.user.avatar_url)
                avatar_url = ctx.author.user.avatar_url
                print("avatar_url: ", avatar_url)
                print("type avatar_url: ", type(avatar_url))
                handle = ctx.author.name
                print("handle: ", handle)
                print("type handle: ", type(handle))
                embed = interactions.Embed(title=handle, description="\u200b", image_url=avatar_url)
                embed.set_footer(text = "Built for Habit Nest, powered by Roo Tech", icon_url = "https://cdn.discordapp.com/icons/864029910507323392/e2eb644133171506b6f22e55fb3daed1.webp")
                embed.set_thumbnail(url=avatar_url)
                for responses in self.response_dict[cid][aid]:
                    for response in responses:
                        if len(response) > 1024:
                            chunks = int(math.ceil(len(response)/1022.0))
                            for ii in range(chunks):
                                beg = ii*1022
                                end = (ii+1)*1022

                                val = ""
                                if ii > 1:
                                    val += "-"
                                val = response[beg:end] + "-"
                                embed.add_field(name="\u200b", value=val, inline=False)
                        else:
                            embed.add_field(name="\u200b", value=response, inline=False)
                # end for
                rchannel = await interactions.get(client, interactions.Channel, object_id=self.response_channel_id[cid])
                await rchannel.send(embeds=embed)

                self.response_dict[cid][aid] = []
            # end if

            msg = ""
            for response in responses:
                msg += f"Your response to {self.button_texts[cid][num]}: {response}"
            # end for

            '''
            if len(msg) > 2000:
                chunks = int(math.ceil(len(msg)/1998))
                for ii in range(chunks):
                    beg = ii*1998
                    end = (ii+1)*1998

                    val = ""
                    if ii > 1:
                        val += "-"

                    if end > len(msg):
                        end = len(msg)
                        val = response[beg:end]
                    else:
                        val = response[beg:end] + "-"
                    # end if/else
                    await ctx.send(val, ephemeral=True)
                # end for
            else:
                await ctx.send(msg, ephemeral=True)
            # end if/else
            '''
            await ctx.send("response received", ephemeral=True)

            print("going to return")
            return
        # end modal_response

        for ii in range(self.max_menus):
            client.component("special_button" + str(ii))(button_func)
            client.component("button" + str(ii))(button_func)
            client.component("menu"   + str(ii))(menu_response)
            client.modal(    "modal"  + str(ii))(modal_response)
        # end for ii

        @client.event
        async def on_ready():
            print("ready!")

            while True:
                await self.airtable_stuff(client)
                await asyncio.sleep(5.0)
            # end while True
        # end on_ready

        client.start()
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()
