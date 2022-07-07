## going to add sappyseals next
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
csfont = {"fontname":"Adobe Garamond Pro"}
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina', quality=100)

EXT = ".txt"
usernames = ["rootroopnft",
             "llamaverse_",
             "sappysealsnft"
            ]

sto = {}
for username in usernames:
  fname = username.lower() + EXT
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

fig, axs = plt.subplots(4,1, figsize=(6,12), dpi=80)
width = 0.25

slate_grey   = "#708090"
canopy_green = "#8CB76E"
llama_purple = "#4103fc"
poop_brown   = "#7b5c00"

sto["rootroopnft"  ]["color"] = canopy_green
sto["llamaverse_"  ]["color"] = llama_purple
sto["sappysealsnft"]["color"] = poop_brown

YTI = 16
XTI = 12
TIT = 18
LAB = 18
LEG = 12

month_lookup = {
    "8":"Aug",
    "9":"Sep",
    "10":"Oct",
    "11":"Nov",
                "12":"Dec",
                 "1":"Jan",
                 "2":"Feb",
                 "3":"Mar",
                 "4":"Apr",
                 "5":"May"
                 }
month_to_ordered_int = {
    "Aug":-4,
    "Sep":-3,
    "Oct":-2,
    "Nov":-1,
    "Dec":0,
    "Jan":1,
    "Feb":2,
    "Mar":3,
    "Apr":4,
    "May":5
}
vals = [-4,-3,-2,-1,0,1,2,3,4,5]
months = ["Aug","Sep","Oct","Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]

offsets = [0,width,2*width]
for jj,username in enumerate(usernames):
    offset = offsets[jj]
    
    stou = sto[username]
    stou["month_data"] = {}
    mo_data = stou["month_data"]

    ## histogram by months first
    for ii in range(len(stou["dates"])):
        mo = stou["dates"][-(ii+1)].split(",")[1].replace(" ","")
        mo_name = month_lookup[mo]

        if mo_name not in mo_data.keys():
            mo_data[mo_name] = {"Likes":0, "Replies":0, 
                            "Retweets":0, "QuoteTweets":0}
        # end if
        mo_data[mo_name]["Likes"      ] += (stou["Likes"      ][-(ii+1)])
        mo_data[mo_name]["Replies"    ] += (stou["Replies"    ][-(ii+1)])
        mo_data[mo_name]["Retweets"   ] += (stou["Retweets"   ][-(ii+1)])
        mo_data[mo_name]["QuoteTweets"] += (stou["QuoteTweets"][-(ii+1)])    
    # end for ii
    
    for mo in month_to_ordered_int.keys():
        if mo not in mo_data.keys():
            mo_data[mo] = {"Likes":0, "Replies":0, 
                            "Retweets":0, "QuoteTweets":0}
        # end if
    # end for

    keys = []
    for mo in mo_data.keys():
        mo_num = month_to_ordered_int[mo]
        ii = -1
        for key in mo_data[mo].keys():
            keys.append(key)
            ii += 1
            axs[ii].bar(mo_num+offset, mo_data[mo][key], width, color=stou["color"])
        # end for
    # end mo
# end for usernames

for ii in range(4):
    ax = axs[ii]

    ax.set_xlim()
    ax.set_yscale("log")
    ax.set_ylabel(keys[ii], fontsize=LAB)
    ax.set_xticks(vals)
    ax.set_xticklabels(months, **csfont)
    ax.tick_params(axis="x", which="major", labelsize=XTI)
    ax.tick_params(axis="y", which="major", labelsize=YTI)
# end for ii

labels = []
un = usernames[0]
pl1, = axs[0].bar(-7, sto[un]["month_data"]["Jan"]["Likes"], color=sto[un]["color"])
labels.append("@" + un)

un = usernames[1]
pl2, = axs[1].bar(-7, sto[un]["month_data"]["Jan"]["Likes"], color=sto[un]["color"])
labels.append("@" + un)

un = usernames[2]
pl3, = axs[2].bar(-7, sto[un]["month_data"]["Jan"]["Likes"], color=sto[un]["color"])
labels.append("@" + un)

plots = [pl1,pl2,pl3]
axs[2].legend(plots, labels, fontsize=LEG, loc="upper left")

axs[0].set_title("Twitter Engagement", fontsize=TIT, **csfont)
plt.tight_layout()
plt.savefig("roos_vs_llamas_vs_seals.png")
plt.close()
