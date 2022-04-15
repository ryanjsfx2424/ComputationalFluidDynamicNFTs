## gac.py 2022-04-13
"""
For gaming ape club. Sends messages in general to acquire their XP thing.

To do: figure out punctuation. for some reason, it sends it to the start
of the string.

Well, the next step I think is to at least do work continuously in
xp commands and then I can work on an AI chat bot :)
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

gac_general = "https://discord.com/channels/927427107666133033/927427109545209887"
gac_xp_commands = "https://discord.com/channels/927427107666133033/955674727584788520"

msg = "!work"
text_box_xpath = "//div[@class='markup-eYLPri editor-H2NA06 slateTextArea-27tjG0 fontSize16Padding-XoMpjI']"

driver = webdriver.Firefox()

driver.get(gac_xp_commands)
input(">>")

for character in msg:
  driver.find_element(By.XPATH, text_box_xpath).send_keys(character)
  time.sleep(0.1)

time.sleep(1)
act = ActionChains(driver)
act.send_keys(Keys.ENTER).perform()

