import os
import requests

first = os.environ["abe1"] + os.environ["abe2"]
url = "https://us-central1-alphaintel.cloudfunctions.net/abe_get_data"
payload =  {"psk": first, "key": "Y"}

#r = requests.post(url, json=payload)

print(r.status_code)
print(r.json())
