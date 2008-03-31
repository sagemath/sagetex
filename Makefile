pkg=sagetexpackage
dest=/home/drake/texmf/tex/latex/sagetex/

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
	latexcleanup clean .
	rm -fr sage-plots-for-* E2.sobj *.pyc sagetex.tar.gz sagetex.py sagetex.pyc sagetex.sty makestatic.py desagetexparser.py

install:
	cp sagetex.py $(dest)
	sed -e '/\\iffalse/ d' \
	    -e '/^%%/ d' \
	    -e 's|directory with sagetex.py|$(dest)|'\
		-e '50,55 s/\\fi//' sagetex.sty > $(dest)/sagetex.sty

dist: all
	@echo
	@echo Did you turn off Imagemagick in example.tex?
	@echo
	@tar zcf sagetex.tar.gz ../sagetex/example.pdf ../sagetex/example.tex ../sagetex/README ../sagetex/sagetexpackage.dtx ../sagetex/sagetexpackage.ins ../sagetex/sagetexpackage.pdf
