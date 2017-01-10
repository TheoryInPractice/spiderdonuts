## Run from /sparkstruck/notes-walk-entropy

rm *.aux
rm *.log
rm *.bbl
rm *.blg


pdflatex preliminaries.tex
pdflatex preliminaries.tex
bibtex preliminaries
bibtex preliminaries
pdflatex preliminaries.tex
pdflatex preliminaries.tex
