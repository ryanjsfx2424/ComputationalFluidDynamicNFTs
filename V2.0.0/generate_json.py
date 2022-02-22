## generate_json.py by Ryan Farber 2022-02-19
"""
To start, I'll just change the name, image, and colormap values.
"""
CID = 'QmQkbk2G1WmHV3DLWQHzbW4uc3iXNNtqh3uQc5p64q6W21/'

import os
import glob
import string
import random
import numpy as np

os.chdir("movies")
fs = glob.glob("*.mp4")

inds = np.arange(0,len(fs))
np.random.shuffle(inds)

def random_file_name(size=32):
  return ''.join(random.SystemRandom().choice(string.ascii_uppercase 
         + string.digits) for ii in range(size))
# end def

base = "OrszagTang_hlld_256_1pt6_"
ext  = ".mp4"
img_base = '  "image": "ipfs://'
img_base_cid = '  "image": "ipfs://' + CID
line_end = '",\n'
cmap_line_end = '"}],\n'
cmap_str = '"Colormap", "value": "'

os.chdir("../metadata")
for ii in range(len(fs)):
  print("ii: ", ii)
  fn = fs[inds[ii]]
  cmap = fn.split(base)[1].split(ext)[0]

  with open(str(ii) + ".json", "w") as fid_write:
    with open("template.json", "r") as fid_read:
      for line in fid_read:
        if   '"name":' in line:
          line = '  "name":"#' + str(ii) + " " + cmap + line_end
        elif img_base in line:
          rfn = random_file_name()
          line = img_base_cid + rfn + line_end

          old = "../movies/" + base + cmap + ext
          new = " ../movies_for_pinata/" + str(ii).zfill(2) + "_" + rfn + ".mp4"

          os.system("mkdir -p ../movies_for_pinata")
          os.system("cp " + old + new)
        elif '"attributes":' in line:
          line = line.split(cmap_str)[0] + cmap_str + cmap + cmap_line_end
        # end if
        fid_write.write(line)
      # end for line
    # end with open read
  # end with open write
# end ii
## end generate_json.py
