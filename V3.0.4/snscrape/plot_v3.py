import time; start = time.time()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
csfont = {"fontname":"Adobe Garamond Pro"}

with open("rootroopnft.txt", "r") as fid:
  line = fid.read()
# end with open

sto = {"dates": [],
     "Replies": [],
     "Likes": [],
     "Retweets": [],
     "QuoteTweets": []}

dates = line.split("date=datetime.datetime(")[1:]
for date in dates:
  sto["dates"].append(date.split(", tzinfo=datetime.timezone.utc")[0])
# end for dates

data = line.split("label=None), replyCount")[1:]
for datum in data:
  counts = datum.split("=")
  sto["Replies"    ].append(int(float(counts[1].split(",")[0].replace(" ",""))))
  sto["Retweets"   ].append(int(float(counts[2].split(",")[0].replace(" ",""))))
  sto["Likes"      ].append(int(float(counts[3].split(",")[0].replace(" ",""))))
  sto["QuoteTweets"].append(int(float(counts[4].split(",")[0].replace(" ",""))))
# end for data

## next, going to bin by day for the past month
plt.close()
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina', quality=100)
fig, axs = plt.subplots(4,1, figsize=(6,12), dpi=80)

YTI = 16
XTI = 13
TIT = 18
LAB = 18

sto["day_data"] = {"days":[], "Likes":[],"Replies":[],"Retweets":[],"QuoteTweets":[]}
dd = sto["day_data"]

for ii in range(len(sto["dates"])):
    mo,day = sto["dates"][-(ii+1)].split(",")[1:3]
    mo  =  mo.replace(" ","")
    day = day.replace(" ","")
    if mo != "5":
        continue
    # end if

    day = int(float(day))
    if day not in dd["days"]:
        dd["days"].append(day)
        dd["Likes"].append(0)
        dd["Replies"].append(0)
        dd["Retweets"].append(0)
        dd["QuoteTweets"].append(0)
    else:
        dd["Likes"][      -1] += sto["Likes"][      -(ii+1)]
        dd["Replies"][    -1] += sto["Replies"][    -(ii+1)]
        dd["Retweets"][   -1] += sto["Retweets"][   -(ii+1)]
        dd["QuoteTweets"][-1] += sto["QuoteTweets"][-(ii+1)]
    # end if/else
# end for ii

slate_grey = "#708090"
canopy_green = "#8CB76E"

mmap = {"0":dd["Likes"],
        "1":dd["Replies"],
        "2":dd["Retweets"],
        "3":dd["QuoteTweets"]}
keys = ["Likes","Replies","Retweets","QuoteTweets"]
for ii in range(4):
    ax = axs[ii]
    ax.bar(dd["days"], mmap[str(ii)], color=canopy_green)

    ax.set_yscale("log")
    ax.set_ylabel(keys[ii], fontsize=LAB)
    #ax.set_xticklabels(months, **csfont)
    ax.tick_params(axis="x", which="major", labelsize=XTI)
    ax.tick_params(axis="y", which="major", labelsize=YTI)
    ax.set_xlim(6.5,20.5)
# end for ii
axs[0].set_title("@RooTroopNFT", fontsize=TIT, **csfont)
plt.tight_layout()
plt.savefig("RooTroopNFT_barsPastFortnight.png")
plt.close()

print("executed in (s): ", time.time() - start)
print("SUCCESS plot")
