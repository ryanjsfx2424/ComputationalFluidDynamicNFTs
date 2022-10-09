import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.headless = True
options.headless = False
#options.add_argument("--start-maximized")
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")

url = "https://app.scottscheapflights.com/login"
driver.get(url)
driver.fullscreen_window()

html = driver.page_source
with open("scotts_login1.txt", "w") as fid:
    fid.write(html)
# end with open

email_xpath  = '//input[@name="email"]'
passw_xpath  = '//input[@name="password"]'
email = os.environ.get("lkEmail")
passw = os.environ.get("lkNDPass")

driver.find_element(By.XPATH, email_xpath ).send_keys(email)
driver.implicitly_wait(10)
driver.find_element(By.XPATH, passw_xpath ).send_keys(passw)

html = driver.page_source
with open("scotts_login2.txt", "w") as fid:
    fid.write(html)
# end with open

act = ActionChains(driver)
act.send_keys(Keys.ENTER).perform()

time.sleep(10)
html = driver.page_source
with open("scotts_app.txt", "w") as fid:
    fid.write(html)
# end with open

base = "https://app.scottscheapflights.com"
url = base + "/route/us/from-auto/nz/to-auckland/standard/auto?cos=economy"

deals_class = "DealCardstyled-sc-1y5rz5y-12 iWtlCA DealGridstyled__DealCardItem-sc-wxnuip-2 fqkPVX"
deals_xpath = '//div[@class="DealCardstyled-sc-1y5rz5y-12 iWtlCA DealGridstyled__DealCardItem-sc-wxnuip-2 fqkPVX"]'
deals_class = '"Link__StyledCoreLink-sc-1h103ma-0 eiEvAU DealCard___StyledLink-sc-1m8z4ys-0 jrpdrz"'
deals_xpath = '//a[@class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU DealCard___StyledLink-sc-1m8z4ys-0 jrpdrz"]'

image_xpath = '//img[@class="RouteImageContainerstyled__RouteImage-sc-1g5bk2f-4 dNbvtN"]'
h1_xpath = '//h1[@class="Headingstyled__H1-sc-1m02ur5-0 gQWhhr RouteTitlestyled-sc-1jwxr9x-3 fzKwOb"]'
cities_xpath = './/span[@class="RouteTitlestyled__RouteCity-sc-1jwxr9x-0 eQFYGB"]'
countries_xpath = './/div[@class="Paragraph-sc-ivzkw1-0 RouteTitlestyled__RouteCountry-sc-1jwxr9x-1 ddVNcC jsCoDc"]'

rarity_xpath = '//span[@class="DealDetailsstyled__DealDetailsValue-sc-2a3eq9-3 bcQPgC"]'
time_xpath = '//span[@class="DealDetailsstyled__DealDetailsValue-sc-2a3eq9-3 lndALR"]'

price_xpath = '//h2[@class="Headingstyled__H2-sc-1m02ur5-1 bgUUHW BookingDetailsstyled__BookingDetailsHeading-sc-1k8ynhk-7 fbgyZM"]'

flight_and_class_xpath = '//div[@class="Paragraph-sc-ivzkw1-0 BookingDetailsstyled__BookingAttribute-sc-1k8ynhk-5 icRgRK sScmo"]'

normal_price_xpath1 = '//div[@class="BookingDetailsstyled__BookingDetailsSection-sc-1k8ynhk-9 kHUIQL"]'
normal_price_xpath2 = './/span'

gf_button1_xpath = '//button[@class="Buttonstyled-sc-ru2yn6-1 gEBqgP BookingDetailsstyled__BookDealButton-sc-1k8ynhk-4 JSAhN"]'
gf_button2_xpath = '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe"]'

other_links_div_xpath = '//div[@class="OtherDeparturesstyled__DeparturesContainer-sc-cwe8z8-5 exWYYM"]'
other_links_xpath = './/a[@class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB"]'

other_buttons_div_xpath = '//div[@class="OtherDeparturesstyled__OtherDepartureServiceClassesContainer-sc-cwe8z8-11 kdSInU"]'
other_buttons_xpath = './/button[@class="Buttonstyled-sc-ru2yn6-1 hTBIOf ButtonTogglestyled-sc-1j1lwek-0 cvwzMQ SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0 kFqOFc"]'

