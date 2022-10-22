import os
import ast
import glob
import json
import time
import socket
import asyncio
import discord
import requests
from region_data import RegionData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.headless = True

exec_path = "/root/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver_linux"
if "MB-145" in socket.gethostname():
  exec_path = "/Users/ryanjsfx/Documents/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver"

class TravelBot(RegionData):
    def __init__(self):
        self.TESTING = False

        self.url = "https://secretflying.com"
        self.sleep_time = 60.1

        #self.icon_url = "https://cdn.discordapp.com/attachments/932056137518444594/991364877467783279/Screenshot_2022-06-28_at_13.56.21.png"
        self.icon_url = "https://cdn.discordapp.com/attachments/953289270771220551/994018807813251193/blurred_logo.jpeg"

        self.BOT_COMMANDS_CIDS = [932056137518444594]

        self.BUSINESS_CID = 1025549865561894972
        self.FIRST_CLASS_CID = 1025550542761635850

        self.ONE_HOUR = 3600
        self.time_since_last_business_ping    = time.time() - self.ONE_HOUR
        self.time_since_last_first_class_ping = time.time() - self.ONE_HOUR
        self.time_since_last_ping = {}

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
        self.fares_scotts = {}

        self.fname_fares = "old_fares.txt"
        if os.path.exists(self.fname_fares) and os.stat(self.fname_fares).st_size != 0:
            with open(self.fname_fares, "r") as fid:
                line = fid.read()
            # end with
            line = line.replace('', "")
            self.fares = ast.literal_eval(line)
        # end if

        self.fname_fares_scotts = "old_fares_scotts.txt"
        self.scotts_already_visited = self.load_json(self.fname_fares_scotts)

        # if os.path.exists(self.fname_fares_scotts) and os.stat(self.fname_fares_scotts).st_size != 0:
        #     with open(self.fname_fares_scotts, "r") as fid:
        #         line = fid.read()
        #     # end with
        #     line = line.replace('', "")
        #     self.fares_scotts = ast.literal_eval(line)
        # # end if

        self.old_fares = []
        if self.fares != {}:
            self.old_fares += self.fares["texts"]

        # if self.fares_scotts != {}:
        #     self.old_fares += self.fares_scotts["texts"]
    # end __init__

    def load_json(self, fname, dtype=[]):
        arr = dtype
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "r") as fid:
                arr = json.load(fid)
            # end with
        # end if
        return arr
    # end load_json

    def save_json(self, fname, data):
        with open(fname, "w") as fid:
            json.dump(data, fid)
        # end with
    # end save_json

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

    async def get_html_nd(self):
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
        await asyncio.sleep(5)
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

    async def get_fares_scotts(self):
        tstart = time.time()
        url = "https://app.scottscheapflights.com/login"

        business_channel    = self.client.get_channel(self.BUSINESS_CID)
        first_class_channel = self.client.get_channel(self.FIRST_CLASS_CID)

        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path=exec_path)
        driver.get(url)
        driver.fullscreen_window()

        email_xpath  = '//input[@name="email"]'
        passw_xpath  = '//input[@name="password"]'
        email = os.environ.get("lkEmail")
        passw = os.environ.get("lkNDPass")

        driver.find_element(By.XPATH, email_xpath ).send_keys(email)
        await asyncio.sleep(0.1)
        driver.implicitly_wait(10)
        await asyncio.sleep(0.1)
        driver.find_element(By.XPATH, passw_xpath ).send_keys(passw)

        act = ActionChains(driver)
        act.send_keys(Keys.ENTER).perform()

        #await asyncio.sleep(10)

        base = "https://app.scottscheapflights.com"
        url = base + "/route/us/from-auto/nz/to-auckland/standard/auto?cos=economy"

        deals_class = "DealCardstyled-sc-1y5rz5y-12 iWtlCA DealGridstyled__DealCardItem-sc-wxnuip-2 fqkPVX"
        deals_xpath = '//div[@class="DealCardstyled-sc-1y5rz5y-12 iWtlCA DealGridstyled__DealCardItem-sc-wxnuip-2 fqkPVX"]'
        deals_class = '"Link__StyledCoreLink-sc-1h103ma-0 eiEvAU DealCard___StyledLink-sc-1m8z4ys-0 jrpdrz"'
        deals_xpath = '//a[@class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU DealCard___StyledLink-sc-1m8z4ys-0 jrpdrz"]'
        deals_csss  = "a.DealCard___StyledLink-sc-1m8z4ys-0"

        image_xpath = '//img[@class="RouteImageContainerstyled__RouteImage-sc-1g5bk2f-4 dNbvtN"]'
        image_csss  = 'img.RouteImageContainerstyled__RouteImage-sc-1g5bk2f-4'


        h1_xpath = '//h1[@class="Headingstyled__H1-sc-1m02ur5-0 gQWhhr RouteTitlestyled-sc-1jwxr9x-3 fzKwOb"]'
        h1_csss  = 'h1.RouteTitlestyled-sc-1jwxr9x-3'

        cities_xpath = './/span[@class="RouteTitlestyled__RouteCity-sc-1jwxr9x-0 eQFYGB"]'
        cities_csss  = 'span.RouteTitlestyled__RouteCity-sc-1jwxr9x-0'
        countries_xpath = './/div[@class="Paragraph-sc-ivzkw1-0 RouteTitlestyled__RouteCountry-sc-1jwxr9x-1 ddVNcC jsCoDc"]'
        countries_csss  = 'div.RouteTitlestyled__RouteCountry-sc-1jwxr9x-1'

        rarity_and_time_csss = 'span.DealDetailsstyled__DealDetailsValue-sc-2a3eq9-3'
        #rarity_xpath = '//span[@class="DealDetailsstyled__DealDetailsValue-sc-2a3eq9-3 bcQPgC"]'
        #time_xpath = '//span[@class="DealDetailsstyled__DealDetailsValue-sc-2a3eq9-3 lndALR"]'

        price_xpath = '//h2[@class="Headingstyled__H2-sc-1m02ur5-1 bgUUHW BookingDetailsstyled__BookingDetailsHeading-sc-1k8ynhk-7 fbgyZM"]'
        price_csss = 'h2.BookingDetailsstyled__BookingDetailsHeading-sc-1k8ynhk-7'
