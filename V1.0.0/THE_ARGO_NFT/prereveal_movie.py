## prereveal_movie.py
"""
To create a prereveal mp4 I just stitch the first frame from each
plot directory together.
"""
import os
import glob
import numpy as np

TOP  = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V0.0.1/"
HOME = TOP + "THE_ARGO_NFT/"

os.system("mkdir -p first_frames")
plotDirs = glob.glob("Plots*")
for ii,plotDir in enumerate(plotDirs):
  os.chdir(HOME + plotDir)
  fn = np.sort(glob.glob("*.png"))[0]
  os.system("cp " + fn + " " + HOME + "first_frames/" + str(ii).zfill(4) + ".png")
# end for plotDirs
os.chdir(HOME + "first_frames")
print("ls: ", os.listdir(os.getcwd()))
os.system("ffmpeg -y -framerate 3 -i %04d.png -pix_fmt yuv420p " + "hidden.mp4")
os.system("mkdir -p " + TOP + "hidden_movies")
os.system("mv hidden.mp4 " + TOP + "hidden_movies/hidden.mp4")
os.system("rm -r " + HOME + "first_frames")
## prereveal_movie.py
