## Run from /Spiderdonuts/notes-walk-entropy

rm *.aux
rm *.log
rm *.bbl
rm *.blg


pdflatex main-walk-entropy.tex
pdflatex main-walk-entropy.tex
bibtex main-walk-entropy
bibtex main-walk-entropy
pdflatex main-walk-entropy.tex
pdflatex main-walk-entropy.tex
