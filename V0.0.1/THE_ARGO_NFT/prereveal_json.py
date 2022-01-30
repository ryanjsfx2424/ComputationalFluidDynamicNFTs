## prereveal_json.py by Ryan Farber 2022-01-28
"""
The purpose of this script is to generate+tweak the metadata for the hidden movie.
"""
IPFS_URL = ""
IPFS_URL = "QmTmcBLYVU3tHt31NS5EoyaYxTZQXWVEzHtemxh3rJfjHk"
import os
import glob

TOP  = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V0.0.1/"

os.chdir(TOP)
os.system("mkdir -p hidden_json")
os.system("cp json/0.json hidden_json/temp.json")
os.chdir(TOP + "hidden_json")

with open("hidden.json", "w") as fid_write:
  fid_write.write("{\n")
  with open("temp.json", "r") as fid_read:
    for line in fid_read:
      if "name" in line:
        line = line.split(":")[0]
        line += ': "hidden",\n'
      elif "description" in line:
        line = line.split(":")[0]
        line += ': "This NFT will be revealed 24H after the start mint time :)",\n'
      elif "image" in line:
        line = line.split(":")[0]
        line += ': "ipfs://' + IPFS_URL + '/hidden.mp4"\n'
      else:
        continue
      # end if/elif  
      fid_write.write(line)
    # end for
  # end with open
  fid_write.write("}\n")
# end with open
os.system("rm " + TOP + "hidden_json/temp.json")
## end prereveal_json
