#!/bin/sh

# this runs Sage on the generated .sage files to see if they work ok

typeset()
{
    pdflatex -interaction=nonstopmode $1
    if [ $? -ne 0 ]
    then
        echo "Error typesetting $1!"
        exit 1
    fi
}

checkdotsage()
{
    sage $1.sagetex.sage
    if [ $? -ne 0 ]
    then
        echo "Error running Sage on $1.sagetex.sage!"
        exit 1
    else
        echo "No problem that spkg-check can detect running Sage on $1.sagetex.sage."
    fi
}

pdflatex -version
if [ $? -ne 0 ]
then
    echo "LaTeX (pdflatex) isn't installed (or isn't in \$PATH). Skipping test of SageTeX spkg."
    exit 0
fi

cd src

# Make sure that we use the version of sagetex.py and example.tex in
# the current working directory.
unset TEXINPUTS

typeset example.tex
checkdotsage example
typeset example.tex
typeset example.tex

typeset sagetex.dtx
checkdotsage sagetex
typeset sagetex.dtx
typeset sagetex.dtx

# if we get here, we assume the .sage files are good, and exit successfully
exit 0

