## just gonna look at past two weeks of RooTroopNFT mentions and engagement to see if introduction of tweeteroo caused a spike.
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

with open("data_big/at_wabdoteth", "r") as fid:
    mentions = fid.read()
# end with
with open("data_big/at_wabdoteth_since_July_12th", "r") as fid:
    mentions += fid.read()
# end with

mentions = mentions.split("Tweet(")[1:]

with open("data_big/at_nftsarenice", "r") as fid:
    mentionsCH = fid.read()
# end with
mentionsCH = mentionsCH.split("Tweet(")[1:]

dates = []
for mention in mentions:
    dates.append(mention.split("date=datetime.datetime(")[1].split(", tzinfo=")[0])
# end for
dates = list(set(dates))

datesCH = []
for mention in mentionsCH:
    datesCH.append(mention.split("date=datetime.datetime(")[1].split(", tzinfo=")[0])
# end for

days = {}
for date in dates[::-1]:
    date = date.replace(" ","")
    if len(date.split(",")) == 6:
        yy,mm,dd,HH,MM,SS = date.split(",")
    else:
        yy,mm,dd,HH,MM = date.split(",")
    if mm != "7":
        continue
    # end if
    day = yy + "-" + mm + "-" + dd
    if day not in days:
        days[day] = 0
    # end if

    days[day] += 1
    #print("days: ", days)
    #input(">>")
# end for

daysCH = {}
for date in datesCH[::-1]:
    date = date.replace(" ","")
    if len(date.split(",")) == 6:
        yy,mm,dd,HH,MM,SS = date.split(",")
    else:
        yy,mm,dd,HH,MM = date.split(",")
    # end if/else
    if mm != "7":
        continue
    # end if
    day = yy + "-" + mm + "-" + dd
    if day not in daysCH:
        daysCH[day] = 0
    # end if

    daysCH[day] += 1
# end for

xx = []
yy = []

for day in days:    
    #xx.append(day.split("-")[-1])
    xx.append(day.replace("2022-",""))
    yy.append(days[day])

xxCH = []
yyCH = []

for day in daysCH:    
    #xx.append(day.split("-")[-1])
    xxCH.append(day.replace("2022-","").replace("2021-",""))
    yyCH.append(daysCH[day])
print("xxCH b4: ", xxCH)
#xxCH.append("7-14")
#yyCH.append(0)

print("1 len xx: ", len(xx))
print("1 len xxCH: ", len(xxCH))
print("1 len yy: ", len(yy))
print("1 len yyCH: ", len(yyCH))

min_len = min(len(xx), len(xxCH))

inds = []
indsCH = []
for ii in range(len(xx)):
  inds.append(float(xx[ii].split("-")[1]))
for ii in range(len(xxCH)):
  indsCH.append(float(xxCH[ii].split("-")[1]))
# end for ii
print("xx: ", xx)
print("xxC: ", xxCH)
inds = np.argsort(np.array(inds))
indsCH = np.argsort(np.array(indsCH))
print("i: ", inds)
print("iC: ", indsCH)

xx = np.array(xx)
yy = np.array(yy)
xxCH = np.array(xxCH)
yyCH = np.array(yyCH)

xx = xx[inds]
yy = yy[inds]
xxCH = xxCH[indsCH]
yyCH = yyCH[indsCH]

xx   = list(xx)
yy   = list(yy)
xxCH = list(xxCH)
yyCH = list(yyCH)

xx = xx[:min_len]
yy = yy[:min_len]
xxCH = xxCH[:min_len]
yyCH = yyCH[:min_len]

print("2 len xx: ", len(xx))
print("2 len xxCH: ", len(xxCH))
print("2 len yy: ", len(yy))
print("2 len yyCH: ", len(yyCH))

slate_grey   = "#708090"
canopy_green = "#8CB76E"
llama_purple = "#4103fc"
poop_brown   = "#7b5c00"

ind = np.arange(len(xx)) # location of x points
print("xx[0]: ", xx[0])
xlabels = ["dud"] + xx[::2] + ["dud"]
xlabels = ["dud", "7-1", "7-3", "7-5", "7-7", "7-9", "7-11", "7-13", "dud"]
width = 0.35

styles = plt.style.available
for style in styles:
    if "seaborn-colorblind" not in style:
        continue
    plt.style.use(style)
    fig = plt.figure(figsize=(10,8))
    plt.bar(ind-width/2.0,yy,   width=width, label="@wabdoteth", color=slate_grey )
    plt.bar(ind+width/2.0,yyCH, width=width, label="@nftsarenice", color=poop_brown)
    plt.axhline(y=sum(yy  ) / 12.0, color=slate_grey)
    plt.axhline(y=sum(yyCH) / 12.0, color=poop_brown)
    
    plt.legend(fontsize=18)
    plt.title("wabdoteth vs. nftsarenice", fontsize=24)
    plt.ylabel("mentions", fontsize=21)
    plt.xlabel("date", fontsize=21)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.gca().set_xticklabels(xlabels)
    plt.tight_layout()
    plt.savefig("wab_vs_menace_style_" + style + ".png")
    plt.close()
# end for
