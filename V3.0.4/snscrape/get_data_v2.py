import snscrape.modules.twitter as sntwitter
import time; start = time.time()

EXT = ".txt"

## collected in the first run:
'''
at_champsonlypass.txt
at_gamingapeclub.txt
at_llamascapenft.txt
at_llamaverse_.txt
at_rootroopnft.txt
at_tothemoonsnft.txt
'''

#usernames = ["rootroopnft",
#             "llamaverse_",
#             "GamingApeClub",
#             "LlamascapeNFT",
#             "champsonlypass",

## to do:
usernames = ["projectPXN",
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
usernames = [
             "esu_xyz"
            ]
## note, moonbirds minted April 16th about 3:13pm UTC
## note, Azuki launched about 150 days ago
## note, BoredApeYachtClub launched 415 days ago (today is June 10th)
##   on April 22nd 3:03am

for username in usernames:
  username = username.lower()
  print("begin get data for: ", username)

  query = "@" + username# + " until:2021-10-01 since:2021-04-01"
  fsave = "at_" + username + EXT# + "_first150ishDays"

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
