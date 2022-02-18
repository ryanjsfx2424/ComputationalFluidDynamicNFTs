For CFD NFTs V2.0.0 I want to produce 32 NFTs.
Since V1.0.0 had 4 traits I'd like there to be 5+.

Traits:
  Riemann Solver: Roe, LLF, HLLE, HLLC (HLLD)
  CFL: values TBD
  Stable: true or false (depends on CFL)
  Resolution: maybe fiducial, 1/2, 2x (maybe 1/4, maybe maybe 4x)
    -> would be easier to go to lower resolutions than higher resolutions.
  Colormaps: all unique again? Or repeat some?
  Divergence cleaning method? (If possible to change)

Note: I've been running fiducial OrszagTang for 14+ minutes now...
  It's running in serial producing VTK files (might be nice to parallelize
  since I have 4 cores. Might also be nice to switch to hdf5).

Fiducial configure command:
  python configure.py --prob orszag_tang -b --flux hlld

To switch between Riemann solvers, modify configure flags:
  python configure.py --prob orszag_tang --flux roe (for example)

For resolutions maybe do:
  high   = 512^2
  med    = 256^2
  low    = 128^2
  poor   =  64^2
  coarse =  32^2
  retro  =  16^2
  8bit   =   8^2

I think 7 would me more than enough. I'll test now if 8bit is...too coarse.
