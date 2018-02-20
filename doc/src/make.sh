#!/bin/sh
# Make the basics.do.txt and bumpy.do.txt documents in various formats

set -x  # show all commands in output

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

if [ $# -ge 1 ]; then
  COURSE=$1
else
  COURSE=any
fi

opt="COURSE=$COURSE"

#names="basics bumpy"
names="basics"

if [ $# -ge 2 ]; then
  names="$2"
fi


# function do_spellcheck {
# name=$1
# system doconce spellcheck -d .dict4spell.txt $name.do.txt
# }

function compile {
    name=$1
    
    system doconce format pdflatex $name --device=paper --minted_latex_style=trac $opt
    system doconce ptex2tex $name envir=minted
    pdflatex -shell-escape $name
    makeindex $name
    pdflatex -shell-escape $name
    pdflatex -shell-escape $name
}

function generate_html {
    name=$1    
# Plain HTML
    system doconce format html $name --html_style=bootstrap $opt --html_code_style=inherit
    system doconce split_html $name.html --pagination
}

function generate_sphinx {
    name=$1
    system doconce format sphinx $name $opt # always generate new
    system doconce split_rst $name
    system doconce sphinx_dir theme=cbc copyright="H. P. Langtangen" $name
    system python automake_sphinx.py
}

function generate_ipynb {
    name=$1
    system doconce format ipynb $name $opt
}

for name in $names; do

if [ $COURSE != "any" ]; then
   oldname=$name
   name="${name}-${COURSE}"
   cp ${oldname}.do.txt ${name}.do.txt
fi

#do_spellcheck $name
#compile $name
#generate_html $name
#generate_sphinx $name
generate_ipynb $name

# Publish
dest=../pub
# rm -rf $dest/sphinx-${name}
# cp -r sphinx-rootdir/_build/html $dest/sphinx-${name}
# cp -r fig-bumpy $name.html ._${name}*.html ${name}.pdf $dest/
cp -r  *.ipynb $dest/
done
