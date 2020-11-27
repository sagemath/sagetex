##
## This is file `sagetexparse.py',
## generated with the docstrip utility.
##
## The original source files were:
##
## scripts.dtx  (with options: `parsermod')
##
## This is a generated file. It is part of the SageTeX package.
##
## Copyright (C) 2008--2015 by Dan Drake <dr.dan.drake@gmail.com>
##
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by the
## Free Software Foundation, either version 2 of the License, or (at your
## option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
## Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program.  If not, see <http://www.gnu.org/licenses/>.
##
import sys

from pyparsing import (
    Literal,
    OneOrMore,
    Optional,
    ParseFatalException,
    SkipTo,
    Suppress,
    Word,
    lineno,
    matchPreviousExpr,
    nestedExpr,
    nums,
    oneOf,
    originalTextFor,
    replaceWith,
    restOfLine,
)


def skipToMatching(opener, closer):
    """

    :param opener: opening token
    :param closer: closing token

    """
    nest = nestedExpr(opener, closer)
    return originalTextFor(nest)


curlybrackets = skipToMatching("{", "}")
squarebrackets = skipToMatching("[", "]")
sagemacroparser = r"\sage" + curlybrackets("code")
sageplotparser = (
    r"\sageplot"
    + Optional(squarebrackets)("opts")
    + Optional(squarebrackets)("format")
    + curlybrackets("code")
)
sagetexpause = Literal(r"\sagetexpause")
sagetexunpause = Literal(r"\sagetexunpause")


class SoutParser:
    """sout file parser"""

    def __init__(self, fn):
        self.label = []
        parselabel = (
            r"\newlabel{@sageinline"
            + Word(nums)("num")
            + "}{"
            + curlybrackets("result")
            + "{}{}{}{}}"
        )
        parselabel.ignore("%" + restOfLine)
        parselabel.setParseAction(self.newlabel)
        try:
            OneOrMore(parselabel).parseFile(fn)
        except IOError:
            print("Error accessing {}; exiting. Does your .sout file exist?".format(fn))
            sys.exit(1)

    def newlabel(self, s, l, t):
        """

        :param s: string with newlabel
        :param t: param l:
        :param l: label content

        """
        self.label.append(t.result[1:-1])


class DeSageTex:
    """ """

    def __init__(self, fn):
        self.sagen = 0
        self.plotn = 0
        self.fn = fn
        self.sout = SoutParser(fn + ".sagetex.sout")
        smacro = sagemacroparser
        smacro.setParseAction(self.sage)
        usepackage = r"\usepackage" + Optional(squarebrackets) + "{sagetex}"
        usepackage.setParseAction(
            replaceWith(
                r"""% "\usepackage{sagetex}" line was here:
        \RequirePackage{verbatim}
        \RequirePackage{graphicx}
        \newcommand{\sagetexpause}{\relax}
        \newcommand{\sagetexunpause}{\relax}"""
            )
        )
        splot = sageplotparser
        splot.setParseAction(self.plot)
        beginorend = oneOf("begin end")
        blockorverb = "sage" + oneOf("block verbatim")
        blockorverb.setParseAction(replaceWith("verbatim"))
        senv = "\\" + beginorend + "{" + blockorverb + "}"
        silent = Literal("sagesilent")
        silent.setParseAction(replaceWith("comment"))
        ssilent = "\\" + beginorend + "{" + silent + "}"
        stexindent = Suppress(r"\setlength{\sagetexindent}" + curlybrackets)
        doit = smacro | senv | ssilent | usepackage | splot | stexindent
        doit.ignore("%" + restOfLine)
        doit.ignore(r"\begin{verbatim}" + SkipTo(r"\end{verbatim}"))
        doit.ignore(r"\begin{comment}" + SkipTo(r"\end{comment}"))
        doit.ignore(r"\sagetexpause" + SkipTo(r"\sagetexunpause"))
        str = "".join(open(fn + ".tex", "r").readlines())
        self.result = doit.transformString(str)

    def sage(self, s, l, t):
        """Return next sagelabel from sout file and increment sagen

        :param s: string
        :param l: location in the string where matching started
        :param t: token
        :returns: next sagelabel from sout file
        :rtype: string

        """
        self.sagen += 1
        return self.sout.label[self.sagen - 1]

    def plot(self, s, l, t):
        """Replace sageplot by includegraphics and increment plotn

        :param s: string
        :param l: loc
        :param t: tok

        """
        self.plotn += 1
        if len(t.opts) == 0:
            opts = r"[width=.75\textwidth]"
        else:
            opts = t.opts[0]
        return r"\includegraphics%s{sage-plots-for-%s.tex/plot-%s}" % (
            opts,
            self.fn,
            self.plotn - 1,
        )


class SageCodeExtractor:
    """ """

    def __init__(self, fn):
        smacro = sagemacroparser
        smacro.setParseAction(self.macroout)

        splot = sageplotparser
        splot.setParseAction(self.plotout)
        env_names = oneOf("sageblock sageverbatim sagesilent")
        senv = (
            r"\begin{"
            + env_names("env")
            + "}"
            + SkipTo(r"\end{" + matchPreviousExpr(env_names) + "}")("code")
        )
        senv.leaveWhitespace()
        senv.setParseAction(self.envout)

        spause = sagetexpause
        spause.setParseAction(self.pause)

        sunpause = sagetexunpause
        sunpause.setParseAction(self.unpause)

        doit = smacro | splot | senv | spause | sunpause

        str = "".join(open(fn + ".tex", "r").readlines())
        self.result = ""

        doit.transformString(str)

    def macroout(self, s, l, t):
        """

        :param s: string
        :param t: tok
        :param l: 

        """
        self.result += "# \\sage{} from line %s\n" % lineno(l, s)
        self.result += t.code[1:-1] + "\n\n"

    def plotout(self, s, l, t):
        """

        :param s: string
        :param t: tok
        :param l:

        """
        self.result += "# \\sageplot{} from line %s:\n" % lineno(l, s)
        if t.format is not "":
            self.result += "# format: %s" % t.format[0][1:-1] + "\n"
            self.result += t.code[1:-1] + "\n\n"

    def envout(self, s, l, t):
        """

        :param s: string
        :param t: tok
        :param l:

        """
        self.result += "# %s environment from line %s:" % (t.env, lineno(l, s))
        self.result += t.code[0] + "\n"

    def pause(self, s, l, t):
        """

        :param s: string
        :param t: tok
        :param l:

        """
        self.result += "# SageTeX (probably) paused on input line %s.\n\n" % (
            lineno(l, s)
        )

    def unpause(self, s, l, t):
        """

        :param s: string
        :param l: loc
        :param t:

        """
        self.result += "# SageTeX (probably) unpaused on input line %s.\n\n" % (
            lineno(l, s)
        )
