import sys, os
import numpy as np

def bumpy_road(url=None, m=60, b=80, k=60, v=5, cy=False):
    """
    Solve model for verticle vehicle vibrations.

    =========   ==============================================
    variable    description
    =========   ==============================================
    url         either URL of file with excitation force data,
                or name of a local file
    m           mass of system
    b           friction parameter
    k           spring parameter
    v           (constant) velocity of vehicle
    cy          Cython version of function solver
    Return      data (list) holding input and output data
                [x, t, [h,a,u], [h,a,u], ...]
    =========   ==============================================
    """
    # Download file (if url is not the name of a local file)
    if url.startswith('http://') or url.startswith('file://'):
        import urllib
        filename = os.path.basename(url)  # strip off path
        urllib.urlretrieve(url, filename)
    else:
        # Check if url is the name of a local file
        filename = url
        if not os.path.isfile(filename):
            print url, 'must be a URL or a filename'
            sys.exit(1)
        # else: ok

    # Load file data into array h_data
    try:
        h_data = np.loadtxt(filename)  # read numpy array from file
    except ValueError:
        print 'Wrong format in file', url
        sys.exit(1)

    x = h_data[0,:]                # 1st column: x coordinates
    h_data = h_data[1:,:]          # other columns: h shapes

    t = x/v                        # time corresponding to x
    dt = t[1] - t[0]
    if dt > 2/np.sqrt(k/float(m)):
        print 'Unstable scheme'

    if cy:
        from solver_cy import solver, Spring
        s = Spring(k)
    else:
        from solver import solver

        def s(u):
            return k*u

    data = [x, t]      # key input and output data (arrays)
    for i in range(h_data.shape[0]):
        h = h_data[i,:]            # extract a column
        a = acceleration(h, x, v)

        u, t = solver(I=0.2, V=0, m=m, b=b, s=s, F=-m*a,
                      t=t, damping='linear')
        data.append([h, a, u])
    return data

def acceleration(h, x, v):
    """Compute 2nd-order derivative of h."""
    # Method: standard finite difference aproximation
    d2h = np.zeros(h.size)
    dx = x[1] - x[0]
    for i in range(1, h.size-1, 1):
        d2h[i] = (h[i-1] - 2*h[i] + h[i+1])/dx**2
    # Extraplolate end values from first interior value
    d2h[0] = d2h[1]
    d2h[-1] = d2h[-2]
    a = d2h*v**2
    return a

def acceleration_vectorized(h, x, v):
    """Compute 2nd-order derivative of h. Vectorized version."""
    d2h = np.zeros(h.size)
    dx = x[1] - x[0]
    d2h[1:-1] = (h[:-2] - 2*h[1:-1] + h[2:])/dx**2
    # Extraplolate end values from first interior value
    d2h[0] = d2h[1]
    d2h[-1] = d2h[-2]
    a = d2h*v**2
    return a

def rms(data):
    """Compute root mean square of displacement."""
    u_rms = np.zeros(t.size)
    for h, a, u in data[2:]:
        u_rms += u**2
    u_rms = np.sqrt(u_rms/u_rms.size)
    data.append(u_rms)
    return data

def prepare_input():
    url = 'http://hplbit.bitbucket.org/data/bumpy/bumpy.dat.gz'
    m = 60
    k = 60
    v = 5
    try:
        b = float(sys.argv[1])
    except IndexError:
        b = 80  # default
    return url, m, b, k, v

def command_line_options():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--m', '--mass', type=float,
                        default=60, help='mass of vehicle')
    parser.add_argument('--k', '--spring', type=float,
                        default=60, help='spring parameter')
    parser.add_argument('--b', '--damping', type=float,
                        default=80, help='damping parameter')
    parser.add_argument('--v', '--velocity', type=float,
                        default=5, help='velocity of vehicle')
    parser.add_argument('--cython', action='store_true')
    url = 'http://hplbit.bitbucket.org/data/bumpy/bumpy.dat.gz'
    parser.add_argument('--roadfile', type=str,
              default=url, help='filename/URL with road data')
    args = parser.parse_args()
    # Extract input parameters
    m = args.m; k = args.k; b = args.b; v = args.v
    url = args.roadfile; cy = args.cython
    return url, m, b, k, v, cy

if __name__ == '__main__':
    #url, m, b, k, v = prepare_input()
    url, m, b, k, v, cy = command_line_options()
    print 'cy', cy

    data = bumpy_road(url=url, m=60, b=b, k=60, v=10, cy=cy)
    data = rms(data)

    # Save data list to file
    import cPickle
    outfile = open('bumpy.res', 'w')
    cPickle.dump(data, outfile)
    outfile.close()
