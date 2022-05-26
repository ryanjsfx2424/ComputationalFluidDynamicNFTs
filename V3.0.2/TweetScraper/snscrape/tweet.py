import snscrape.modules.twitter as sntwitter
import time; start = time.time()

#query = "Rooty Roo" # didn't save :*(
#query = "from:rootroopnft" # saved :)

ext = ".txt"
username = "llamaverse_"
params = {"query": "from:" + username,
          "savename": username + ext}

cnt = 0
tweets = sntwitter.TwitterSearchScraper(query).get_items()
data = []
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
  cnt += 1
  if cnt % 100 == 0:
    print(cnt)
  # end if
  data.append(tweet)
# end for
with open(".txt", "w") as fid:
  fid.write(str(data))
# end with open

print("executed in: ", time.time() - start)
