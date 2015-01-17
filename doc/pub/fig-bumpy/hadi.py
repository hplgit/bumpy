
from pysketcher import *

R=1; H=2; w_1=5
drawing_tool.set_coordinate_system(xmin=-3*R, xmax= 6*w_1 ,ymin=-2, ymax=5*H,axis=True)

# Elements related to Road
h  =lambda x: 0.5*sin(1.5*x) +1   # Road function
dh =lambda x: 0.75*cos(1.5*x)     # first-order
ddh=lambda x: -1.125*sin(1.5*x)   # second-order

Road = Wavy(main_curve= h,
             interval=[-2*R,6*w_1],
             wavelength_of_perturbations=1,
             amplitude_of_perturbations=0,
             smoothness=0)

tp = linspace(0, 15, 25)        # number of animation frames
dt = tp[1] - tp[0]              # delta t
v=lambda t: 2*t                 # velocity function

# Displacement Function
from solver import *
m=2                             # mass of the system
b=0.8                           # friction parameter
k=2                             # spring parameter
V=1.5
t=linspace(0,25,41)
s =lambda u: k*u                # restoring force of spring
F =lambda t: -m*ddh(v(t)*t)

# solver function --> you can change damping mode from 'linear'
# to 'quadratic' the result would be changed
u,t = solver(I=0, V=V, m=m, b=b, s=s, F=F, t=t,damping='linear')

'''
# if you want to see plot of solver function,turn me on
import matplotlib.pyplot as plt
plt.plot(t, u)
plt.show()
'''

#My figure
over  = Rectangle(lower_left_corner=(-1.5*R, 2*H),width=3*R, height=.75*H)

tire = Composition({
    'wheel': Circle(center=(0, 0), radius=R),
    'cross': Composition({'cross1': Line((0,-1),(0,R)),
                          'cross2': Line((-R,0),(R,0))})})

wheel=Circle(center=(0, 0), radius=R)
device=Composition({'over':over,'tire':tire })

fig=Composition({'fig':Composition({'device':device,'road':Road})})

# colorize & patterns & Styles
fig['fig']['device']['over'].set_linecolor('black')
fig['fig']['device']['over'].set_filled_curves(pattern='/')

fig['fig']['device']['tire']['wheel'].set_linecolor('black')
fig['fig']['device']['tire']['wheel'].set_filled_curves('red')
fig['fig']['device']['tire'].set_linecolor('black')
fig['fig']['device']['tire'].set_linewidth(1)

fig['fig']['road'].set_linecolor('green')
fig['fig']['road'].draw()

dev=fig['fig']['device']

# Calculating the center of Circle in every frame
X_Touch=linspace(0, 6*w_1,28)
X=zeros(len(X_Touch))
H=zeros_like(X)

for j in xrange(len(X_Touch)):
    theta_Touch=dh(X_Touch[j])
    L=R*sin(theta_Touch)
    Y_C=R*cos(theta_Touch)
    X[j]=X_Touch[j]-L
    H[j]=h(X_Touch[j])+Y_C

    j+=1

dev=fig['fig']['device']
dev.translate((X[0],H[0]))
dev.draw()

import numpy
from math import degrees
i=1
def Move(t,fig):

    # Device movement and Rotation
    global w_1,i,H,X
    fig['fig']['device'].translate((X[i]-X[i-1],H[i]-H[i-1]))

    x_displace= dt * v(t)
    angle = - x_displace/2*R
    fig['fig']['device']['tire'].rotate(degrees(angle),
                                        center=(X[i],H[i]))

    # vertical vibration
    Myspring=Spring(start=(X[i],H[i]+R),length=2+R+u[i],width=R,
                    bar_length=.1,num_windings=6, teeth=True)
    Myspring.set_linecolor('black')
    Myspring.draw()

    sHolder = Rectangle(lower_left_corner=(X[i]-0.15*R,H[i]+R),
                        width=.3*R, height=2+R+u[i])
    sHolder.set_linecolor('black')
    sHolder.set_filled_curves('black')
    sHolder.draw()


    fig['fig']['device']['over'].translate((0,u[i]-u[(i-1)]))

    i+=1

animate(fig, tp, Move, moviefiles=True,pause_per_frame=0)
from scitools.std import movie
movie('tmp_frame_*.png',encoder='html',fps=2,output_file='Movie1.html')
