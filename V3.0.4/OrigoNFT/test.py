import os

## worked!
cmd = 'curl --header "X-API-KEY: ' + os.environ["rtOS"] + \
      '" --request GET -i --url ' + "'https://api.opensea.io/api/v1/assets'"

#print("cmd: ", cmd)
#os.system(cmd)

import requests

url = "https://api.opensea.io/api/v1/collection/doodles-official"

response = requests.get(url)

print(response.text)
