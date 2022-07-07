## going to add sappyseals next
REACTIONS = 100
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
csfont = {"fontname":"Adobe Garamond Pro"}
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina', quality=100)

EXT = ".txt"
DATA_DIR = "PublicMetricsData"
TYPES = ["Likes", "Replies", "Retweets", "QuoteTweets"]

fs = glob.glob(DATA_DIR + "/*.txt")

sto = {}
for ii,fname in enumerate(fs):
  username = fname.replace(EXT,"").split("/")[1]
  with open(fname, "r") as fid:
    line = fid.read()
  # end with open
  sto[username] = {
     "dates":       [],
     "Replies":     [],
     "Likes":       [],
     "Retweets":    [],
     "QuoteTweets": []
     }
  stou = sto[username]

  stou["followers"] = int(float(line.split("followersCount=")[1].split(",")[0]))

  dates = line.split("date=datetime.datetime(")[1:]
  for date in dates:
    stou["dates"].append(date.split(", tzinfo=datetime.timezone.utc")[0])
  # end for dates

  data = line.split("label=None), replyCount")[1:]
  for datum in data:
    counts = datum.split("=")
    stou["Replies"    ].append(int(float(counts[1].split(",")[0].replace(" ",""))))
    stou["Retweets"   ].append(int(float(counts[2].split(",")[0].replace(" ",""))))
    stou["Likes"      ].append(int(float(counts[3].split(",")[0].replace(" ",""))))
    stou["QuoteTweets"].append(int(float(counts[4].split(",")[0].replace(" ",""))))
  # end for data
# end for usernames

TYPES = ["Likes", "Replies", "Retweets", "QuoteTweets"]
OFFSET = 0.1
MULTIPLIER = [1,3,2,4]

YTI = 14
XTI = 12
LAB = 16
TIT = 18

ys = np.logspace(np.log10(3e-3),np.log10(2e3),len(fs))[::-1]

fig = plt.figure(figsize=(8,6))
usernames = []
colors = [
    "#641E16",
    "#7B241C", #2
    "#922B21", #3
    "#A93226", #4
    "#C0392B", #5
    "#CD6155", #6
    "#D98880", #7
    "#E6B0AA", #8
    "#F2D7D5", #9
    "#F9EBEA", #10
    "#EAF2F8", #11
    "#D4E6F1", #12
    "#A9CCE3", #13
    "#7FB3D5", #14
    "#5499C7", #15
    "#2980B9", #16
    "#2471A3", #17
    "#1F618D", #18
    "#1A5276", #19
    "#154360", #20
    "#424949", #21
    "#515A5A", #22
    "#616A6B", #23
    "#707B7C", #24
    "#7F8C8D", #25
    "#99A3A4", #26
    "#B2BABB", #27
]
colors = ["r", "b", "y", "c", "m"]
xtickvals_bot = []
xtickvals_top = []
xticklabels_bot = []
xticklabels_top = []
for ii,fname in enumerate(fs):
  #color = colors[ii]
  color = colors[ii%len(colors)]
  username = fname.replace(EXT,"").split("/")[1]

  stou = sto[username]
  usernames.append("@" + username)

  num_tweets = len(np.array(stou["dates"]))
  points = np.zeros(num_tweets)
  for jj in range(len(TYPES)):
    vals = stou[TYPES[jj]]
    if len(vals) < num_tweets:
      vals = vals + [0]*(num_tweets - len(vals))
    # end if
    points += np.array(vals) * MULTIPLIER[jj]
  # end for
  points = points / float(stou["followers"]) * 2e4 / float(num_tweets) * 100
  med = np.median(points)
  ymin,ymax = np.percentile(points, [25,75])

  if ii % 2 == 0:
    xtickvals_bot.append(ii)
    xticklabels_bot.append(str(ii))
  else:
    xtickvals_top.append(ii)
    xticklabels_top.append(str(ii))
    
  plt.scatter(ii, med, c=color, marker="o")#markers[jj])
  plt.vlines( ii, ymin=ymin, ymax=ymax, color=color)
  plt.text(x=len(fs)+1, y=ys[ii], s=str(ii).rjust(2) + ": @" + username, 
           fontsize=14, color=color)
# end for
plt.title("Twitter Engagement",fontsize=TIT)
plt.ylabel("Counts / 20k Followers / 100 Tweets",fontsize=LAB)
plt.yticks(fontsize=YTI)
plt.yscale("log")
plt.xticks(xtickvals_bot, xticklabels_bot, fontsize=XTI)
plt.ylim(5e-3,2e3)
plt.xlim(-1,len(fs))

ax = plt.gca()
axT = ax.secondary_xaxis("top")

axT.set_xticks(xtickvals_top)
axT.set_xticklabels(xticklabels_top, fontsize=XTI)

plt.tight_layout()
plt.savefig("points_per20kFollowersPer100Tweets.png")
plt.close()
