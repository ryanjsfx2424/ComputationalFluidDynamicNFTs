## note, almost 4 minutes to plot every 6th file (100 total) for 32x64.
## note, ~2.5 minutes to plot every 9th file for 64x128.
## note, 128x256 took about 3 minutes to run for tlim=8.5 so it'd take
## about 24 minutes to go to tlim 69
## v2 will loop over runs & colormaps.
import os
import sys
import glob

import time; start = time.time()
import numpy as np
import yt; yt.enable_parallelism()
from yt.funcs import mylog; mylog.setLevel(50)

AXIS = "z"
FIELD = "density"

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
         "GRN-RED-BLU-WHT",
         "CMRmap",
         "16 LEVEL",
         "Pastel1",
         "Pastel2",
         "Peppermint",
         "Plasma",
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
         "gist_yarg",
         "gist_ncar",
         "gist_heat",
         "gist_earth",
         "dusk",
         "cubehelix",
         "copper",
         "prism",
         "cool",
         "bwr",
         "brg",
         "afmhot",
         "Wistia",
         "STERN SPECIAL",
         "STD GAMMA-II",
         "Rainbow18",
         "Rainbow",
         "RED TEMPERATURE",
         "Purple-Red + Stripes",
         "Pastels",
         "Paired",
         "PRISM",
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
         "Blues",
         "algae",
         "rainbow",
         "octarine",
         "magma",
         "nipy_spectral",
         "kelp",
         "kamae",
         "RdBu"
        ]
print("len CMAPS: ", len(CMAPS))

#RUNDIRS = ["hllc512x1024"]*len(CMAPS)

RUNDIRS  = list(np.sort(glob.glob("hll*")))
RUNDIRS += list(np.sort(glob.glob("llf*")))
RUNDIRS += list(np.sort(glob.glob("roe*")))
print("len RUNDIRS: ", len(RUNDIRS))

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V2.0.1/athena/MY_RUNS/"

OUTPUT_FREQ = len(RUNDIRS)*[3]
for rr,rundir in enumerate(RUNDIRS):
  CMAP = CMAPS[rr]
  freq = OUTPUT_FREQ[rr]

  run_path  = HOME + rundir
  plot_path = HOME + "Plots_" + rundir
  if CMAP != "RdBu":
    plot_path += "_" + CMAP.replace(" ","_")
  # end if

  if CMAP in ["autumn", "dusk", "GRN-RED-BLU-WHT", "Reds",
              "spring", "winter", "summer"]:
    continue
  # end if

  os.chdir(HOME + rundir)
  fs = np.sort(glob.glob("*.athdf"))
  fs = fs[::freq]
  os.system("mkdir -p " + plot_path)

  fs_plots = np.sort(glob.glob(plot_path + "/*.png"))

  for fn in yt.parallel_objects(fs):
    num = fn.split(".")[2]
    if CMAP != "RdBu":
      save_name = plot_path + "/" + FIELD + "_" + AXIS + "_" + CMAP.replace(" ","_") + "_" + num + ".png"
    else:
      save_name = plot_path + "/" + FIELD + "_" + AXIS + "_" + num + ".png"
    # end if/else

    if save_name in fs_plots:
      continue
    # end if
    print("fn: ", fn)

    ds = yt.load(fn)
    slc = yt.SlicePlot(ds, axis=AXIS, fields=FIELD)
    slc.set_cmap(field=FIELD, cmap=CMAP)
    slc.hide_colorbar()
    slc.hide_axes()

    os.chdir(plot_path)
    slc.save(save_name)
    os.chdir(run_path)
  # end for fs
# end for RUNDIRS
print("execution rate: ", time.time() - start)
print("SUCCESS the_plotter.py")
## end the_plotter.py
