import os
import sys
import glob
import numpy as np
from the_fluid import The_Fluid
import os; cur_path = os.getcwd()
if sys.version_info.major == 3:
  import _pickle as cPickle
else:
  import cPickle
# end if/else
my_fluid = cPickle.load(open("my_fluid.p", "rb"))

os.chdir(my_fluid.PLOT_DIR)

fs = np.sort(glob.glob("hat_*.png"))
cnt = 0
for ii,fn in enumerate(fs):
  print(fn)
  new_fn = fn.split("_")
  new_fn[-1] = str(cnt).zfill(9) + ".png"
  new_fn = "_".join(new_fn)
  os.system("mv " + fn + " " + new_fn)
  cnt += 1
# end for ii
