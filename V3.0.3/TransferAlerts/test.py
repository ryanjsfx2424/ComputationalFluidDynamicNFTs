# scrape_rarity_tools
"""
Just use selenium to get data.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

contract = "0xb716600ed99b4710152582a124c697a7fe78adbf" # punks comics 3
#contract = "0xf4d2888d29d722226fafa5d9b24f9164c092421e"
URL = "https://opensea.io/assets/ethereum/" + contract + "/1"

driver = webdriver.Firefox(executable_path="./geckodriver", options=options)
driver.get(URL)
html_source = driver.page_source
try:
  collection = html_source.split('CollectionLink--link" href="')[1].split('"')[0]
except:
  collection = "not on opensea!"
# end try/except

name = html_source.split('CollectionLink--link" href="')[1].split("<div class=")[1].split(">")[1].split("<")[0]
print("name: ", name)
sys.exit()

#el = driver.find_element_by_xpath("//div[contains(@class, 'm-1')]")
time.sleep(100)
print("going to find element")
sys.exit()

rarities = []
els = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-sm font-bold overflow-ellipsis')]")
for el in els:
  rarities.append(el.text)
# end for

for ii in range(2,115+1):
  print("ii: ", ii)
  buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'select-none smallBtn')]")
  for button in buttons:
    if button.text == "Next >":
      button.click()
      print("clicked next button")
      break
  '''
  for page in pages:
    print("page.text == str(ii)", page.text==str(ii))
    print("page.text: ", page.text)
    print("str ii: ", str(ii))
    if page.text == str(ii):
      print("true")
      page.click()
      break
    # end if
  '''
  # end for
  print("sleeping")
  time.sleep(3)

  els = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-sm font-bold overflow-ellipsis')]")

  for el in els:
    rarities.append(el.text)
  # end for els

  with open("foo42", "w") as fid:
    fid.write(str(rarities))
  # end with open
  print("saved rarities")
# end for
with open("foo42", "w") as fid:
  fid.write(str(rarities))
# end with open
driver.quit()
