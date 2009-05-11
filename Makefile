SHELL=/bin/bash
pkg=sagetexpackage
dest=/home/drake/texmf/tex/latex/sagetex/
# the subdir stuff makes the tarball have the directory correct
srcs=../sagetex/example.tex ../sagetex/README ../sagetex/sagetexpackage.dtx ../sagetex/sagetexpackage.ins
ver=2.0.2

all: ins
	latex $(pkg).dtx
	sage $(pkg).sage
	make index
	latex $(pkg).dtx
	sage $(pkg).sage
	latex $(pkg).dtx
	pdflatex $(pkg).dtx
	latex example.tex
	sage example.sage
	latex example.tex
	pdflatex example.tex

index:
	sed -e 's/usage|hyperpage/usagehyperpage/g' -i sagetexpackage.idx
	makeindex -s gglo.ist -o $(pkg).gls $(pkg).glo 
	makeindex -s gind.ist -o $(pkg).ind $(pkg).idx

ins:
	yes | latex $(pkg).ins

clean: 
	latexcleanup clean .
	rm -fr sage-plots-for-* E2.sobj *.pyc sagetex.tar.gz sagetex.py sagetex.pyc sagetex.sty makestatic.py sagetexparse.py extractsagecode.py dist MANIFEST

# the following bit requires SHELL=bash
auxclean:
	rm -f {$(pkg),example}.{glo,gls,aux,sout,out,toc,dvi,pdf,ps,log,ilg,ind,idx,sage}

install: ins
	cp sagetex.sty $(dest)

# make a tarball suitable for CTAN uploads, or for someone who knows how
# to handle .dtx files
ctandist: all
	@echo
	@echo Did you turn off Imagemagick in example.tex?
	@echo
	tar zcf sagetex.tar.gz $(srcs) ../sagetex/example.pdf ../sagetex/sagetexpackage.pdf

# this may seem silly, since running 'all' runs Sage just like the test
# script does, but sometimes it scrolls by too fast, and I want obvious
# output in front of me that tells me the results.
test: all
	clear
	./test

# make a source distribution, used for building the spkg
dist: all
	python setup.py sdist --formats=tar
