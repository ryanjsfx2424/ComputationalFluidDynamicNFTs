import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.headless = True
options.headless = False
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")

url = "https://app.scottscheapflights.com/login"
driver.get(url)

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

## the link thing is giving me syntax error not a valid selector
## might need to make window full screen. Received a not clickable exception because div id="c-main" obscures it (for the deals div)

driver.implicitly_wait(10)
#elems = driver.find_elements(By.CLASS_NAME, deals_class)
elems = driver.find_elements(By.XPATH, deals_xpath)
print("elems: ", elems)
print("len elems: ", len(elems))
for elem in elems:
    result = elem.click()
    print("result of click: ", result)
    time.sleep(5)
    break

html = driver.page_source
with open("scotts_deal1.txt", "w") as fid:
    fid.write(html)
# end with open
