## going to add sappyseals next
import os
import ast
import time; start = time.time()
import numpy as np

sto = {"dates":[]}
fname = "at_rootroopnft.txt"
with open(fname, "r") as fid:
    line = fid.read()
# end with open

tweets = line.split("Tweet(url=")
print("num_tweets: ", len(tweets))

## doing this all at once is v slow b/c of building up the arrays
## for some reason it's faster to do it one at a time :D
sto["tweet_creation_times"] = []
for jj,tweet in enumerate(tweets[1:]):
    if jj % 10000 == 0:
        print(jj)
    date = tweet.split("date=datetime.datetime(")[1]
    date = date.split(", tzinfo=datetime.timezone.utc")[0]
    arr = date.split(",")
    
    for ii,el in enumerate(arr):
        arr[ii] = el.replace(" ", "")
        if ii != 0:
            arr[ii] = arr[ii].zfill(2)
    # end for ii
    
    if len(arr) == 6:
        yy,mm,dd,HH,MM,SS = arr[:]
    else:
        yy,mm,dd,HH,MM = arr[:]
        SS = "00"
    # end if/else    
    
    date = yy + "-" + mm + "-" + dd + "T" + HH + ":" + MM + ":" + SS + ".000Z"
    sto["tweet_creation_times"].append(date)
# end for tweets
print("len(sto[tweet_creation_times]: ", len(sto["tweet_creation_times"]))

## doing this all at once is v slow b/c of building up the arrays
## for some reason it's faster to do it one at a time :D
sto["tweet_ids"] = []
for jj,tweet in enumerate(tweets[1:]):
    if jj % 10000 == 0:
        print(jj)
    # end if
    
    status = tweet.split("/status/")[1]
    sto["tweet_ids"].append(status.split("',")[0])    
# end for tweets
print("len(sto[tweet_ids]: ",      len(sto["tweet_ids"]))

## doing this all at once is v slow b/c of building up the arrays
## for some reason it's faster to do it one at a time :D
sto["usernames"] = []
for jj,tweet in enumerate(tweets[1:]):
    if jj % 10000 == 0:
        print(jj)
    # end if
    
    username = tweet.split("https://twitter.com")[1]
    sto["usernames"].append(username.split("/status/")[0][1:])    
# end for tweets
print("len(sto[usernames]: ",      len(sto["usernames"]))

## doing this all at once is v slow b/c of building up the arrays
## for some reason it's faster to do it one at a time :D
sto["user_ids"] = []
for jj,tweet in enumerate(tweets[1:]):
    if jj % 10000 == 0:
        print(jj)
    # end if
    
    idn = tweet.split(", user=User(username='")[1]
    idn = idn.split(", displayname=")[0]
    idn = idn.split("id=")[1]
    sto["user_ids"].append(idn)
# end for tweets
print("len(sto[user_ids]: ", len(sto["user_ids"]))

## doing this all at once is v slow b/c of building up the arrays
## for some reason it's faster to do it one at a time :D
sto["tweet_contents"] = []
for jj,tweet in enumerate(tweets[1:]):
    if jj % 1 == 0:
        print(jj)
    # end if
    
    content = tweet.split("content=")[1]
    sto["tweet_contents"].append(content.split("renderedContent")[0])
# end for tweets
print()
print("len(sto[tweet_creation_times]: ", len(sto["tweet_creation_times"]))
print("len(sto[tweet_contents]: ", len(sto["tweet_contents"]))
print("len(sto[usernames]: ",      len(sto["usernames"]))
print("len(sto[user_ids]: ",       len(sto["user_ids"]))
print("len(sto[tweet_ids]: ",      len(sto["tweet_ids"]))
print("executed in (s): ", time.time() - start)
#input(">>")
arr = np.array([ sto["tweet_creation_times"], sto["tweet_contents"],
                 sto["usernames"], sto["user_ids"], sto["tweet_ids"] ])
np.savetxt("rootroop_keyword_arrays.txt", arr, fmt="%s")

with open("../twitter_data/activity_by_user.json", "r") as fid:
    activity_by_user = ast.literal_eval(fid.read())
# end with open
print("loaded abu")

num_ids = len(sto["user_ids"])
special_tweeters = {"1447280926967304195":"rootroopnft",
                    "1477912158730170370":"troopsales"}

for ii in range(num_ids):
    print("ii: ", ii)
    
    uid     = sto["user_ids"      ][ii]
    twid    = sto["tweet_ids"     ][ii]    
    un      = sto["usernames"     ][ii]
    content = sto["tweet_contents"][ii]
    
    if uid in special_tweeters.keys():
        print("uid in special tweeters")
        continue
    # end if
 
    if "rootroop" not in content.lower():
      print("rootroop not in content so skipping!")
      continue
    # end if
   
    if uid not in activity_by_user.keys():
        # then it's a pain :D
        print("uid not in abu!")
        activity_by_user[uid] = \
              {"usernames": [],
               "num_keyword_replies": 0,
               "num_keyword_retweets": 0,
               "tweet_ids": [],
               "tweet_contents": [],
               "tweet_creation_times": [],
               "Likes": {"num_Likes": 0, "tweet_ids": [], "tweet_creation_times": []},
               "Retweets": {"num_Retweets": 0, "tweet_ids": [], "tweet_creation_times": []},
               "QuoteTweets": {"num_QuoteTweets": 0, "tweet_ids": [], "tweet_creation_times": [], "tweet_contents": []},
               "Replies": {"num_Replies": 0, "tweet_ids": [], "tweet_creation_times": [], "tweet_contents": []}
              }
        abu = activity_by_user[uid]

    else:
        abu = activity_by_user[uid]
        
        if twid in abu["tweet_ids"]:
            print("twid in twids so continuing")
            continue
        # end if
    # end if
    abu["tweet_ids"].append(twid)
    abu["tweet_ids"] = list(set(abu["tweet_ids"]))
    
    if un not in abu["usernames"]:
        print("added username!")
        print("un: ", un)
        abu["usernames"].append(un)
        print("abu last 2 usernames: ", abu["usernames"][-2:])
        print("uid: ", uid)
        print("twid: ", twid)
        print("content: ", content)
        print("tweets[ii+1]: ", tweets[ii+1])
        print()
        #if ii >  22924:
        #  input(">>")
    # end if
    abu["usernames"] = list(set(abu["usernames"]))
    
    if content[:3] == "RT ":
        abu["num_keyword_retweets"] += 1
    else:
        abu["num_keyword_replies"]  += 1
    # end if/else
    abu["tweet_contents"].append(content)
    abu["tweet_contents"]= list(set(abu["tweet_contents"]))

    abu["tweet_creation_times"].append(sto["tweet_creation_times"][ii])
    abu["tweet_creation_times"] = list(set(abu["tweet_creation_times"]))
# end for

with open("../twitter_data/activity_by_user2.json", "w") as fid:
    fid.write(str(activity_by_user))
# end with open
## end process_historical_mentions.py
