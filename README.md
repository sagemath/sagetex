# This is the SageTeX package. 

It allows you to embed code, results of
computations, and plots from the Sage mathematics software suite
(https://www.sagemath.org) into LaTeX documents.

## Using SageTeX

SageTeX is included with Sage, so to use it, you only need to make the
file sagetex.sty known to TeX; that file will be in
SAGE_ROOT/venv/share/texmf/tex/latex/sagetex, along with
documentation and examples. See the Sage tutorial at
https://doc.sagemath.org/html/en/tutorial/sagetex.html 
for a quick usage introduction, and for complete installation
instructions later on the same page at
https://doc.sagemath.org/html/en/tutorial/sagetex.html#sec-sagetex-install

The complete documentation is in sagetex.pdf, in
the SAGE_ROOT/... directory mentioned above.

## Generating SageTeX

If you want to extract any of SageTeX's files from the .dtx sources, you
can do

  0. Run `latex sagetex.ins`

To regenerate the documentation, do

  1. Run `latex sagetex.dtx`
  2. Run `sage sagetex.sage`
  3. Run the indexing commands that the .ins file told you about.
  4. Run `latex sagetex.dtx` again.

You can skip step 3 if you don't care about the index. You will need the
pgf and tikz packages installed to typeset the figures.

The file example.tex has, as you likely guessed, a bunch of examples
showing you how this package works. You can compile it using a another
latex-sage-latex cycle as in steps 1-2-4 above. Note that example.tex
includes some PNG graphics which latex cannot use; to see those, use
pdflatex instead of regular latex or enable the imagemagick option. (See
the documentation.)

To use the SageTeX package with your own documents, see the
"Installation" section of the documentation.

## Contributing to SageTeX

Please let us know your experience with SageTeX, especially bug
reports or feature requests, at 
https://github.com/sagemath/sagetex/

SageTeX welcomes code contributions, subject to approval by the
maintainers.  Release managers should note the instructions at HACKING.md

This work builds on a lot of work by others; see the CONTRIBUTORS file
and the "Credits" section of the documentation for credits. The source
code may be modified and distributed under the terms of the GPL, version
2 or later; the documentation may be modified and distributed under a
Creative Commons Attribution - Share Alike 3.0 License. See the "Copying
and licenses" section of the documentation.

Sagemath Developers and SageTeX maintainers
