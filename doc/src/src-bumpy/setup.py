from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name='solver_cy',
  ext_modules=[Extension('solver_cy', ['solver.pyx'],)],
  cmdclass={'build_ext': build_ext},
)
