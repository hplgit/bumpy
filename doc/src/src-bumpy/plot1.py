import numpy as np
import matplotlib.pyplot as plt

v0 = 0.2
a = 2
n = 21  # No of t values for plotting

t = np.linspace(0, 2, n+1)
s = v0*t + 0.5*a*t**2

plt.plot(t, s)
plt.savefig('myplot.png')
plt.show()

