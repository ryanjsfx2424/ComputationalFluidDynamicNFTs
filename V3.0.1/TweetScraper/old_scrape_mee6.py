import os
import json
import numpy as np # just for saving the data

LIMIT    = 100
GUILD    = "893963935672324118" # roo troop

BASE_URL  = "https://mee6.xyz/api/plugins/levels/leaderboard/"
CURL_BASE = "curl --request GET -H 'Accept: Application/json' --url "

FNAME_BASE = "mee6_response_page" 
FNAME_EXT  = ".txt"

SAVE_NAME = "RooTroopMee6Data.txt"

flag = False
xps  = []
ids  = []
levels    = []
avatars   = []
usernames = []
message_counts = []
detailed_xp1s  = []
detailed_xp2s  = []
detailed_xp3s  = []
detailed_xp_flag = 0

cnt = 0
url = BASE_URL + GUILD + "?page=0"# + "?limit=" + str(LIMIT) + "&page=0"
while True:
  url = url[:-1] + str(cnt)
  fname = FNAME_BASE + str(cnt) + FNAME_EXT
  print("url: ", url)
  input(">>")

  curl = CURL_BASE + url + " > " + fname
  print("curl: ", curl)
  input(">>")
  #os.system(curl)
  print("did the curl!")
  input(">>")

  num_old_usernames = len(usernames)

  with open(fname, "r") as fid:
    line = fid.read()
    line = json.loads(line)
    print("line: ", line)
    print("len line: ", len(line))
    print("type line: ", type(line))
    print("line.keys(): ", line.keys())
    print("len line['players']: ", len(line["players"]))
    print("line['players'][0].keys(): ", line["players"][0].keys())
    for player in line["players"]:
      avatar
      usernames.append(player["username"])
    input(">>")
    for ii,line in enumerate(fid):
      print(line)
      if ii % 10 == 0:
        input(">>")
      if '"players":' in line:
        flag = True
      # end if

      if flag:
        if detailed_xp_flag == 3:
          line = line.replace(" ","").replace(",","")
          detailed_xp3s.append(float(line))
          detailed_xp_flag = 0
          print("xp3: ", detailed_xp3s)
        # end if

        if detailed_xp_flag == 2:
          line = line.replace(" ","").replace(",","")
          detailed_xp2s.append(float(line))
          detailed_xp_flag += 1
          print("xp2: ", detailed_xp2s)
        # end if

        if detailed_xp_flag == 1:
          line = line.replace(" ","").replace(",","")
          detailed_xp1s.append(float(line))
          detailed_xp_flag += 1
          print("xp1: ", detailed_xp1s)
        # end if

        if '"avatar"' in line:
          line = line.replace(" ","").replace(",","").replace("\n","")
          line = line.replace('"',""); line = line.split(":")[1]
          avatars.append(line)
          print("avatars: ", avatars)

        elif '"detailed_xp":' in line:
          detailed_xp_flag = 1

        elif '"id":' in line:
          line = line.replace(" ","").replace(",","").replace("\n","")
          line = line.replace('"',""); line = line.split(":")[1]
          ids.append(float(line))
          print("ids: ", ids)

        elif '"level":' in line:
          line = line.replace(" ","").replace(",","").replace("\n","")
          line = line.replace('"',""); line = line.split(":")[1]
          levels.append(float(line))
          print("levels: ", levels)

        elif '"message_count":' in line:
          line = line.replace(" ","").replace(",","").replace("\n","")
          line = line.replace('"',""); line = line.split(":")[1]
          message_counts.append(float(line))
          print("message_counts: ", message_counts[-1])
          print("len message_counts: ", len(message_counts))

        elif '"username":' in line:
          line = line.replace(" ","").replace(",","").replace("\n","")
          line = line.replace('"',""); line = line.split(":")[1]
          usernames.append(line)
          print("usernames: ", usernames[-1])
          print("len usernames: ", len(usernames))

        elif '"xp":' in line:
          line = line.replace(" ","").replace(",","").replace("\n","")
          line = line.replace('"',""); line = line.split(":")[1]
          xps.append(float(line))
          print("xps -1: ", xps[-1])
          print("len xps: ", len(xps))

        elif '"role_rewards":' in line:
          flag = False

        # end if/elifs
        print(line)
        if "}" in line:
          input(">>")
        # end if
      # end if
    # end for
  # end with open

  print("len usernames: ", len(usernames))
  input(">>")

  if len(usernames) - num_old_usernames < LIMIT:
    break
  # end if

  cnt += 1
# end while
print("done with while loop!")

arr = [xps, ids, levels, avatars, usernames, message_counts,
       detailed_xp1s, detailed_xp2s, detailed_xp3s]

#np.savetxt(arr, SAVE_NAME, fmt="%s")

print("SUCCESS scrape_mee6")
## end scrape_mee6.py
