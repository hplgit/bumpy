"""
Solve vibration equation m*u'' + b*u' + k*u = 0
with the aid of sympy.

TODO:
It is probably easier to compute with real sin/cos expressions only.
"""
from sympy import *
t, m, b, k, I_, V = symbols(
    't m b k I_ V',  # Use I_ for initial condition u(0)
    real=True)       # Wise when doing complex calculations
w = symbols('w', complex=True)

def diff_eq_lhs(u):
    return m*diff(u, t, t) + b*diff(u, t) + k*u

# Homogeneous solution
ansatz = exp(I*w*t)  # I is the imaginary unit
# Insert ansatz to get an equation for the unknown w
eq = diff_eq_lhs(ansatz)
# Divide by ansatz to get quadratic equation for w
eq = eq/ansatz
eq = simplify(eq)
print 'Equation for w:', eq, '= 0'
# Solve w equation
r = solve(eq, w)
print r

# Form solution as sum of the ansatz with each w solution
u1 = ansatz.subs(w, r[0])
u2 = ansatz.subs(w, r[1])
print 'u1:', u1
u1 = expand(u1)
print 'u1 after expansion', u1
# Assume -b**2 + 4*k*m > 0 so we get sin/cos solution;
# set c = -b**2 + 4*k*m
c = symbols('c', positive=True)
u1 = u1.subs(sqrt(-b**2 + 4*k*m)/(2*m), c)
print 'u1 with c:', u1
u2 = expand(u2).subs(sqrt(-b**2 + 4*k*m)/(2*m), c)
print 'u2 with c:', u2
C1, C2 = symbols('C1 C2')  # Constants to be determined
u_h = C1*u1 + C2*u2

# Particular solution
A, phi = symbols('A phi', real=True)
F = A*exp(I*phi*t)
B = symbols('B', complex=True)
ansatz = B*exp(I*phi*t)
eq = diff_eq_lhs(ansatz) - F
eq = simplify(eq/ansatz)
print 'u_p with B:', eq
r = solve(eq, B)
print 'B:', r[0]
u_p = ansatz.subs(B, r[0])
u_p = expand(u_p, complex=True)
print 'u_p after expand:', u_p
u_p = simplify(u_p)
print 'u_p after simplify:', u_p
print 're(u_p):', re(u_p)

# The following gives too huge expressions so we
# drop u_p
u_p = 0

# Determine A and B from initial conditions
u = u_h + u_p
eqs = [u.subs(t, 0) - I_,           # u(0)=I_
       diff(u, t).subs(t, 0) - V]   # u'(0)=V
r = solve(eqs, [C1, C2])
r = {k: simplify(r[k]) for k in [C1, C2]}
print 'Solutions for C1 and C2:', r

# Final solution
u = r[C1]*u1 + r[C2]*u2
print 'u:', u
u = expand(u)
print 'after expand:\n', u
u = trigsimp(u)
print 'after trigsimp:\n', u
# Take the physical solution as the real part
u = re(u)
I_.name = 'I'  # Switch to I as name of initial condition
print 'Physical solution (re(u)):\n', u

# Check that u fulfills the initial conditions
print 'u(0)=', simplify(u.subs(t, 0))
print "u'(0)=", simplify(diff(u, t).subs(t, 0))
# Check the differential equation, but replace c by the
# parameters in the equation
print 'diff.eq:', \
  simplify(diff_eq_lhs(u.subs(c, sqrt(-b**2 + 4*k*m)/(2*m))))


