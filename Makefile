pkg=sagetexpackage

all:
	latex $(pkg).ins
	latex $(pkg).dtx
	sage $(pkg).sage
	makeindex -s gglo.ist -o $(pkg).gls $(pkg).glo 
	makeindex -s gind.ist -o $(pkg).ind $(pkg).idx
	latex $(pkg).dtx
	latex example.tex
	sage example.sage
	latex example.tex
	pdflatex example.tex

clean: 
	@latexcleanup clean .
	@rm -fr sage-plots-for-* E2.sobj *.pyc

