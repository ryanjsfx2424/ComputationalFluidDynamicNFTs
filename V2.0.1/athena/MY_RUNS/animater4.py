## generate_json.py
import os
import glob
import numpy as np
FRAMERATE = 7

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V2.0.1/athena/MY_RUNS/"

MOVIEDIR = HOME + "MOVIES_NEW/"
os.system("mkdir -p " + MOVIEDIR)

RUNDIRS  = list(np.sort(glob.glob("hll*")))
RUNDIRS += list(np.sort(glob.glob("llf*")))
RUNDIRS += list(np.sort(glob.glob("roe*")))

plotdirs = glob.glob("Plots_*")[::-1]

'''
plotdirs_saved = []
cmaps = []
for pp,plotdir in enumerate(plotdirs):
  if "period"  in plotdir:
    cmap = plotdir.split("period")[1]
  elif "grav"  in plotdir:
    cmap = plotdir.split("grav")[1]
  elif "gamma" in plotdir:
    cmap = plotdir.split("gamma")[1]
  elif "iprob" in plotdir:
    cmap = plotdir.split("iprob")[1]
  elif "2xBox" in plotdir:
    cmap = plotdir.split("2xBox")[1]
  elif "b0pt01_tlim69"  in plotdir:
    cmap = plotdir.split("b0pt01_tlim69")[1]
  elif "tlim"  in plotdir:
    cmap = plotdir.split("tlim")[1]
  elif "128x256" in plotdir:
    cmap = plotdir.split("128x256")[1]
  elif "512x1024" in plotdir:
    cmap = plotdir.split("512x1024")[1]
  # end if/elifs

  ind = cmap.find("_")+1
  cmap = cmap[ind:]

  if cmap in cmaps or cmap in ["autumn", "dusk", "GRN-RED-BLU-WHT", 
     "Reds", "spring", "winter", "summer"]:
    continue
  # end if
  plotdirs_saved.append(plotdir)
  cmaps.append(cmap)
# end for
print("plotdirs_saved: ", plotdirs_saved)
'''
## the result of the above was the following.
## I might have screwed up the ordering by moving
## stuff to the usb drive (transfer still in process...)

