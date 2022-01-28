## INPUTS_NonlinearAdvectionPeriodic2D.py
## by Ryan Farber 22 January 2015
## Last modified: 05 May 2015
"""
This is an INPUTS file tailored for the
ExplicitNonlinearAdvectionPeriodic2D problem.

NOTE: NX,NY,NZ,DX,DY, and DZ are required constants to
instantiate the my_fluid object; additional problem specific
constants are added after creating the my_fluid object below.
"""
import os
import numpy as np
from matplotlib import cm
from the_fluid_solver_2d import The_Fluid_Solver_2D

##General Constatns
NX = 81 # number of zones in x
NY = 81 # number of zones in y
NZ = "NA" # not applicable to a 1D problem

XMIN = 0.0
XMAX = 2.0
YMIN = 0.0
YMAX = 2.0

DX = (XMAX - XMIN) / (NX - 1) # width of a cell in x
DY = (YMAX - YMIN) / (NY - 1) # width of a cell in y
DZ = "NA"
##End General Constants


my_fluid = The_Fluid_Solver_2D(NX,NY,NZ, DX,DY,DZ)


##Problem Constants
my_fluid.cycle_start = 1 # cycle to start at (1 is default)
my_fluid.NT = 800 # number of time steps
my_fluid.S = 0.26 # stability constant
my_fluid.DT = DX*my_fluid.S # chosen for stability
##End Problem Constants


my_fluid.SAVE_FREQ = 3 # save state every SAVE_FREQ cycles

my_fluid.framerate = 60

##Plotting Constants
my_fluid.XMIN = XMIN
my_fluid.XMAX = XMAX
my_fluid.YMIN = YMIN
my_fluid.YMAX = YMAX

my_fluid.PLT_TYP = "surface velocity"
my_fluid.LABEL = "hat_periodic_boundaries"
my_fluid.MAX_CYC_MAG = 9 # magnitude of max cycles

my_fluid.cmap = cm.Greys
##End Plotting Constants
my_fluid.solver = 'implicit'

my_fluid.DATA_DIR = "StateFiles_" + my_fluid.solver + "CFL" + \
str(my_fluid.S).replace(".", "pt")

my_fluid.PLOT_DIR = my_fluid.DATA_DIR.replace("StateFiles","Plots")

os.system("mkdir -p " + my_fluid.DATA_DIR)
os.chdir(my_fluid.DATA_DIR)
my_fluid.save_state(my_fluid, "my_fluid.p")
os.system("cp my_fluid.p ..") # so nonlinear*.py can know which StateFile dir


## end INPUTS_ExplicitNonlinearAdvectionPeriodic2D.py