#<button aria-pressed="false" class="Buttonstyled-sc-ru2yn6-1 hTBIOf ButtonTogglestyled-sc-1j1lwek-0 cvwzMQ SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0 kFqOFc" data-chromatic="" tabindex="0" type="button"><span class="ButtonTogglestyled__LabelPosition-sc-1j1lwek-1 feBQxt">Economy</span></button>
#<div class="OtherDeparturesstyled__OtherDepartureServiceClassesContainer-sc-cwe8z8-11 kdSInU"><button aria-pressed="false" class="Buttonstyled-sc-ru2yn6-1 hTBIOf ButtonTogglestyled-sc-1j1lwek-0 cvwzMQ SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0 kFqOFc" data-chromatic="" tabindex="0" type="button"><span class="ButtonTogglestyled__LabelPosition-sc-1j1lwek-1 feBQxt">Economy</span></button><button aria-pressed="false" class="Buttonstyled-sc-ru2yn6-1 hTBIOf ButtonTogglestyled-sc-1j1lwek-0 cvwzMQ SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0 kFqOFc" data-chromatic="" tabindex="0" type="button"><span class="ButtonTogglestyled__LabelPosition-sc-1j1lwek-1 feBQxt">Premium Economy</span></button><button aria-pressed="true" class="Buttonstyled-sc-ru2yn6-1 hTBIOf ButtonTogglestyled-sc-1j1lwek-0 byRVEM SharedComponentsstyled__OtherDepatureServiceClass-sc-14cmb39-0 ewmmrS" data-chromatic="" tabindex="0" type="button"><span class="ButtonTogglestyled__LabelPosition-sc-1j1lwek-1 feBQxt">Business Class</span></button></div>
#<div class="OtherDeparturesstyled__DeparturesContainer-sc-cwe8z8-5 exWYYM"><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-bwi/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Baltimore (BWI) - $2,880" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Baltimore (BWI) - $2,880</div><div style="display: flex; opacity: 0; transform: translateX(-10px) translateZ(0px);"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-bos/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Boston (BOS) - $2,071" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Boston (BOS) - $2,071</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-buf/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Buffalo (BUF) - $2,862" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRz"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Buffalo (BUF) - $2,862</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-ord/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Chicago (ORD) - $2,466" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Chicago (ORD) - $2,466</div><div style="display: flex; opacity: 0; transform: translateX(-10px) translateZ(0px);"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-mia/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Miami (MIA) - $2,588" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Miami (MIA) - $2,588</div><div style="display: flex; opacity: 0; transform: translateX(-10px) translateZ(0px);"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-msp/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Minneapolis (MSP) - $2,880" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Minneapolis (MSP) - $2,880</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-ewr/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Newark (EWR) - $2,168" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Newark (EWR) - $2,168</div><div style="display: flex; opacity: 0; transform: translateX(-10px) translateZ(0px);"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-jfk/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="New York City (JFK) - $2,168" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">New York City (JFK) - $2,168</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-phl/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Philadelphia (PHL) - $2,974" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Philadelphia (PHL) - $2,974</div><div style="display: flex; opacity: 1; transform: none;"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-roc/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Rochester (ROC) - $2,862" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRz"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Rochester (ROC) - $2,862</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-sfo/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="San Francisco (SFO) - $2,998" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">San Francisco (SFO) - $2,998</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a><a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-iad/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Washington (IAD) - $2,369" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Washington (IAD) - $2,369</div><div style="display:flex;opacity:0;transform:translateX(-10px) translateZ(0)"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a></div>
#<a rel="noopener" tabindex="0" class="Link__StyledCoreLink-sc-1h103ma-0 eiEvAU OtherDeparturesstyled__DepartureItem-sc-cwe8z8-2 hMzepB" href="/route/us/from-bwi/fr/to-paris/standard/business" target="_blank"><div class="Link__Flex-sc-1h103ma-1 dmSDUs"><div aria-label="Baltimore (BWI) - $2,880" class="Paragraph-sc-ivzkw1-0 OtherDeparturesstyled__DepartureCity-sc-cwe8z8-1 icRgRK jYaWRy"><div class="OtherDeparturesstyled__DepartureLabel-sc-cwe8z8-3 jNPFTH">Baltimore (BWI) - $2,880</div><div style="display: flex; opacity: 0; transform: translateX(-10px) translateZ(0px);"><span class="Icon___StyledSpan-sc-13z1e94-0 eXJeJd OtherDeparturesstyled__DepartureArrowIcon-sc-cwe8z8-0 izTRAO"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" height="12" width="12"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m10.64 4.173 3.873 3.873-3.874 3.782M14.513 8.073H1.487"></path></svg></span></div></div></div></a>

driver.implicitly_wait(10)
#elems = driver.find_elements(By.CLASS_NAME, deals_class)
elems = driver.find_elements(By.XPATH, deals_xpath)
links = [elem.get_attribute("href") for elem in elems]
print("elems: ", elems)
print("len elems: ", len(elems))
print("links: ", links)
print("len links: ", len(links))

locations = [] # done
dates = [] # done
rarities = [] # done
prices = []
flight_types = [] # done
flight_classes = [] # done

