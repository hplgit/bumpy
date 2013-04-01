import numpy as np
cimport numpy as np
import sys, os

cdef class Spring:
    cdef double k

    def __init__(self, k):
        self.k = k

    cpdef force(self, double u):
        return self.k*u

import cython
@cython.boundscheck(False)  # turn off array bounds check
@cython.wraparound(False)   # turn off negative indices (u[-1,-1])
cpdef solver(
    double I,
    double V,
    double m,
    double b,
    Spring s,
    np.ndarray[np.float_t, ndim=1, mode='c'] F,
    np.ndarray[np.float_t, ndim=1, mode='c'] t,
    damping='linear'):
    cdef int N = t.size - 1
    cdef double dt = t[1] - t[0]
    cdef np.ndarray[np.float_t, ndim=1, mode='c'] u = np.zeros(N+1)
    s_ = s.force  # simplify call

    u[0] = I
    if damping == 'linear':
        u[1] = u[0] + dt*V + dt**2/(2*m)*(-b*V - s_(u[0]) + F[0])
    elif damping == 'quadratic':
        u[1] = u[0] + dt*V + \
               dt**2/(2*m)*(-b*V*abs(V) - s_(u[0]) + F[0])

    for n in range(1,N):
        if damping == 'linear':
            u[n+1] = 1./(m + b*dt/2)*(2*m*u[n] + \
                    (b*dt/2 - m)*u[n-1] + dt**2*(F[n] - s_(u[n])))
        elif damping == 'quadratic':
            u[n+1] = (2*m*u[n] - m*u[n-1] + b*u[n]*abs(u[n] - u[n-1])
                      - dt**2*(s_(u[n]) - F[n]))/\
                      (m + b*abs(u[n] - u[n-1]))
    # Putting n loop inside tests does not give better C translation
    return u, t
