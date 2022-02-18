## automater.py
import os

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V1.0.1/"
RUN_PATH = HOME + "RUNS/"
os.system("mkdir -p " + RUN_PATH)

ATHENA_PATH = HOME + "athena/"
INPUT_PATH  = ATHENA_PATH + "inputs/mhd/athinput.orszag-tang"

solvers = ["hlld",
           "hllc",
           "hlle",
           "roe"]

## first step, compile
'''
for solver in solvers:
  os.system("mkdir -p " + RUN_PATH + solver)

  os.chdir(ATHENA_PATH)
  os.system("python configure.py --prob orszag_tang -b -hdf5 --flux " + solver)
  os.system("make clean")
  os.system("make -j 4")

  os.system("cp bin/athena " + RUN_PATH + solver)
  os.system("cp " + INPUT_PATH + " " + RUN_PATH + solver)
# end for solvers
'''
## second, do simulations
cfls = [0.4, 0.8, 1.2, 1.6]

## end automater.py
