#!/bin/sh
name=bumpy
wrap=$name

# Plain HTML
doconce format html $wrap
if [ $? -ne 0 ]; then echo "doconce could not compile document"; exit; fi

# Sphinx
doconce format sphinx $wrap  # always generate new
doconce sphinx_dir theme=cbc title="A Worked Example on Scientific Computing with Python" author="H. P. Langtangen" $wrap
python automake_sphinx.py

# Publish
dest=../pub
rm -rf $dest/sphinx
cp -r sphinx-rootdir/_build/html $dest/sphinx
