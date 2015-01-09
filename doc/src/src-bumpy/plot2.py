import numpy as np
import matplotlib.pyplot as plt

v0 = 0.2
n = 21  # No of t values for plotting

t = np.linspace(0, 2, n+1)
a = 2
s0 = v0*t + 0.5*a*t**2
a = 3
s1 = v0*t + 0.5*a*t**2

plt.plot(t, s0, 'r-',  # Plot s0 curve with red line
         t, s1, 'bo')  # Plot s1 curve with blue circles
plt.xlabel('t')
plt.ylabel('s')
plt.title('Distance plot')
plt.legend(['$s(t; v_0=2, a=0.2)$', '$s(t; v_0=2, a=0.8)$'],
           loc='upper left')
plt.savefig('myplot.png')
plt.show()
