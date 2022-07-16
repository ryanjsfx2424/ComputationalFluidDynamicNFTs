import snscrape.modules.twitter as sntwitter
import time; start = time.time()
import os
os.chdir("data_big")

EXT = ".txt"

usernames = [
             "gamingapeclub"
            ]

for username in usernames:
  username = username.lower()
  print("begin get data for: ", username)

  query = "from:" + username
  fsave = "from_" + username

  cnt = 0
  tweets = sntwitter.TwitterSearchScraper(query).get_items()
  data = []
  for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    cnt += 1
    if cnt % 100 == 0:
      print(cnt)
      with open(fsave, "w") as fid:
        fid.write(str(data))
      # end with open
    # end if
    data.append(tweet)
  # end for
  with open(fsave, "w") as fid:
    fid.write(str(data))
  # end with open

  print("finished with: ", username)
  print("executed in: ", time.time() - start)
# end for

print("all done in: ", time.time() - start)
print("SUCCESS get_data")
