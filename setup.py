from distutils.core import setup
setup(name='sagetex',
      description='Embed Sage code and plots into LaTeX',
      long_description="""The SageTeX package allows you to embed code,
  results of computations, and plots from the Sage mathematics
  software suite (http://sagemath.org) into LaTeX documents.""",
      version='2.2',
      author='Dan Drake',
      author_email='ddrake@member.ams.org',
      url='http://mathsci.kaist.ac.kr/~drake',
      license='GPLv2+',
      py_modules=['sagetex'],
      data_files = [('share/texmf/tex/generic/sagetex',
        ['example.pdf',
         'example.tex',
         'extractsagecode.py',
         'makestatic.py',
         'scripts.dtx',
         'remote-sagetex.dtx',
         'remote-sagetex.py',
         'py-and-sty.dtx',
         'sagetexpackage.dtx',
         'sagetexpackage.ins',
         'sagetexpackage.pdf',
         'sagetexparse.py',
         'sagetex.sty'])])


