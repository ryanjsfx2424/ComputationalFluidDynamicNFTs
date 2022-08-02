## scrape_os.py
import requests
from bs4 import BeautifulSoup

url = "https://opensea.io/collection/roo-troop/activity?token=96047490de144c8b91be74ba7605ab69"
url = "https://opensea.io/collection/roo-troop/activity?search[isSingleCollection]=true&search[eventTypes][0]=AUCTION_SUCCESSFUL&search[eventTypes][1]=AUCTION_CREATED"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

resp = requests.get(url, headers=headers)
with open("bar.txt", "w") as fid:
  fid.write(resp.text)
## end with open
text = resp.text
sys.exit()

with open("bar.json", "r") as fid:
  text = fid.read()
# end with

soup = BeautifulSoup(text, "html.parser")

resultsRow = soup.find_all("div", {"role": "listitem"})

print("resultsRow: ", resultsRow)
for resultRow in resultsRow:
  print("dir rr: ", dir(resultRow))
  print("rr: ", resultRow)
  break
