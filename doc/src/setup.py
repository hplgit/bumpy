from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import sys

setup(
  name='Bumpy',
  ext_modules=[Extension('bumpy2_cy', ['bumpy2.pyx'],)],
  cmdclass={'build_ext': build_ext},
)
