#!/bin/sh
# Create slides from lectures.do.txt in a variety of formats

# bash make.sh
# bash make.sh TKT4140 lectures-basics

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

# Spellcheck must be performed in the dir where the file resides
# cd lec-bumpy
# system doconce spellcheck -d ../.dict4spell.txt basics.do.txt
# system doconce spellcheck -d ../.dict4spell.txt bumpy.do.txt
# cd ..

names="lectures-basics"
if [ $# -ge 2 ]; then
  names="$2"
fi

for name in $names; do

if [ $COURSE != "any" ]; then
   oldname=$name
   name="${name}-${COURSE}"
   cp ${oldname}.do.txt ${name}.do.txt
fi

# Note: can be smart to run beamer slides first since latex finds
# more errors in the slides than the doconce HTML translation

# reval.js HTML5 slides
html=${name}-reveal
system doconce format html $name --pygments_html_style=native --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html reveal --html_slide_theme=darkgray
doconce replace 'pre style="' 'pre style="font-size: 110%; ' $html.html
#exit

html=${name}-reveal-beige
system doconce format html $name --pygments_html_style=perldoc --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html reveal --html_slide_theme=beige

html=${name}-reveal-white
system doconce format html $name --pygments_html_style=default --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html reveal --html_slide_theme=simple

# deck.js HTML5 slides
html=${name}-deck
system doconce format html $name --pygments_html_style=perldoc --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html deck --html_slide_theme=sandstone.default


# Plain HTML slides, 1 big file in solarized style
html=${name}-solarized
system doconce format html $name --pygments_html_style=perldoc --html_style=solarized3 --html_links_in_new_window --html_output=$html $opt
# Don't split into separate pages since we need the enlargen the
# font in the browser (must often be redone for each page)
system doconce split_html $html.html --method=space8
#system doconce slides_html $html doconce --nav_button=text


# One big HTML file with space between the slides (good for browsing)
html=${name}-1
system doconce format html $name --html_style=bloodish --html_links_in_new_window --html_output=$html $opt
# Add space between splits
system doconce split_html $html.html --method=space8


# One bit HTML file with space between the slides (as above) with Bootstrap-gray
html=${name}-bootstrap_bg
doconce format html $name --html_style=bootstrap_bluegray --html_links_in_new_window --html_output=$html $opt
doconce split_html $html.html --method=space8


# LaTeX Beamer slides

rm -f *.aux   # old .aux files can do harm

beamertheme=red_shadow

system doconce format pdflatex $name --latex_title_layout=beamer --latex_table_format=footnotesize --latex_admon_title_no_period $opt
system doconce ptex2tex $name envir=minted
#exit
system doconce slides_beamer $name --beamer_slide_theme=$beamertheme
system pdflatex -shell-escape ${name}
system pdflatex -shell-escape ${name}
cp $name.pdf ${name}-beamer.pdf
cp $name.tex ${name}-beamer.tex

# Handouts based on Beamer
system doconce format pdflatex $name --latex_title_layout=beamer --latex_table_format=footnotesize --latex_admon_title_no_period $opt
system doconce ptex2tex $name envir=minted
system doconce slides_beamer $name --beamer_slide_theme=red_shadow --handout
system pdflatex -shell-escape $name
pdflatex -shell-escape $name
pdflatex -shell-escape $name
pdfnup --nup 2x3 --frame true --delta "1cm 1cm" --scale 0.9 --outfile ${name}-beamer-handouts2x3.pdf ${name}.pdf
rm -f ${name}.pdf

# Ordinary plain LaTeX documents (kind of study guide)
rm -f *.aux  # important after beamer!
system doconce format pdflatex $name --minted_latex_style=trac --latex_admon=paragraph --latex_table_format=footnotesize $opt
system doconce ptex2tex $name envir=minted
doconce replace 'section{' 'section*{' $name.tex
pdflatex -shell-escape $name
makeindex $name
pdflatex -shell-escape $name
mv -f $name.pdf ${name}-minted.pdf
cp $name.tex ${name}-plain-minted.tex

# IPython notebook
rm -f *.tar.gz
system doconce format ipynb $name $opt

# Publish
dest=../pub

cp -r reveal.js deck.js ${name}-*.html ${name}-*.pdf *.ipynb $dest/
#cp ._${name}-*.html $dest
done
