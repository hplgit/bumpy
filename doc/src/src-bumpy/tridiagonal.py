import numpy as np
N = 6
diagonals = np.zeros((3, N))   # 3 diagonals
diagonals[0,:] = np.linspace(-1, -N, N)
diagonals[1,:] = -2
diagonals[2,:] = np.linspace(1, N, N)
import scipy.sparse
A = scipy.sparse.spdiags(diagonals, [-1,0,1], N, N, format='csc')
A_d = A.toarray()    # make corresponding dense matrix
print A_d

# Solve linear system
x = np.linspace(-1, 1, N)  # choose solution
b = A.dot(x)               # sparse matrix vector product
import scipy.sparse.linalg
x = scipy.sparse.linalg.spsolve(A, b)
print x

# Compare with dense matrix computations
b = np.dot(A_d, x)   # standard matrix vector product
x = np.linalg.solve(A_d, b)
print x
