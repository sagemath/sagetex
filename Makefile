pkg=sagetexpackage
dest=/home/drake/texmf/tex/latex/sagetex/
# the subdir stuff makes the tarball have the directory correct
srcs=../sagetex/example.tex ../sagetex/README ../sagetex/sagetexpackage.dtx ../sagetex/sagetexpackage.ins
ver=2.0

all: ins
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

ins:
	yes | latex $(pkg).ins

clean: 
	latexcleanup clean .
	rm -fr sage-plots-for-* E2.sobj *.pyc sagetex.tar.gz sagetex.py sagetex.pyc sagetex.sty makestatic.py sagetexparse.py extractsagecode.py dist MANIFEST

install:
	cp sagetex.py $(dest)
	sed -e '/\\iffalse/ d' \
	    -e '/^%%/ d' \
	    -e 's|directory with sagetex.py|$(dest)|'\
		-e '50,55 s/\\fi//' sagetex.sty > $(dest)/sagetex.sty

# make a tarball suitable for CTAN uploads, or for someone who knows how
# to handle .dtx files
ctandist: all
	@echo
	@echo Did you turn off Imagemagick in example.tex?
	@echo
	tar zcf sagetex.tar.gz $(srcs) ../sagetex/example.pdf ../sagetex/sagetexpackage.pdf

# make a spkg for Sage
spkg:
	python setup.py sdist
	cd dist
	gunzip dist/sagetex-$(ver).tar.gz
	bzip2 dist/sagetex-$(ver).tar
	cp dist/sagetex-$(ver).tar.bz2 dist/sagetex-$(ver).spkg
