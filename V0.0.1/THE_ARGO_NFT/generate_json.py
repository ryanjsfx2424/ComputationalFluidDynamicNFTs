## generate_json.py by Ryan Farber
"""
This will create a json file for each movie and also a _metadata.json
file that stitches them together. Basing it off Hashlips art engine.
"""
import os
import glob
import time
from hashlib import sha1
HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V0.0.1/"

os.chdir(HOME + "/THE_ARGO_NFT/movies")
movies = glob.glob("*.mp4")

NUM = len(movies)
cfl_nums = []
solvers = []
cmaps = []
stable = []

for movie in movies:
  cmap, sim = movie.split("_")

  solver,cfl = sim.split("CFL")

  cmaps.append(cmap)
  solvers.append(solver)
  cfl_nums.append(cfl[:-4].replace("pt","."))

  if solver == "explicit" and float(cfl_nums[-1]) > 0.27:
    stable.append("False")
  else:
    stable.append("True")
# end for movies

changes = {
           "name" : ["ComputationalFluidDynamicsV0 #" + str(ii) for ii in range(NUM)],

           "description" : NUM*["This is the first version of a series of Computational Fluid Dynamics collections. In this version, we utilize THE_ARGO, which is a finite-difference, magnetohydrodynamics python code I wrote for my undergraduate honors thesis. THE_ARGO was intended as a learning tool; you can learn more by reading 'Magnetohydrodynamical modeling in Python: simulating magnetic fluids.'\\n\\nIn this version, we demonstrate how varying the Courant-Friedrichs-Lewy (CFL) number impacts the solution when using explicit vs. implicit solvers for the nonlinear advection of a top hat function with periodic boundary conditions. While an explicit solver exhibits numerical instability for CFL greater than unity, it exhibits the least dissipation for unity CFL. Meanwhile, the implicit solver remains stable even if the CFL constraint is violated, yet solutions are more dissipative.\\n\\nSimulations were performed on a 2013 MacBook Pro (2 GHz Quad-Core Intel Core i7; 8 GB 1600 MHz DDR3).\\n\\nv0.0.1 features " + str(NUM) + " unique NFTs."],

           "image" : ["ipfs://QmVfWbJvZmeNB4EGjqDrrXQmnW7Li4gwma5vUevG1LdQG3/" + str(ii) + ".mp4" for ii in range(NUM)],

           "dna" : ["" + sha1(str(ii).encode('utf-8')).hexdigest() for ii in range(NUM)],
           "edition" : [ii for ii in range(NUM)],

           "date" : [int(time.time()*10000)+ii for ii in range(NUM)],

           "compiler" : NUM*["THE_ARGO_NFT Engine"],

           "attributes" : [[
            {
             'trait_type': 'Stable',
             'value': stable[ii]
            },
            {
             'trait_type': 'CFL',
             'value': cfl_nums[ii]
            },
            {
             'trait_type': 'Solver',
             'value': solvers[ii]
            },
            {
             'trait_type': 'Colormap',
             'value': cmaps[ii]
            }
            ] for ii in range(NUM)]
          }
# end changes dictionary

os.system("mkdir -p " + HOME + "/json")
os.chdir(HOME + "json")
with open("_metadata.json", "w") as fid_write_global:
  fid_write_global.write("[\n")

  for ii,movie in enumerate(movies):
    print("movie: ", movie)
    cmap = movie[:-4]
    with open(HOME + "/json/template.json", "r") as fid_read:
      with open(str(ii) + ".json", "w") as fid_write_local:
        for line in fid_read:
          for key in changes.keys():
            if key in line:
              line = line.split(":")[0]
              if type(changes[key][ii]) == type("str"):
                line += ': "' + str(changes[key][ii]) + '",\n'
              else:
                line += ': ' + str(changes[key][ii]) + ',\n'
              # end if/else

              if "attributes" in line:
                new_line = ""
                for char in line:
                  if char == "'":
                    char = '"'
                  # end if
                  new_line += char
                line = new_line
              # end if

              if key == "compiler":
                line = line[:-2] + "\n"
              # end if
            # end if
          # end for
          fid_write_local.write(line)
          if ii < NUM-1 and line.split()[0] == "}":
            line = line[:-1] + ",\n"
          # end if
          fid_write_global.write(4*" " + line)
        # end for
      # end with
    # end with
    name_old = HOME + "movies/" + movie
    name_new = HOME + "movies/" + str(ii) + ".mp4"
    print("name_old: ", name_old)
    print("name_new: ", name_new)
    os.system("mv " + name_old + " " + name_new)
  # end for
  fid_write_global.write("]")
# end with
## end generate_json.py
