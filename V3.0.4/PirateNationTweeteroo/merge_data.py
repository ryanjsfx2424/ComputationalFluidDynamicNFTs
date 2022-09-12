import os
import glob
import numpy as np

cnt = 0

os.chdir("data_big_old/keywords_data")
fs = np.sort(glob.glob("keywords*.txt"))

for fn in fs:
  cnt += 1
  os.system("cp " + fn + " ../../data_big/keywords_data/keywords" + str(cnt).zfill(6) + "_piratenationnft.txt")
# end for fs

os.chdir("../../data_big2/keywords_data")
fs2 = np.sort(glob.glob("keywords*.txt"))

for fn in fs2:
  cnt += 1
  os.system("cp " + fn + " ../../data_big/keywords_data/keywords" + str(cnt).zfill(6) + "_piratenationnft.txt")
# end for fs
