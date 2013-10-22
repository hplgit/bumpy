#!/bin/sh
name=bumpy
wrap=$name

doconce format html $wrap
if [ $? -ne 0 ]; then echo "doconce could not compile document"; exit; fi

doconce sphinx_dir theme=cbc title="A Worked Example on Scientific Computing with Python" author="H. P. Langtangen" $wrap
python automake_sphinx.py

doconce format html $wrap

# Copy to hplgit (or maybe just gh-pages?)
#dest=~/vc/hplgit.github.com/teamods/bumpy/
dest=../pub
rm -rf $dest/sphinx
cp -r sphinx-rootdir/_build/html $dest/sphinx
