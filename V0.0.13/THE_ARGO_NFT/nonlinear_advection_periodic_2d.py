## explicit_nonlinear_advection_periodic_2d.py
## by Ryan Farber 29 December 2014
## Last modified: 06 March    2015
"""
The purpose of this program is to apply the_argo to propagate
a hat function by explicit nonlinear advection in two dimensions
with periodic boundaries.
"""
import os
import sys
import glob
import numpy as np
from the_fluid import The_Fluid
if sys.version_info.major == 3:
  import _pickle as cPickle
else:
  import cPickle
# end if/else

my_fluid = cPickle.load(open("my_fluid.p", "rb"))
os.chdir(my_fluid.DATA_DIR)

##Setup
ext = ".p"  # filename extension for pickling
XX,YY = np.mgrid[1:my_fluid.NX-1, 1:my_fluid.NY-1]# imitates 2D for loop

if my_fluid.cycle_start == 1:
    u = np.ones( (my_fluid.NX,my_fluid.NY) ) # x-component of velocity
    v = np.ones( (my_fluid.NX,my_fluid.NY) ) # y-component of velocity

    u[ int(0.5/my_fluid.DX) : int(1.0/my_fluid.DX)+1,
       int(0.5/my_fluid.DY) : int(1.0/my_fluid.DY)+1 ] = 2.0
    v[ int(0.5/my_fluid.DX) : int(1.0/my_fluid.DX)+1,
       int(0.5/my_fluid.DY) : int(1.0/my_fluid.DY)+1 ] = 2.0


    ##Save the state of the initial condition of the fluid
    cycles = 0
    file_name = my_fluid.get_file_name(cycles, my_fluid.MAX_CYC_MAG,
                                               my_fluid.LABEL, ext)
    my_fluid.save_state([cycles, u,v, "NA", "NA","NA", "NA","NA", "NA","NA"],
               file_name )
else:
    data_file = glob.glob("*" + str(my_fluid.cycle_start) + "*")
    if data_file == []:
        print("Error! my_fluid.cycle_start data file not found.")
        raise
    # end if
    data_file = data_file[0]
    the_data = cPickle.load(open(data_file))
    u = the_data[1]; v = the_data[2]
    the_data = 0 # to save memory
# end if


##Solve!
for cycles in range(my_fluid.cycle_start, my_fluid.NT+1):
    ##Update ghost zones so boundaries are periodic
    u[ 0, : ] = u[ -2,  : ]; u[ -1,  : ] = u[ 1, : ]
    u[ :, 0 ] = u[  :, -2 ]; u[  :, -1 ] = u[ :, 1 ]
    
    v[ 0, : ] = v[ -2,  : ]; v[ -1,  : ] = v[ 1, : ]
    v[ :, 0 ] = v[  :, -2 ]; v[  :, -1 ] = v[ :, 1 ]

    if   my_fluid.solver.lower() == "explicit":
      u[1:-1,1:-1] -= my_fluid.nonlinear_advect_explicit_2d(u, u,v)
      v[1:-1,1:-1] -= my_fluid.nonlinear_advect_explicit_2d(v, u,v)

    elif my_fluid.solver.lower() == "implicit":
      u[1:-1,1:-1] = my_fluid.nonlinear_advect_implicit_periodic_2d(u, u,v, XX,YY)
      v[1:-1,1:-1] = my_fluid.nonlinear_advect_implicit_periodic_2d(v, u,v, XX,YY)

    else:
      print("ERROR! Only explicit or implicit solvers accepted for this problem")
      raise
    # end if/elif/else

    if (cycles % my_fluid.SAVE_FREQ == 0 or cycles in [100,200,300]):
        file_name = my_fluid.get_file_name(cycles, my_fluid.MAX_CYC_MAG,
                                                   my_fluid.LABEL, ext)
        my_fluid.save_state([cycles, u,v, 
                             "NA", "NA","NA", "NA","NA", "NA","NA"], file_name)
    # end if
# end for
file_name = my_fluid.get_file_name(cycles, my_fluid.MAX_CYC_MAG,
                                   my_fluid.LABEL, ext)
my_fluid.save_state([cycles, u,v, "NA", "NA","NA", "NA","NA", "NA","NA"],
           file_name )

## end explicit_nonlinear_advection_periodic_2d.py
