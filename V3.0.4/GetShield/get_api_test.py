import os

url = "http://35.85.50.164:3000/api/v1/analysis"
command  = "curl -X POST '" + url + "' -H 'Content-Type: application/json'"
command += " -d '{\"address\": [\"0x3ac26f27595EffeB5e426BD093081EC30eBdD545\""
command += ", \"0xd4A02ad632a73480E53F5182EFD144FbEcC3D943\", "
command += "\"0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae\"]}'"

os.system(command)
