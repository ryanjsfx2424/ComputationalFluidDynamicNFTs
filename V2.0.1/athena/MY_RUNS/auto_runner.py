## auto_runner.py
"""
This script will set up and do a bunch of runs for me.
"""
import os
import sys
import glob
import numpy as np

traits = {"Riemann":    {"llf":0.125, "hlle":0.25, "hllc":1.0},
          "resolution": {"32x64":0.125, "256x512":0.25, "64x128": 1.0},
          "gamma":      {"1.666666": 0.125, "1.333":0.25, "1.4":1.0},
          "drat":       {"2.42": 0.125, "2.69":0.25, "2.0":1.0},
          "grav":       {"0.33": 0.125, "0.25": 0.25, "0.1":1.0},
          "period":     {"4.0": 0.125, "Inf":0.25, "1.0":1.0}}
trait_keys = list(traits.keys())

for ii in range(48):
  name = ""
  choices = np.random.random(len(trait_keys))
  print("choices: ", choices)

  for jj,trait_key in enumerate(trait_keys):
    for kk,trait_key_key in enumerate(traits[trait_key]):
      print("trait_key_key: ", trait_key_key)
      if choices[jj] < traits[trait_key][trait_key_key]:
        if jj > 1:
          name += trait_key
        # end if

        name += trait_key_key
        if jj != 0 and jj != len(trait_keys)-1:
          name += "_"
        # end if

        if jj == 0:
          riemann = name

        break
      # end if
    # end for kk
  # end for jj
  name = name.replace(".", "pt")
  print("name: ", name)

  nx1 = name.split(riemann)[1].split("x")[0]
  nx2 = name.split(riemann)[1].split("x")[1].split("_")[0]
  gamma = name.split("gamma")[1].split("_")[0]
  grav = name.split("grav")[1].split("_")[0]
  drat = name.split("drat")[1].split("_")[0]
  period = name.split("period")[1]

  os.system("mkdir -p " + name)
  os.system("cp " + riemann + "64x128_tlim69/ath* " + name)
  os.chdir(name)

  os.system("cp athinput.rt2d delete_me.txt")
  with open("delete_me.txt", "r") as fid_read:
    with open("athinput.rt2d", "w") as fid_write:
      for line in fid_read:

        if   "nx1" in line:
          line = "nx1 = " + nx1
        elif "nx2" in line:
          line = "nx2 = " + nx2
        elif "tlim" in line:
          line = "tlim = 69"
        elif "gamma" in line:
          line = "gamma = " + gamma
        elif "grav_acc2" in line:
          line = "grav_acc2 = -" + grav
        elif "iprob" in line:
          if period == "Inf":
            line = "iprob = 6.9"
          else:
            line = "iprob = 1"
        elif "drat" in line:
          line = "drat = " + drat.replace("pt", ".") + "\n"
          fid_write.write(line)
          line = "period = " + period
        else:
          line = line[:-1]
        # end ifs
        line = line.replace("pt",".") + "\n"
          
        fid_write.write(line)
      # end for line in fid
    # end with open
  # end with open
  os.system("rm delete_me.txt")
  os.system("./athena -i athinput.rt2d")
  os.chdir("..")
# end for ii
## end auto_runner.py
