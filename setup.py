#!/usr/bin/env python
#
# setup for PyRAxML library packages
#
# use the following to install:
#   python setup.py build
#   python setup.py install
#

from distutils.core import setup, Extension
import os,sys

VERSION = '0.1'

#old_filename = os.path.join("python", "raxml.py")
#new_filename = os.path.join("python", "__init__.py")
#if os.path.exists(old_filename):
#    os.rename(old_filename, new_filename)

extra_link_args = []
if sys.platform != 'darwin':
    extra_link_args.append('-s')

#srcs = []
srcs = [os.path.join('src',fn) for fn in os.listdir('src') 
        if (not os.path.isdir(fn)) and fn.endswith('.c')]
raxml_module = Extension('_raxml',
                         sources=['python/raxml/raxml_wrap.c'] + srcs,
#                         libraries=['example'],
#                         library_dirs=['lib'],
                         extra_link_args=extra_link_args
                         )
 
setup(
    name='raxml',
    version=VERSION,
    description='Python wrapper for RAxML',
    author='Yi-Chieh Wu',
    author_email='yjw@mit.edu',
#    url='http://compbio.mit.edu/raxml_python/',

    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
	  'Programming Language :: C',
          'Topic :: Education',
          ],

    package_dir = {'raxml':'python'},
    packages = ['raxml'],
#    py_modules=['raxml'],
    ext_modules=[raxml_module]
    )
