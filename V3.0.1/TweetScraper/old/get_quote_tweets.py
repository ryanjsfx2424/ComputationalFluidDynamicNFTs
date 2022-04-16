## get_retweets.py 2022-04-14
"""
The purpose of this function is to simply get all users (by id and
username, ideally sort by username but id in case they changed username)
that quote tweeted a given tweet.

I'll make this a method in a class later.
"""
import os

TW_BT  = "AAAAAAAAAAAAAAAAAAAAA" + "ErfbQEAAAAA4siTkqCljmdikM1sMstce"
TW_BT += "C5cLsc%3DBFO7678SQQUacoQQjzL8PLH9QsRXFLYMrvlddHGKJpb4P899KF"

ID_NUM = "1514103176831545344" # roo troop recent tweet
ID_NUM = "1503175613149970433" # older tweet (from pi day = 14th march)
ID_NUM = "1484347788632592388" # even older tweet from 22nd Jan 2022
FNAME = "quote_tweets_of_" + ID_NUM + ".txt"

url = "https://api.twitter.com/2/tweets/" + ID_NUM + "/quote_tweets?user.fields=username&expansions=author_id"

os.system("curl --request GET --url '" + url + "' --header 'Authorization: Bearer " + TW_BT + "' > " + FNAME)

print("SUCCESS")
## end get_retweets
