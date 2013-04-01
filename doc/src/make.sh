#!/bin/sh
name=bumpy
wrap=bumpy

doconce format html $wrap
if [ $? -ne 0 ]; then echo "doconce could not compile document"; exit; fi

doconce sphinx_dir theme=pyramid title="A Worked Example on Scientific Computing with Python: Vehicle on Bumpy Road" $wrap
python automake_sphinx.py

doconce format html $wrap

# Copy to hplgit (or maybe just gh-pages?)
dest=~/vc/hplgit.github.com/teamods/bumpy/
cp -r sphinx-rootdir/_build/html $dest
cp vibcase.html $dest/bumpy.html