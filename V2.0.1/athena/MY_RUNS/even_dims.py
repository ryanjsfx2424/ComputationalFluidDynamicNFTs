import os
import glob

plotdirs = glob.glob("Plots_*")
for plotdir in plotdirs:
  os.chdir(plotdir)
  os.system("cp ../make_even_dims.bash .")
  os.system("bash make_even_dims.bash")
  os.chdir("..")
