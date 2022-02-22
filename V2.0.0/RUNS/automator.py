## automator.py
"""
Changes run parameters and cleans up after to avoid running out of disk.
Note that I'm assuming you already configured athena and have roe,
hllc,hlld,hlle folders in here with athena and athinput...

Eh I decided to be kinda lazy and just run one cfl for each solver,
resolution for tlim=6.0 and just truncate the movies to save me time
from running the sims...
"""
import os

## being kinda lazy about CFL for rarities,
## pretty much anything I choose will look the same
## but lower CFL take longer to run for same tlim
##   This will change after I disable athena from
## peskily guaranteeing stability (if I set cfl to 0.8 it resets it to 0.5).
CFLs = [0.499] + 16*[0.47] + 8*[0.48] + 6*[0.49] + [0.495]

## this is to save space as the movies for a full tlim=6.0 are rather
## large. I also feel like it reaches a ~steady state by tlim=3.0 or so.
TLIMs = [6.0] + 16*[1.0] + 2*[1.2] + 8*[2.0] + 4*[3.0] + [2.4]

RESOLUTIONS = 1*[512] + 26*[256] + 4*[128] + 1*[64]

## roe is most expensive so I only use it with the low resolution run
## hlld is best but I only use it for one for rarity purposes :)
SOLVERS = ["hlld"] + 26*["hlle"] + 4*["hllc"] + ["roe"]



## end automator.py
