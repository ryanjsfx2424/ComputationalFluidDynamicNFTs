import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = False
#options.headless = True

exec_path = "/root/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver_linux"
if socket.gethostname() == "MB-145.local":
  exec_path = "/Users/ryanjsfx/Documents/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver"
driver = webdriver.Firefox(options=options, executable_path=exec_path)
OS_BASE = "https://opensea.io/assets/ethereum/"

os_url = "https://opensea.io/assets/ethereum/0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258/1"
driver.get(os_url)

html_source = driver.page_source
with open("html.txt", "w") as fid:
  fid.write(html_source)
# end with open

os_collection = html_source.split('CollectionLink--link" href="')[1].split('"')[0]
os_name = html_source.split('CollectionLink--link" href="')[1].split(
                    "<div class=")[1].split(">")[1].split("<")[0]
os_url = "https://opensea.io" + os_collection

print("os_name: ", os_name)
print("os_url: ", os_url)
