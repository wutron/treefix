#!/usr/bin/env python
#
# setup for TreeFix-RAxML library packages
#
# use the following to install:
#   python setup.py build
#   python setup.py install
#

from distutils.core import setup, Extension
import os,sys

VERSION = '0.2.3'

extra_link_args = []
if sys.platform != 'darwin':
    extra_link_args.append('-s')

srcs = [os.path.join('src',fn) for fn in os.listdir('src') 
        if (not os.path.isdir(fn)) and fn.endswith('.c')]
raxml_module = Extension('treefix_raxml._raxml',
                         sources=['python/treefix_raxml/raxml.i'] + srcs,
                         extra_link_args=extra_link_args
                         )
 
setup(
    name='treefix_raxml',
    version=VERSION,
    description='Python wrapper for RAxML',
    author='Yi-Chieh Wu',
    author_email='yjw@mit.edu',
#    url='http://compbio.mit.edu/treefix/index.html#raxml',

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

    package_dir = {'': 'python'},
    packages = ['treefix_raxml',
                'treefix_raxml.deps.rasmus', 'treefix_raxml.deps.rasmus.ply',
                'treefix_raxml.deps.compbio'],
#    py_modules=['raxml'],
    ext_modules=[raxml_module]
    )
