import os
import sys
from the_fluid import The_Fluid
import os; cur_path = os.getcwd()
if sys.version_info.major == 3:
  import _pickle as cPickle
else:
  import cPickle
# end if/else
my_fluid = cPickle.load(open("my_fluid.p", "rb"))

FRAMERATE = my_fluid.framerate

os.system("mkdir -p movies")


input_name  = my_fluid.PLOT_DIR + "/hat_periodic_boundaries_cycle_%09d.png"
output_name = "movies/" + my_fluid.cmap.name + "_" + \
             my_fluid.PLOT_DIR.split("_")[1] + ".mp4"
#output_name = "movies/" + my_fluid.cmap.name + ".mp4"

os.system("ffmpeg -y -framerate " + str(FRAMERATE) + " -i " + input_name 
          + " -pix_fmt yuv420p " + output_name)
## end animater.py
