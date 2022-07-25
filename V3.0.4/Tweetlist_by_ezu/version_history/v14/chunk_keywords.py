with open("data_big/keywords_ezu_xyz.txt", "r") as fid:
  tweets = fid.read()
# end with open
tweets = tweets.split("Tweet(")[1:]
print("split the tweets!")

cnt = 0
to_save = []
for ii,tweet in enumerate(tweets):
  if ii % 1000 == 0 and ii != 0:
    print("ii: ", ii)
    cnt += 1
    with open("data_big/keywords_data/keywords" + str(cnt).zfill(6) + "_ezu_xyz.txt", "w") as fid:
      fid.write("".join(to_save))
      to_save = []
    # end with open
  # end if
  to_save.append("Tweet(" + tweet)
# end for
