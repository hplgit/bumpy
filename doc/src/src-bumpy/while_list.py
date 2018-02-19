v0 = 2
a = 0.2
dt = 0.1  # Increment
t = 0
t_values = []
s_values = []
while t <= 2.1:
    s = v0*t + 0.5*a*t**2
    t_values.append(t)
    s_values.append(s)
    t = t + dt
print s_values  # Just take a look at a created list
print t_values

# Print a nicely formatted table
i = 0
while i <= len(t_values)-1:
    print '%.18f  %.4f' % (t_values[i], s_values[i])
    i += 1   # Same as i = i + 1



