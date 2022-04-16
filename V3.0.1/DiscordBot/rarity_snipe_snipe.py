# rarity_snipe_snipe 2022-03-31
"""
Note, it took 25 minutes to do requests.get using the http ipfs gateway.
Using 'ipfs get' on command line took about 4 minutes for holy heroes I
think but is probably taking >> 30m for Holy Villains...

So possibly I should use a driver script and try both methods so
if ipfs happens to be faster great, if the http get goes faster, great.

Although I don't think 25 minutes for a worst case scenario is good
enough...

For now, just using the data that I saved locally to fine-tune
holy heros to match rarity sniper hopefully.
"""

import os, os.path
import ast
import json
import time; start = time.time()
import requests
import numpy as np
from web3 import Web3

UPDATE_DATA = False
UPDATE_RARE = True
NAME = "holh"

URI_NAMES = ["uri", "uri_name"]

COLLECTIONS = {
               "holh": {"os_url": "holyheroes",
                        "contract_address":
                        "0x07511e88628F990d0aDA3c446Da3859833A0798F",
                        "uri_name":"uri"},
               "holv": {"os_url": "holyvillainsnft",
                        "contract_address":
                        "0x581416181453cDb892451db4ACd476D95Fc9fe66"},
               "llam": {"os_url": "llamaverse-genesis",
                        "contract_address":
                        "0x9df8Aa7C681f33E442A0d57B838555da863504f3"},
               "wowg": {"os_url": "world-of-women-galaxy",
                        "contract_address": 
                        "0xf61F24c2d93bF2dE187546B14425BF631F28d6dC",
                        "uri_name":"tokenURI"}
              }
rare_fname = "./RARITY_DATA/rarities_" + NAME + ".txt"

if UPDATE_RARE or (not os.path.isfile(rare_fname)):
  OS_BASE = "https://api.opensea.io/api/v1/collection/"

  abi_path = "ABIs/abi_" + NAME + ".json"
  data_fname = "./OS_COLLECTION_DATA/data_" + NAME + ".txt"
  url = OS_BASE + COLLECTIONS[NAME]["os_url"]


  ## I'll use infura to get the base uri, and for wow-g at least it's easy :)
  INFURA_API_KEY = os.environ["INFURA_API_KEY"]
  INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY

  w3 = Web3(Web3.HTTPProvider(INFURA_URL))

  with open(abi_path, "r") as fid:
    rl = "".join(fid.readlines())
    abi = json.loads(rl)
  # end with open

  ## goal is to update token URI based on how many are held
  ## by that owner (but deployer doesn't count!)
  contract = w3.eth.contract(address=COLLECTIONS[NAME]["contract_address"], 
                            abi=abi)

  totalSupply = contract.functions.totalSupply().call()
  rarities = np.ones(totalSupply)

  headers = {"Accept": "application/json"}
  if UPDATE_DATA or (not os.path.isfile(data_fname)):
    response = requests.request("GET", url, headers=headers)
    np.savetxt(data_fname, [response.text], fmt="%s")
  # end if

  data = np.loadtxt(data_fname, dtype=str)

  max_num = 0
  data = "".join(data)

  traits_dict = data.split('traits":')[1]
  traits_dict = traits_dict.split("}},")[0] + "}}"
  traits_dict = ast.literal_eval(traits_dict)

  for trait_type in traits_dict.keys():
    num = 0

    for trait in traits_dict[trait_type].keys():
      num += traits_dict[trait_type][trait]
    # end for

    num *= 1.0
    max_num = max(max_num, num)

    traits_dict[trait_type]["num_with_trait_type"] = num
  # end for
  print("total supply: ", totalSupply)
  print("max_num: ", max_num)

  new_traits_dict = {}
  for trait_type in traits_dict.keys():
    new_traits_dict[trait_type] = {}

    for trait in traits_dict[trait_type].keys():
      new_traits_dict[trait_type][trait + "_pct"] = \
          traits_dict[trait_type][trait] / totalSupply #max_num
    # end for
  #end for

  uriMethod = getattr(contract.functions, COLLECTIONS[NAME]["uri_name"])
  tokenURI = uriMethod(10).call()
  baseURI = tokenURI[:tokenURI.rfind("/")]

  cid = baseURI.split("/ipfs/")[1]

  #totalSupply = 10
  for tokenNum in range(totalSupply):
    print("tokenNum: ", tokenNum)

    if NAME == "holh":
      tokenURI = baseURI + "/" + hex(tokenNum)[2:].zfill(64)
    # end if

    if not os.path.isdir(cid):
      response = requests.get(tokenURI)
      token = ast.literal_eval(response.text)
    else:
      tokenURI = cid + "/" + hex(tokenNum)[2:].zfill(64)
      with open(tokenURI) as json_file:
        token = json.load(json_file)
      #end with
    # end if/else

    rarity = 1.0
    attributes = token["attributes"]
    for attribute in attributes:
      att = attribute["trait_type"].replace(" ", "")
      av  = attribute["value"].lower().replace(" ", "")

      rarity *= new_traits_dict[att][av + "_pct"]
    # end for
    rarities[tokenNum] = rarity
  # end for
  #np.savetxt(rare_fname, [rarities])
# end if
#rarities = np.loadtxt(rare_fname)

ind = np.argmin(rarities)
print("most rare: ", ind)
print("its rarity: ", rarities[ind])

print("execution rate: ", time.time() - start)
print("SUCCESS rarity_snipe_snipe")
