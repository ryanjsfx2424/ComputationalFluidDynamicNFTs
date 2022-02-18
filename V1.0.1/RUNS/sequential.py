import os
import sys
import glob
import numpy as np

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V1.0.1/athena/MY_RUNS/"

PLOTDIR  = HOME + "Plots_hlld_256_0pt4/"

os.chdir(PLOTDIR)
fs = np.sort(glob.glob("OrszagTang.out2.?????_Slice_z_density.png"))
for ii,fn in enumerate(fs):
  os.system("mv " + fn + " " + str(ii).zfill(5) + ".png")
# end for ii
