"""Test of bumpy.py for very long time integration."""

from bumpy import bumpy_road, rms
from generate_road_profiles import generate_bumpy_roads
import time, os

filename = 'bumpy.dat.gz'
if not os.path.isfile(filename):
    t0 = time.clock()
    generate_bumpy_roads(L=2000, nroads=3, resolution=3000)
    #generate_bumpy_roads(L=2000, nroads=3, resolution=300)
    t1 = time.clock()
    print 'Generate data:', t1-t0
else:
    t1 = time.clock()

# Note: we tried cpdef s_(u) inside solver.pyx instead of s_ = s.force
# and it did not reduce the CPU time.

#for cy in False, True:
for cy in [True]:
    data = bumpy_road(url=filename, cy=cy)
    t2 = time.clock()
    data = rms(data)
    t3 = time.clock()
    import cPickle
    outfile = open('bumpy.res', 'w')
    cPickle.dump(data, outfile)
    outfile.close()
    t4 = time.clock()

    print 'Cython acceleration:', cy
    print 'Solve equation:', t2-t1
    print 'Compute rms:', t3-t2
    print 'Pickle to file:', t4-t3

"""
Generate data: 11.99
Solve equation: 15.87
Compute rms: 0.01
Pickle to file: 2.54

Generate data: 6.72
Solve equation: 10.74
Compute rms: 0.02
Pickle to file: 3.3
Solve equation, Cython: 2.53
"""

