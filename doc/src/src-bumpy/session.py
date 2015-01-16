from solver import solver_linear_damping
from numpy import *

def s(u):
    return 2*u

T = 10*pi      # simulate for t in [0,T]
dt = 0.2
N = int(round(T/dt))
t = linspace(0, T, N+1)
F = zeros(t.size)
I = 1; V = 0
m = 2; b = 0.2
u = solver_linear_damping(I, V, m, b, s, F, t)

from matplotlib.pyplot import *
plot(t, u)
savefig('tmp.pdf')   # save plot to PDF file
savefig('tmp.png')   # save plot to PNG file
show()
# End solver_linear_damping

import numpy as np
from numpy import sin, pi  # for nice math
from solver import solver

def F(t):
    # Sinusoidal bumpy road
    return A*sin(pi*t)

def s(u):
    return k*(0.2*u + 1.5*u**3)

A = 0.25
k = 2
t = np.linspace(0, 100, 10001)
u, t = solver(I=0.1, V=0, m=2, b=0.5, s=s, F=F, t=t,
              damping='quadratic')

# Show u(t) as a curve plot
import matplotlib.pyplot as plt
plt.plot(t, u)
plt.savefig('tmp.png')
plt.savefig('tmp.pdf')
plt.show()
