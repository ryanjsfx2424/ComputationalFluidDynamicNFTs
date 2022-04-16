## scrape_tweets.py 2022-04-14
"""
Playing around with tweepy for now.

JK mostly using os curl requests
"""
import os
import sys
import requests
import tweepy

TW_BT  = "AAAAAAAAAAAAAAAAAAAAA" + "ErfbQEAAAAA4siTkqCljmdikM1sMstce"
TW_BT += "C5cLsc%3DBFO7678SQQUacoQQjzL8PLH9QsRXFLYMrvlddHGKJpb4P899KF"

## for re-tweets/quote tweets
id_num = "1354143047324299264"
id_num = "1514103176831545344" # roo troop recent tweet
id_num = "1515192646578290688"

## last thing to figure out is how to get replies to a given tweet
## (specifically the user ids/usernames that replies)
url = "https://api.twitter.com/2/tweets/search/recent?query=conversation_id:" + id_num + "&max_results=100&expansions=author_id&user.fields=username"
#url = "https://api.twitter.com/2/tweets/" + id_num + "/liking_users?user.fields=username"

os.system("curl --request GET --url '" + url + "' --header 'Authorization: Bearer " + TW_BT + "'")

#url = "https://api.twitter.com/2/tweets/" + id_num + "/quote_tweets?user.fields=username&expansions=author_id"
#url = "https://api.twitter.com/2/tweets/" + id_num + "/liking_users?user.fields=username"

#os.system("curl --request GET --url '" + url + "' --header 'Authorization: Bearer " + TW_BT + "'")


#url = "https://api.twitter.com/2/tweets/" + id_num + "/retweeted_by?user.fields=created_at&expansions=pinned_tweet_id&tweet.fields=created_at"
url = "https://api.twitter.com/2/tweets/" + id_num + "/retweeted_by?user.fields=username"

#os.system("curl --request GET --url '" + url + "' --header 'Authorization: Bearer " + TW_BT + "'")

print("SUCCESS")
sys.exit()

# this worked!
#os.system("curl --request GET --url 'https://api.twitter.com/2/tweets?ids=1225917697675886593&tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username' --header 'Authorization: Bearer " + TW_BT + "'")

## didn't work - maybe tweet was too old? (nah didn't work for roo troop either)
#os.system("curl --request GET --url 'https://api.twitter.com/2/tweets/search/recent?query=conversation_id:1279940000004973111&tweet.fields=in_reply_to_user_id,author_id,created_at,conversation_id'  --header 'Authorization: Bearer " + TW_BT + "'")


## now let's try to apply it to a recent roo troop tweet.
id_num = "1514103176831545344"
id_num = "1499858580568109058"
# this worked but only shows tweet text and info requested not the replies
#os.system("curl --request GET --url 'https://api.twitter.com/2/tweets?ids=" + id_num + "&tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username' --header 'Authorization: Bearer " + TW_BT + "'")


## maybe this will show replies? -> nerp just text of orig tweet
#os.system("curl --request GET --url 'https://api.twitter.com/2/tweets?ids=" + id_num + "' --header 'Authorization: Bearer " + TW_BT + "'")

## this worked :)
#os.system("curl --request GET --url 'https://api.twitter.com/2/tweets/search/recent?query=from%3Atwitterdev&tweet.fields=public_metrics' --header 'Authorization: Bearer " + TW_BT + "'")

## the below gave 403 no access for api.home_timeline()
# most basic - works!
#os.system('curl -X GET -H "Authorization: Bearer ${TW_BT}" "https://api.twitter.com/2/tweets/20"')

#os.system('curl "https://api.twitter.com/2/users/by/username/RooTroopNFT" -H "Authorization: Bearer ${TW_BT}"')

## grabbed the tweets Roo Troop sent recently (idk how many)
#os.system('curl "https://api.twitter.com/2/tweets/search/recent?query=from:RooTroopNFT&tweet.fields=created_at&expansions=author_id&user.fields=created_at" -H "Authorization: Bearer ${TW_BT}"')

## gives 401, unauthorized :(
#os.system("curl --request GET 'https://api.twitter.com/2/users/TheLunaLabs/tweets' --header 'Authorization: Bearer ${TW_BT}'")

## tutorial
# also unauthorized :(
#os.system("curl --request GET --url 'https://api.twitter.com/2/tweets?ids=1260294888811347969' --header 'Authorization: Bearer ${TW_BT}'")

RooTweet = "https://twitter.com/RooTroopNFT/status/1499858580568109058?s=20&t=akwNHnsGLbvpDC-yfjvBVw"
## this worked! Would be v messy to scrape but seems possible
## actually, didn't work b/c twitter notices we don't have JS enabled...
#foo = requests.get(RooTweet)

#with open("tweet_data.txt", "w") as fid:
#  for line in foo.text:
#    fid.write(line)
#print("SUCCESS!")

## this is still saying doesn't work b/c JS not enabled...
'''
from requests_html import HTMLSession
session = HTMLSession()
r = session.get(RooTweet)
r.html.render()
print(r.html.links)

r2 = r.html.find(".css-1dbjc4n r-1wbh5a2 r-dnmrzs")
print(r2)

#with open("tweet_data3.html", "w") as fid:
#  for line in r.text:
#    fid.write(line)
print("SUCCESS!")
'''

'''
#TW_BT = os.environ["TW_BT"]
#TW_BT = 21*"A" + "ErfbQE" + 5*"A" + "nw%2f6gK2CGmK1Gd17oxlVzD7Twy4%"
#TW_BT += "3Dk57PWx3AsGD4LCQqykrl6Q24T76LL7kBN6lh"
#TW_BT += "vGeKJD8EgTJll9"
TW_BT  = "AAAAAAAAAAAAAAAAAAAAA" + "ErfbQEAAAAA4siTkqCljmdikM1sMstce"
TW_BT += "C5cLsc%3DBFO7678SQQUacoQQjzL8PLH9QsRXFLYMrvlddHGKJpb4P899KF"
auth = tweepy.OAuth2BearerHandler(TW_BT)
api = tweepy.API(auth)

text_query = "2020 US Election"
count = 150

## this doesn't work either
tweets = tweepy.Cursor(api.search, q=text_query).items(count)
print(tweets)

tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
print(tweets_list)
'''

'''
public_tweets = api.home_timeline()
for tweet in public_tweets:
  print(tweet.text)
  print("\n")
'''

## from towardsdatascience: api no "search" method :(
'''
RooTweet = "https://twitter.com/RooTroopNFT/status/1499858580568109058?s=20&t=akwNHnsGLbvpDC-yfjvBVw"

name = "RooTroopNFT"
tweet_id = "1499858580568109058"

replies = []
for tweet in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', timeout=120).items(1000):
  if hasattr(tweet, 'in_reply_to_status_id_str'):
    if (tweet.in_reply_to_status_id_str==tweet_id):
      replies.append(tweet)

with open('replies_clean.csv', 'w') as fid:
  csv_writer = csv.DictWriter(fid, fieldnames=("user", "text"))
  csv_writer.writeheader()
  for tweet in replies:
    row = {"user": tweet.user.screen_name, "text":tweet.text.replace("\n", " ")}
    csv_writer.writerow(row)
'''
