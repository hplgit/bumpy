"""Explore the bumpy.py model via making various plots."""

# Import Matlab-style plotting commands + from numpy import *
# using the Matplotlib plotting package
from matplotlib.pylab import *

# Load computed data
import cPickle
outfile = open('bumpy.res', 'r')
data = cPickle.load(outfile)
outfile.close()

x, t = data[0:2]
u_rms = data[-1]

case = 1

# Plot the complete u
figure()
title('Complete time series of u')
plot(t, data[case+2][2])

import sys
try:
    # Show the last part of h, a and u, starting at some
    # user-specified time t_s
    t_s = float(sys.argv[1])
except IndexError:
    # No command-line argument was given, use a default values
    t_s = 180

indices = t >= t_s   # True/False boolean array
t = t[indices]       # fetch the part of t for which t > t_s
x = x[indices]       # fetch the part of x for which t > t_s

# Plot rms value of all u arrays
figure()
u_rms = u_rms[indices]
plot(t, u_rms)
legend(['u'])
xlabel('t')
title('Root mean square value of u(t) functions')
savefig('u_rms.png')

def frequency_analysis(u, t):
    A = fft(u)
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


h, a, u = data[case+2]
h = h[indices]
a = a[indices]
u = u[indices]

figure()
subplot(3, 1, 1)
plot(x, h, 'g-')
legend(['h %d' % case])
hmax = (abs(h.max()) + abs(h.min()))/2
axis([x[0], x[-1], -hmax*5, hmax*5])
xlabel('distance'); ylabel('height')

subplot(3, 1, 2)
plot(t, a)
legend(['a %d' % case])
xlabel('t'); ylabel('acceleration')

subplot(3, 1, 3)
plot(t, u, 'r-')
legend(['u %d' % case])
xlabel('t'); ylabel('displacement')
savefig('hau%d.png' % case)

# Make spectra of u and a
figure()
title('Spectra')
subplot(2, 1, 1)
u = data[case+2][2][indices]
f, A = frequency_analysis(u, t)
plot(f, A)
legend(['u spectrum'])
print 'Dominating frequency u:', f[A.tolist().index(A.max())]

subplot(2, 1, 2)
a = data[case+2][1][indices]
f, A = frequency_analysis(a, t)
plot(f, A)
legend(['a spectrum'])
savefig('spectra.png')
print 'Dominating frequency a:', f[A.tolist().index(A.max())]

show()
