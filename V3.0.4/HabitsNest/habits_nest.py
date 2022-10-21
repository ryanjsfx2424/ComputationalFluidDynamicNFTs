## invite link: https://discord.com/api/oauth2/authorize?client_id=1019966201008488488&permissions=3072&scope=bot
## above uses scopes (1): 1) bot
## above uses perms (2): 1) read messages/view channels & 2) send messages
## current channel permissions required (4): 1) view channel, 2) send messages, 3) embed links, 4) attach files
import os
import io
import sys
import math
import json
import time
import glob
import copy
import shutil
import pickle
import socket
import requests
import asyncio
import datetime
import numpy as np
from pytz import timezone
import interactions

class HabitsNest(object):
    def __init__(self):
        self.max_menus = 10

        self.labels = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣".split()

        self.APPROVED_USERS = [855616810525917215, 866735417566429225, 318615282245566466, 869988952688451594] # me, Lin, Mikey, Ari
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

        self.fname_button_texts        = "data_big/button_texts.pickle"
        self.fname_modals              = "data_big/modals.pickle"
        self.fname_select_menus        = "data_big/select_menus.pickle"
        self.fname_message_text        = "data_big/message_text.pickle"
        self.fname_response_channel_id = "data_big/response_channel_id.pickle"
        self.fname_response_buttons    = "data_big/response_buttons.pickle"
        self.fname_special_button_messages = "data_big/special_button_messages.pickle"
        self.fname_guilds = "data_big/guilds.pickle"
        self.fname_prompts = "data_big/prompts.pickle"

        self.fname_button_ids = "data_big/button_ids.pickle"
        self.fname_menu_ids = "data_big/menu_ids.pickle"
        self.fname_modal_ids = "data_big/modal_ids.pickle"
        self.fname_special_button_ids = "data_big/special_button_ids.pickle"
    # end init_fnames

    def init_data(self):
        self.rows_handled =  self.load_arr() # obselete
        self.response_dict = self.load_json(self.fname_response_dict, dtype = {}) #obselete
        self.times_handled = self.load_pickle(self.fname_times, dtype = {
            1001020922423152691:
                [
                    "2024-10-04 1:00 PM", 
                    "2024-10-05 1:01 PM", 
                    "2024-10-05 1:01 PM",
                    "2022-10-07 1:01 PM",
                    "2022-10-17 11:40AM",
                    "2022-10-18 12:40PM",
                    "2022-10-19 10:00AM",
                    "2022-10-20 10:00AM"
                ]
            }
        )

        self.button_texts        = self.load_pickle(self.fname_button_texts)
        self.modals              = self.load_pickle(self.fname_modals)
        self.select_menus        = self.load_pickle(self.fname_select_menus)
        self.message_text        = self.load_pickle(self.fname_message_text)
        self.response_channel_id = self.load_pickle(self.fname_response_channel_id)
        self.response_buttons    = self.load_pickle(self.fname_response_buttons)
        self.special_button_messages = self.load_pickle(self.fname_special_button_messages)

        self.GUILDS = self.load_pickle(self.fname_guilds, dtype=self.GUILDS)
        self.prompts = self.load_pickle(self.fname_prompts)

        self.button_ids = self.load_pickle(self.fname_button_ids)
        self.menu_ids = self.load_pickle(self.fname_menu_ids)
        self.modal_ids = self.load_pickle(self.fname_modal_ids)
        self.special_button_ids = self.load_pickle(self.fname_special_button_ids)
    # end init_data

    def save_pickles(self):
        self.save_pickle(self.fname_times,               self.times_handled)
        self.save_pickle(self.fname_button_texts,        self.button_texts)
        self.save_pickle(self.fname_modals,              self.modals)
        self.save_pickle(self.fname_select_menus,        self.select_menus)
        self.save_pickle(self.fname_message_text,        self.message_text)
        self.save_pickle(self.fname_response_channel_id, self.response_channel_id)
        self.save_pickle(self.fname_response_buttons, self.response_buttons)
        self.save_pickle(self.fname_special_button_messages, self.special_button_messages)
        self.save_pickle(self.fname_guilds, self.GUILDS)
        self.save_pickle(self.fname_prompts, self.prompts)
        self.save_pickle(self.fname_button_ids, self.button_ids)
        self.save_pickle(self.fname_menu_ids, self.menu_ids)
        self.save_pickle(self.fname_modal_ids, self.modal_ids)
        self.save_pickle(self.fname_special_button_ids, self.special_button_ids)
    # end save_pickles

    def save_pickle(self, fname, obj):
        with open(fname, "wb") as fid:
            pickle.dump(obj, fid, pickle.HIGHEST_PROTOCOL)
        # end with
    # end save_pickle

    def load_pickle(self, fname, dtype={}):
        result = copy.deepcopy(dtype)
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
        # print("[HH], [MM]: ", [HH], [MM])

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

    async def airtable_stuff(self, button_func, menu_response, modal_response):
        if "airTable" not in os.environ:
            print("err, forgot to export airTable environment variable.")
            sys.exit()
        # end if
        headers = {"Content-Type":"json", "Authorization":"Bearer " + os.environ["airTable"]}
        req = requests.get(self.airtable_url, headers=headers)
        # print("airtable_stuff req.status_code: ", req.status_code)
        
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

        with open("data_big/debug_airtable.json", "w") as fid:
            json.dump(result, fid)
        # end with

        for record in result["records"]:
            if str(record) in self.rows_handled:
                continue
            # end if
            fields = record["fields"]

            if len(fields) < 4:
                continue
            # end if

            if "Discord Message" not in fields:
                continue

            try:
                time_to_send = fields["TimeEST"]

            except Exception as err:
                continue

            time_to_send = time_to_send.replace(" copy", "")
            try:
                good_to_send = self.process_time(time_to_send)
            except:
                good_to_send = False

            if not good_to_send:
                continue
            # end if

            try:
                channel_id  = fields["Button Channel Id"]
                rchannel_id = fields["Response Channel Id"]

            except Exception as err:
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
                channel  = await interactions.get(self.client, interactions.Channel, object_id=channel_id)
                rchannel = await interactions.get(self.client, interactions.Channel, object_id=rchannel_id)
            
            except Exception as err:
                print("couldn't get channel for channel_id: ", channel_id)
                print("205 err: ", err)
                print("206 err.args: ", err.args[:])
                continue
            # end try/except
            print("got channel!")

            cid = channel_id

            # print("self.times_handled: ", self.times_handled)
            # input(">>")

            if cid in self.times_handled and time_to_send in self.times_handled[cid]:
                #print("times handled skip")
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
                custom_id = "button" + str(ii) + "_" + time_to_send + "_" + str(cid)

                buttons.append(interactions.Button(style=1, label=label,
                                custom_id=custom_id
                                ))
                self.client.component(custom_id)(button_func)

                if cid not in self.button_ids:
                    self.button_ids[cid] = {}

                if time_to_send not in self.button_ids[cid]:
                    self.button_ids[cid][time_to_send] = []

                self.button_ids[cid][time_to_send].append(custom_id)

                select_options = []
                for dropdown_option in dropdowns[ii]:
                    select_options.append(interactions.SelectOption(
                        label=dropdown_option, value=dropdown_option, description=dropdown_option))
                # end for

                custom_id = "menu" + str(ii) + "_" + time_to_send + "_" + str(cid)
                select_menus.append(interactions.SelectMenu(
                    options=select_options,
                    placeholder=label,
                    custom_id=custom_id
                ))
                self.client.component(custom_id)(menu_response)

                if cid not in self.menu_ids:
                    self.menu_ids[cid] = {}

                if time_to_send not in self.menu_ids[cid]:
                    self.menu_ids[cid][time_to_send] = []

                self.menu_ids[cid][time_to_send].append(custom_id)
            # end for
            
            cnt = 0
            modals = []
            for jj in range(len(textinputs)):
                cnt2 += 1
                label = self.labels[cnt2]

                custom_id = "button" + str(cnt2) + "_" + time_to_send + "_" + str(cid)
                button_texts.append(label)
                buttons.append(interactions.Button(style=1, label=label,
                                custom_id=custom_id))
                self.client.component(custom_id)(button_func)

                if cid not in self.button_ids:
                    self.button_ids[cid] = {}

                if time_to_send not in self.button_ids[cid]:
                    self.button_ids[cid][time_to_send] = []

                self.button_ids[cid][time_to_send].append(custom_id)


                modal_components = []
                for kk in range(len(textinputs[jj])):
                    cnt += 1
                    modal_components.append(interactions.TextInput(
                        style=interactions.TextStyleType.PARAGRAPH,
                        label=textinputs[jj][kk],
                        custom_id="text-input-" + str(cnt) + "_" + time_to_send,
                    ))
                # end for

                custom_id = "modal" + str(cnt2) + "_" + time_to_send + "_" + str(cid)
                modals.append(interactions.Modal(
                            title=label,
                            custom_id=custom_id,
                            components=modal_components
                ))
                self.client.modal(custom_id)(modal_response)

                if cid not in self.modal_ids:
                    self.modal_ids[cid] = {}

                if time_to_send not in self.modal_ids[cid]:
                    self.modal_ids[cid][time_to_send] = []

                self.modal_ids[cid][time_to_send].append(custom_id)
            # end for

            prompts = []
            for ii,label in enumerate(self.labels):
                if label in message_text:
                    prompt = message_text.split(label)[-1]
                    if ii+1 < len(self.labels):
                        if self.labels[ii+1] in prompt:
                            prompt = prompt.split(self.labels[ii+1])[0]
                        else:
                            if "\n" in prompt:
                                prompt = prompt.split("\n")[0]
                    else:
                        if "\n" in prompt:
                            prompt = prompt.split("\n")[0]
                    prompts.append(prompt)
                # end if
            # end for

            #print("message_text1: ", message_text)
            #print("548 special_button_messages: ", self.special_button_messages)
            #print("549 special_button_messages: ", special_button_messages)

            if cid not in self.message_text:
                self.modals[cid] = {} # not tested
                self.button_texts[cid] = {} # not tested
                self.select_menus[cid] = {} # not tested

                self.message_text[cid] = {}
                self.response_channel_id[cid] = {}
                self.special_button_messages[cid] = {}
                self.response_buttons[cid] = {}
                self.prompts[cid] = {}
            # end if
            self.modals[cid][time_to_send] = modals
            self.button_texts[cid][time_to_send] = button_texts
            self.select_menus[cid][time_to_send] = select_menus

            self.message_text[cid][time_to_send] = message_text.replace("\\n", "\n").replace("\*", "*")
            self.response_channel_id[cid][time_to_send] = rchannel_id
            self.special_button_messages[cid][time_to_send] = special_button_messages
            self.response_buttons[cid][time_to_send] = buttons
            self.special_button_messages[cid][time_to_send] = special_button_messages
            self.prompts[cid][time_to_send] = prompts

            if cid not in self.times_handled:
                self.times_handled[cid] = []
            # end if

            self.times_handled[cid].append(time_to_send)
            self.save_pickles()

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
                    custom_id = "special_button" + str(mm) + "_time" + time_to_send + "_" + str(cid)
                    button = interactions.Button(style=1, label=special_button_names[mm],
                                custom_id=custom_id)
                    self.client.component(custom_id)(button_func)

                    if cid not in self.special_button_ids:
                        self.special_button_ids[cid] = {}

                    if time_to_send not in self.special_button_ids[cid]:
                        self.special_button_ids[cid][time_to_send] = []

                    self.special_button_ids[cid][time_to_send].append(custom_id)


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

                with open("data_big/" + image_name, "wb") as fid:
                    shutil.copyfileobj(r.raw, fid)
                # end with
                print("Image downloaded!")
                image_file = interactions.File(filename="data_big/" + image_name)

                print("channel_id: ", channel_id)
                await channel.send(files=image_file)
            # end for attachments

            self.save_pickle(self.fname_special_button_ids, self.special_button_ids)

            self.rows_handled.append(str(record))
            self.save_arr()
        # end records
    # end airtable_stuff

    async def post_to_airtable(self, url, headers, data):
        req = requests.post(url, headers=headers, json=data)        
        print("req.status_code: ", req.status_code)

    def discord_bot(self):
        client = interactions.Client(token=os.environ["habitsNestBotPass"])#, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)
        self.client = client

        @client.command(
            name="habit-nest-add-guild",
            description="Add a guild (discord server) habit nest daily challenge bot will accept commands from",
            scope=self.GUILDS,
            options=[
                interactions.Option(
                    name="guild_id",
                    description="The discord server ('guild') id.",
                    type=interactions.OptionType.STRING,
                    required=True,
                )
            ]
        )
        async def add_guild(ctx: interactions.CommandContext, guild_id: str):
            if int(ctx.author.id) not in self.APPROVED_USERS:
                await ctx.send("Error, only Luna, Lin, Mikey, and Ari can use this command presently.", ephemeral=True)
                return

            try:
                guild_id = int(guild_id)
            except Exception as err:
                print("629 err: ", err)
                print("630 err.args: ", err.args[:])
                await ctx.send("error, guild_id was not an integer", ephemeral=True)
            # end try/except

            self.GUILDS.append(guild_id)
            self.save_pickle(self.fname_guilds, self.GUILDS)
            await ctx.send("saved guild. now we need to rooboot for that to take effect", ephemeral=True)

            fname = "data_big/pid.txt"
            os.system("ps aux | grep habits_nest.py > " + fname)
            with open(fname, "r") as fid:
                for line in fid:
                    if "grep" not in line:
                        pid = line.split()[1]
                        break

            logfiles = np.sort(glob.glob("logfile*"))
            num = 1
            if len(logfiles) != 0:
                num = int(logfiles[-1].replace("logfile","").replace(".txt",""))
            # end if

            newlog = "logfile" + str(num).zfill(6) + ".txt"
            await ctx.send("okay all is swell, launching new process then killing myself to complete the reboot", ephemeral=True)
            os.system("nohup python3 -u habits_nest.py > " + newlog + " 2>&1 &")
            os.system("kill " + pid)
        # end add_guild

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
                    type=interactions.OptionType.STRING,
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
        async def cmd(ctx: interactions.CommandContext, prompt1: str, days_old: str = None, 
                      image_upload: interactions.Attachment = None,
                      prompt2: str=None,
                      prompt3: str=None,
                      prompt4: str=None,
                      prompt5: str=None,
                      prompt6: str=None,
                      prompt7: str=None,
                      prompt8: str=None,
                      prompt9: str=None):
            gid = int(ctx.guild.id)
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
                try:
                    days_old = int(days_old)
                except Exception as err:
                    print("762 err: ", err)
                    print("763 err.args: ", err.args[:])
                    await ctx.send("error, expected an integer for 'days_old' but received: " + str(days_old), ephemeral=True)
                    return
            else:
                days_old = 0
            # end if/else

            if days_old < 0:
                await ctx.send("error, exptected 'days_old' >= 0 but received: " + str(days_old), ephemeral=True)
                return
            # end if

            times_to_send = np.sort(list(self.message_text[cid].keys()))
            if days_old >= len(times_to_send):
                await ctx.send("error days_old > number of daily challenges in this discord! Received: " + str(days_old), ephemeral=True)
                return
            # end if
            time_to_send = times_to_send[-1-days_old]

            response_map = {0:"today", 1:"yesterday"}
            if days_old == 0:
                description = "responses for today's challenge!"
            elif days_old == 1:
                description = "responses for yesterday's challenge!"
            else:
                description = "responses for challenge from " + str(days_old) + " days ago!"
            # end if/elif/else

            avatar_url = ctx.author.user.avatar_url
            title = ctx.author.name + "#" + ctx.author.user.discriminator
            embed = interactions.Embed(title=title, description=description, image_url=avatar_url)
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
            responses = ""
            for ii,prompt in enumerate(prompts):
                if prompt != None:

                    if ii < len(self.prompts[cid][time_to_send]):
                        end = min(40,len(self.prompts[cid][time_to_send][ii]))
                        if end < 40:
                            name = self.labels[ii] + " " + self.prompts[cid][time_to_send][ii][:end]
                        else:
                            name = self.labels[ii] + " " + self.prompts[cid][time_to_send][ii][:end] + "..."
                        value = prompt

                    else:
                        name = "\u200b"
                        value = self.labels[ii] + " " + prompt
                    # end if/else
                    responses += self.labels[ii] + " " + prompt + "\n\n"
                    embed.add_field(name=name, value=value, inline=False)
            # end for

            rchannel = await interactions.get(client, interactions.Channel, object_id=self.response_channel_id[cid][time_to_send])
            await rchannel.send(embeds=embed)
            await ctx.send("We posted your response in <#" + str(self.response_channel_id[cid][time_to_send]) + ">\nGood work!", ephemeral=True)

            if image_url:
                r = requests.get(image_url, stream=True)
                print("r.status_code: ", r.status_code)
                r.raw.decode_content = True

                image_name = "data_big/temp_image_file_" + str(int(time.time())) + "." + image_upload.content_type.split("/")[1]
                with open(image_name, "wb") as fid:
                    shutil.copyfileobj(r.raw, fid)
                # end with

                print("Image downloaded!")
                image_file = interactions.File(filename=image_name)
                message = await rchannel.send(files=image_file)
                print("dir message of image: ", dir(message))
                print("dir message.attachments: ", dir(message.attachments))
                print("message.attachments: ", message.attachments)
                print("dir message.attachments0: ", dir(message.attachments[0]))
                print("message.attachments0.url: ", message.attachments[0].url)
                image_url = message.attachments[0].url
                print("message.url: ", message.url)
                await ctx.send("And now we sent your uploaded iamge too :)", ephemeral=True)
                os.system("rm " + image_name)
            # end if

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            fields = {
                        "TimeEST": time_to_send,
                        "Button Channel Id": str(cid),
                        "Response Channel Id": str(self.response_channel_id[cid][time_to_send]),
                        "Discord Message": self.message_text[cid][time_to_send],
                        "FromGuildId": str(gid),
                        "TimeSubmitted": tnow,
                        "FromDiscordId": str(aid),
                        "FromDiscordUsernameAndDiscriminator": ctx.author.name + "#" + ctx.author.user.discriminator,
                        "Responses": responses
                    }

            if image_url:
                fields["AttachmentSubmittedURL"] = image_url
            # end if

            data = {
                "records": [
                            {
                                "fields": fields
                            }
                           ]
                    }

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}
            url = (self.airtable_base + "Responses").replace(" ", "%20")
            print("url: ", url)
            asyncio.create_task(self.post_to_airtable(url, headers, data))

            return

        async def button_func(ctx: interactions.ComponentContext):
            cid = int(ctx.channel_id)

            custom_id = ctx.data.custom_id
            print("custom_id: ", custom_id)
            if "special_button" in custom_id:
                print("special_button in custom_id")
                ii = custom_id.replace("special_button", "")

                if "_" not in ii:
                    await ctx.send("clicked on a really old button? sorry I can't handle that rn :(", ephemeral=True)
                    return
                # end if

                ii,time_to_send,junk = ii.split("_")
                time_to_send = time_to_send.replace("time","")
                ii = int(ii)

                print("special_button_messages[cid][time_to_send]: ", self.special_button_messages[cid][time_to_send])

                trues = 0
                for jj in range(len(self.response_buttons[cid][time_to_send])):
                    if self.labels[jj] in self.special_button_messages[cid][time_to_send][ii]:
                        trues += 1
                # end for

                if trues == len(self.response_buttons[cid][time_to_send]):
                    row = interactions.ActionRow(components=self.response_buttons[cid][time_to_send])
                    await ctx.send(self.special_button_messages[cid][time_to_send][ii], components=row, ephemeral=True)
                else:
                    await ctx.send(self.special_button_messages[cid][time_to_send][ii], ephemeral=True)
                # end if/else

                return
            # end if

            ii = custom_id.replace("button", "")
            if "_" not in ii:
                await ctx.send("clicked on a really old button? sorry I can't handle that rn :(", ephemeral=True)
                return
            # end if

            ii,time_to_send,junk = ii.split("_")
            time_to_send = time_to_send.replace("time","")
            ii = int(ii)

            if ii < len(self.select_menus[cid][time_to_send]):
                print("ii, self.select_menus[ii]: ", ii, self.select_menus[cid][time_to_send][ii])
                await ctx.send(components=self.select_menus[cid][time_to_send][ii], ephemeral=True)

            else:
                jj = len(self.select_menus[cid][time_to_send]) - ii
                print("ii, jj, self.modals[jj]: ", ii, jj, self.modals[cid][time_to_send][jj])
                await ctx.popup(self.modals[cid][time_to_send][jj])
            # end if/else

            return
        # end def

        async def menu_response(ctx: interactions.CommandContext, response: str):
            gid = int(ctx.guild.id)
            aid = int(ctx.author.id)
            cid = int(ctx.channel_id)

            custom_id = ctx.data.custom_id
            num = custom_id.replace("menu", "").replace("modal","")

            if "_" not in num:
                await ctx.send("clicked on a really old button? sorry I can't handle that rn :(", ephemeral=True)
                return
            # end if

            num,time_to_send,junk = num.split("_")
            time_to_send = time_to_send.replace("time","")
            num = int(num)

            if type(response) == type([]):
                response = response[0]
            # end if

            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fields = {
                        "TimeEST": time_to_send,
                        "Button Channel Id": str(cid),
                        "Response Channel Id": str(self.response_channel_id[cid][time_to_send]),
                        "Discord Message": self.message_text[cid][time_to_send],
                        "FromGuildId": str(gid),
                        "TimeSubmitted": tnow,
                        "FromDiscordId": str(aid),
                        "FromDiscordUsernameAndDiscriminator": ctx.author.name + "#" + ctx.author.user.discriminator,
                        "MenuResponse": response
                    }
            data = {
                "records": [
                            {
                                "fields": fields
                            }
                           ]
                    }

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}
            url = (self.airtable_base + "Responses").replace(" ", "%20")
            print("url: ", url)
            asyncio.create_task(self.post_to_airtable(url, headers, data))
            await ctx.send("Selection received!", ephemeral=True)

            ## this would be an embed now
            # rchannel = await interactions.get(client, interactions.Channel, object_id=self.response_channel_id[cid][time_to_send])
            # await rchannel.send(msg)
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
            num = custom_id.replace("menu", "").replace("modal","")

            if "_" not in num:
                await ctx.send("clicked on a really old button? sorry I can't handle that rn :(", ephemeral=True)
                return
            # end if

            num,time_to_send,junk = num.split("_")
            time_to_send = time_to_send.replace("time","")
            num = int(num)

            responses = []
            rs = [response1, response2, response3, response4, response5,
                  response6, response7, response8, response9]
            for r in rs:
                if r is not None:
                    responses.append(self.labels[num] + " " + r)
                # end if
            # end for
            print("responses: ", responses)


            tnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ## need to adjust the below!! e.g., get gid
            fields = {
                        "TimeEST": time_to_send,
                        "Button Channel Id": str(cid),
                        "Response Channel Id": str(self.response_channel_id[cid][time_to_send]),
                        "Discord Message": self.message_text[cid][time_to_send],
                        "FromGuildId": str(gid),
                        "TimeSubmitted": tnow,
                        "FromDiscordId": str(aid),
                        "FromDiscordUsernameAndDiscriminator": ctx.author.name + "#" + ctx.author.user.discriminator,
                        "Responses": "\n\n".join(responses)
                    }
            data = {
                "records": [
                            {
                                "fields": fields
                            }
                           ]
                    }

            headers = {"Content-Type":"application/json", "Authorization":"Bearer " + os.environ["airTable"]}
            url = (self.airtable_base + "Responses").replace(" ", "%20")
            print("url: ", url)
            asyncio.create_task(self.post_to_airtable(url, headers, data))

            if cid not in self.response_dict:
                self.response_dict[cid] = {}
            if time_to_send not in self.response_dict[cid]:
                self.response_dict[cid][time_to_send] = {}
            if aid not in self.response_dict[cid][time_to_send]:
                self.response_dict[cid][time_to_send][aid] = []

            self.response_dict[cid][time_to_send][aid].append(responses)
            self.save_json(self.fname_response_dict, self.response_dict)

            if len(self.response_dict[cid][time_to_send][aid]) == len(self.button_texts[cid][time_to_send]):
                # first, build the embed
                avatar_url = ctx.author.user.avatar_url
                title = ctx.author.name + "#" + ctx.author.user.discriminator
                embed = interactions.Embed(title=title, description="\u200b", image_url=avatar_url)
                embed.set_footer(text = "Built for Habit Nest, powered by Roo Tech", icon_url = "https://cdn.discordapp.com/icons/864029910507323392/e2eb644133171506b6f22e55fb3daed1.webp")
                embed.set_thumbnail(url=avatar_url)
                for responses in self.response_dict[cid][time_to_send][aid]:
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
                rchannel = await interactions.get(client, interactions.Channel, object_id=self.response_channel_id[cid][time_to_send])
                await rchannel.send(embeds=embed)

                self.response_dict[cid][time_to_send][aid] = []
            # end if

            await ctx.send("response received", ephemeral=True)

            return
        # end modal_response

        for cid in self.special_button_ids:
            for time_to_send in self.special_button_ids[cid]:
                for special_button_id in self.special_button_ids[cid][time_to_send]:
                    self.client.component(special_button_id)(button_func)
        for cid in self.button_ids:
            for time_to_send in self.button_ids[cid]:
                for button_id in self.button_ids[cid][time_to_send]:
                    self.client.component(button_id)(button_func)
        for cid in self.menu_ids:
            for time_to_send in self.menu_ids[cid]:
                for menu_id in self.menu_ids[cid][time_to_send]:
                    self.client.component(menu_id)(menu_response)
        for cid in self.modal_ids:
            for time_to_send in self.modal_ids[cid]:
                for modal_id in self.modal_ids[cid][time_to_send]:
                    self.client.modal(modal_id)(modal_response)

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
                await self.airtable_stuff(button_func, menu_response, modal_response)
                await asyncio.sleep(5.0)
            # end while True
        # end on_ready

        client.start()
    # end discord_bot
# end HabitsNest

if __name__ == "__main__":
    hn = HabitsNest()
    hn.discord_bot()
