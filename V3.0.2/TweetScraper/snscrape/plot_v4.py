## going to post llamaverse side-by-side with rootroop
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

slate_grey = "#708090"
canopy_green = "#8CB76E"
llama_purple = "#4103fc"
sto["rootroopnft"  ]["color"] = canopy_green
sto["llamverse_"   ]["color"] = llama_purple
sto["sappysealsnft"]["color"] = llama_purple

YTI = 16
XTI = 13
TIT = 18
LAB = 18

month_lookup = {
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
    "Oct":-1,
    "Nov":0,
    "Dec":1,
    "Jan":2,
    "Feb":3,
    "Mar":4,
    "Apr":5,
    "May":6
}
months = ["pad","Oct","Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]

sto["month_data"] = {}
mo_data = sto["month_data"]

sto2["month_data"] = {}
mo_data2 = sto2["month_data"]

## histogram by months first
for ii in range(len(sto["dates"])):
    mo = sto["dates"][-(ii+1)].split(",")[1].replace(" ","")
    mo_name = month_lookup[mo]
    
    if mo_name not in mo_data.keys():
        mo_data[mo_name] = {"Likes":0, "Replies":0, 
                        "Retweets":0, "QuoteTweets":0}
    # end if
    mo_data[mo_name]["Likes"      ] += (sto["Likes"      ][-(ii+1)])
    mo_data[mo_name]["Replies"    ] += (sto["Replies"    ][-(ii+1)])
    mo_data[mo_name]["Retweets"   ] += (sto["Retweets"   ][-(ii+1)])
    mo_data[mo_name]["QuoteTweets"] += (sto["QuoteTweets"][-(ii+1)])    
# end for ii

mo_data["Oct"] = {"Likes":0, "Replies":0, 
                        "Retweets":0, "QuoteTweets":0}

## histogram by months first
for ii in range(len(sto2["dates"])):
    mo = sto2["dates"][-(ii+1)].split(",")[1].replace(" ","")
    mo_name = month_lookup[mo]
    
    if mo_name not in mo_data2.keys():
        mo_data2[mo_name] = {"Likes":0, "Replies":0, 
                        "Retweets":0, "QuoteTweets":0}
    # end if
    mo_data2[mo_name]["Likes"      ] += (sto2["Likes"      ][-(ii+1)])
    mo_data2[mo_name]["Replies"    ] += (sto2["Replies"    ][-(ii+1)])
    mo_data2[mo_name]["Retweets"   ] += (sto2["Retweets"   ][-(ii+1)])
    mo_data2[mo_name]["QuoteTweets"] += (sto2["QuoteTweets"][-(ii+1)])    
# end for ii

width = 0.35

keys = []
for mo in mo_data.keys():
    mo_num = month_to_ordered_int[mo]
    ii = -1
    for key in mo_data[mo].keys():
        keys.append(key)
        ii += 1
        axs[ii].bar(mo_num, mo_data[mo][key], width, color=canopy_green)
    # end for
# end mo

keys = []
for mo in mo_data2.keys():
    mo_num = month_to_ordered_int[mo]
    ii = -1
    for key in mo_data2[mo].keys():
        keys.append(key)
        ii += 1
        axs[ii].bar(mo_num+width, mo_data2[mo][key], width, color=llama_purple)
    # end for
# end mo

for ii in range(4):
    ax = axs[ii]
#    labels = [item.get_text() for item in ax.get_xticklabels()]
    #labels[1] = 'Testing'

    ymax = 2e4
    if ii == 0:
        ymax = 3e4
    elif ii == 3:
        ymax = 1e3
    ax.set_yscale("log")
    #ax.set_ylim(0,ymax)
    ax.set_ylabel(keys[ii], fontsize=LAB)
    ax.set_xticklabels(months, **csfont)
    ax.tick_params(axis="x", which="major", labelsize=XTI)
    ax.tick_params(axis="y", which="major", labelsize=YTI)
# end for ii
axs[0].set_title("@RooTroopNFT vs. @Llamaverse_", fontsize=TIT, **csfont)
plt.tight_layout()
plt.savefig("roos_vs_llamas.png")
plt.close()
