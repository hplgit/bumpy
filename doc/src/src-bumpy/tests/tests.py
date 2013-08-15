import nose.tools as nt
import sympy as sm
import numpy as np
from solver import solver, solver_linear_damping
from bumpy import acceleration, acceleration_vectorized

def test_acceleration():
    x = np.linspace(0, 10, 5)
    h = x**2
    v = np.sqrt(0.5)
    # v**2*h'' should equal 1 exactly, except perhaps at
    # the end points where we extrapolate
    a_s = acceleration(h, x, v)
    a_v = acceleration_vectorized(h, x, v)
    diff = np.abs(a_s - a_v).max()
    nt.assert_almost_equal(diff, 0, places=14)

def lhs_eq(t, m, b, s, u, damping='linear'):
    """Return lhs of differential equation as sympy expression."""
    v = sm.diff(u, t)
    if damping == 'linear':
        return m*sm.diff(u, t, t) + b*v + s(u)
    else:
        return m*sm.diff(u, t, t) + b*v*sm.Abs(v) + s(u)

def test_quadratic():
    """Verify a quadratic solution."""
    I = 1.2; V = 3; m = 2; b = 0.9; k = 4
    s = lambda u: k*u
    T = 2
    dt = 0.2
    N = int(round(T/dt))
    time_points = np.linspace(0, T, N+1)

    # Test linear damping
    t = sm.Symbol('t')
    q = 2  # arbitrary constant
    u_exact = I + V*t + q*t**2   # sympy expression
    exact_solution = sm.lambdify(t, u_exact, modules='numpy')
    F = sm.lambdify(t, lhs_eq(t, m, b, s, u_exact, 'linear'))
    u1, t1 = solver(I, V, m, b, s, F, time_points, 'linear')
    error = abs(exact_solution(t1) - u1).max()
    nt.assert_almost_equal(error, 0, places=13)

    # Test quadratic damping: u_exact must be linear
    # in order exactly recover this solution
    u_exact = I + V*t
    exact_solution = sm.lambdify(t, u_exact, modules='numpy')
    F = sm.lambdify(t, lhs_eq(t, m, b, s, u_exact, 'quadratic'))
    u2, t2 = solver(I, V, m, b, s, F, time_points, 'quadratic')
    error = abs(exact_solution(t2) - u2).max()
    nt.assert_almost_equal(error, 0, places=13)

def test_quadratic_all_functions():
    """Verify a quadratic solution."""
    I = 1.2; V = 3; m = 2; b = 0.9
    s = lambda u: 4*u
    t = sm.Symbol('t')
    T = 2
    dt = 0.2
    N = int(round(T/dt))
    time_points = np.linspace(0, T, N+1)

    def solver_linear_damping_wrapper(
        I, V, m, b, s, F, t, damping='linear'):
        """Wrapper such that solver_linear_damping can be called as solver."""
        if callable(F):
            F = F(t)
        return solver_linear_damping(I, V, m, b, s, F, t), t

    functions = [solver, solver_linear_damping_wrapper]
    try:
        from solver_cy import solver as solver_cy
        functions.append(solver_cy)
    except ImportError:
        print 'Cython module is not compiled'
        pass

    for function in functions:
        print 'testing', function.__name__
        # Test linear damping
        q = 2  # arbitrary constant
        u_exact = I + V*t + q*t**2
        exact_solution = sm.lambdify(t, u_exact, modules='numpy')
        F = sm.lambdify(t, lhs_eq(t, m, b, s, u_exact, 'linear'))
        u1, t1 = solver(I, V, m, b, s, F, time_points, 'linear')
        error = abs(exact_solution(t1) - u1).max()
        nt.assert_almost_equal(error, 0, places=13)

        # Test quadratic damping
        if function != solver_linear_damping_wrapper:

            # In the quadratic damping case, u_exact must be linear
            # in order exactly recover this solution
            u_exact = I + V*t
            exact_solution = sm.lambdify(t, u_exact, modules='numpy')
            F = sm.lambdify(t, lhs_eq(t, m, b, s, u_exact, 'quadratic'))
            u2, t2 = solver(I, V, m, b, s, F, time_points, 'quadratic')
            error = abs(exact_solution(t2) - u2).max()
            nt.assert_almost_equal(error, 0, places=13)

if __name__ == '__main__':
    test_quadratic()
    test_acceleration()
