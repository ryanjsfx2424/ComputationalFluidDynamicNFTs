import os
import glob
import json
import requests
from region_data import RegionData
class TravelBot(RegionData):
    def __init__(self):
        self.url = "https://secretflying.com"
        self.sleep_time = 60.1

        self.icon_url = "https://cdn.discordapp.com/attachments/932056137518444594/991364877467783279/Screenshot_2022-06-28_at_13.56.21.png"

        self.BOT_COMMANDS_CIDS = [932056137518444594]

        self.CIDS     = self.load_discord_ids("region_data/channel_id_data.json")
        self.TIDS_USA = self.load_discord_ids("region_data/us_region_thread_id_data.json")

        self.load_region_data()
        self.fares = {}
    # end __init__

    def load_discord_ids(self, path):
        with open(path, "r") as fid:
            ids = json.loads(fid.read())
        # end with open
        return ids
    # end load_discord_ids

    def get_html(self):
        resp = requests.get(self.url)
        print("resp: ", resp)
        self.html = resp.text

        with open("html.txt", "w") as fid:
            fid.write(self.html)
        # end with open
    # end get_html

    def get_fares(self, fare_type):
        if fare_type == "err":
            fares = self.html.split("Latest Error Fares")[1].split("Popular Departure Cities")[0]
        else:
            fares = self.html.split("Latest Deals")[1].split("As seen on")[0]
        # end if/else
        imgs = fares.split("<img ")[1:]

        images = []
        for image in imgs:
            image = image.split('src="')[1].split('"')[0]
            if "EXPIRED" not in image or fare_type != "err":
                images.append(image)
            # end if
        # end for

        fares = fares.split('<h3 class="entry-title">')
        for ii,fare in enumerate(fares[1:]):
            url = fare.split('<a href="')[2].split(" ")[0].split('"')[0]
            fare = fare.split('title="')[1].split('" ')[0]
            image = images[ii]
            if "Hotel" in fare:
                continue
            # end if

            if self.fares == {} or fare not in self.fares["texts"]:
                if self.fares == {}:
                    self.fares["urls"]   = []
                    self.fares["texts"]  = []
                    self.fares["images"] = []
                    self.fares["hashtags"] = []
                # end if
                self.fares["urls"].append(url)
                self.fares["texts"].append(fare)
                self.fares["images"].append(image)
                if fare_type == "err":
                    self.fares["hashtags"].append(["#error-fares"])
                else:
                    self.fares["hashtags"].append([])
                # end if/else
                self.get_new_hashtags_from_regions()
            # end if
        # end for
    # end get_fares

    def get_new_hashtags_from_regions(self):
        text = self.fares["texts"][-1]
        hashtags = self.fares["hashtags"][-1]

        for region in self.region_data:
            #print("region: ", region)
            for subregion in self.region_data[region]:
                #print("subregion: ", subregion)
                if subregion in text.lower().replace(" ",""):
                    if region == "us_city_map":
                        hashtag = "#" + self.region_data["us_city_map"][subregion]
                        
                        if "#usa" not in hashtags:
                            hashtags.append("#usa")
                        # end if
                    else:
                        hashtag = "#" + region
                    # end if

                    if hashtag not in hashtags:
                        hashtags.append(hashtag)
                    # end if
                # end if
            # end for
        # end for
    # end get_new_hashtags_from_regions
# end class TravelBot
## end travel.py