pkg=sagetex
dtxs=$(wildcard *.dtx)
# the subdir stuff makes the tarball have the directory correct
srcs=example.tex README sagetex.ins

.SUFFIXES:

all: sagetex.sty sagetex.py example.pdf $(pkg).pdf

# just depend on the .ind file, since we'll make the .gls and .ind together;
# TEXOPTS is used by spkg-install to specify nonstopmode when building docs
$(pkg).pdf: $(dtxs) $(pkg).ind
	latex $(TEXOPTS) $(pkg).dtx
	sage $(pkg).sagetex.sage
	latex $(TEXOPTS) $(pkg).dtx
	sage $(pkg).sagetex.sage
	latex $(TEXOPTS) $(pkg).dtx
	pdflatex $(TEXOPTS) $(pkg).dtx

example.pdf: example.tex sagetex.sty sagetex.py
	pdflatex $(TEXOPTS) example.tex
	sage example.sagetex.sage
	pdflatex $(TEXOPTS) example.tex
	pdflatex $(TEXOPTS) example.tex

%.ind: $(dtxs)
	latex $(TEXOPTS) $(pkg).dtx
	sed -e 's/usage|hyperpage/usagehyperpage/g' -i sagetex.idx
	makeindex -s gglo.ist -o $(pkg).gls $(pkg).glo
	makeindex -s gind.ist -o $(pkg).ind $(pkg).idx

sagetex.sty: py-and-sty.dtx $(pkg).dtx
	yes | latex $(TEXOPTS) $(pkg).ins

sagetex.py: py-and-sty.dtx $(pkg).dtx
	yes | latex $(TEXOPTS) $(pkg).ins

remote-sagetex.py: remote-sagetex.dtx
	yes | latex $(TEXOPTS) $(pkg).ins

run-sagetex-if-necessary.py makestatic.py extractsagecode.py sagetexparse.py: scripts.dtx
	yes | latex $(TEXOPTS) $(pkg).ins

clean: auxclean
	rm -fr sage-plots-for-* E2.sobj *.pyc sagetex.tar.gz sagetex.py sagetex.pyc sagetex.sty makestatic.py sagetexparse.py extractsagecode.py dist MANIFEST remote-sagetex.py auto *_doctest.sage *_doctest.sage.py example-*.table run-sagetex-if-necessary.py

auxclean:
	/bin/bash -c "rm -f {$(pkg),example}.{glo,gls,aux,out,toc,dvi,pdf,ps,log,ilg,ind,idx,fdb_latexmk,sagetex.*}"
	rm -f *_doctest.sage

# otherwise, make gets confused since there's a file named "test"
.PHONY: test clean auxclean all dist
test:
	./test

# make a source distribution, used for building the spkg
dist: sagetex.sty
	python setup.py sdist --formats=tar
