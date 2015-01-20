"""Explore the bumpy.py model via making various plots."""

# Import a Matlab-like environment
from numpy import *
from matplotlib.pyplot import *

# Load computed data
import cPickle
outfile = open('bumpy.res', 'r')
data = cPickle.load(outfile)
outfile.close()

# data = [x, t, [h, a, u], [h, a, u], ..., u_rms]
x, t = data[0:2]

import sys
try:
    # Show the last part of h, a and u, starting at some
    # user-specified time t_s
    t_s = float(sys.argv[1])
except IndexError:
    # No command-line argument was given, use a default value
    t_s = 180

indices = t >= t_s   # True/False boolean array
t = t[indices]       # fetch the part of t for which t >= t_s
x = x[indices]       # fetch the part of x for which t >= t_s

# Plot u for second realization
figure()
realization = 1
u = data[2+realization][2][indices]
plot(t, u)
title('Displacement')
savefig('u1.png')
savefig('u1.pdf')

# Compute and plot velocity in second realization
dt = t[1] - t[0]
v = zeros_like(u)
v[1:-1] = (u[2:] - u[:-2])/(2*dt)
v[0] = (u[1] - u[0])/dt
v[-1] = (u[-1] - u[-2])/dt
figure()
plot(t, v)
legend(['velocity'])
xlabel('t')
title('Velocity')
savefig('v1.png')
savefig('v1.pdf')

# Smooth the velocity (only internal points)
v[1:-1] = (v[2:] + 2*v[1:-1] + v[:-2])/4.0
figure()
plot(t, v)
legend(['smoothed velocity'])
xlabel('t')
title('Velocity')
savefig('v1s.png')
savefig('v1s.pdf')

def frequency_analysis(u, t):
    A = fft.fft(u)
    A = 2*A
    dt = t[1] - t[0]
    N = t.size
    freq = arange(N/2, dtype=float)/N/dt
    A = abs(A[0:freq.size])/N
    # Remove small high frequency part
    tol = 0.05*A.max()
    for i in xrange(len(A)-1, 0, -1):
        if A[i] > tol:
            break
    return freq[:i+1], A[:i+1]

for realization in range(len(data[2:])):
    h, F, u = data[2+realization]
    h = h[indices]
    F = F[indices]
    u = u[indices]

    figure()
    subplot(3, 1, 1)
    plot(x, h, 'g-')
    legend(['h %d' % realization])
    hmax = (abs(h.max()) + abs(h.min()))/2
    axis([x[0], x[-1], -hmax*5, hmax*5])
    xlabel('distance'); ylabel('height')

    subplot(3, 1, 2)
    plot(t, F)
    legend(['F %d' % realization])
    xlabel('t'); ylabel('acceleration')

    subplot(3, 1, 3)
    plot(t, u, 'r-')
    legend(['u %d' % realization])
    xlabel('t'); ylabel('displacement')
    savefig('hFu%d.png' % realization)

    # Make spectra of u and a
    figure()
    title('Spectra')
    subplot(2, 1, 1)
    u = data[2+realization][2][indices]
    f, A = frequency_analysis(u, t)
    plot(f, A)
    legend(['u spectrum'])
    print 'Dominating frequency u:', f[A.tolist().index(A.max())]

    subplot(2, 1, 2)
    a = data[realization+2][1][indices]
    f, A = frequency_analysis(F, t)
    plot(f, A)
    legend(['F spectrum'])
    savefig('spectra%d.png' % realization)
    savefig('spectra%d.pdf' % realization)
    print 'Dominating frequency F:', f[A.tolist().index(A.max())]

show()
