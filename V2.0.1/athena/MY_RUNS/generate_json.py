## generate_json.py
import os
import glob
import numpy as np

image_line_base = '  "image": "ipfs://QmXr3XgiuCwHhPz3Z63umzxPQB2tYw1KjsfCpxvMxpRehU/'
image_line_ext  = '",\n'

HOME = "/Users/redx/Documents/Desktop/NFTs/ComputationalFluidDynamicNFTs/V2.0.1/athena/MY_RUNS/"

os.system("mkdir -p " + HOME + "metadata")
os.chdir(HOME + "metadata")

## ugly but at least it guarantees I don't mix up the order...
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

description_line = '  "description": "This is the third version of a series of Computational Fluid Dynamics collections. In this version, we utilize Athena++, which is an open-source finite-volume, magnetohydrodynamics code (further details in Stone et al. 2020, ApJ, 249, 4).\\n\\nIn this version, we simulate the Rayleigh-Taylor instability which occurs when a perturbation disturbs an unstable equilibrium such as when a more bouyant material is below a less bouyant material, with widespread applications, from the convective motions of i) boiling water, ii) in a low-mass star\'s outer envelope, iii) in a high-mass star\'s core, iv) \'salt fingering\' as occurs in Earth\'s oceans and putatively the sub-ice south polar lake of Enceladus, and the sub-ice ocean of Jupiter\'s moon Europa.\\n\\nWe include cases of a simple sinusoidal perturbation with a wavelength set to match the box width, a wavelength four times smaller than the box width, 6.9 times smaller than the box width, and a noisy perturbation. Particularly for the noisy perturbation, the Kelvin-Helmholtz instability clearly operates, which we plan to spread awareness of in the subsequent version of CFD NFTs.\\n\\nSimulations were performed on a 2013 MacBook Pro (2 GHz Quad-Core Intel Core i7; 8 GB 1600 MHz DDR3; 256 GB SSD)\\n\\nv3.0.0 features 69 NFTs.",\n'


# okay great! Now I just need to actually
# generate the json now :O

with open("_metadata.json", "w") as fid_global_write:
  fid_global_write.write("{")

  print("len ps: ", len(plotdirs_saved))
  for jj,plotdir in enumerate(plotdirs_saved):
    print("plotdir: ", plotdir)

    ## first, get the colormap
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
    elif "p0pt5" in plotdir:
      cmap = plotdir.split("p0pt5")[1]
    elif "tlim"  in plotdir:
      cmap = plotdir.split("tlim")[1]
    elif "128x256" in plotdir:
      cmap = plotdir.split("128x256")[1]
    elif "512x1024" in plotdir:
      cmap = plotdir.split("512x1024")[1]
    # end if/elifs

    ind = cmap.find("_")+1
    cmap = cmap[ind:]

    ## second, get the resolution
    res = plotdir.split("_")[1]
    if "llf" in res or "roe" in res:
      res = res[3:]
    else:
      res = res[4:]
    # end if/else

    ## third, Riemann solver
    riemann = plotdir.split("_")[1]
    if "llf" in riemann or "roe" in riemann:
      riemann = riemann[:3]
    else:
      riemann = riemann[:4]
    # end if/else
    print("riemann: ", riemann)

    ## fourth, gamma
    if "gamma" in plotdir:
      gamma = plotdir.split("gamma")[1].split("_")[0]
    else:
      gamma = "1pt4"
    # end if
    gamma = gamma.replace("pt", ".")

    ## fifth, density contrast
    if "drat" in plotdir:
      drat = plotdir.split("drat")[1].split("_")[0]
    else:
      drat = "2pt0"
    # end if
    drat = drat.replace("pt", ".")

    ## sixth, gravitational acceleration
    if "grav" in plotdir:
      grav = plotdir.split("grav")[1].split("_")[0]
    else:
      grav = "0pt1"
    # end if
    grav = grav.replace("pt", ".")

    ## seventh, perturbation period
    if "p0pt5" in plotdir:
      period = "0pt5"
    elif "period" in plotdir:
      period = plotdir.split("period")[1].split("_")[0]
    else:
      period = "1pt0"
    # end if
    period = period.replace("pt", ".")
    print("period: ", period)

    rewind = "True"
    if jj in [7,45,64]:
      rewind = "False"
    # end if

    attributes_line = '  "attributes": [{"trait_type": "Resolution", "value": "' + res + '"}, {"trait_type": "CFL", "value": "0.4"}, {"trait_type": "Stable", "value": "True"}, {"trait_type":"Rewind", "value": "' + rewind + '"}, {"trait_type": "Colormap", "value": "' + cmap + '"}, {"trait_type":"Riemann Solver", "value":"' + riemann + '"}, {"trait_type":"adiabatic index", "value":"' + gamma + '"}, {"trait_type": "density contrast", "value": "' + drat + '"}, {"trait_type": "gravitational acceleration", "value": "-' + grav + '"}, {"trait_type":"perturbation period", "value":"' + period + '"}],\n'

    with open(str(jj) + ".json", "w") as fid_local_write:
      fid_local_write.write("{\n")
      fid_local_write.write('  "name":"#' + str(jj) + '",\n')
      fid_local_write.write(description_line)
      fid_local_write.write(image_line_base + str(jj) + ".mp4" + image_line_ext)
      fid_local_write.write('  "edition": ' + str(jj) + ',\n')
      fid_local_write.write(attributes_line)
      fid_local_write.write('  "compiler": "CFD_NFT Engine"\n')
      fid_local_write.write("}")
    # end with open

    fid_global_write.write("  {\n")
    fid_global_write.write('    "name":"#' + str(jj) + '",\n')
    fid_global_write.write("  " + description_line)
    fid_global_write.write("  " + image_line_base + str(jj) + ".mp4" + image_line_ext)
    fid_global_write.write('    "edition": ' + str(jj) + ',\n')
    fid_global_write.write("  " + attributes_line)
    fid_global_write.write('    "compiler": "CFD_NFT Engine"\n')

    if jj < 68:
      fid_global_write.write("  },\n")
    else:
      fid_global_write.write("  }\n")
    # end if/else
  # end for jj
  fid_global_write.write("}")
# end with open

print("SUCCESS!")
