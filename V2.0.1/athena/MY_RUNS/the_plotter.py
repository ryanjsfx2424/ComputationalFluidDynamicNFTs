## note, almost 4 minutes to plot every 6th file (100 total) for 32x64.
## note, ~2.5 minutes to plot every 9th file for 64x128.
## note, 128x256 took about 3 minutes to run for tlim=8.5 so it'd take
## about 24 minutes to go to tlim 69
import os
import sys
import glob

import time; start = time.time()
import numpy as np
import yt; yt.enable_parallelism()
from yt.funcs import mylog; mylog.setLevel(50)

RUNDIRS = ["hllc69x138_tlim69_gamma1pt69_drat1pt69_grav0pt069_period6pt9"]
#RUNDIRS = ["hllc64x128_tlim69_p0pt5"]
#RUNDIRS = ["hllc512x1024"]
AXIS = "z"
FIELD = "density"
CMAP = "RdBu"
#CMAP = "Accent"

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V2.0.1/athena/MY_RUNS/"

for rundir in RUNDIRS:
  run_path  = HOME + rundir
  plot_path = HOME + "Plots_" + rundir
  if CMAP != "RdBu":
    plot_path += "_" + CMAP
  # end if

  os.chdir(HOME + rundir)
  fs = np.sort(glob.glob("*.athdf"))
  fs = fs[::9]
  #fs = fs[::int(len(fs)/3)]
  os.system("mkdir -p " + plot_path)

  fs_plots = np.sort(glob.glob(plot_path + "/*.png"))

  for fn in yt.parallel_objects(fs):
    num = fn.split(".")[2]
    if CMAP != "RdBu":
      save_name = plot_path + "/" + FIELD + "_" + AXIS + "_" + CMAP + "_" + num + ".png"
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
# end for
print("execution rate: ", time.time() - start)
print("SUCCESS the_plotter.py")
## end the_plotter.py
