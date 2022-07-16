## check_num_ezu_tweets
with open("data_big/at_ezu_xyz", "r") as fid:
  line = fid.read()
# end with open

tweets = line.split("Tweet(")
print("len tweets: ", len(tweets))

print("SUCCESS check_num_ezu_mentions")
## end check_num_ezu_tweets.py