#<h2 class="Headingstyled__H2-sc-1m02ur5-1 bgUUHW BookingDetailsstyled__BookingDetailsHeading-sc-1k8ynhk-7 cJYfXP">$558</h2>

        flight_and_class_xpath = '//div[@class="Paragraph-sc-ivzkw1-0 BookingDetailsstyled__BookingAttribute-sc-1k8ynhk-5 icRgRK sScmo"]'
        flight_and_class_csss = "div.BookingDetailsstyled__BookingDetailsAttributeContainer-sc-1k8ynhk-6"
        flight_and_class_csss = "div.BookingDetailsstyled__BookingAttribute-sc-1k8ynhk-5"

        #<div class="Paragraph-sc-ivzkw1-0 BookingDetailsstyled__BookingAttribute-sc-1k8ynhk-5 icRgRK fNXfxv">Roundtrip</div>
        #<div class="Paragraph-sc-ivzkw1-0 BookingDetailsstyled__BookingAttribute-sc-1k8ynhk-5 icRgRK fNXfxv">Business Class</div>
#div.DealInformationContainerstyled__BookingDetailsContainer-sc-kj793i-0.zQIwD

#body > div.react-root > div > div.styled__PageContent-sc-1pa7pq-6.EDwB > main > div > div.Routestyled__RoutePageMobileView-sc-1ipck3y-8.ivrSl > div:nth-child(2) > div > div > div > div.DealInformationContainerstyled__BookingDetailsContainer-sc-kj793i-0.zQIwD > div > div:nth-child(2) > div > div > div:nth-child(1)

