from sympy import *
w = Symbol('w')
m = 60
b = 60
k = 60
eq = -m*w**2 + I*b*w + k
sol = solve(eq, w)
print sol
print re(sol[0])
print re(sol[0]).evalf()

print [factor(i) for i in sol]
