import requests

url = "https://opensea.io/assets/ethereum/0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258/1"
#url = "https://opensea.io/collection/otherdeed/activity"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
"Authority":"opensea.io"
}

fname = "test2_3.txt"

'''
resp = requests.get(url, headers=headers)
text = resp.text

with open(fname, "w") as fid:
  fid.write(text)
# end with open
print("text: ", text)
#sys.exit()
'''

with open(fname, "r") as fid:
  text = fid.read()
# end with open

fname = "test2_5.txt"
slug = '"slug":"'
slug = text.split(slug)[1].split('"')[0]
url = "https://opensea.io/collection/" + slug# + "/activity"
print("url: ", url)

name = '"name":"'
name = text.split(name)[1].split('"')[0]
print("name: ", name)
sys.exit()

'''
resp = requests.get(url, headers=headers)
text = resp.text
with open(fname, "w") as fid:
  fid.write(text)
# end with open
'''
with open(fname, "r") as fid:
  text = fid.read()
# end with open

fpt = '"floorPrice":{"unit":"'
floorPrice = text.split(fpt)[1].split('"')[0]

vol = '"totalVolume":{"unit":"'
totalVolume = text.split(vol)[1].split('"')[0]
totalVolume = "924.239482"
totalVolumeF = float(totalVolume)
if len(totalVolume.split(".")[0]) > 3: 
  totalVolume = "Volume Traded: %.1fk eth" % (totalVolumeF/1000.0)
else:
  totalVolume = "Volume Traded %.0f eth" % totalVolumeF
# end if/else
print("totalVolume: ", totalVolume)
sys.exit()

for fp in fps:
  ml = min(100, len(fp))
  fp = fp[:ml]
  unit = '"unit":"'
  if unit in fp:
    fp = fp.split(unit)[1].split('"')[0]
    break
  # end if
# end for
print("fp: ", fp)

#print("fp in text: ", "floorPrice" in text)
