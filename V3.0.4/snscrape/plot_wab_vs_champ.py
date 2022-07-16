## just gonna look at past two weeks of RooTroopNFT mentions and engagement to see if introduction of tweeteroo caused a spike.
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

with open("data_big/at_wabdoteth", "r") as fid:
    mentions = fid.read()
# end with
mentions = mentions.split("Tweet(")[1:]

with open("data_big/at_champtgram", "r") as fid:
    mentionsCH = fid.read()
# end with
mentionsCH = mentionsCH.split("Tweet(")[1:]

dates = []
for mention in mentions:
    dates.append(mention.split("date=datetime.datetime(")[1].split(", tzinfo=")[0])
# end for

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

slate_grey   = "#708090"
canopy_green = "#8CB76E"
llama_purple = "#4103fc"
poop_brown   = "#7b5c00"

ind = np.arange(len(xx)) # location of x points
print("xx[0]: ", xx[0])
xlabels = ["dud"] + xx[::2] + ["dud"]
width = 0.35

styles = plt.style.available
for style in styles:
    if "seaborn-colorblind" not in style:
        continue
    plt.style.use(style)
    fig = plt.figure(figsize=(10,8))
    plt.bar(ind-width/2.0,yy,   width=width, label="@wabdoteth", color=slate_grey )
    plt.bar(ind+width/2.0,yyCH, width=width, label="@champtgram", color=poop_brown)
    plt.axhline(y=sum(yy  ) / 12.0, color=slate_grey)
    plt.axhline(y=sum(yyCH) / 12.0, color=poop_brown)
    
    plt.legend(fontsize=18)
    plt.title("wabdoteth vs. champtgram", fontsize=24)
    plt.ylabel("mentions", fontsize=21)
    plt.xlabel("date", fontsize=21)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.gca().set_xticklabels(xlabels)
    plt.tight_layout()
    plt.savefig("wab_vs_champ_style_" + style + ".png")
    plt.close()
# end for
