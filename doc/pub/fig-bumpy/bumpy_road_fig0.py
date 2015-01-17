import numpy as np
from pysketcher import *

R = 1; H = 2; w_1 = 5
drawing_tool.set_coordinate_system(
    xmin=-3*R, xmax= 6*w_1, ymin=-2, ymax=7*H,
    axis=True)

# Elements related to the road
import sympy as sp
x = sp.symbols('x')
h = 0.5*sp.sin(1.5*x) + 1   # mean road elevation
dh  = sp.diff(h, x)
d2h = sp.diff(h, x, x)
# Turn symbolic expressions to Python functions
h   = sp.lambdify([x], h,   modules='numpy')
dh  = sp.lambdify([x], dh,  modules='numpy')
d2h = sp.lambdify([x], d2h, modules='numpy')

road_xmin = -2*R
road_xmax = 6*w_1

road = Wavy(main_curve=h,
            interval=[road_xmin, road_xmax],
            wavelength_of_perturbations=1,
            amplitude_of_perturbations=0,
            smoothness=0)

tp = np.linspace(0, 15, 25)     # number of animation frames
dt = tp[1] - tp[0]              # delta t for animation frames
v = 2.0                         # velocity (constant)

# Vertical displacement calculation
m = 2                           # mass of the system
b = 0.8                         # friction parameter
k = 2                           # spring parameter
V = 1.5
T = road_xmax/v                 # end time
t = np.linspace(0, T, 101)      # numerical time mesh
s = lambda u: k*u               # restoring force of spring
F = lambda t: -m*d2h(v*t)       # excitation force

import sys, os
sys.path.insert(0, os.path.join(os.pardir, 'src-bumpy'))
import solver

print road_xmax, T, v, v*T

u, t = solver.solver(I=0, V=V, m=m, b=b, s=s, F=F, t=t,
                     damping='linear')

'''
# if you want to see plot of solver function, turn me on
import matplotlib.pyplot as plt
plt.plot(t, u)
plt.show()
'''
u_solution = Curve(v*t, 5*H + 0.5*H*u)

over  = Rectangle(lower_left_corner=(-1.5*R, 2*H),width=3*R, height=.75*H)

tire = Composition({
    'wheel': Circle(center=(0, 0), radius=R),
    'cross': Composition({'cross1': Line((0,-1),(0,R)),
                          'cross2': Line((-R,0),(R,0))})})

wheel = Circle(center=(0, 0), radius=R)
device = Composition({'over':over,'tire':tire })

fig = Composition({'fig': Composition(
    {'device': device, 'road': road, 'solution': u_solution})})

# colorize & patterns & Styles
fig['fig']['device']['over'].set_linecolor('black')
fig['fig']['device']['over'].set_filled_curves('black')

dev = fig['fig']['device']
dev['tire']['wheel'].set_linecolor('black')
dev['tire']['wheel'].set_filled_curves('red')
dev['tire'].set_linecolor('black')
dev['tire'].set_linewidth(1)

fig['fig']['road'].set_linecolor('green')
fig['fig']['road'].draw()
fig['fig']['solution'].set_linecolor('blue').set_linestyle('dashed').set_linewidth(1)


# Calculating the center of Circle in every frame
X_Touch = linspace(0, road_xmax, len(t))
X = np.zeros(len(X_Touch))
H = np.zeros(len(X_Touch))

for j in xrange(len(X_Touch)):
    theta_Touch = dh(X_Touch[j])
    L = R*sin(theta_Touch)
    Y_C = R*cos(theta_Touch)
    X[j] = X_Touch[j]-L
    H[j] = h(X_Touch[j])+Y_C

    j+=1

dev=fig['fig']['device']
dev.translate((X[0],H[0]))
dev.draw()

import numpy
from math import degrees
i = 1

def Move(t, fig):

    x = X[i]
    h = H[i]
    x_prev = X[i-1]
    h_prev = H[i-1]

    # Device movement and Rotation
    global w_1,i,H,X
    fig['fig']['device'].translate((x-x_prev,h-h_prev))

    angle = - sqrt((x-x_prev)**2 + (h-h_prev)**2)/R
    fig['fig']['device']['tire'].rotate(degrees(angle),
                                        center=(x,h))

    # vertical vibration
    Myspring=Spring(start=(x,h+R),length=2+R+u[i],width=R,
                    bar_length=.1,num_windings=6, teeth=True)
    Myspring.set_linecolor('black')
    Myspring.draw()

    sHolder = Rectangle(lower_left_corner=(x-0.15*R,h+R),
                        width=.3*R, height=2+R+u[i])
    sHolder.set_linecolor('black')
    sHolder.set_filled_curves('black')
    #sHolder.draw()

    fig['fig']['device']['over'].translate((0,u[i]-u[(i-1)]))

    i+=1

animate(fig, t[:int(0.9*len(t))], Move, moviefiles=True, pause_per_frame=1)
from scitools.std import movie
movie('tmp_frame_*.png',encoder='html',fps=2,output_file='Movie1.html')
