## the_plotter_2d.py
## by Ryan Farber 21 January  2015
## Last modified: 07 March    2015
"""
The purpose of this program is to load fluid variables processed by
The Argo 2D from a saved state file and to plot the 2D variable.

  NOTE: This file must be copied by a bash script to the specific
Problem file folder it shall be used in to work.

Indexing of "the_data" depends on what dimension of "save_state"
was used; the below disambiguates for data from The Argo 2D.

the_data[0] = cycles
the_data[1] = u       # x-component of velocity
the_data[2] = v       # y-component of velocity
the_data[3] = cn      # concentration (tracer density)
the_data[4] = p       # pressure
the_data[5] = src     # src term of pressure poisson eqn
the_data[6] = Fx      # x-comp of external force
the_data[7] = Fy      # y-comp of external force
the_data[8] = Bx      # x-comp of magnetic field
the_data[9] = By      # y-comp of magnetic field

Note that my_fluid.PLT_TYP must be constructed in the INPUTS* file
with care for proper operation of this file. Below are suggestions
(note: order of the keywords does not matter and spacing between
keywords similarly does not matter):

my_fluid.PLT_TYP = "quiver"               # quiver only plot of velocity
my_fluid.PLT_TYP = "quiver"+"pcolormesh"  # quiver plot of velocity on a
                                          # concentration pcolormesh
my_fluid.PLT_TYP = "quiver"+"contour"     # quiver plot of velocity on
                                          # pressure contours
my_fluid.PLT_TYP = "surface"+"velocity"   # surface   plot of velocity
my_fluid.PLT_TYP = "surface"+"pressure"   # surface   plot of pressure
my_fluid.PLT_TYP = "wireframe"+"velocity" # wireframe plot of velocity
my_fluid.PLT_TYP = "wireframe"+"pressure" # wireframe plot of pressure
"""
import glob
import numpy as np
import matplotlib.pyplot as plt; fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import sys
from the_fluid import The_Fluid
import os; cur_path = os.getcwd()
if sys.version_info.major == 3:
  import _pickle as cPickle
else:
  import cPickle
# end if/else
my_fluid = cPickle.load(open("my_fluid.p", "rb"))
data_dir = cur_path + "/" + my_fluid.DATA_DIR
plot_dir = cur_path + "/" + my_fluid.PLOT_DIR
os.chdir(data_dir)

##Parameters
data_file_ext = ".p"
plot_file_ext = ".png"

os.system("mkdir -p " + plot_dir)
os.chdir(plot_dir)
plotfiles = np.sort(glob.glob("*cycle*" + plot_file_ext))

os.chdir(data_dir)
datafiles = np.sort(glob.glob("*cycle*" + data_file_ext))#[:1]

pfiles = glob.glob("*cycle*.p")
for datafile in datafiles:
    if (datafile[:-len(data_file_ext)] + plot_file_ext) in plotfiles:
        continue
    the_data = cPickle.load(open(datafile, "rb"))
    os.chdir(plot_dir)

    plt_title = "Cycle " + str(the_data[0])
    plt_name  = datafile[:-len(data_file_ext)] + plot_file_ext
    
    X = np.linspace(my_fluid.XMIN, my_fluid.XMAX, my_fluid.NX)
    Y = np.linspace(my_fluid.YMIN, my_fluid.YMAX, my_fluid.NY)
    Y,X = np.meshgrid(X,Y)

    if the_data[1] != "NA":
        u = the_data[1]
        v = the_data[2]
    if the_data[3] != "NA":
        cn = the_data[3]
    if the_data[4] != "NA":
        p  = the_data[4]
    if the_data[8] != "NA":
        Bx = the_data[8]
        By = the_data[9]
    # end ifs

    if not ("include"    in my_fluid.PLT_TYP and
            "boundaries" in my_fluid.PLT_TYP):
        X = X[1:-1,1:-1]; Y = Y[1:-1,1:-1]
        if the_data[1] != "NA":
            u = u[1:-1,1:-1]
            v  = v[1:-1,1:-1]
        if the_data[3] != "NA":
            cn = cn[1:-1,1:-1]
        if the_data[4] != "NA":
            p  =  p[1:-1,1:-1]
        if the_data[8] != "NA":
            Bx = Bx[1:-1,1:-1]
            By = By[1:-1,1:-1]
    # end if not
                
    if   "quiver" in my_fluid.PLT_TYP:
        if   "pcolormesh" in my_fluid.PLT_TYP:
            if ("concentration" in my_fluid.PLT_TYP or
                "cn" in my_fluid.PLT_TYP or
                "density" in my_fluid.PLT_TYP):
                var = cn
                lbl = "Tracer Concentration "
            elif "mag" in my_fluid.PLT_TYP:
                var = 0.5*(Bx**2 + By**2)
                lbl = "Magnetic Field Energy Density "
            # end if/elif
            
            plt.pcolormesh(X,Y, var)
            plt.colorbar()

            plt.quiver(X,Y, u,v, color='w')

            plt_title  = "Velocity Arrows on Tracer Concentration "
            plt_title += "Colormesh at Cycle " + str(the_data[0])

#            if "magnetism" in my_fluid.PLT_TYP:
#                fig2 = plt.figure()
                
            
        elif "contour" in my_fluid.PLT_TYP:
            plt.contourf(X,Y, p, alpha=0.5)
            plt.colorbar()

            plt.contour(X,Y,  p)

            plt.quiver(X[::2, ::2],Y[::2, ::2], u[::2, ::2],
                                                v[::2, ::2])
            plt_title  = "Velocity Arrows on Pressure Contours at Cycle"
            plt_title += " " + str(the_data[0]) 
        else:
            plt.quiver(X[::3, ::3],Y[::3, ::3], u[::3, ::3],
                                                v[::3, ::3])
        # end if/elif/else
        plt.axis([X.min(),X.max(), Y.min(),Y.max()])
    else:
        ax = fig.gca(projection="3d")
        
        if   "velocity" in my_fluid.PLT_TYP:
            zlbl = "velocity"
            var  = u
            ax.set_zlim(1, 2.5)
        elif "pressure" in my_fluid.PLT_TYP:
            zlbl = "pressure"
            var  = p
            ax.view_init(30, 225)
        elif "mag"      in my_fluid.PLT_TYP:
            zlbl = "magnetic energy"
            var = 0.5*(Bx**2 + By**2)
        else:
            print("""Sorry, only non-quiver plots of velocity and
                  pressure are currently available. Please edit the
                  value of my_fluid.PLT_TYP accordingly.""")
            sys.exit()
        # end if/elif/else
                  
        if   "surface"   in my_fluid.PLT_TYP:
            ax.plot_surface(X,Y, var, rstride=1,cstride=1,
                            cmap=my_fluid.cmap, linewidth=0,
                            antialiased=False)
        elif "wireframe" in my_fluid.PLT_TYP:
            ax.plot_wireframe(X,Y, var)
        else:
            print("""Sorry, the only non-quiver plots currently
                  available are surface and wireframe. Please edit the
                  value of my_fluid.PLT_TYP accordingly.""")
            sys.exit()
        # end if/elif/else
        ax.set_xlim(my_fluid.XMIN, my_fluid.XMAX)
        ax.set_ylim(my_fluid.YMIN, my_fluid.YMAX)
        #ax.set_zlabel(zlbl)
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.zaxis.set_ticklabels([])
    # end if/else
    #plt.xlabel("x"); plt.ylabel("y")
    plt.title(plt_title)
    plt.savefig(plt_name)

    plt.clf()
    os.chdir(data_dir)
# end for
## end the_plotter_2d.py
