import os
import requests

base = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/"
url = base + "Day 5 Gratitude".replace(" ","%20")

headers = {"Content-Type":"application/json", 
           "Authorization":"Bearer " + os.environ["airTable"]}

body = {
        "id": "a",
        "fields": {
          "TimeEst": "2022-09-17 12:00 PM",
          "Attachments": [],
          "ButtonText": "Day 5 Gratitude",
          "Discord Message": "foo",
          "Prompt1": "What I shared",
          "Prompt2": "What for fun"
          }
        }

data = {
  "records": [
    {
     "fields": {
          "TimeEST": "2022-09-17 12:00 PM",
          "Attachments": [],
          "ButtonText": "Day 5 Gratitude",
          "Discord Message": "foo",
          "Prompt1": "What I shared",
          "Prompt2": "What for fun",
          "FromDiscordID": "foobar"
          }
    }
  ]
}

r = requests.post(url, headers=headers, json=data)
print(r.status_code)
