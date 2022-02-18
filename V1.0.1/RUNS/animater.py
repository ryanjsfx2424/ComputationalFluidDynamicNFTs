import os
import sys
FRAMERATE = 20

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V1.0.1/RUNS/"

PROB = "hlld_256_1pt6"

PLOTDIR  = HOME + "Plots_" + PROB
MOVIEDIR = HOME + "movies/"
os.system("mkdir -p " + MOVIEDIR)

CMAPS = [
         "Blue Waves_r",
         "Accent",
         "B-W LINEAR",
         "B-W LINEAR_r",
         "Dark2",
         "Eos A",
         "Hardcandy",
         "Haze",
         "Hue Sat Value 2",
         "Nature",
         "Ocean",
         "Pastel1",
         "Pastel2",
         "Peppermint",
         "Plasma",
         "RdBu",
         "STEPS",
         "Set3",
         "Volcano",
         "Waves",
         "bone",
         "coolwarm",
         "doom",
         "flag",
         "hsv",
         "jet",
         "prism",
         "Greys",
         "twilight",
         "autumn",
         "inferno",
         "summer",
         "viridis",
         "winter",
         "seismic",
         "ocean",
         "Reds",
         "spring",
         "Blues"
        ]

for cmap in CMAPS:
  cmap_name = cmap.replace(" ","_")
  plotdir_now = PLOTDIR + "_" + cmap_name + "/"

  input_name  = plotdir_now + "%05d.png"
  output_name = MOVIEDIR + "OrszagTang_" + PROB + "_" + cmap_name + ".mp4"

  os.system("ffmpeg -y -framerate " + str(FRAMERATE) + " -i " + input_name 
          + " -pix_fmt yuv420p " + output_name)
## end animater.py
