## the_solver_2d.py
## by Ryan Farber 28 January 2015
## Last modified: 03 May     2015

from the_fluid import The_Fluid

class The_Solver_2D(The_Fluid):
    """
    The_Solver_2D inherits __init__ from The_Fluid and requires
    minimally as input variables for instantiation:
    NX,NY,NZ (the number of zones in x,y, and z) and
    DX,DY,DZ (the width of a cell [zone] in x,y, and z).
    See an input file for further on instantiating a
    The_Solver_2D instance.

    The_Fluid_Solver_2D includes finite differencing methods for solving differential equations.
    """
    
    def back_diff_1st_2d(self, f, coeff1,coeff2):
        """Applies the 1st derivative of 2D field f (input) to
        a 2D field g (output), by backward differencing."""

        g  = coeff1*( f[ 1:-1, 1:-1 ] - f[  :-2, 1:-1 ] ) /  \
                                    self.DX
        g += coeff2*( f[ 1:-1, 1:-1 ] - f[ 1:-1,  :-2 ] ) /  \
                                    self.DY
        
        return g
    # end back_diff_2d

    
    def central_diff_implicit_1st_2d(self, f, coeff1,coeff2):
        """Applies the 1st derivative of a 2D field f (input) to a 2D field g (output), by central differencing."""
        
        g  = coeff1*( f[ 2:  , 1:-1 ] + f[  :-2, 1:-1 ] ) /  \
                                (2*self.DX)
        g += coeff2*( f[ 1:-1, 2:   ] + f[ 1:-1,  :-2 ] ) /  \
                                (2*self.DY)
        
        return g
    # end central_diff_implicit_1st_2d

    
    def central_diff_1st_2dX(self, f, coeff):
        """Applies the 1st derivative of the x-component of a
        2D field f (input) to a 2D field g (output), by central differencing."""

        g = coeff*( f[ 2:  , 1:-1 ] - f[  :-2, 1:-1 ] ) /  \
                                (2*self.DX)
        
        return g
    # end central_diff_1st_2dX

    
    def central_diff_1st_2dY(self, f, coeff):
        """Applies the 1st derivative of the y-component of a
        2D field f (input) to a 2D field g (output), by central differencing."""
        
        g = coeff*( f[ 1:-1, 2:   ] - f[ 1:-1,  :-2 ] ) /  \
                                (2*self.DY)
        
        return g
    # end central_diff_1st_2dY
 
       
    def central_diff_2nd_2d(self, f, coeff1,coeff2):
        """Applies the 2nd derivative of a 2D field f (input) to a
        2D field g (output), by central differencing."""
            
        g = (coeff1/self.DX**2 * 
 (f[ 2:  , 1:-1 ] - 2*f[ 1:-1, 1:-1 ] + f[  :-2, 1:-1 ])
                                                                      
          +  coeff2/self.DY**2 * 
 (f[ 1:-1, 2:   ] - 2*f[ 1:-1, 1:-1 ] + f[ 1:-1,  :-2 ])
            )
        return g
    # end central_diff_2nd_2d

# end The_Solver_2D

## end the_solver_2d.py
