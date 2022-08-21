## make_metadata.py
"""
Uses metadata.json as a template. Just gives a unique name for each token.
"""
import os
os.chdir("data_big/metadata")

with open("template.json", "r") as fid:
  lines = fid.readlines()
# end with open

for ii in range(3000):
  with open(str(ii) + ".json", "w") as fid:
    for line in lines:
      if "name" in line:
        p1,p2 = line.split(":")
        p2 = ' "#' + str(ii) + '",\n'
        line = ":".join([p1,p2])
      # end if

      if "description" in line:
        line = line.replace("RC3", "RC8T")
      # end if
      fid.write(line)
    # end for
  # end with open
# end for ii
