infile = open('.input.dat', 'r')
for line in infile:
    # Typical line: variable = value
    variable, value = line.split('=')
    variable = variable.strip()  # remove leading/traling blanks
    if variable == 'v0':
        v0 = float(value)
    elif variable == 'a':
        a = float(value)
    elif variable == 'dt':
        dt = float(value)
    elif variable == 'interval':
        interval = eval(value)
infile.close()

t_values = []
s_values = []
n = int(round(interval[1]/dt)) + 1  # No of t values
for i in range(n):
    t = i*dt
    s = v0*t + 0.5*a*t**2
    t_values.append(t)
    s_values.append(s)

# Write nicely formatted table to file
outfile = open('table1.dat', 'w')
outfile.write('# t    s(t)\n')  # write table header
for t, s in zip(t_values, s_values):
    outfile.write('%.2f  %.4f\n' % (t, s))

# Alternative: use numpy.savetxt
import numpy as np
# Make two-dimensional array of [t, s(t)] values in each row
data = np.array([t_values, s_values]).transpose()

# Write data array to file in table format
np.savetxt('table2.dat', data, fmt=['%.2f', '%.4f'],
           header='t   s(t)', comments='# ')

# Read the file back
data = np.loadtxt('table2.dat', comments='#')
