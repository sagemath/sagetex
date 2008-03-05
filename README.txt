This is the SageTeX package. It allows you to embed Sage code into LaTeX
documents.

To use SageTeX, you must first extract the LaTeX style file and Python
module from the .dtx file. To do that:

  0. Run `latex sagetexpackage.ins'

Then, to get the documentation for this package, which includes usage
information:

  1. Run `latex sagetexpackage.dtx'
  2. Run `sage sagetexpackage.sage'
  3. Run the indexing commands that the .ins file told you about.
  4. Run `latex sagetexpackage.dtx' again.

You can skip step 3 if you don't care about the index.

The file example.tex has, as you likely guessed, a bunch of examples
showing you how this package works. You can compile it using a another
latex-sage-latex cycle as in steps 1-2-4 above. Note that example.tex
includes some PNG graphics which latex cannot use; to see those, use
pdflatex instead of regular latex.

This works builds on a lot of work by others; see the last section of
the documentation for credits.

Please let me know if you find any bugs or have any ideas for
improvement!

- Dan Drake <ddrake@member.ams.org>
