# v1 downsampled by 14
# v2 "" by 140
# v3 "" by 70
VN = "4"
import os
import sys
import glob
import time; start = time.time()
import numpy as np
from skimage  import io
from pyxelate import Pyx, Pal
print("imported in (s): ", time.time() - start)

os.chdir("PNG")
os.system("mkdir -p PixelV" + VN)

fs = np.sort(glob.glob("*.png"))
for ii,fn in enumerate(fs):
  print("ii, fn: ", ii, fn)
  #load image with 'skimage.io.imread()'
  image = io.imread(fn)  
  print("loaded image in (s): ", time.time() - start)
  downsample_by = 35  # new image will be 1/14th of the original in size
  palette = 7  # find 7 colors

  #1) Instantiate Pyx transformer

  pyx = Pyx(factor=downsample_by, palette=palette)

  #2) fit an image, allow Pyxelate to learn the color palette

  pyx.fit(image)
  print("fit image in (s): ", time.time() - start)

  #3) transform image to pixel art using the learned color palette

  new_image = pyx.transform(image)
  print("transformed image in (s): ", time.time() - start)
  #save new image with 'skimage.io.imsave()'
  os.chdir("PixelV" + VN)
  io.imsave("pixel_" + fn, new_image)
  os.chdir("..")
  print("saved image in (s): ", time.time() - start)
  if ii > 3:
    break
  # end if
# end for ii
