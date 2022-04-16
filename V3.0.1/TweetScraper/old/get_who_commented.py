## get_who_liked.py 2022-04-14
"""
The purpose of this function is to simply get all users (by id and
username, ideally sort by username but id in case they changed username)
that liked a given tweet.

I'll make this a method in a class later.
"""
import os

TW_BT  = "AAAAAAAAAAAAAAAAAAAAA" + "ErfbQEAAAAA4siTkqCljmdikM1sMstce"
TW_BT += "C5cLsc%3DBFO7678SQQUacoQQjzL8PLH9QsRXFLYMrvlddHGKJpb4P899KF"

ID_NUM = "1514103176831545344" # roo troop recent tweet
FNAME = "users_liked_tweet_" + ID_NUM + ".txt"

url = "https://api.twitter.com/2/tweets/" + ID_NUM + "/liking_users?user.fields=username"

os.system("curl --request GET --url '" + url + "' --header 'Authorization: Bearer " + TW_BT + "' > " + FNAME)

print("SUCCESS")
## end get_retweets
