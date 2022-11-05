import os
import urllib
from pymongo import MongoClient


user = urllib.parse.quote("pymongo-user")
word = os.environ["atlP1"] + os.environ["atlP2"] + os.environ["atlP3"]
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

for document in cursor:
  print(document)
  if "subscribed_role_feed_map" in document:
    print("document[srfm]: ", document["subscribed_role_feed_map"])
  else:
    print("\n\nnope roles")
  if "subscribed_chanel_feed_map" in document:
    print("document[scfm]: ", document["subscribed_channel_feed_map"])
  else:
    print("\n\nnope channels")
  print("\n\n")
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

