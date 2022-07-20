## playing around with logging in and doing stuff on app.nextdeparture.ca
'''
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.headless = True
options.headless = False
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")

url = "https://app.nextdeparture.ca/login"
driver.get(url)

email_xpath = "//input[@id='email']"
passw_xpath = "//input[@id='password']"
email = "Loungekeyio@gmail.com"
passw = "DealsLounge"
driver.find_element(By.XPATH, email_xpath).send_keys(email)
driver.find_element(By.XPATH, passw_xpath).send_keys(passw)

act = ActionChains(driver)
act.send_keys(Keys.ENTER).perform()

time.sleep(5)
url = "https://app.nextdeparture.ca/user/deals"
driver.get(url)

html = driver.page_source
with open("debug1.txt", "w") as fid:
  fid.write(html)
# end with open
'''
with open("debug1.txt", "r") as fid:
  html = fid.read()
# end with open

spl_beg = '<h4 class="card-title mt-3">'
spl_end = '</h4>'
deals = html.split(spl_beg)[1:]

print("len deals: ", len(deals))

spl_beg = '<div class="card mb-3">'
cards = html.split(spl_beg)[1:]

print("len cards: ", len(cards))

spl_beg = '<h4 class="card-title mt-3">'
fare = cards[0].split(spl_beg)[1].split(spl_end)[0]
print("fare: ", fare)

spl_beg = '<img src="'
img = cards[0].split(spl_beg)[1].split('"')[0]
print("img: ", img)

spl_beg = '<a href="'
link = cards[0].split(spl_beg)[1].split('"')[0]
print("link: ", link)

sys.exit()

deals_clean = []
for deal in deals:
  deals_clean.append(deal.split(spl_end)[0].replace("&amp;","&"))
# end for
print("deals_clean: ", deals_clean)

print("SUCCESS")
