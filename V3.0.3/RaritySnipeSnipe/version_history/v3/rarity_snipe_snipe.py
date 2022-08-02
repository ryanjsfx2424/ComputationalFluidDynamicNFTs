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
import glob
import json
import time; start = time.time()
import asyncio
import aiohttp
import numpy as np
from web3 import Web3

class RaritySnipeSnipe(object):
  def __init__(self, collection_name):
    self.NAME = collection_name
    self.data_fname = "./OS_COLLECTION_DATA/data_" + self.NAME + ".txt"
    self.rare_fname = "./RARITY_DATA/rarities_"    + self.NAME + ".txt"

    self.COLLECTIONS = {
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
                        "uri_name":"tokenURI"},
               "root": {"os_url": "roo-troop",
                        "contract_address": 
                        "0x928f072C009727FbAd81bBF3aAa885f9fEa65fcf",
                        "uri_name":"tokenURI"}
                        }
    self.metadir = "METADATA"
    self.make_dirs()
    self.init_w3()
  # end rarity_snipe_snipe

  def make_dirs(self):
    os.system("mkdir -p ABIs")
    os.system("mkdir -p " + self.metadir)
    os.system("mkdir -p RARITY_DATA")
    os.system("mkdir -p OS_COLLECTION_DATA")
  # end make_dirs

  def load_abi(self):
    abi_path = "ABIs/abi_" + self.NAME + ".json"
    with open(abi_path, "r") as fid:
      rl = "".join(fid.readlines())
      self.abi = json.loads(rl)
    # end with open
  # end load_abi

  def init_w3(self):
    self.load_abi()
    ## I'll use infura to get the base uri, and for wow-g at least it's easy :)
    INFURA_API_KEY = os.environ["INFURA_API_KEY"]
    INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    self.contract = w3.eth.contract(address=self.COLLECTIONS[self.NAME]["contract_address"], 
                              abi=self.abi)
    self.totalSupply = self.contract.functions.totalSupply().call()
    
    uriMethod = getattr(self.contract.functions, self.COLLECTIONS[self.NAME]["uri_name"])
    tokenURI = uriMethod(10).call()
    self.baseURI = tokenURI[:tokenURI.rfind("/")]

    self.cid = self.baseURI.split("/ipfs/")[1]
  # end init_w3

  def get_os_data(self):
    OS_BASE = "https://api.opensea.io/api/v1/collection/"
    url = OS_BASE + self.COLLECTIONS[self.NAME]["os_url"]

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    np.savetxt(self.data_fname, [response.text], fmt="%s")
  # end get_os_data

  def get_tasks(self, session):
    tasks = []
    for tokenNum in range(1, self.totalSupply+1):
      print("tokenNum: ", tokenNum)
      if self.NAME == "holh":
        tokenURI = self.baseURI + "/" + hex(tokenNum)[2:].zfill(64)
      else:
        tokenURI = self.baseURI + "/" + str(tokenNum)
      # end if
      print("tokenURI: ", tokenURI)
      tasks.append(asyncio.create_task(session.get(tokenURI, ssl=False)))
    # end for
    return tasks
  # end get_tasks

  async def get_metadata(self):
    os.chdir(self.metadir)
    os.system("mkdir -p " + self.cid)
    os.chdir(self.cid)

    async with aiohttp.ClientSession() as session:
      tasks = self.get_tasks(session)
      responses = await asyncio.gather(*tasks)
      print("responses0: ", responses[0])
      for ii in range(len(responses)):
        with open(str(ii+1), "w") as fid:
          fid.write(await responses[ii].text())
        # end with
      # end for
    os.chdir("../..")
  # end get_metadata

  def get_traits(self):
    data = np.loadtxt(self.data_fname, dtype=str)

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
    print("total supply: ", self.totalSupply)
    print("max_num: ", max_num)

    new_traits_dict = {}
    for trait_type in traits_dict.keys():
      new_traits_dict[trait_type] = {}

      for trait in traits_dict[trait_type].keys():
        new_traits_dict[trait_type][trait + "_pct"] = \
            traits_dict[trait_type][trait] / self.totalSupply #max_num
      # end for
    #end for
    self.traits_dict = new_traits_dict
    print(self.traits_dict)
  # end get_traits

  def get_rarity(self):
    os.chdir(self.metadir)
    os.chdir(self.cid)
    fs = np.sort(glob.glob("*"))
    rarities = np.ones(self.totalSupply)
    for tokenNum, fn in enumerate(fs):
      with open(fn, "r") as fid:
        token = json.load(fid)
      #end with

      rarity = 1.0
      attributes = token["attributes"]
      for attribute in attributes:
        att = attribute["trait_type"].replace(" ", "")
        av  = attribute["value"].lower().replace(" ", "")

        rarity *= self.traits_dict[att][av + "_pct"]
      # end for
      rarities[tokenNum] = rarity
    # end for
    os.chdir("../..")
    np.savetxt(self.rare_fname, [rarities])
    ind = np.argmin(rarities)
    print("most rare: ", ind)
    print("its rarity: ", rarities[ind])
  # end get_rarity

  def get_rarity_tools(self):


  def print_rarities(self):
    rarities = np.loadtxt(self.rare_fname)
    inds = np.argsort(rarities)
    rarities = rarities[inds]
    print("r0: ",  rarities[ 0])
    print("r-1: ", rarities[-1])
    print("i0: ", inds[0])
    print("i-1: ", inds[-1])
    print("i top 20: ", inds[:20])
  # end print_rarities
# end def class

if __name__ == "__main__":
  rss = RaritySnipeSnipe("root")
  #rss.get_os_data()
  #asyncio.run(rss.get_metadata())
  #rss.get_traits()
  #rss.get_rarity()
  rss.print_rarities()
# end if __name___

print("execution rate: ", time.time() - start)
print("SUCCESS rarity_snipe_snipe")
