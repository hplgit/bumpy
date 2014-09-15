import numpy as np
from matplotlib.pyplot import *
data = np.loadtxt('bumpy.dat.gz')
x = data[0]
n = len(x)
m = n/40
h = data[1:]
for i in range(len(h)):
    plot(x[:m], h[i][:m])
legend(['Curve 0', 'Curve 1', 'Curve 2'])
title('Curves in class pysketcher.StochasticWavyCurve')
savefig('tmp.png')
savefig('tmp.pdf')

def write_array(a):
    s = 'np.array(['
    for e in a:
        s += '%.4f, ' % e
    s += '])'
    return s

f = open('tmp.py', 'w')
f.write("""
x = %s
y = [None]*3
y[0] = %s
y[1] = %s
y[2] = %s
""" % (write_array(x[:m]), write_array(h[0][:m]), write_array(h[1][:m]), write_array(h[2][:m])))
f.close()
from scitools.avplotter import Plotter
p = Plotter(-0.15, 0.17, width=70)
for i in range(3):
    print '-'*70
    for x_, h_ in zip(x[:m:5], h[i][:m:5]):
        print p.plot(x_, h_)
show()
