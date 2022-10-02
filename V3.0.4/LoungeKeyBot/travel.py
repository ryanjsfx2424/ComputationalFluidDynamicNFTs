import os
import ast
import glob
import json
import time
import socket
import requests
from region_data import RegionData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.headless = True

exec_path = "/root/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver_linux"
if socket.gethostname() == "MB-145.local":
  exec_path = "/Users/ryanjsfx/Documents/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver"

class TravelBot(RegionData):
    def __init__(self):
        self.url = "https://secretflying.com"
        self.sleep_time = 60.1

        #self.icon_url = "https://cdn.discordapp.com/attachments/932056137518444594/991364877467783279/Screenshot_2022-06-28_at_13.56.21.png"
        self.icon_url = "https://cdn.discordapp.com/attachments/953289270771220551/994018807813251193/blurred_logo.jpeg"

        self.BOT_COMMANDS_CIDS = [932056137518444594]

        self.CID_VEGAS = 1000549429276848221
        self.CIDS     = self.load_discord_ids("region_data/channel_id_data.json")
        self.TIDS_USA = self.load_discord_ids("region_data/us_region_thread_id_data.json")

        self.roles = {"Authenticated": "979452786355867679",
                      "error-fares"        :"951232895949897779",
                      "usa"                :"985752938376998932",
                      "canada"             :"985753142186618960",
                      "c-america-carribean":"985753244481499187",
                      "south-america"      :"985753389784784947",
                      "europe"             :"985753496391397417",
                      "me-and-north-africa":"985753570504769547",
                      "africa"             :"985753667850338364",
                      "c-and-s-asia"       :"985753732664930354",
                      "east-asia"          :"985753842765398056",
                      "oceania"            :"985753911631700049",
                      "uk-and-ireland"     :"985754061770993684",
                      "northwest"          :"992563715352309830",
                      "southwest"          :"992563988237918299",
                      "greatlakes"         :"992564308967948378",
                      "southeast"          :"992564207910391848",
                      "newengland"         :"992564378673098762",
                      "south"              :"992564134736568473",
                      "midwest"            :"992564037055418438"
                      }

        self.load_region_data()
        self.fares = {}

        self.fname_fares = "old_fares.txt"
        if os.path.exists(self.fname_fares) and os.stat(self.fname_fares).st_size != 0:
            with open(self.fname_fares, "r") as fid:
                line = fid.read()
            # end with
            line = line.replace('', "")
            self.fares = ast.literal_eval(line)
        # end if
    # end __init__

    def load_discord_ids(self, path):
        with open(path, "r") as fid:
            ids = json.loads(fid.read())
        # end with open
        return ids
    # end load_discord_ids

    def get_html(self):
        try:
          resp = requests.get(self.url)
        except:
          return
        print("resp: ", resp)
        self.html = resp.text

        with open("debug0.txt", "w") as fid:
            fid.write(self.html)
        # end with open
    # end get_html

    def get_html_nd(self):
        url = "https://app.nextdeparture.ca/login"

        driver = webdriver.Firefox(options=options, executable_path=exec_path)
        try:
          driver.get(url)
        except Exception as err:
          print("97 err: ", err)
          print("98 err: ", err.args[:])
          driver.close()
          return
        # end try/except

        email_xpath = "//input[@id='email']"
        passw_xpath = "//input[@id='password']"

        email = os.environ.get("lkEmail")
        passw = os.environ.get("lkNDPass")

        driver.find_element(By.XPATH, email_xpath).send_keys(email)
        driver.find_element(By.XPATH, passw_xpath).send_keys(passw)

        act = ActionChains(driver)
        act.send_keys(Keys.ENTER).perform()

        print("sleeping for 5s in nextdeparture")
        time.sleep(5)
        url = "https://app.nextdeparture.ca/user/deals"
        driver.get(url)

        html = driver.page_source
        driver.quit()
        with open("debug1.txt", "w") as fid:
            fid.write(html)
        # end with open

        if self.fares == {}:
            self.fares["urls"]   = []
            self.fares["texts"]  = []
            self.fares["images"] = []
            self.fares["hashtags"] = []
        # end if

        spl_beg = '<div class="card mb-3">'
        fares = html.split(spl_beg)[1:]
        
        for fare in fares:
            spl_beg = '<h4 class="card-title mt-3">'
            spl_end = '</h4>'
            fare_text = fare.split(spl_beg)[1].split(spl_end)[0].replace("&amp;", "&")
            if fare_text in self.fares["texts"]:
                continue
            # end if
            self.fares["texts"].append(fare_text)

            spl_beg = '<img src="'
            spl_end = '"'
            self.fares["images"].append(fare.split(spl_beg)[1].split(spl_end)[0])

            spl_beg = '<a href="'
            self.fares["urls"].append(fare.split(spl_beg)[1].split(spl_end)[0])

            self.fares["hashtags"].append(["#canada_from"])
        # end for

        if self.fares == {} or fare not in self.fares["texts"]:
            if self.fares == {}:
                self.fares["urls"]   = []
                self.fares["texts"]  = []
                self.fares["images"] = []
                self.fares["hashtags"] = []

    # end get_html_nd

    def get_fares(self, fare_type):
        if fare_type == "err":
            try:
              fares = self.html.split("Latest Error Fares")[1].split("Popular Departure Cities")[0]
            except Exception as err:
              print("170 err: ", err)
              print("171 err.args: ", err.args[:])
              print("172 Traceback, html ", self.html)
              return
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

        print("text: ", text)
        for region in self.region_data:
            #print("region: ", region)
            for subregion in self.region_data[region]:
                #print("subregion: ", subregion)
                if subregion.lower().replace(" ","") in text.lower().replace(" ",""):
                    if region == "us_city_map":
                        hashtag = "#" + self.region_data["us_city_map"][subregion]
                        
                        if "#usa" not in hashtags:
                            hashtags.append("#usa")
                        # end if
                    else:
                        if "washingtondc" in text.lower().replace(" ",""):
                            continue
                        # end if
                        hashtag = "#" + region
                    # end if

                    if hashtag not in "".join(hashtags):
                        hashtags.append(hashtag)
                    # end if

                    if subregion in text.split(" to ")[0].lower().replace(" ", ""):
                        if "usa" not in hashtags[-1]:
                            hashtags[-1] = hashtags[-1] + "_from"
                # end if
            # end for
        # end for
    # end get_new_hashtags_from_regions
# end class TravelBot
## end travel.py
