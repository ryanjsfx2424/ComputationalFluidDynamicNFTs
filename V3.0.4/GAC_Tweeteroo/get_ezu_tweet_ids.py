## get_ezu_tweet_ids.py

with open("data_big/from_ezu_xyz", "r") as fid:
  line = fid.read()
# end with

twids = line.split("https://twitter.com/ezu_xyz/status/")[1:]

tweet_ids = []
for twid in twids:
  twid = twid.split("'")[0]
  tweet_ids.append(twid)
# end for twids

with open("data_big/tweet_ids_ezu_xyz", "w") as fid:
  fid.write(str(tweet_ids))
# end with open

print("SUCCESS get_ezu_tweet_ids")
## end get_ezu_tweet_ids.py
