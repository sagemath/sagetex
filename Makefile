pkg=sagetexpackage

all:
	latex $(pkg).ins
	latex $(pkg).dtx
	sage $(pkg).sage
	makeindex -s gglo.ist -o $(pkg).gls $(pkg).glo 
	makeindex -s gind.ist -o $(pkg).ind $(pkg).idx
	latex $(pkg).dtx
	pdflatex $(pkg).dtx
	latex example.tex
	sage example.sage
	latex example.tex
	pdflatex example.tex

clean: 
	@latexcleanup clean .
	@rm -fr sage-plots-for-* E2.sobj *.pyc sagetex.tar.gz

dist: all
	tar zcf sagetex.tar.gz ../sagetex/example.pdf ../sagetex/example.tex ../sagetex/README.txt ../sagetex/sagetexpackage.dtx ../sagetex/sagetexpackage.ins ../sagetex/sagetexpackage.pdf ../sagetex/sagetex.py ../sagetex/sagetex.sty
