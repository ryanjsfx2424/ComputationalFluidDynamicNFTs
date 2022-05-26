## process_rootroopnft.py
import matplotlib.pyplot as plt

# first let's just check how many tweets it grabbed.
with open("rootroopnft.txt", "r") as fid:
  line = fid.read()
# end with open

sto = {"dates": [],
     "replyCount": [],
     "likeCount": [],
     "retweetCount": [],
     "quoteCount": []}

dates = line.split("date=datetime.datetime(")[1:]
for date in dates:
  sto["dates"].append(date.split(", tzinfo=datetime.timezone.utc")[0])
# end for dates

data = line.split("label=None), replyCount")[1:]
for datum in data:
  counts = datum.split("=")
  sto["replyCount"  ].append(int(float(counts[1].split(",")[0].replace(" ",""))))
  sto["retweetCount"].append(int(float(counts[2].split(",")[0].replace(" ",""))))
  sto["likeCount"   ].append(int(float(counts[3].split(",")[0].replace(" ",""))))
  sto["quoteCount"  ].append(int(float(counts[4].split(",")[0].replace(" ",""))))
# end for data


