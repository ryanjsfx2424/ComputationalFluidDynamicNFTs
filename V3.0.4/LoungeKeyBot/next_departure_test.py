## playing around with logging in and doing stuff on app.nextdeparture.ca
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")



print("SUCCESS")
