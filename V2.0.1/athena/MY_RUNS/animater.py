import os
import sys
import glob
import numpy as np
FRAMERATE = 7

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V2.0.1/athena/MY_RUNS/"
MOVIEDIR = HOME + "movies/"
os.system("mkdir -p " + MOVIEDIR)

plotdirs = glob.glob("Plots_*")

for plotdir in plotdirs:
  os.system("mkdir -p temp")
  os.system("cp " + plotdir + "/*.png temp/")
  os.chdir("temp")

  fs = np.sort(glob.glob("*.png"))
  for ii,fn in enumerate(fs):
    os.system("mv " + fn + " " + fn[:-9] + str(ii).zfill(5) + ".png")
  # end for
  os.system("cp ../make_even_dims.bash .")
  os.system("bash make_even_dims.bash")
  os.chdir(HOME)


  input_name  = HOME + "temp/" + fn[:-9] + "%05d.png"
  output_name = MOVIEDIR + fn[:-10] + ".mp4"

  os.system("ffmpeg -y -framerate " + str(FRAMERATE) + " -i " + input_name 
          + " -pix_fmt yuv420p " + output_name)
  os.system("rm -r temp")
## end animater.py
