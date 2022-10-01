import os
import glob
import numpy as np

os.system("mkdir -p data_big/metadata_OrigoGenesisFinal")
fs = np.sort(glob.glob("data_big/metadata/*.json"))

description = "Origo is a unique collection of 3,000 characters redefining digital art. The art-based project explores an opportunity to dive deeper into what makes us unique. Intending to create the first full 1/1 collection, we have honed in on characteristics and features that match various personalities."

old_cid = "ipfs://bafybeibsfhktut3cuc56j2mauhivcc2q6v2kiephlne5ry3ur7a4zkn5re"
new_cid = "ipfs://bafybeib7ctov4f23eraa2ujvcntf4ww6vy3apgwfiynqrgprrhcolkx3ke"

for ii in range(len(fs)):
  with open("data_big/metadata/" + str(ii) + ".json", "r") as fid:
    lines = fid.readlines()
  # end with

  lines[1] = lines[1].split("#")[0] + "Origo Genesis #" + str(ii) + '",\n'

  lines[2] = lines[2].replace(old_cid, new_cid)

  lines[3] = lines[3].split("RC8T")[0] + description + '"\n'

  with open("data_big/metadata_OrigoGenesisFinal/" + str(ii) + ".json", "w") as fid:
    for line in lines:
      fid.write(line)
    # end for
  # end with
# end for
