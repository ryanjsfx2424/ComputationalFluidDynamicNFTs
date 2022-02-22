## update_json.py by Ryan Farber 2022-02-19
"""
This just updates the cid for the 'image'
"""
CID = 'QmeyyYPc5fC9xLpsBhAYV8FDoHs1mNa51YzSVLtSb3bsui/'

import os
import glob
import string
import random
import numpy as np

os.chdir("movies")
fs = np.sort(glob.glob("*.mp4"))

img_base = '  "image": "ipfs://'
img_base_cid = '  "image": "ipfs://' + CID
line_end = '",\n'

os.chdir("../metadata")
with open("_metadata.json", "w") as fid_write_global:
  fid_write_global.write("[\n")

  for ii in range(len(fs)):
    print("ii: ", ii)
    fn = fs[ii]

    num = fn.split(".mp4")[0]
    os.system("cp " + str(num) + ".json " + str(num) + ".json_copy")

    with open(str(num) + ".json", "w") as fid_write:
      with open(str(num) + ".json_copy", "r") as fid_read:
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
    os.system("rm " + str(num) + ".json_copy")
  # end ii
  fid_write_global.write("]")
# end with open global
## end update_json.py