plotdirs_saved = ["Plots_hllc512x1024_brg", 
                   'Plots_hllc256x512_gamma1pt333_drat2pt0_grav0pt1_period1pt0_B-W_LINEAR_r', 
'Plots_hllc512x1024_Pastel1',
 'Plots_hllc512x1024_gist_ncar',
 'Plots_hllc256x512_gamma1pt4_drat2pt0_grav0pt25_period1pt0_Eos_A',
 'Plots_hllc512x1024_Pastels',#5
 'Plots_hllc512x1024_STEPS',
 'Plots_hllc512x1024_doom',
 'Plots_hllc512x1024_STD_GAMMA-II',
 'Plots_hllc512x1024_algae',
 'Plots_hllc512x1024_16_LEVEL',
 'Plots_hllc512x1024_Hardcandy', #11
 'Plots_llf64x128_tlim69_dusk',
 'Plots_hllc64x128_gamma1pt4_drat2pt0_grav0pt33_period1pt0_coolwarm',
 'Plots_hllc64x128_gamma1pt666666_drat2pt0_grav0pt1_period1pt0_gist_yarg',
 'Plots_hllc512x1024_Rainbow18', #15
 'Plots_hllc256x512_gamma1pt666666_drat2pt0_grav0pt33_period1pt0_Eos_A',
 'Plots_hlld64x128_b0pt01_tlim69_gist_yarg',
 'Plots_hllc256x512_B-W_LINEAR',
 'Plots_hllc512x1024_bone', #19
 'Plots_hllc512x1024_jet',
 'Plots_hllc256x512_gamma1pt4_drat2pt0_grav0pt25_period1pt0_Dark2',
 'Plots_hllc256x512_gamma1pt666666_drat2pt42_grav0pt1_periodInf_Hardcandy',
 'Plots_hllc512x1024_CMRmap',
 'Plots_hllc512x1024_Accent',
 'Plots_hllc512x1024_RED_TEMPERATURE', #25
 'Plots_hllc64x128_gamma1pt4_drat2pt0_grav0pt1_period1pt0_Set3',
 'Plots_roe16x32_tlim50_gamma1pt42_drat2pt069_grav0pt169_cubehelix',
 'Plots_hllc64x128_gamma1pt666666_drat2pt42_grav0pt1_period4pt0_gist_heat',
 'Plots_hllc64x128_tlim69_p0pt5_cool',
 'Plots_hllc512x1024_magma', #30
 'Plots_hllc64x128_tlim68_Volcano',
 'Plots_hllc512x1024_seismic',
 'Plots_hllc64x128_tlim69_p0pt5_2xBox_hsv',
 'Plots_hllc256x512_gamma1pt666666_drat2pt42_grav0pt1_periodInf_Hue_Sat_Value_2',
 'Plots_hllc256x512_gamma1pt666666_drat2pt0_grav0pt33_period1pt0_Haze',#35
 'Plots_hllc512x1024_octarine',
 'Plots_hllc512x1024_gist_earth',
 'Plots_hllc512x1024_inferno',
 'Plots_hllc512x1024_kelp',
 'Plots_hllc64x128_gamma1pt333_drat2pt0_grav0pt1_period1pt0_Peppermint',#40
 'Plots_hllc512x1024_flag',
 'Plots_hllc512x1024_Paired',
 'Plots_hllc512x1024_kamae',
 'Plots_hllc512x1024_Purple-Red_+_Stripes',
 'Plots_hllc64x128_tlim69_iprob69_prism',#45
 'Plots_hllc512x1024_Pastel2',
 'Plots_hllc512x1024_bwr',
 'Plots_hllc512x1024_Ocean',
 'Plots_hllc512x1024_Plasma',
 'Plots_hllc512x1024_Greys',#50
 'Plots_hllc512x1024_viridis',
 'Plots_hllc512x1024_Nature',
 'Plots_hllc512x1024_STERN_SPECIAL',
 'Plots_hllc64x128_tlim69_p0pt5_flag',
 'Plots_hllc512x1024_twilight',#55
 'Plots_hllc512x1024_nipy_spectral',
 'Plots_hllc512x1024_Blues',
 'Plots_hllc512x1024_Set3',
 'Plots_hllc512x1024_cool',
 'Plots_hllc512x1024_afmhot',#60
 'Plots_hllc512x1024_Volcano',
 "Plots_hllc512x1024_Rainbow"]

# from animater2.py
plotdirs_saved += [
 "Plots_hllc64x128_gamma1pt4_drat2pt0_grav0pt1_periodInf_Pastel1",
 "Plots_hllc64x128_gamma1pt4_drat2pt0_grav0pt1_periodInf_Waves",
 "Plots_hllc69x138_tlim69_gamma1pt69_drat1pt69_grav0pt069_period6pt9_jet",#65
 "Plots_hlle64x128_gamma1pt4_drat2pt0_grav0pt33_periodInf_gist_heat",
 "Plots_hllc64x128_tlim69_iprob69_doom",
 "Plots_hllc32x64_tlim69_Pastel1",#68 (0-indexed so 69 total!)
 ]

# okay great! Now I just need to re-generate movies and actually
# generate the json now :O

print("len ps: ", len(plotdirs_saved))
for jj,plotdir in enumerate(plotdirs_saved):
  print("plotdir: ", plotdir)

  if jj not in [40]:
    continue
  # end if
  FRAMERATE = 7

  os.chdir(HOME + "KEEP/" + plotdir)
  os.system("cp " + HOME + "make_even_dims.bash .")
  os.system("bash make_even_dims.bash")

  os.system("rm -r temp")
  os.system("mkdir -p temp")
  os.system("cp *.png temp/")
  os.chdir("temp")

  fs = list(np.sort(glob.glob("*.png")))
  fs = fs[::2]
  #fs = fs[:int(len(fs)/1.2)]
  fs += fs[::-1]
  for ii,fn in enumerate(fs):
    os.system("cp " + fn + " " + str(ii).zfill(5) + ".png")
  # end for ii

  input_name  = "%05d.png"
  output_name = MOVIEDIR + str(jj) + ".mp4"
  print("input_name: ", input_name)
  print("output_name: ", output_name)

  os.system("ffmpeg -y -framerate " + str(FRAMERATE) + " -i " + input_name 
          + " -pix_fmt yuv420p " + output_name)
  os.chdir("..")
  os.system("rm -r temp")
  os.chdir(HOME)
# end for jj

print("SUCCESS!")
