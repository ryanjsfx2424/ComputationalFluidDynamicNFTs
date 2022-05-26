## going to add sappyseals next
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

XTI = 14
LAB = 18
TIT = 20

slate_grey   = "#708090"
canopy_green = "#8CB76E"
llama_purple = "#4103fc"
poop_brown   = "#7b5c00"

sto["colors"] = {"rootroopnft":canopy_green,
                 "sappysealsnft":poop_brown,
                 "llamaverse_":llama_purple,
                 "gamingapeclub":slate_grey
                }
extra_colors = ["b", "r", "c", "m", "y", "k", #6
                "slategrey", "lightsalmon", "darkred", #9
                "deepskyblue", ""
                
               ]

sto["markers"] = {"rootroopnft": "*", #square
                 "sappysealsnft":"v", #upside-down triangle
                 "llamaverse_":  "d"   #diamond
                }
extra_markers = ["^", ">", "<", "P", "X", r"$\Xi$", 
                 r"$\bigodot$", r"$\bigoplus$", r"$\bigotimes$"]

markers = ["s", "o", "d", "P"]
colors  = ["b", "r", "c", "m"]

cnt = 0
xvals = []
yvals = []
yerrs = []
#colors  = []
#markers = []
usernames = []
for ii,fname in enumerate(fs):
  username = fname.replace(EXT,"").split("/")[1]

  if username not in sto["colors"].keys():
    continue
  # end if
  cnt += 1

  stou = sto[username]
  usernames.append("@" + username)    
  for jj in range(len(TYPES)):
    arr = np.array(stou[TYPES[jj]])
    yvals.append(np.median(arr))
    xvals.append(cnt+jj*OFFSET)
    yerrs.append(np.percentile(arr, [25,75]))
    #colors.append(color)
    #markers.append(marker)
    yvals[-1] = max(yvals[-1],1)
    plt.scatter(xvals[-1], yvals[-1], c=colors[jj], marker=markers[jj])
    plt.vlines(xvals[-1], ymin=yerrs[-1][0], ymax=yerrs[-1][1], color=colors[jj])
  # end for
# end for
plt.title("Twitter Engagement",fontsize=TIT)
plt.ylabel("Counts",fontsize=LAB)
plt.yticks(fontsize=XTI)
plt.yscale("log")
plt.xticks([1,3], usernames[::2], fontsize=XTI)
plt.xlim(0.85,4.5)

plots = []
for ii in range(len(colors)):
  pl, = plt.plot(-1,1, c=colors[ii], marker=markers[ii])
  plots.append(pl)
# end for ii
plt.legend(plots, TYPES, loc="upper center")

ax = plt.gca()
axT = ax.secondary_xaxis("top")

axT.set_xticks([2,4])
axT.set_xticklabels(usernames[1::2], fontsize=XTI)
plt.tight_layout()
plt.savefig("lrrtqt_plot_llamas_roos_seals_gac.png")
plt.close()
