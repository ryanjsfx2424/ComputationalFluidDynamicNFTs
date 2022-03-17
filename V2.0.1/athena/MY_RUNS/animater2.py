import os
import sys
import glob
import numpy as np
FRAMERATE = 7

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V2.0.1/athena/MY_RUNS/"
MOVIEDIR = HOME + "moviesSpecial/"
os.system("mkdir -p " + MOVIEDIR)

#plotdirs = glob.glob("Plots_*")
plotdirs = [
            "Plots_hllc64x128_gamma1pt4_drat2pt0_grav0pt1_periodInf_Pastel1"
            #"Plots_hllc64x128_gamma1pt4_drat2pt0_grav0pt1_periodInf_Waves",
            #"Plots_hllc69x138_tlim69_gamma1pt69_drat1pt69_grav0pt069_period6pt9_jet",
            #"Plots_hlle64x128_gamma1pt4_drat2pt0_grav0pt33_periodInf_gist_heat",
            #"Plots_hllc64x128_tlim69_p0pt5_flag",
            #"Plots_hllc64x128_tlim69_iprob69_doom",
            #"Plots_hllc32x64_tlim69_Pastel1"
           ]


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
  output_name = MOVIEDIR + fn[:-10] + "_2.mp4"

  os.system("ffmpeg -y -framerate " + str(FRAMERATE) + " -i " + input_name 
          + " -pix_fmt yuv420p " + output_name)
  os.system("rm -r temp")
## end animater.py
