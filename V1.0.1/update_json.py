## update_json.py by Ryan Farber 2022-02-19
"""
This just updates the cid for the 'image'
"""
CID = 'QmU5zjeBCPozW8Kb4ZmW7zZmhDCypf6HZvdEdpY7BUUd9y/'

import os
import glob
import string
import random
import numpy as np

os.chdir("movies_for_pinata")
fs = glob.glob("*.mp4")

base = "OrszagTang_hlld_256_1pt6_"
ext  = ".mp4"
img_base = '  "image": "ipfs://'
img_base_cid = '  "image": "ipfs://' + CID
line_end = '",\n'

os.chdir("../metadata")
for ii in range(len(fs)):
  print("ii: ", ii)
  fn = fs[ii]

  with open("_metadata.json", "w") as fid_write_global:
    fid_write_global.write("[\n")
    os.system("cp " + str(ii) + ".json " + str(ii) + ".json_copy")

    with open(str(ii) + ".json", "w") as fid_write:
      with open(str(ii) + ".json_copy", "r") as fid_read:
        for line in fid_read:
          if img_base in line:
            line = img_base_cid + fn + line_end
          # end if
          fid_write.write(line)

          if ii < len(fs)-1 and line.split()[0] == "}":
            line = line[:-1] + ",\n"
          # end if
          fid_write_global.write(4*" " + line)
        # end for line
      # end with open read
    # end with open write
    fid_write_global.write("]")
    os.system("rm " + str(ii) + ".json_copy")
  # end with open global
# end ii
## end update_json.py
