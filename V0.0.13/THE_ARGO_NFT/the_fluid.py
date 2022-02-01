## the_fluid.py
## by Ryan Farber 20 January  2015
## Last modified: 20 December 2015
"""
The_Fluid contains all the instance wide constants (attributes)
that will be used by the_argo to solve fluid mechanics problems;
these attributes and The_Fluid instance are instantiated by
the input file of a problem.

The_Fluid also now (v >= 0.4.9) has save_state and the_file_getter
and is supposed to contain all methods that should be shared across
all dimensions.
"""
import sys
if sys.version_info.major == 3:
  import _pickle as cPickle
else:
  import cPickle
# end if/else

class The_Fluid(object):
    def __init__(self, NX,NY,NZ, DX,DY,DZ):
        
        self.NX = NX   # number of zones in x
        self.NY = NY
        self.NZ = NZ
        
        self.DX = DX   # width of a cell (zone) in x
        self.DY = DY
        self.DZ = DZ
    # end __init__

    def save_state(self, the_data, file_name):
        """
        INPUT: 'the_data' ; TYPE == numpy.array; self-explanatory!
        INPUT: 'file_name'; TYPE == string     ; output file name

        Save all the data by pickling.
        """

        cPickle.dump(the_data, open(file_name, "wb"))
    # end save_state

    def get_file_name(self, cycles, max_cyc_mag, label, ext):
        """
        OUTPUT: 'file_name'  ; TYPE == string; zero prepended file name
         INPUT: 'cycles'     ; TYPE == float ; the current cycle
         INPUT: 'max_cyc_mag'; TYPE == float ; maximum number of cycles
         INPUT: 'ext'        ; TYPE == string; problem file name

        Prepends zeros to the cycle number to be used in the saved file
        name so that files show up in the correct (directory) order.
        """
        
        cyc_lbl = ""
        for i in range(1, max_cyc_mag+1):
            if cycles < 10**i:
                cyc_lbl   = "0"*(max_cyc_mag- i) + str(cycles)
                file_name = label + "_cycle_" + cyc_lbl + ext
                return file_name
            # end if
        # end for
    # end get_file_name
    
# end class The_Fluid

## end the_fluid.py
