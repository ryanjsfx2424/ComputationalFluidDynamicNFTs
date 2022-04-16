import ast
import requests
import numpy as np

CONTRACT_ADDRESSES = {
                      "bayc": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
                     }

# needs api key :*)
url = "https://api.opensea.io/api/v1/account?address=0xd4b7315fE51081f829cA1F6486E97C44BEFb688b"
url = "https://api.opensea.io/api/v1/assets?order_direction=desc&limit=20&include_orders=false"
url = "https://api.opensea.io/api/v1/events"
url = "https://api.opensea.io/api/v1/asset_contract/0x06012c8cf97bead5deae237070f9587f8e7a266d"
url = "https://api.opensea.io/api/v1/asset/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/8520/offers?limit=20"
url = "https://api.opensea.io/api/v1/asset/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/1/?include_orders=false"
url = "https://api.opensea.io/wyvern/v1/orders?bundled=false&include_bundled=false&limit=20&offset=0&order_by=created_date&order_direction=desc"

## No API Key needed!!
url = "https://api.opensea.io/api/v1/collections?offset=0&limit=300"
url = "https://api.opensea.io/api/v1/collections?offset=0&limit=300&asset_owner=0xb32b4350c25141e779d392c1dbe857b62b60b4c9"

url = "https://api.opensea.io/api/v1/bundles?limit=20&offset=0"
url += "&asset_contract_address=" + CONTRACT_ADDRESSES["bayc"]

url = "https://api.opensea.io/api/v1/collection/doodles-official"
url = "https://api.opensea.io/api/v1/collection/world-of-women-galaxy"

## TBD


headers = {"Accept": "application/json"}

#response = requests.request("GET", url, headers=headers)
#print(dir(response))
#print(response.text)
#sys.exit()
#print(response.text)

#np.savetxt("wow-galaxy.txt", [response.text], fmt="%s")

data = np.loadtxt("wow-galaxy.txt", dtype=str)

max_num = 0
data = "".join(data)
traits_dict = data.split('traits":')[1]
traits_dict = traits_dict.split("}},")[0] + "}}"
traits_dict = ast.literal_eval(traits_dict)
for trait_type in traits_dict.keys():
  print("trait_type: ", trait_type)
  print("values trait_type: ", traits_dict[trait_type])
  num = 0
  for trait in traits_dict[trait_type].keys():
    print("trait: ", trait)
    print("value trait: ", traits_dict[trait_type][trait])
    num += traits_dict[trait_type][trait]
  # end for
  num *= 1.0
  max_num = max(max_num, num)
  print("num: ", num)
  print("max_num: ", max_num)
  traits_dict[trait_type]["num_with_trait_type"] = num
  #input(">>")
# end for

new_traits_dict = {}
for trait_type in traits_dict.keys():
  new_traits_dict[trait_type] = {}
  print("tt 2: ", trait_type)
  for trait in traits_dict[trait_type].keys():
    print("t2: ", trait)
    new_traits_dict[trait_type][trait + "_pct"] = traits_dict[trait_type][trait] \
                                            / max_num
    print("td tt pct: ", new_traits_dict[trait_type][trait + "_pct"])
    #input(">>")
  # end for
#end for

## I guess I should next query for the token metadata and check
## how rare each is

## I'll use infura to get the base uri, and for wow-g at least it's easy :)
INFURA_API_KEY = os.environ["INFURA_API_KEY"]
INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

sys.exit()


saved = []
traits = False
for line in data:
  print(line)
  if traits:
    saved.append(line)
    traits = False
  if "traits" in line:
    traits = True
    saved.append(line)
print("\n\n\n")
print(saved)
