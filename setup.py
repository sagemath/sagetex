from setuptools import setup, find_packages

setup(
      name='sagetex',
      description='Embed Sage code and plots into LaTeX',
      long_description="""The SageTeX package allows you to embed code,
  results of computations, and plots from the Sage mathematics
  software suite (http://sagemath.org) into LaTeX documents.""",
      long_description_content_type='text/markdown',
      version='3.6',
      author='Dan Drake',
      author_email='dr.dan.drake@gmail.com',
      maintainer='SageMath developers',
      maintainer_email='sage-devel@googlegroups.com',
      url='https://github.com/sagemath/sagetex',
      license='GPLv2+',
      py_modules=['sagetex', 'sagetexparse'],
      packages=find_packages(),
      scripts=['sagetex-run', 'sagetex-extract', 'sagetex-makestatic', 'sagetex-remote'],
      install_requires=['pyparsing'],
      classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Operating System :: OS Independent",
      ],
      data_files = [('share/texmf/tex/latex/sagetex',
        ['example.tex',
         'CONTRIBUTORS',
         'scripts.dtx',
         'remote-sagetex.dtx',
         'py-and-sty.dtx',
         'sagetex.dtx',
         'sagetex.ins',
         'sagetex.sty']),
      ('share/doc/sagetex', [
         'example.tex',
         'sagetex.pdf',
         'example.pdf'])])
