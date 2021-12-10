import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.build_py import build_py
import ninja

class pre_develop(develop):
    """Pre-installation for development mode."""
    def run(self):
        ninja.subprocess.run(['ninja'],check=True)
        # ninja.subprocess.run(['make'],check=True)
        develop.run(self)

class pre_install(install):
    """Pre-installation for installation mode."""
    def run(self):
        ninja.subprocess.run(['ninja'],check=True)
        install.run(self)

class pre_build(build_py):
    """Pre-installation for build mode."""
    def run(self):
        ninja.subprocess.run(['ninja'],check=True)
        build_py.run(self)

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
      cmdclass={
          'develop': pre_develop,
          'install': pre_install,
          'build_py': pre_build,
      },
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
      ('', ['build.ninja']),  
      ('share/doc/sagetex', [
         'example.tex',
         'sagetex.pdf',
         'example.pdf'])])
