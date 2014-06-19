#!/usr/bin/env python
#
# setup for TreeFix library packages
#
# use the following to install:
#   python setup.py build
#   python setup.py install
#

import os,sys
from distutils.core import setup, Extension

sys.path.insert(0, os.path.realpath(
    os.path.join(os.path.dirname(__file__), "python")))
import treefix
VERSION = treefix.PROGRAM_VERSION_TEXT

extra_link_args = ['-lm']
if sys.platform != 'darwin':
    extra_link_args.append('-s')

srcs = [os.path.join('src/raxml',fn) for fn in os.listdir('src/raxml')
        if (not os.path.isdir(fn)) and fn.endswith('.c')]
raxml_module = Extension('treefix_raxml._raxml',
                         sources=['python/treefix_raxml/raxml.i'] + srcs,
                         extra_link_args=extra_link_args
                         )

setup(
    name='treefix',
    version=VERSION,
    description='TreeFix',

    author='Yi-Chieh Wu',
    author_email='yjw@mit.edu',
#    url='http://compbio.mit.edu/treefix/',
#    download_url='http://compbio.mit.edu/treefix/pub/sw/treefix-%s.tar.gz' % VERSION,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        ],

    package_dir = {'': 'python'},
    packages=['treefix',
              'treefix.models',
              'treefix.deps.rasmus',
              'treefix.deps.compbio',
              'treefix_raxml',
              'treefix_raxml.deps.rasmus',
              'treefix_raxml.deps.compbio'],
    py_modules=[],
    scripts=['bin/treefix',
             'bin/treefix_compute',
             'bin/tree-annotate'],
    ext_modules=[raxml_module]
    )
