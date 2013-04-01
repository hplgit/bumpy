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
