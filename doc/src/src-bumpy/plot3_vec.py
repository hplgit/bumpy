import numpy as np
import matplotlib.pyplot as plt

def s_func(t, v0, a0, t1):
    if isinstance(t, (float,int)):
        if t <= t1:
            s = v0*t + 0.5*a0*t**2
        else:
            s = v0*t + 0.5*a0*t1**2 + a0*t1*(t-t1)
    elif isinstance(t, np.ndarray):
        s = np.where(t <= t1,
                     v0*t + 0.5*a0*t**2,
                     v0*t + 0.5*a0*t1**2 + a0*t1*(t-t1))
        """
        # Alternative
        s = np.zeros_like(t)
        s[t <= t1] = (v0*t + 0.5*a0*t**2)[t <= t1]
        s[t > t1]  = (v0*t + 0.5*a0*t1**2 + a0*t1*(t-t1))[t > t1]
        """
    return s

n = 201  # No of t values for plotting
t1 = 1.5

t = np.linspace(0, 2, n+1)
s = s_func(t, v0=0.2, a0=20, t1=t1)

plt.plot(t, s, 'b-')
plt.plot([t1, t1], [0, s_func(t=t1, v0=0.2, a0=20, t1=t1)], 'r--')
plt.xlabel('t')
plt.ylabel('s')
plt.savefig('myplot.png')
plt.show()

