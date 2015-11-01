"""
Make animation of vehicle on bumpy road. Sketch the vehicle and the
surroundings. Then solve the differential equations for the vertical
oscillatory motion, feed the solution to the sketch, and move
the sketch to the right.
"""

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
road_xmax = 15*w_1
n = road_xmax*10

road = Wavy(main_curve=h,
            interval=[road_xmin, road_xmax],
            wavelength_of_perturbations=8,
            amplitude_of_perturbations=0.25,
            smoothness=0).set_linecolor('green')

v = 2.0                         # velocity (constant)

# Vertical displacement calculation
m = 2                           # mass of the system
b = 0.2                         # friction parameter
k = 1.5                         # spring parameter
T = road_xmax/v                 # end time
t = np.linspace(0, T, n+1)      # numerical time mesh
s = lambda u: k*u               # restoring force of spring
F = lambda t: -m*d2h(v*t)       # excitation force

import sys, os
sys.path.insert(0, os.path.join(os.pardir, 'src-bumpy'))
import solver

u, t = solver.solver(I=0, V=0, m=m, b=b, s=s, F=F, t=t,
                     damping='linear')

u_amplitude = (u.max() - u.min())/2
u_scaled = R*u/u_amplitude
u_solution = Curve(v*t, 5*H + u_scaled).set_linecolor('blue').set_linewidth(1)

arc_length = 0  # arc_length along road

def draw_vehicle(x, y, x0, y0, u):
    mass_width = 3*R
    mass_height = 1.5*R
    spring_length = 3*R
    spring_start = (x, y+2*R)

    tire_center = point(x, y+R)
    tire = Composition({
        'wheel': Circle(center=tire_center, radius=R),
        'cross': Composition({'cross1': Line((x,y),(x,y+2*R)),
                              'cross2': Line((x-R,y+R),(x+R,y+R))})})
    global arc_length
    arc_length += sqrt((x-x0)**2 + (y-y0)**2)
    angle = - arc_length/R
    tire.rotate(degrees(angle), center=tire_center)
    spring = Spring(start=tire_center + point(0,R),
                    length=spring_length+u, width=R,
                    bar_length=.1, num_windings=6, teeth=True)
    spring.set_linecolor('black')
    mass = Rectangle(
        lower_left_corner=(x - mass_width/2.0,
                           spring.geometric_features()['end'][1]),
        width=mass_width, height=mass_height)

    tire.set_linecolor('black').set_filled_curves('red').set_linewidth(1)
    mass.set_linecolor('black').set_filled_curves('black')
    vehicle = Composition({'tire': tire,
                           'mass': mass,
                           'spring': spring,
                           })

    # Is the tire below or above the road? Adjust the height!
    bumps = road(vehicle['tire']['wheel']['arc'].x)
    below = (bumps - vehicle['tire']['wheel']['arc'].y).max()
    vehicle.translate((0, below))

    return vehicle


import numpy
from math import degrees
i = 1
x = 0

def move(t, fig):
    global x, i
    x_1 = x
    x = v*t
    y = h(x)
    y_1 = h(x_1)
    drawing_tool.set_coordinate_system(
        xmin=x-5*R, xmax=x+3*w_1, ymin=-2, ymax=7*H,
        axis=True, new_figure=False)

    fig['vehicle'] = draw_vehicle(x, y, x_1, y_1, u_scaled[i])
    fig.draw()
    i+=1

fig = Composition({'road': road, 'solution': u_solution,
                   'vehicle': draw_vehicle(0, h(0), 0, h(0), 0)})

show = True
try:
    if sys.argv[1] == 'batch':
        show = False
except:
    pass

title = 'm=%g, b=%g, k=%g' % (m, b, k)
animate(fig, t[:int(0.9*len(t))], move, moviefiles=True, pause_per_frame=0.2,
        show_screen_graphics=show, title=title)
from scitools.std import movie
movie('tmp_frame_*.png',encoder='html',fps=2,output_file='index.html')
