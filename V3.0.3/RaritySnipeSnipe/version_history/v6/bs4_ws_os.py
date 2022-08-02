from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json


def Request_page(url):
    html = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("html: ", html)

    url = urlopen(html)
    print("url: ", url)
    bs = BeautifulSoup(url, "html.parser")
    print("bs: ", bs)
    return bs

raw_data = Request_page("https://opensea.io/collection/roo-troop/activity").find('script').text
print("raw_data: ", raw_data)
#print(raw_data)
data = raw_data.replace("window.__wired__=", "")
#json_object = json.loads(data)

with open('data.json', 'w') as f:
    f.write(str(data))
print("Created Json File! :)")
sys.exit()

array = []
for nfts in json_object["records"]:
    if "client:root" not in nfts:
        nft = json_object["records"][nfts]
        array.append(nft)

links = []
for itens in array:
    for item in itens:
        if item == "name": 
            print(f"Coleção NFT: {itens[item]}")
        if item == "slug":
            url_collection = "https://opensea.io/collection/"
            #print(f"URL: {url_collection + itens[item]}")
            links.append(url_collection + itens[item])

print("array: ", array)
print("linkes: ", links)
