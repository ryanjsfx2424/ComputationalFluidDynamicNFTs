import os
import cv2
import glob
from random import randrange
import numpy as np

fs = glob.glob("movies_for_pinata/*mp4")
inds = np.arange(0,len(fs))
np.random.shuffle(inds)
for ii,fn in enumerate(fs):
  print("fn: ", fn)

  ## first frame
  #os.system('ffmpeg -i ' + fn + ' -vf "select=eq(n\,0)" -q:v 3 ' 
  #          + str(ii).zfill(4) + '.png')
  
  videocap = cv2.VideoCapture(fn)
  totalFrames = videocap.get(cv2.CAP_PROP_FRAME_COUNT)
  frame = randrange(totalFrames)
  videocap.set(cv2.CAP_PROP_POS_FRAMES,frame)
  ret,frame = videocap.read()
  cv2.imwrite(str(ii).zfill(4) + ".png", frame)
  cv2.destroyAllWindows()

  #os.system('ffmpeg -sseof -' + str(frame) + ' -i ' + fn + ' -update 1 -q:v 1 '
  #          + str(ii).zfill(4) + '.png')
# end for fs

FRAMERATE = 2
os.system("ffmpeg -y -framerate " + str(FRAMERATE) + " -i %04d.png"
        + " -pix_fmt yuv420p hidden_movie.mp4")
os.system("rm *.png")
os.system("mkdir -p hidden_movie")
os.system("mv hidden_movie.mp4 hidden_movie/hidden_movie.mp4")

## get_hidden_movie.py
