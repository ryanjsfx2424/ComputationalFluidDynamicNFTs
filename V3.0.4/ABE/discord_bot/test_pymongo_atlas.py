import os
import urllib
from pymongo import MongoClient


user = urllib.parse.quote("pymongo-user")
word = os.environ["atlP1"] + os.environ["atlP2"] + "5!#!%"
word = urllib.parse.quote(os.environ["atlP"])

connection_string = "mongodb+srv://" + user + ":" + word \
                  + "@cluster0.pqg6c02.mongodb.net/" \
                  + "?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db = client.get_database("abe")
#collection = db["abe-guild-channels"]
collection = db["abe-guilds-data"]
print("collection: ", collection)

cursor = collection.find({})
print("cursor: ", cursor)

trial_map = {
                            "952352992626114622": 1e50, # ABE
                            "922678240798187550": 5, # sketches by gabo
                            "999414546496229498": 1e50, # Test
                            "984574397870399528": 30*24*3600, # momentum
                            "967786268077461604": 18*24*3600, # beyond-alpha
                            "978987192573657089": 14*24*3600,
                            "889254570906239028": 16*24*3600 # origins
                        }

for document in cursor:
  print(document)
  print(document.keys())
  print("\n\n")
  print("guild name: ", document["guild_name"])
  print("subscription date: ", document["date"])
  if "subscribed_role_feed_map" in document:
    print("document[srfm]: ", document["subscribed_role_feed_map"])
  else:
    print("\n\nnope roles")
  if "subscribed_channel_feed_map" in document:
    print("document[scfm]: ", document["subscribed_channel_feed_map"])
  else:
    print("\n\nnope channels")
  if document["guild_id"] in trial_map:
    print("yup in trial map")
  else:
    print("not in trial map")
  print("\n\n")
  input(">>")
'''
collection.find_one_and_update({"guild_id": "931482273440751638"}, 
{"$set": {"testfield":"foobar"}})

cursor = collection.find({})
print("cursor: ", cursor)

for document in cursor:
  print(document)
'''

#print(collection.count_documents({}))
#print("collection.find({}): ", collection.find({}))
#collection.delete_many({})
#print(collection.count_documents({}))

new_guild_data = {
  "guild_id": 124,
  "guild_channels":{
    "announcements": 124,
    "general": 125,
    "bots":126},
  "subscribed":False}
#collection.insert_one(new_guild_data)

'''
new_guild_channels = {
  "guild_id":123,
  "guild_channels":{
    "announcements":124,
    "general":125,
    "bots":126}
}
collection.insert_one(new_guild_channels)
'''

