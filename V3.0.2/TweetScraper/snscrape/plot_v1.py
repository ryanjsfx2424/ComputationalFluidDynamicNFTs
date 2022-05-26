import time; start = time.time()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
csfont = {"fontname":"Adobe Garamond Pro"}

TMI = 12
TMA = 14
TIT = 18
LAB = 16

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

fig, axs = plt.subplots(4,1, figsize=(6,12), dpi=80)
ii = -1
for key in sto.keys():
    if key == "dates":
        continue
    # end if
    ii += 1
    ax = axs[ii]
    ax.plot(np.arange(len(sto["dates"])), sto[key])
    ax.set_ylabel(key, fontsize=LAB, **csfont)
    ax.set_ylim(0, np.percentile(np.array(sto[key]), 99))
        
    ax.tick_params(axis="both", which="major", labelsize=TMA)
    ax.tick_params(axis="both", which="minor", labelsize=TMI)
# end for
axs[0].set_title("@RooTroopNFT", fontsize=TIT, **csfont)
axs[3].set_xlabel("tweet no.", fontsize=LAB, **csfont)
#axs[3].set_xticklabels(xticks, fontsize=TIC)
plt.tight_layout()
plt.savefig("RooTroopNFT_allData_99thPercentile6.png")
plt.close()

print("executed in (s): ", time.time() - start)
print("SUCCESS plot")
