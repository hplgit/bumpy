#!/bin/sh
python setup.py build_ext --inplace
# Test if module works
python -c "import solver_cy"
if [ $? -eq 0 ]; then
  echo "Cython module successfully built"
fi
# Compile and view C code
cython -a solver.pyx
#google-chrome solver.html
