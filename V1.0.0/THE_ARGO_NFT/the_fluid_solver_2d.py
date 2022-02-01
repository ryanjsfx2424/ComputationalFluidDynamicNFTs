## the_fluid_solver_2d.py
## by Ryan Farber 20 January  2015
## Last modified: 19 December 2015

import numpy as np
from the_solver_2d import The_Solver_2D

class The_Fluid_Solver_2D(The_Solver_2D):
    """
    The_Fluid_Solver_2D inherits __init__ from The_Fluid and requires minimally as input variables for instantiation:
    NX,NY,NZ (the number of zones in x,y, and z) and DX,DY,DZ
    (the width of a cell [zone] in x,y, and z). See an input file for further on instantiating a The_Fluid_Solver_2D instance. The_Fluid_Solver_2D includes methods for solving the navier stokes equations in two dimensions; however, the
    flows must be: constant density, constant viscosity, incompressible, and isothermal fluid flows.
    """
    
    def linear_advect_explicit_2d(self, f):
        """Performs linear advection of a 2D field,
        by explicit backward differencing."""

        return self.DT*self.back_diff_1st_2d(f, self.C,self.C)
    # end linear_advect_explicit_2d

    def advect_explicit_CFD_2dX(self, u,v):
        """Performs linear advection of a 2D field for project
        problem 3.1 of Computational Fluid Dynamics I."""

        term1 = (u[2:  ,1:-1] + u[1:-1,1:-1])**2/4.0

        term2 = (u[1:-1,1:-1] + u[ :-2,1:-1])**2/4.0

        term3 = ((u[1:-1,1:-1] + u[1:-1,2:])/2.0 * 
                 (v[1:-1,1:-1] + v[2:,1:-1])/2.0 )

        term4 = ((u[1:-1,1:-1] + u[1:-1,:-2])/2.0 *
                 (v[1:-1, :-2] + v[2:  ,:-2])/2.0 )
        

        A = (term1 - term2)/self.DX + (term3 - term4)/self.DY
        

        return self.DT*A

    def advect_explicit_CFD_2dY(self, u,v):
        """Performs linear advection of a 2D field for project
        problem 3.1 of Computational Fluid Dynamics I."""

        A = np.zeros(u.shape)

        term1 = (v[1:-1,2:  ] + v[1:-1,1:-1])**2/4.0

        term2 = (v[1:-1,1:-1] + v[1:-1, :-2])**2/4.0

        term3 = ((u[1:-1,1:-1] + u[1:-1,2:])/2.0 * 
                 (v[1:-1,1:-1] + v[2:,1:-1])/2.0 )

        term4 = ((u[1:-1,1:-1] + u[1:-1,:-2])/2.0 * 
                 (v[1:-1, :-2] + v[2:  ,:-2])/2.0 )

        A = (term1 - term2)/self.DX + (term3 - term4)/self.DY
        

        return self.DT*A

    def diffuse_CFD_2d(self, f):
        RE = 1.0 # Reynolds number

        D = (1.0/RE) * ((f[2:,1:-1] - 2*f[1:-1,1:-1] + f[:-2,1:-1])/self.DX**2
                     +  (f[1:-1,2:] - 2*f[1:-1,1:-1] + f[1:-1,:-2])/self.DY**2)

        return self.DT*D

        
        
    
    def linear_advect_implicit_2d(self, f, XX,YY):
        """Performs linear advection of a 2D field (f) implicitly, keeping all values bounded within the domain, by cell-centered back-tracking and applying necessary weights."""

        x = XX - (self.DT/self.DX * self.C)
        y = YY - (self.DT/self.DY * self.C)

        x = np.where(x < 0.5, 0.5, x)
        y = np.where(y < 0.5, 0.5, y)
        
        x = np.where(x > (self.NX-2) + 0.5,
                     (self.NX-2) + 0.5, x)
        y = np.where(y > (self.NY-2) + 0.5,
                     (self.NY-2) + 0.5, y)

        i0 = x.astype(int); j0 = y.astype(int)
        i1 = i0 + 1; j1 = j0 + 1

        s1 = x - i0; t1 = y - j0
        s0 = 1 - s1; t0 = 1 - t1
        
        return (s0 * (t0 *  f[ i0, j0 ] + t1 *  f[ i0, j1 ])
              + s1 * (t0 *  f[ i1, j0 ] + t1 *  f[ i1, j1 ]))
    # end linear_advect_implicit_2d

    
    def linear_advect_implicit_periodic_2d(self, f, XX,YY):
        """Performs linear advection of a 2D field (f) implcitly, with periodic boundaries, by cell-centered back-tracking and applying necessary weights."""

        x = XX - (self.DT/self.DX * C)
        y = YY - (self.DT/self.DY * C)

        x = x % (self.NX - 2)
        y = y % (self.NY - 2)

        i0 = x.astype(int); j0 = y.astype(int)
        i1 = i0 + 1; j1 = j0 + 1

        s1 = x - i0; t1 = y - j0
        s0 = 1 - s1; t0 = 1 - t1
        
        return (s0 * (t0 *  f[ i0, j0 ] + t1 *  f[ i0, j1 ])
             +  s1 * (t0 *  f[ i1, j0 ] + t1 *  f[ i1, j1 ]))
    # end linear_advect_implicit_periodic_2d

    
    def nonlinear_advect_explicit_2d(self, f, fx,fy):
        """Performs nonlinear advection of 2D field (f), by 2D vector field (fx,fy) by explicit backward differencing."""

        return self.DT*self.back_diff_1st_2d(f,
                fx[ 1:-1, 1:-1 ], fy[ 1:-1, 1:-1 ])
    # end nonlinear_advect_explicit_2d

    
    def nonlinear_advect_implicit_2d(self, f, fx,fy, XX,YY):
        """Performs nonlinear advection of 2D field (f) by 2D vector field (fx,fy), keeping all values bounded within the domain, by cell-centered back-tracking and applying necessary weights."""

        x = XX - (self.DT/self.DX * fx[1:-1,1:-1])
        y = YY - (self.DT/self.DY * fy[1:-1,1:-1])

        x = np.where(x < 0.5, 0.5, x)
        y = np.where(y < 0.5, 0.5, y)
        
        x = np.where(x > (self.NX-2) + 0.5,
                     (self.NX-2) + 0.5, x)
        y = np.where(y > (self.NY-2) + 0.5,
                     (self.NY-2) + 0.5, y)

        i0 = x.astype(int); j0 = y.astype(int)
        i1 = i0 + 1; j1 = j0 + 1

        s1 = x - i0; t1 = y - j0
        s0 = 1 - s1; t0 = 1 - t1
        
        return (s0 * (t0 *  f[ i0, j0 ] + t1 *  f[ i0, j1 ])
              + s1 * (t0 *  f[ i1, j0 ] + t1 *  f[ i1, j1 ]))
    # end nonlinear_advect_implicit_2d

    
    def nonlinear_advect_implicit_periodic_2d(self, f, fx,fy,
                                              XX,YY):
        """Advection by 2D field (fx,fy) of any component of a 2D field (f), with periodic boundaries, by cell-centered back-tracking and applying necessary weights."""

        x = XX - (self.DT/self.DX * fx[1:-1,1:-1])
        y = YY - (self.DT/self.DY * fy[1:-1,1:-1])

        x = x % (self.NX - 2)
        y = y % (self.NY - 2)

        i0 = x.astype(int); j0 = y.astype(int)
        i1 = i0 + 1; j1 = j0 + 1

        s1 = x - i0; t1 = y - j0
        s0 = 1 - s1; t0 = 1 - t1
        
        return (s0 * (t0 *  f[ i0, j0 ] + t1 *  f[ i0, j1 ])
             +  s1 * (t0 *  f[ i1, j0 ] + t1 *  f[ i1, j1 ]))
    # end nonlinear_advect_implicit_periodic_2d

        
    def diffuse_explicit_2d(self, f):
        """Performs diffusion of a 2D field,
        by explicit central differencing;
        viscosity is assumed to be constant."""

        return self.DT*self.central_diff_2nd_2d(f, self.NU,
                                                self.NU)
    # end diffuse_explicit_2d

    
    def diffuse_implicit_2d(self, f0,f, diff_coeff):
        """Performs diffusion of a 2D field implicitly; diff_coef (NU or ETA is assumed to be constant."""

        return ( (f0[1:-1,1:-1]

+ (diff_coeff*self.DT)/(self.DX**2 * self.DY**2)

* (self.DY**2 * (f[2:  , 1:-1] + f[ :-2, 1:-1])
+  self.DX**2 * (f[1:-1, 2:  ] + f[1:-1,  :-2])) )

/ (1 + (2*diff_coeff*self.DT) / (self.DX**2 * self.DY**2)
                           * (self.DY**2 + self.DX**2)) )
    # end diffuse_implicit_2d

    
    def apply_pressure_2dX(self, p, c):
        """Applies the pressure gradient to the x-component of a 2D field, by central differencing; c is assumed to be
        constant (density or magnetic permeability)."""

        return self.DT*self.central_diff_1st_2dX(p, c)
    # end apply_pressure_2dX

    
    def apply_pressure_2dY(self, p, c):
        """Applies the pressure gradient to the y-component of a 2D field, by central differencing; c is assumed to be
        constant (density or magnetic permeability)."""

        return self.DT*self.central_diff_1st_2dY(p, c)
    # end apply_pressure_2dY

    
    def apply_force_2d(self, g):
        """Applies the acceleration due to a force [such as gravity] (g) to a component of a 2D field (f)."""

        return self.DT*g[ 1:-1, 1:-1 ]
    # end apply_force_2d

    
    def calc_source_2d(self, u,v):
        """Calculates the source term of the pressure poisson equation; for the divergence terms."""

        return (self.central_diff_1st_2dX(u, self.RHO/self.DT)  
              + self.central_diff_1st_2dY(v, self.RHO/self.DT) )
    # end calc_source_2d

    def SOR_pressure_CFD_2d(self, p, u,v, beta):
        p[1:-1,1:-1] = beta*((p[2:,1:-1] + p[:-2,1:-1] +
                              p[1:-1,2:] + p[1:-1,:-2] ) / 4.0 +
         (self.DX/self.DT)*(u[1:-1,1:-1] - u[:-2,1:-1] +
                             v[1:-1,1:-1] - v[1:-1,:-2]) / 4.0 ) + \
                             (1-beta)*p[1:-1,1:-1]
        return p
    
    def relax_pressure_poisson_2d(self, p, src):
        """Solves the poisson equation for a 2D pressure field by central differencing in both dimensions. This solves
        the laplace equation for a 2D pressure field
        when src=0"""

        p[1:-1, 1:-1] = ((self.DY**2 *
                        (p[2:  , 1:-1] + p[ :-2, 1:-1])
                      +   self.DX**2 *
                        (p[1:-1, 2:  ] + p[1:-1,  :-2])
                         
                      -   self.DX**2 * self.DY**2 *
                        src[1:-1,1:-1])

                      / (2*(self.DX**2 + self.DY**2)) )
        return p
    # end relax_pressure_poisson_2d
    

    def transform_pressure_poisson_2d(self, p, src):
        """Solves the poisson equation for a 2D pressure field by the Fast Fourier Transform (fft). This solves the laplace equation for a 2D pressure field when src=0"""

        srcTrans = np.fft.fft2(src[1:-1,1:-1])

        kx,ky = np.meshgrid(np.fft.fftfreq(self.NX-2,
                                           d=self.DX),
                            np.fft.fftfreq(self.NY-2,
                                           d=self.DY))
        
        denom = 1.0/(4 - 2*np.cos(2*np.pi*kx*self.DX)
                       - 2*np.cos(2*np.pi*ky*self.DY))
        denom[0,0] = 0

        p[1:-1,1:-1] = np.real_if_close(np.fft.ifft2(-srcTrans*
                                    denom*self.DX*self.DY))

        return p
    # end transform_pressure_poisson_2d

    
    def mag_curl_term_2dX(self, u,v, Bx,By):
        """Applies the x-component of curl(u x B) to evolve
        the x-component of the magnetic field."""

        return self.DT*(
        By[1:-1,1:-1]*( u[1:-1,2:] -  u[1:-1,:-2])/self.DY
    +    u[1:-1,1:-1]*(By[1:-1,2:] - By[1:-1,:-2])/self.DY
    -   Bx[1:-1,1:-1]*( v[1:-1,2:] -  v[1:-1,:-2])/self.DY
    +    v[1:-1,1:-1]*(Bx[1:-1,2:] - Bx[1:-1,:-2])/self.DY
                       )
    # end mag_curl_term_2dX

    
    def mag_curl_term_2dY(self, u,v, Bx,By):
        """Applies the y-component of curl(u x B) to evolve
        the y-component of the magnetic field."""

        return self.DT*(
       -By[1:-1,1:-1]*( u[2:,1:-1] -  u[:-2,1:-1])/self.DX
    +    u[1:-1,1:-1]*(By[2:,1:-1] - By[:-2,1:-1])/self.DX
    -   Bx[1:-1,1:-1]*( v[2:,1:-1] -  v[:-2,1:-1])/self.DX
    +    v[1:-1,1:-1]*(Bx[2:,1:-1] - Bx[:-2,1:-1])/self.DX
                       )
    # end mag_curl_term_2dY

    
    def mag_diffuse_2d(self, fx,fy):
        """Performs diffusion of a 2D field, by central differencing; resistivity and permeability are assumed to be constant."""

        return np.array([self.DT*self.central_diff_2nd_2d(fx,
                         self.ETA/self.MU, self.ETA/self.MU),
                         self.DT*self.central_diff_2nd_2d(fy,
                         self.ETA/self.MU,self.ETA/self.MU)])
    # end mag_diffuse_2d

    
    def mag_diffuse_implicit_2d(self, Bx,By):
        """Performs implicit diffusion of the magnetic field; resistivity and permeability are assumed to be constant"""
                
        const = (self.ETA/self.MU*self.DT) / \
                (self.DX**2 * self.DY**2)

        return np.array([Bx[1:-1,1:-1] / (
                    (1+2*const*(self.DY**2+self.DX**2)))
+ const / (    (1+2*const*(self.DY**2+self.DX**2)))
    *(self.DY**2*(Bx[2:,1:-1]+Bx[:-2,1:-1])
+ self.DX**2*(Bx[1:-1,2:]+Bx[1:-1,:-2])), 

                         By[1:-1,1:-1] / (
                    (1+2*const*(self.DY**2+self.DX**2)))
+ const / (    (1+2*const*(self.DY**2+self.DX**2)))
    *(self.DY**2*(By[2:,1:-1]+By[:-2,1:-1])
+ self.DX**2*(By[1:-1,2:]+By[1:-1,:-2]))])
    # end mag_diffuse_implicit_2d

    def set_bnds_fixed_2d(self, f, amt):
        """Sets all walls of input 2d numpy array to a fixed amount of type int or float for Dirichlet boundary conditions."""

        f[ 0, : ] = amt; f[ -1,  : ] = amt
        f[ :, 0 ] = amt; f[  :, -1 ] = amt

        return f
    # end set_bnds_fixed_2d
    
    def set_bnds_fixed_2dXI(self, f, amt):
        """Sets initial wall along x of input 2d numpy array to a fixed amount of type int or float for Dirichlet (value) or Neumann (zero flux) or periodic boundary conditions."""

        f[ 0, : ] = amt

        return f
    # end set_bnds_fixed_2dXI

    def set_bnds_fixed_2dXF(self, f, amt):
        """Sets final wall along x of input 2d numpy array to a fixed amount of type int or float for Dirichlet (value) or Neumann (zero flux) boundary conditions."""

        f[ -1,  : ] = amt

        return f
    # end set_bnds_fixed_2dXF

    def set_bnds_fixed_2dYI(self, f, amt):
        """Sets initial wall along y of input 2d numpy array to a fixed amount of type int or float for Dirichlet (value) or Neumann (zero flux) or periodic boundary conditions."""

        f[ :, 0 ] = amt

        return f
    # end set_bnds_fixed_2dYI

    def set_bnds_fixed_2dYF(self, f, amt):
        """Sets final wall along y of input 2d numpy array to a fixed amount of type int or float for Dirichlet (value) or Neumann (zero flux) boundary conditions."""

        f[ :, -1 ] = amt

        return f
    # end set_bnds_fixed_2dYF

    def set_bnds_zero_flux_walls_2dX(self, f):
        """Sets zero flux boundary conditions on the walls of a 2D field."""

        f[ 0, : ] = -f[ 1, : ];  f[ -1,  : ] = -f[ -2,  : ]
        f[ :, 0 ] =  f[ :, 1 ];  f[  :, -1 ] =  f[  :, -2 ]

        return f
    # end set_bnds_zero_flux_walls_2dX

    def set_bnds_zero_flux_walls_2dY(self, f):
        """Sets zero flux boundary conditions on the walls of a 2D field."""

        f[ 0, : ] =  f[ 1, : ];  f[ -1,  : ] =  f[ -2,  : ]
        f[ :, 0 ] = -f[ :, 1 ];  f[  :, -1 ] = -f[  :, -2 ]

        return f
    # end set_bnds_zero_flux_walls_2dY

    def set_bnds_zero_flux_walls_scalar_2d(self, f):
        """Sets zero flux boundary conditions on the walls of a 2D field."""

        f[ 0, : ] =  f[ 1, : ];  f[ -1,  : ] =  f[ -2,  : ]
        f[ :, 0 ] =  f[ :, 1 ];  f[  :, -1 ] =  f[  :, -2 ]

        return f
    # end set_bnds_zero_flux_walls_scalar_2d

    def set_bnds_zero_flux_corners_2d(self, f):
        """Sets zero flux boundary conditions on the corners of a 2D field."""
        
        f[  0,  0 ] = (f[  1,  0 ] + f[  0,  1 ]) / 2.0    
        f[ -1,  0 ] = (f[ -2,  0 ] + f[ -1,  1 ]) / 2.0
        f[  0, -1 ] = (f[  1, -1 ] + f[  0, -2 ]) / 2.0
        f[ -1, -1 ] = (f[ -2, -1 ] + f[ -1, -2 ]) / 2.0
        
        return f
    # end set_bnds_zero_flux_corners_2d

    def set_bnds_periodic_diffusion_2dX(self, g):
        """Sets periodic boundary conditions along the x-dimension for any component of a 2D field (f) specifically for explicit central differencing diffusion of the input field (g) which has values of f at the old time step."""

        f  = self.NU*(self.DT/self.DX**2
    * (g[  0, 1:-1 ] - 2*g[ -1, 1:-1 ] + g[ -2, 1:-1 ]))
                                        
        f += self.NU*(self.DT/self.DY**2
    * (g[ -1, 2:   ] - 2*g[ -1, 1:-1 ] + g[ -1,  :-2 ]))
        
        return f
    # end set_bnds_periodic_diffusion_2dX

    def set_bnds_periodic_diffusion_2dY(self, g):
        """Sets periodic boundary conditions along the y-dimension for any component of a 2D field (f) specifically for explicit central differencing diffusion of the input field (g) which has values of f at the old time step."""

        f  = self.NU*(self.DT/self.DX**2
    * (g[ 2:  , -1 ] - 2*g[ 1:-1, -1 ] + g[  :-2, -1 ]))
            
        f += self.NU*(self.DT/self.DY**2
    * (g[ 1:-1,  0 ] - 2*g[ 1:-1, -1 ] + g[ 1:-1, -2 ]))
                              
        return f
    # end set_bnds_periodic_diffusion_2dY

    def set_bnds_periodic_diffusion_corners_2d(self, f,g):
        """Sets periodic boundary conditions of the corners for any component of a 2D field (f) specifically for explicit central differencing diffusion of the input field (g) which has values of f at the old time step."""
        f[  0,  0 ] += self.DT * (self.NU *
       (g[  1,  0 ] - 2*g[  0,  0 ] + g[ -1,  0 ]) / self.DX**2
                                 )
        f[  0,  0 ] += self.DT * (self.NU *
       (g[  0,  1 ] - 2*g[  0,  0 ] + g[  0, -1 ]) / self.DY**2
                                 )
        
        f[ -1,  0 ] += self.DT * (self.NU *
       (g[  0,  0 ] - 2*g[ -1,  0 ] + g[ -2,  0 ]) / self.DX**2
                                 )                                   
        f[ -1,  0 ] += self.DT * (self.NU *
       (g[ -1,  1 ] - 2*g[ -1,  0 ] + g[ -1, -1 ]) / self.DY**2
                                 )
        
        f[  0, -1 ] += self.DT * (self.NU *
       (g[  1, -1 ] - 2*g[  0, -1 ] + g[ -1, -1 ]) / self.DX**2
                                 )
        f[  0, -1 ] += self.DT * (self.NU *
       (g[  0,  0 ] - 2*g[  0, -1 ] + g[  0, -2 ]) / self.DY**2
                                 )

        f[ -1, -1 ] += self.DT * (self.NU *
       (g[  0, -1 ] - 2*g[ -1, -1 ] + g[ -2, -1 ]) / self.DX**2
                                 )                                   
        f[ -1, -1 ] += self.DT * (self.NU *
       (g[ -1,  0 ] - 2*g[ -1, -1 ] + g[ -1, -2 ]) / self.DY**2
                                 )
        return f
    # end set_bnds_periodic_diffusion_corners_2d

    def set_bnds_periodic_apply_pressure_2dX(self, fx,fy, p):
        """Sets periodic boundary conditions along the x-dimension for a 2D field (f) specifically for a pressure gradient."""

        fx[ -1 , 1:-1 ] -= self.DT/(2*self.RHO*self.DX)*(
                            p[  0 , 1:-1 ] - p[  -2 , 1:-1 ])

        fy[ -1 , 1:-1 ] -= self.DT/(2*self.RHO*self.DY)*(
                            p[ -1 , 2:   ] - p[  -1 ,  :-2 ])
        return [fx, fy]
    # end set_bnds_periodic_apply_pressure_2dX

    def set_bnds_periodic_apply_pressure_2dY(self, fx,fy, p):
        """Sets periodic boundary conditions along the y-dimension for a 2D field (f) specifically for a pressure gradient."""

        fx[ 1:-1,  -1 ] -= self.DT/(2*self.RHO*self.DX)*(
                            p[ 2:  ,  -1 ] - p[  :-2,  -1 ])

        fy[ 1:-1,  -1 ] -= self.DT/(2*self.RHO*self.DY)*(
                            p[ 1:-1,   0 ] - p[ 1:-1 , -2 ])
        return [fx, fy]
    # end set_bnds_periodic_apply_pressure_2dY

    def set_bnds_periodic_apply_force_2dX(self, f,g):
        """Sets periodic boundary conditions along the x-dimension for a 2D field (f) specifically for the acceleration due to an external force."""

        f[ -1 , 1:-1 ] += self.DT * g[ -1, 1:-1 ]

        return f
    # end set_bnds_periodic_apply_force_2dX

    def set_bnds_periodic_apply_force_2dY(self, f,g):
        """Sets periodic boundary conditions along the y-dimension for a 2D field (f) specifically for the acceleration due to an external force."""
            
        f[ 1:-1, -1 ] += self.DT * g[ 1:-1, -1 ]

        return f
    # end set_bnds_periodic_apply_force_2dY

    def set_bnds_periodic_src_2dX(self, src, u,v):
        """Sets boundary conditions along the x-dimension for the source term of the poisson eqn of velocity in the navier-stokes equation."""
        
        src[ -1, 1:-1 ] = self.RHO*(1.0/self.DT*(
            (u[  0, 1:-1 ] - u[ -2, 1:-1 ])/(2*self.DX)
      +     (v[ -1, 2:   ] - v[ -1,  :-2 ])/(2*self.DY)
                                      )
      -    ((u[  0, 1:-1 ] - u[ -2, 1:-1 ]) / (2*self.DX))**2
      -  2*((u[ -1, 2:   ] - u[ -1,  :-2 ]) / (2*self.DY)
      *     (v[  0, 1:-1 ] - v[ -2, 1:-1 ]) / (2*self.DX))
      -    ((v[ -1, 2:   ] - v[ -1,  :-2 ]) / (2*self.DY))**2
                                   )
        ##set first equal to last
        src[ 0, 1:-1 ] = src[ -1, 1:-1 ]

        return src
    # end set_bnds_periodic_src_2dX

    def set_bnds_periodic_src_2dY(self, src, u,v):
        """Sets boundary conditions along the y-dimension for the source term of the poisson eqn of velocity in the navier-stokes equation."""
        
        src[ 1:-1, -1 ] = self.RHO*(1.0/self.DT*(
            (u[ 2:  , -1 ] - u[  :-2, -1 ]) / (2*self.DX)
      +     (v[ 1:-1,  0 ] - v[ 1:-1, -2 ]) / (2*self.DY)
                                                )
      -    ((u[ 2:  , -1 ] - u[  :-2, -1 ]) / (2*self.DX))**2
      -  2*((u[ 1:-1,  0 ] - u[ 1:-1, -2 ]) / (2*self.DY)
      *     (v[ 2:  , -1 ] - v[  :-2, -1 ]) / (2*self.DX))
      -    ((v[ 1:-1,  0 ] - v[ 1:-1, -2 ]) / (2*self.DY))**2
                                   )
        ##set first equal to last
        src[ 1:-1, 0 ] = src[ 1:-1, -1 ]

        return src
    # end set_bnds_periodic_src_2dY

    def set_bnds_periodic_src_div_only_2dX(self, src, u,v):
        """Sets boundary conditions along the x-dimension for the source term of the poisson eqn of velocity in the navier-stokes equation."""
        
        src[ -1, 1:-1 ] = self.RHO*(1.0/self.DT*(
            (u[  0, 1:-1 ] - u[ -2, 1:-1 ])/(2*self.DX)
      +     (v[ -1, 2:   ] - v[ -1,  :-2 ])/(2*self.DY)
                                      )
                               )
        ##set first equal to last
        src[ 0, 1:-1 ] = src[ -1, 1:-1 ]

        return src
    # end set_bnds_periodic_src_div_only_2dX

    def set_bnds_periodic_src_div_only_2dY(self, src, u,v):
        """Sets boundary conditions along the y-dimension for the source term of the poisson eqn of velocity in the navier-stokes equation."""
        
        src[ 1:-1, -1 ] = self.RHO*(1.0/self.DT*(
            (u[ 2:  , -1 ] - u[  :-2, -1 ]) / (2*self.DX)
      +     (v[ 1:-1,  0 ] - v[ 1:-1, -2 ]) / (2*self.DY)
                                                )
                               )
        ##set first equal to last
        src[ 1:-1, 0 ] = src[ 1:-1, -1 ]

        return src
    # end set_bnds_periodic_src_div_only_2dY

    def set_bnds_periodic_pressure_2dX(self, p,p_old, src):
        """Sets periodic boundary conditions along the x-dimension for pressure for the navier-stokes equations."""
            ## first in x
        p[ -1, 1:-1 ]  = ( self.DY**2 /
( 2*(self.DX**2 + self.DY**2) ) *
(p_old[  0, 1:-1 ] + p_old[ -2, 1:-1 ]) )
                           
            ## now in y
        p[ -1, 1:-1 ] += ( self.DX**2 /
( 2*(self.DX**2 + self.DY**2) )
* (p_old[ -1, 2:   ] + p_old[ -1,  :-2 ]) )
                           
            ## last, the source
        p[ -1, 1:-1 ] -= (src[ -1, 1:-1 ] *
self.DX**2 * self.DY**2
/ (2*(self.DX**2 + self.DY**2)) )
        
            ##set first equal to last
        p[ 0, 1:-1 ] = p[ -1, 1:-1 ]

        return p
    # end set_bnds_periodic_pressure_2dX

    def set_bnds_periodic_pressure_2dY(self, p,p_old, src):
        """Sets periodic boundary conditions along the y-dimension for
        pressure for the navier-stokes equations."""
            ## first in x
        p[ 1:-1, -1 ]  = (self.DY**2 / ( 2*(self.DX**2 + self.DY**2) )
                       * (p_old[ 2:  , -1 ] + p_old[  :-2, -1 ]) )
            ## now in y
        p[ 1:-1, -1 ] += (self.DX**2 / ( 2*(self.DX**2 + self.DY**2)) 
                       * (p_old[ 1:-1,  0 ] + p_old[ 1:-1, -2 ]) )
                           
            ## last, the source
        p[ 1:-1, -1 ] -= (src[ 1:-1, -1 ] * self.DX**2 * self.DY**2
                           / (2*(self.DX**2 + self.DY**2)) )
        
            ##set first equal to last
        p[ 1:-1, 0 ] = p[ 1:-1, -1 ]

        return p
    # end set_bnds_periodic_pressure_2dY
       
# end The_Fluid_Solver_2D

## end the_fluid_solver_2d.py