#<div class="Paragraph-sc-ivzkw1-0 BookingDetailsstyled__BookingAttribute-sc-1k8ynhk-5 icRgRK fNXfxv">Roundtrip</div>

        normal_price_xpath1 = '//div[@class="BookingDetailsstyled__BookingDetailsSection-sc-1k8ynhk-9 kHUIQL"]'
        normal_price_csss = 'div.BookingDetailsstyled__BookingDetailsSection-sc-1k8ynhk-9'
        normal_price_xpath2 = './/span'

        gf_button1_xpath = '//button[@class="Buttonstyled-sc-ru2yn6-1 gEBqgP BookingDetailsstyled__BookDealButton-sc-1k8ynhk-4 JSAhN"]'
        gf_button1_csss  = 'button.BookingDetailsstyled__BookDealButton-sc-1k8ynhk-4'
        gf_button2_xpath = '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe"]'

        ## class changed at end for xpath :(
        other_links_div_csss  = 'div.OtherDeparturesstyled__DeparturesContainer-sc-cwe8z8-5'
        other_links_div_xpath = '//div[@class="OtherDeparturesstyled__DeparturesContainer-sc-cwe8z8-5 exWYYM"]'
        other_links_xpath = './/a[@class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB"]'
        other_links_csss  = 'a.OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2'

        other_buttons_div_xpath = '//div[@class="OtherDeparturesstyled__OtherDepartureServiceClassesContainer-sc-cwe8z8-11 kdSInU"]'
        other_buttons_div_csss  = 'div.OtherDeparturesstyled__OtherDepartureServiceClassesContainer-sc-cwe8z8-11'
        other_buttons_xpath = './/button[@class="Buttonstyled-sc-ru2yn6-1 hTBIOf ButtonTogglestyled-sc-1j1lwek-0 cvwzMQ SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0 kFqOFc"]'
        other_buttons_csss  = 'button.SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0'

        await asyncio.sleep(0.1)
        driver.implicitly_wait(10)
        await asyncio.sleep(0.1)

        elems = driver.find_elements(By.CSS_SELECTOR, deals_csss)
        links = [elem.get_attribute("href") for elem in elems]

        locations      = []
        dates          = []
        rarities       = []
        prices         = []
        flight_types   = []
        flight_classes = []

        normal_prices   = []
        gf_links        = []
        images          = []
        fares           = []
        already_visited = self.scotts_already_visited + []

        if self.fares_scotts == {}:
            self.fares_scotts["urls"]   = []
            self.fares_scotts["texts"]  = []
            self.fares_scotts["images"] = []
            self.fares_scotts["hashtags"] = []
        # end if

        #links = ["https://app.scottscheapflights.com/route/us/from-abe/fr/to-paris/standard/premium-economy"]
        while len(links) > 0:
            link = links[0]
            
            print("link: ", link)
            driver.get(link)
            driver.implicitly_wait(10)

            elem = driver.find_element(By.CSS_SELECTOR, h1_csss)
            cities = elem.find_elements(By.CSS_SELECTOR, cities_csss)
            countries = elem.find_elements(By.CSS_SELECTOR, countries_csss)
            #print("elem: ", elem)
            #print("cities: ", cities)
            #print("countries: ", countries)
            
            departs_from = cities[0].get_attribute("innerText").replace("\n", ", ")
            goes_to      = cities[1].get_attribute("innerText").replace("\n", ", ")
            #to_froms.append(cities[0].get_attribute("innerText").split("\\n")[0] + ", " + countries[0].get_attribute("innerText") + " to " +
            #                cities[1].get_attribute("innerText") + ", " + countries[1].get_attribute("innerText"))
            location = departs_from + " to " + goes_to
            #print("location: ", location)


            elems = driver.find_elements(By.CSS_SELECTOR, flight_and_class_csss)

            flight_type  = elems[0].get_attribute("innerText")
            flight_class = elems[1].get_attribute("innerText")

            #print("flight_type: ", flight_type)
            #print("flight_class: ", flight_class)

            # print("flight_types: ", flight_types)
            # print("flight_classes: ", flight_classes)

            # for ee, elem in enumerate(elems):
            #     print("ee: ", ee)
            #     innerText = elem.get_attribute("innerText")
            #     print("innerText: ", innerText)
            # # end for

            if flight_type == []:
                sys.exit()

            ## get price
            elem = driver.find_element(By.CSS_SELECTOR, price_csss)
            price = elem.get_attribute("innerText")
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(elem, 5, 0)
            action.click()
            action.perform()
            #print("price: ", price)


            if location + price + flight_type + flight_class in already_visited:
                del links[0]
                await asyncio.sleep(2)
                continue
            # end if

            prices.append(price)
            locations.append(location)
            flight_types.append(flight_type)
            flight_classes.append(flight_class)

            elem = driver.find_element(By.CSS_SELECTOR, image_csss)
            #elem = driver.find_element(By.XPATH, image_xpath)
            image = elem.get_attribute("src")
            #print("elem: ", elem)
            #print("image: ", image)

            images.append(image)


            elems = driver.find_elements( By.CSS_SELECTOR, rarity_and_time_csss)
            print("len elems: ", len(elems))
            for ee, elem in enumerate(elems):
              print("ee, innerText: ", ee, elem.get_attribute("innerText"))
            rarity = elems[1]
            when = elems[2]
            #rarity = driver.find_element( By.XPATH, rarity_xpath)
            #when   = driver.find_elements(By.XPATH, time_xpath)

            #print("rarity elem: ", rarity)
            #print("time elemt: ", time)

            rarities.append("Rarity: " + rarity.get_attribute("innerText"))
            dates.append("When: " + when.get_attribute("innerText"))
            #dates.append("When: " + when[1].get_attribute("innerText"))

            #print("rarities: ", rarities)
            #print("dates: ", dates)

            try:
                #elem  = driver.find_element(By.XPATH, normal_price_xpath1)
                elem  = driver.find_element(By.CSS_SELECTOR, normal_price_csss)
                #print("elem: ", elem)
                elem2 = elem.find_elements(  By.XPATH, normal_price_xpath2)
                #print("elem2: ", elem2)

                normal_prices.append(elem2[0].get_attribute("innerText") + elem2[1].get_attribute("innerText"))
                #print("normal_prices: ", normal_prices)
            except:
                normal_prices.append("")
            # end try/except

            ## now grab links to all the other departs from things
            #### first grab all the ones present now
            #elem = driver.find_element(By.XPATH, other_links_div_xpath)
            elem = driver.find_element(By.CSS_SELECTOR, other_links_div_csss)
            #print("164 elem: ", elem)
            #elems = elem.find_elements(By.XPATH, other_links_xpath)
            elems = elem.find_elements(By.CSS_SELECTOR, other_links_csss)
            #print("166 elems: ", elems)

            for elem in elems:
                links.append(elem.get_attribute("href"))
            # end for
            #print("171 links: ", links)

            #### next, click on the other buttons, if they exist
            buttons_exist = True
            try:
                #elem = driver.find_element(By.XPATH, other_buttons_div_xpath)
                elem = driver.find_element(By.CSS_SELECTOR, other_buttons_div_csss)
                #print("176 elem: ", elem)
            except NoSuchElementException:
                buttons_exist = False
            # end try/except

            if buttons_exist:
                #print("buttons_exist!")
                buttons_to_click = []
                #elems = elem.find_elements(By.XPATH, other_buttons_xpath)
                elems = elem.find_elements(By.CSS_SELECTOR, other_buttons_csss)

                #print("184 elems: ", elems)
                for elem in elems:
                    aria_pressed = elem.get_attribute("aria-pressed")
                    #print("aria_pressed, type: ", [aria_pressed], type(aria_pressed))

                    if aria_pressed == "false":
                        buttons_to_click.append(elem)
                    # end if
                # end for

                #print("going to click buttons")
                for button in buttons_to_click:
                    await asyncio.sleep(1)
                    button.click()

                    ## now grab links to all the other departs from things
                    #### first grab all the ones present now
                    elem = driver.find_element(By.CSS_SELECTOR, other_links_div_csss)
                    #elem = driver.find_element(By.XPATH, other_links_div_xpath)
                    #print("203 elem: ", elem)
                    #elems = elem.find_elements(By.XPATH, other_links_xpath)
                    elems = elem.find_elements(By.CSS_SELECTOR, other_links_csss)
                    #print("205 elems: ", elems)

                    for elem in elems:
                        links.append(elem.get_attribute("href"))
                    # end for
                    #print("211 links: ", links)
                # end for buttons_to_click
            # end if buttons_exist
            #print("done with buttons")

            await asyncio.sleep(3)
            #elem = driver.find_element(By.XPATH, gf_button1_xpath).click()
            elem = driver.find_element(By.CSS_SELECTOR, gf_button1_csss).click()
            await asyncio.sleep(3)
            google_url1 = driver.current_url
            if "consent.google.com" in google_url1:
                await asyncio.sleep(0.1)
                driver.implicitly_wait(10)
                await asyncio.sleep(0.1)
                elem = driver.find_element(By.XPATH, gf_button2_xpath).click()
                await asyncio.sleep(3)
            # end if
            gf_links.append(driver.current_url)

            fares.append(locations[-1] + " " + dates[-1] + " " + rarities[-1] + " for " + prices[-1] + " " + flight_types[-1] + " " + flight_classes[-1])

            fare = fares[-1]
            image = images[-1]
            url = gf_links[-1]
            hashtags = []
            hashtags = self.get_new_hashtags_from_regions(fare, hashtags)
            print("fare: ", fare)
            print("hashtags: ", hashtags)

            # if fares[-1] not in self.fares_scotts["texts"]:
            #     self.fares_scotts["texts"].append(fares[-1])
            #     self.fares_scotts["images"].append(images[-1])
            #     self.fares_scotts["urls"].append(gf_links[-1])
            #     self.fares_scotts["hashtags"].append([])

            #     self.fares_scotts["hashtags"] = self.get_new_hashtags_from_regions(
            #                                         self.fares_scotts[   "texts"][-1], 
            #                                         self.fares_scotts["hashtags"][-1])
            # end if

            roles_mentioned = []

            title = fare
            description = ""

            ports = []; roles = []; channels = []
            for jj,hashtag in enumerate(hashtags):
                description += hashtag + ", "

                if "_from" in hashtag:
                    if "usa" in hashtag:
                        #print("usa in hashtag")
                        continue
                    # end if

                    hashtag = hashtag.replace("_from","")
                    if "#mena" in hashtag:
                        hashtag = "#me-and-north-africa"
                    # end if

                    roles.append(self.roles[hashtag[1:]])
                    ports.append(jj)

                    if   hashtag[1:] in self.CIDS:
                        did = self.CIDS[hashtag[1:]]

                    elif hashtag[1:] in self.TIDS_USA:
                        did = self.TIDS_USA[hashtag[1:]]

                    else:
                        print("34 err hashtag not in CIDS, TIDS_USA")
                        print("hashtag: ", hashtag)
                        print("hashtag[1:]: ", hashtag[1:])
                        print("CIDS keys: ", self.CIDS.keys())
                        print("TIDS_USA keys: ", self.TIDS_USA.keys())
                        raise
                    # end if/elif
                    channels.append(self.client.get_channel(did))
                # end if
            # end for
            description = description[:-2]
            description = description.replace("_from","")
            #description = ", ".join(self.fares["hashtags"][ii])

            if "to Las Vegas" in title:
                #print("Las vegas in title, now: ", datetime.datetime.now())

                embed = discord.Embed(title=title, description=title,
                    color=discord.Color.blue(), url=url)
                embed.set_thumbnail(url=image)
                embed.set_footer(text = "Built for Solana Vegas Tour, Powered by @TheLunaLabs",
                    icon_url=self.icon_url)
                try:
                    #print("going to get LV channel, now: ", datetime.datetime.now())
                    channel = self.client.get_channel(self.CID_VEGAS)
                    #print("got LV channel, now: ", datetime.datetime.now())
                    if not self.TESTING:
                        await channel.send(embed=embed)
                    print("LV sent embed, now: ", datetime.datetime.now())
                except Exception as err:
                    print("error LV, now: ", datetime.datetime.now())
                    print("111 tdb err: ", err)
                    print("112 tdb err: ", err.args[:])
                # end try/except
            # end if

            embed = discord.Embed(title=title, description=description,
                color=discord.Color.blue(), url=url)
            embed.set_thumbnail(url=image)
            embed.set_footer(text = "Built for Key Lounge IO, Powered by @TheLunaLabs",
                icon_url=self.icon_url)
            #embed.add_field(name="Hey @Authenticated", value="\u200b")

            #channel = client.get_channel(self.BOT_COMMANDS_CIDS[0])
            print("roles: ", roles)
            print("self.roles: ", self.roles)
            for jj,role in enumerate(roles):
                channel = channels[jj]
                if role not in roles_mentioned:
                    try:
                        if not self.TESTING:
                            if "business class" not in title.lower() and "first class" not in title.lower():
                                if role not in self.time_since_last_ping or self.time_since_last_ping[role] - time.time() > self.ONE_HOUR:
                                    self.time_since_last_ping[role] = time.time()
                                    await channel.send("Hey <@&" + role + ">")
                    except Exception as err:
                        print("112 err: ", err)
                        print("113 err_args: ", err.args[:])
                        print("channel: ", channel)
                        print("jj: ", jj)
                        print("role: ", role)
                        print("channels: ", channels)
                        print("title: ", title)
                        print("description: ", description)
                        print("hashtags: ", hashtags)
                    # end try/except
                    roles_mentioned.append(role)
                # end if
                try:
                    if not self.TESTING:
                        if "business class" not in title.lower() and "first class" not in title.lower():
                            await channel.send(embed=embed)
                        
                    else:
                        await test_channel.send(embed=embed)

                except Exception as err:
                    print("129 err: ", err)
                    print("130 err_args: ", err.args[:])
                    print("channel: ", channel)
                # end try/except
            # end for

            if "business class" in title.lower():
                if  self.time_since_last_business_ping - time.time() > self.ONE_HOUR:
                    self.time_since_last_business_ping = time.time()
                    #await business_channel.send("Hey <@&" + role + ">")
                await business_channel.send(embed=embed)
            # end if

            if "first class" in title.lower():
                if  self.time_since_last_first_class_ping - time.time() > self.ONE_HOUR:
                    self.time_since_last_first_class_ping = time.time()
                    #await first_class_channel.send("Hey <@&" + role + ">")
                await first_class_channel.send(embed=embed)
            # end if
            self.old_fares.append(fare)


            already_visited.append(location + price + flight_type + flight_class)
            self.save_json(self.fname_fares_scotts, already_visited)

            del links[0]
            await asyncio.sleep(1.0)
        # end while

        print("get_fares_scotts took: ", time.time() - tstart)
    # end get_fares_scotts

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
            fares = self.html.split("Latest Deals")[1].split("As Seen On")[0]
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
            #print("0 fare: ", fare)
            fare = fare.split("</h3>")[0]
            #print("1 fare: ", fare)
            fare = fare.split('<a href="')[-1]
            #print("2 fare: ", fare)
            url = fare.split('" ')[0]
            fare = fare.split('title="')[1].split('" ')[0]
            #print("3 fare: ", fare)
            ## note, I had ('<a href="')[2] but modified for the hotel error fare thing.
            #url = fare.split('<a href="')[1].split(" ")[0].split('"')[0]
            #fare = fare.split('title="')[1].split('" ')[0]
            try:
                image = images[ii]
            except Exception as err:
                print("674 err: ", err)
                print("675 err.args: ", err.args[:])
                print("fare: ", fare)
            #if "Hotel" in fare:
            #    continue
            ## end if

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
                self.fares["hashtags"][-1] = self.get_new_hashtags_from_regions(
                                                self.fares[   "texts"][-1], 
                                                self.fares["hashtags"][-1])
            # end if
        # end for
    # end get_fares

    def get_new_hashtags_from_regions(self, text, hashtags):
        #print("text: ", text)
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

                    if " to " in text:
                        if subregion.lower().replace(" ","") in text.split(" to ")[0].lower().replace(" ", ""):
                            if "usa" not in hashtags[-1]:
                                hashtags[-1] = hashtags[-1] + "_from"
                    elif " in " in text:
                        if subregion.lower().replace(" ","") in text.split(" in ")[0].lower().replace(" ", ""):
                            if "usa" not in hashtags[-1]:
                                hashtags[-1] = hashtags[-1] + "_from"
                    # end if/elif
                # end if
            # end for
        # end for
        return hashtags
    # end get_new_hashtags_from_regions
# end class TravelBot
## end travel.py
