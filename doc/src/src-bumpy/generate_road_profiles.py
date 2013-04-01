"""
Generate the geometry of a bumpy road.
Method: excite an oscillator with white noise and use the
relatively smooth displacement as the height of the road.
"""
from solver import solver, np

# Generate bumpy road

def generate_bumpy_road(nbumps=12, L=200, resolution=500):
    """Generate one road profile by using a vibration ODE."""
    n = nbumps*resolution      # no of compute intervals along the road
    x = np.linspace(0, L, n+1) # points along the road
    dx = x[1] - x[0]           # step along the road
    white_noise = np.random.randn(n+1)/np.sqrt(dx)
    # Compute h(x)
    k = 1.
    m = 4.
    if dx > 2/np.sqrt(k/m):
        print 'Unstable scheme'
    def s(u):
        return k*u

    h, x = solver(I=0, V=0, m=m, b=3, s=s, F=white_noise,
                  t=x, damping='linear')
    h = h/h.max()*0.2
    return h, x

def generate_bumpy_roads(L, nroads, resolution):
    """Generate many road profiles."""
    np.random.seed(1)
    nbumps = int(L/30.)
    h_list = []
    for i in range(3):
        h, x = generate_bumpy_road(nbumps, L, resolution)
        h_list.append(h)
    h_list.insert(0, x)
    data = np.array(h_list)
    np.savetxt('bumpy.dat.gz', data)  # saves in gzip'ed format

if __name__ == '__main__':
    generate_bumpy_roads(L=2000, nroads=3, resolution=500)
