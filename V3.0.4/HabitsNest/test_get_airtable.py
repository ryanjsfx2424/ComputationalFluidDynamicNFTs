import os
import json
import requests
import shutil

'''
url = "https://api.airtable.com/v0/appPp5AF5PoGQk7ls/Table%201"
headers = {"Content-Type":"json", "Authorization":"Bearer " + os.environ["airTable"]}
req = requests.get(url, headers=headers)
print("req: ", req)
print("req.status_code: ", req.status_code)
print("req.text: ", req.text)
print("req.json(): ", req.json())
result = req.json()

with open("test.json", "w") as fid:
  json.dump(result, fid)
# end with
print("good")
sys.exit()
'''
with open("test.json", "r") as fid:
  result = json.load(fid)
# end with

'''
print("result len records: ", len(result["records"]))
print("result records -1.keys: ", result["records"][-1].keys())
print("result records -1 fields: ", result["records"][-1]["fields"].keys())
print("result records -1 fields Attachments: ", result["records"][-1]["fields"]["Attachments"])
print("result records -1 fields Attachments len: ", len(result["records"][-1]["fields"]["Attachments"]))
print("result records -1 fields Attachments -1 keys: ", result["records"][-1]["fields"]["Attachments"][-1].keys())
print("result records -1 fields Attachments -1 url: ", result["records"][-1]["fields"]["Attachments"][-1]["url"])

image_url = result["records"][-1]["fields"]["Attachments"][-1]["url"]
image_name = image_url.split("/")[-1]
'''

records = result["records"]
print("len records: ", len(records))
for ii in range(len(records)):
  print(records[ii]["fields"])
  input(">>")
# end for ii
record = records[0]
fields = record["fields"]
print("TimeToSendEST: ", fields["TimeToSendEST"])
print("Attach -1 url: ", fields["Attachments"][-1]["url"])
print("ButtonText: ", fields["ButtonText"])
print("Discord Message: ", fields["Discord Message"])

num_prompts = 0
prompts = []
for field in fields:
  if "Prompt" in field:
    num_prompts += 1
    prompts.append("")
  # end if
# end for

for field in fields:
  if "Prompt" in field:
    ind = int(field.replace("Prompt",""))-1
    prompts[ind] = fields[field]
  # end if
# end for
  
print("prompts: ", prompts)

'''
r = requests.get(image_url, stream=True)
print("r.status_code: ", r.status_code)
r.raw.decode_content = True

with open(image_name, "wb") as fid:
  shutil.copyfileobj(r.raw, fid)
# end with
print("Image downloaded!")
'''
