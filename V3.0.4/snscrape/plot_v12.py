## comparing mentions of bluechips
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
csfont = {"fontname":"Adobe Garamond Pro"}

fs = [
      "at_azukiofficial.txt_150days",
      "at_boredapeyc.txt_first150ishDays",
      "at_goblintownwtf.txt_20days",
      "at_moonbirds.txt_55days"
     ]

sto = {}
for ii,fname in enumerate(fs):
  username = fname.split(".txt")[0][3:]
  print("username: ", username)

  with open(fname, "r") as fid:
    line = fid.read()
  # end with open
  print("chars in line: ", len(line))

  tweets = line.split("Tweet(url=")[1:]
  print("num tweets: ", len(tweets))
  dates     = []
  followers = np.zeros(len(tweets))
  for jj in range(len(tweets)):
    tweet = tweets[jj]
    print("jj: ", jj)
    followers[jj] = int(float(tweet.split("followersCount=")[1].split(",")[0]))
    dates.append(tweet.split("date=datetime.datetime(")[1].split(
                            ", tzinfo=datetime.timezone.utc")[0])
  # end for jj
  dates = np.array(dates)
  np.savetxt(username + "_mentions_data.txt", [dates,followers], fmt="%s")
# end for usernames
## end plot_v12.py
