#!/bin/sh
name=bumpy
wrap=$name

doconce format pdflatex $wrap --device=paper
doconce ptex2tex $wrap envir=minted
pdflatex -shell-escape $wrap
pdflatex -shell-escape $wrap


# Plain HTML
doconce format html $wrap --html_style=bootstrap
if [ $? -ne 0 ]; then echo "doconce could not compile document"; exit; fi
doconce split_html $wrap.html --pagination

# Sphinx
doconce format sphinx $wrap  # always generate new
doconce sphinx_dir theme=cbc title="A Worked Example on Scientific Computing with Python" author="H. P. Langtangen" $wrap
python automake_sphinx.py

# Publish
dest=../pub
rm -rf $dest/sphinx
cp -r sphinx-rootdir/_build/html $dest/sphinx
cp -r fig-bumpy $wrap.html ._${wrap}*.html ${wrap}.pdf $dest/
