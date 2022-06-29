# scrape_rarity_tools
"""
Just use selenium to get data.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://rarity.tools/roo-troop"

driver = webdriver.Firefox(executable_path="./geckodriver")
driver.get(URL)

#el = driver.find_element_by_xpath("//div[contains(@class, 'm-1')]")
time.sleep(10)
print("going to find element")

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