normal_prices = [] # need for embed
gf_links = [] # need for embed
images = [] # need for embed
fares = [] # need for embed
already_visited = []
while len(links) > 0:
    link = links[0]
    
    print("link: ", link)
    driver.get(link)
    driver.implicitly_wait(10)

    elem = driver.find_element(By.XPATH, h1_xpath)
    cities = elem.find_elements(By.XPATH, cities_xpath)
    countries = elem.find_elements(By.XPATH, countries_xpath)
    print("elem: ", elem)
    print("cities: ", cities)
    print("countries: ", countries)
    
    departs_from = cities[0].get_attribute("innerText").replace("\n", ", ")
    goes_to      = cities[1].get_attribute("innerText").replace("\n", ", ")
    #to_froms.append(cities[0].get_attribute("innerText").split("\\n")[0] + ", " + countries[0].get_attribute("innerText") + " to " +
    #                cities[1].get_attribute("innerText") + ", " + countries[1].get_attribute("innerText"))
    location = departs_from + " to " + goes_to
    print("location: ", location)


    elems = driver.find_elements(By.XPATH, flight_and_class_xpath)
    print("elems: ", elems)

    flight_type  = elems[0].get_attribute("innerText")
    flight_class = elems[1].get_attribute("innerText")

    print("flight_types: ", flight_types)
    print("flight_classes: ", flight_classes)


    ## get price
    elem = driver.find_element(By.XPATH, price_xpath)
    print("elem: ",elem)
    price = elem.get_attribute("innerText")
    print("price: ", price)


    if location + price + flight_type + flight_class in already_visited:
        del links[0]
        time.sleep(2)
        continue
    # end if

    prices.append(price)
    locations.append(location)
    flight_types.append(flight_type)
    flight_classes.append(flight_class)
    already_visited.append(location + price + flight_type + flight_class)


    elem = driver.find_element(By.XPATH, image_xpath)
    image = elem.get_attribute("src")
    print("elem: ", elem)
    print("image: ", image)

    images.append(image)


    rarity = driver.find_element( By.XPATH, rarity_xpath)
    when   = driver.find_elements(By.XPATH, time_xpath)

    print("rarity elem: ", rarity)
    print("time elemt: ", time)

    rarities.append("Rarity: " + rarity.get_attribute("innerText"))
    dates.append("When: " + when[1].get_attribute("innerText"))

    print("rarities: ", rarities)
    print("dates: ", dates)


    elem  = driver.find_element(By.XPATH, normal_price_xpath1)
    print("elem: ", elem)
    elem2 = elem.find_elements(  By.XPATH, normal_price_xpath2)
    print("elem2: ", elem2)

    normal_prices.append(elem2[0].get_attribute("innerText") + elem2[1].get_attribute("innerText"))
    print("normal_prices: ", normal_prices)

    ## now grab links to all the other departs from things
    #### first grab all the ones present now
    elem = driver.find_element(By.XPATH, other_links_div_xpath)
    print("164 elem: ", elem)
    elems = elem.find_elements(By.XPATH, other_links_xpath)
    print("166 elems: ", elems)

    for elem in elems:
        links.append(elem.get_attribute("href"))
    # end for
    print("171 links: ", links)

    #### next, click on the other buttons, if they exist
    buttons_exist = True
    try:
        elem = driver.find_element(By.XPATH, other_buttons_div_xpath)
        print("176 elem: ", elem)
    except NoSuchElementException:
        buttons_exist = False
    # end try/except

    if buttons_exist:
        print("buttons_exist!")
        buttons_to_click = []
        elems = elem.find_elements(By.XPATH, other_buttons_xpath)

        print("184 elems: ", elems)
        for elem in elems:
            aria_pressed = elem.get_attribute("aria-pressed")
            print("aria_pressed, type: ", [aria_pressed], type(aria_pressed))

            if aria_pressed == "false":
                buttons_to_click.append(elem)
            # end if
        # end for

        print("going to click buttons")
        for button in buttons_to_click:
            time.sleep(1)
            button.click()

            ## now grab links to all the other departs from things
            #### first grab all the ones present now
            elem = driver.find_element(By.XPATH, other_links_div_xpath)
            print("203 elem: ", elem)
            elems = elem.find_elements(By.XPATH, other_links_xpath)
            print("205 elems: ", elems)

            for elem in elems:
                links.append(elem.get_attribute("href"))
            # end for
            print("211 links: ", links)
        # end for buttons_to_click
    # end if buttons_exist
    print("done with buttons")


    break

    time.sleep(3)
    elem = driver.find_element(By.XPATH, gf_button1_xpath).click()
    time.sleep(3)
    google_url1 = driver.current_url
    print("first post button url: ", google_url1)
    if "consent.google.com" in google_url1:
        driver.implicitly_wait(10)
        elem = driver.find_element(By.XPATH, gf_button2_xpath).click()
        time.sleep(3)
        print("new url: ", driver.current_url)
    # end if
    gf_links.append(driver.current_url)
    print("gf_links: ", gf_links)

    fares.append(locations[-1] + " " + dates[-1] + " " + rarities[-1] + " for " + prices[-1] + " " + flight_types[-1] + " " + flight_classes[-1])

    del links[0]
    #time.sleep(10)
    #print("slept 10 seconds!")
    

html = driver.page_source
with open("scotts_deal1.txt", "w") as fid:
    fid.write(html)
# end with open
