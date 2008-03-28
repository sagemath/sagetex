import sys
sys.path.append('/home/drake/k/urohome/download/pyparsing-1.4.11')

from pyparsing import *


def skipToMatching(opener, closer):
  nest = nestedExpr(opener, closer)
  nest.setParseAction(lambda l, s, t: l[s:getTokensEndLoc()])
  return nest

curlybrackets = skipToMatching('{', '}')
squarebrackets = skipToMatching('[', ']')

class SoutParser():

  def __init__(self, fn):
    self.label = {}

    parselabel = '\\newlabel{@sagelabel' + \
                 Word(nums).setResultsName('num') + \
                 '}{' + \
                 curlybrackets.setResultsName('result') + \
                 '{}{}{}{}}'
    parselabel.ignore('%' + restOfLine)
    parselabel.setParseAction(self.newlabel)

    OneOrMore(parselabel).parseFile(fn)

  def newlabel(self, s, l, t):
    self.label[int(t.num)] = t.result[1:-1]


class DeSageTex():

  def __init__(self, fn_):
    self.fn = fn_
    self.sagen = 0
    self.plotn = 0

    self.sout = SoutParser(self.fn + '.sout')

    # \sage{}:
    smacro = '\\sage' + curlybrackets
    smacro.setParseAction(self.sage)

    # \usepackage[]{sagetex}:
    usepackage = '\\usepackage' + \
                 Optional(squarebrackets) + \
                 '{sagetex}'
    usepackage.setParseAction(replaceWith("""\\RequirePackage{verbatim}
\\RequirePackage{graphicx}"""))

    # \sageplot[][]{}:
    splot = '\\sageplot' + \
            Optional(squarebrackets).setResultsName('options') + \
            Optional(squarebrackets) + \
            curlybrackets
    splot.setParseAction(self.plot)

    # the printed environments:
    beginorend = oneOf('begin end')

    blockorverb = 'sage' + oneOf('block verbatim') 
    blockorverb.setParseAction(replaceWith('verbatim'))
    senv = '\\' + beginorend + '{' + blockorverb + '}'

    # the non-printed environment:
    silent = Literal('sagesilent')
    silent.setParseAction(replaceWith('comment'))

    ssilent = '\\' + beginorend + '{' + silent + '}'

    # \sagetexindent:
    stexindent = Suppress('\\setlength{\\sagetexindent}' + curlybrackets)

    doit = smacro | senv | ssilent | usepackage | splot | stexindent
    doit.ignore('%' + restOfLine)
    doit.ignore('\\begin{verbatim}' + SkipTo('\\end{verbatim}'))
    doit.ignore('\\begin{comment}' + SkipTo('\\end{comment}'))
    
    f = open(self.fn + '.tex', 'r')
    str = ''.join(f.readlines())
    self.result = doit.transformString(str)

  def sage(self, s, l, t):
    self.sagen += 1
    return self.sout.label[self.sagen - 1]

  def plot(self, s, l, t):
    self.plotn += 1
    if len(t.options) == 0:
      opts = '[width=.75\\textwidth]'
    else:
      opts = t.options[0]
    return '\\includegraphics%s{sage-plots-for-%s.tex/plot-%s}' % \
      (opts, self.fn, self.plotn - 1)


if __name__ == '__main__':
  sout = SoutParser('example.sout')
  print '=' * 50
  print sout.label
