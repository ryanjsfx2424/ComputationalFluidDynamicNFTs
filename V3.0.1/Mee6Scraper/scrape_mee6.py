import os
import time
import json
import numpy as np # just for saving the data

LIMIT    = 100 # this is the default
GUILD    = "893963935672324118" # roo troop

BASE_URL  = "https://mee6.xyz/api/plugins/levels/leaderboard/"
CURL_BASE = "curl --request GET -H 'Accept: Application/json' --url "

FNAME_BASE = "mee6_response_page" 
FNAME_EXT  = ".txt"

SAVE_NAME = "RooTroopMee6Data.json"

## note, for some strange reason it doesn't let me have more than one query
url = BASE_URL + GUILD + "?page=10"

cnt = 11
flag = True
players = {}

while flag:
  url = url[:-len(str(cnt-1))] + str(cnt)
  fname = FNAME_BASE + str(cnt) + FNAME_EXT
  print("url: ", url)

  curl = CURL_BASE + url + " > " + fname
  print("curl: ", curl)
  os.system(curl)
  print("did the curl!")

  with open(fname, "r") as fid:
    line = json.loads(fid.read())
  # end with open

  for player in line["players"]:
    if len(players.keys()) == 0:
      for key in player.keys():
        players[key + "s"] = [player[key]]
      # end for
    else:
      for key in player.keys():
        players[key + "s"].append(player[key])
      # end for
    # end if/else
  # end for
  if len(line["players"]) < LIMIT:
    flag = False
    break
  # end if

  cnt += 1
  time.sleep(5)
# end while
print("done with while loop!")

#print("players: ", players)
with open(SAVE_NAME, "w") as fid:
  fid.write(str(players))
# end with open

print("SUCCESS scrape_mee6")
## end scrape_mee6.py
