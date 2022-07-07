import snscrape.modules.twitter as sntwitter
import time; start = time.time()

EXT = ".txt"

'''
usernames = ["llamaverse_",
             "GamingApeClub",
             "LlamascapeNFT",
             "champsonlypass",
             "projectPXN",
             "PGodjira",
             "Forgot3thWorlds",
             "psychedelic_nft",
             "EthaliensNFT",
             "SappySealsNFT",
             "NotBoredApes",
             "BoredBonesClub",
             "cryptopunksnfts",
             "AzukiOfficial",
             "coolcatsnft",
             "doodles",
             "okaybears",
             "BoredBunnyNFT",
             "AlphaSharksNFT",
             "TheSpaceBulls",
             "DormantDragons",
             "FlowerFamNFT",
             "cncpts",
             "TrippinApeNFT"]
'''
usernames = ["rootroopnft",
             "ThePlagueNFT",
             "goblintownwtf"
            ]

for username in usernames:
  username = username.lower()
  print("begin get data for: ", username)

  query = "from:" + username
  fsave = username + EXT

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
  with open(fsave, "w") as fid:
    fid.write(str(data))
  # end with open

  print("finished with: ", username)
  print("executed in: ", time.time() - start)
# end for

print("all done in: ", time.time() - start)
print("SUCCESS get_data")
