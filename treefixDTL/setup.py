#!/usr/bin/env python
# 
# setup for TreeFixDTL library packages
#
# use the following to install:
#   python setup.py build
#   python setup.py install
#

import os, sys, shutil
from distutils.core import setup, Extension

VERSION = '1.0.0'

if not os.path.exists('bin/ranger-dtl-U'):
    if sys.platform == 'darwin':
        ranger_dtl_script = 'bin/ranger-dtl-U.mac'
    else:
        ranger_dtl_script = 'bin/ranger-dtl-U.linux'
    shutil.copy(ranger_dtl_script, 'bin/ranger-dtl-U')

extra_link_args = []
if sys.platform != 'darwin':
    extra_link_args.append('-s')

srcs = [os.path.join('src/raxml',fn) for fn in os.listdir('src/raxml') 
        if (not os.path.isdir(fn)) and fn.endswith('.c')]
raxml_module = Extension('treefix_raxml._raxml',
                         sources=['python/treefix_raxml/raxml.i'] + srcs,
                         extra_link_args=extra_link_args
                         )

setup(
    name='treefixDTL',
    version=VERSION,
    description='TreeFixDTL',
    long_description = """
            """,
    author='Yi-Chieh Wu',
    author_email='yjw@mit.edu',
#    url='http://compbio.mit.edu/treefixDTL/',
#    download_url='http://compbio.mit.edu/pub/treefixDTL/treefixDTL-%s.tar.gz' % VERSION,
    
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
              'treefix.deps.rasmus', 'treefix.deps.rasmus.ply', 
              'treefix.deps.compbio',
	      'treefix_raxml',
	      'treefix_raxml.deps.rasmus', 'treefix_raxml.deps.rasmus.ply',
	      'treefix_raxml.deps.compbio'],
    py_modules=[],
    scripts=['bin/treefix', 'bin/treefix_compute', 'bin/treefixDTL', 'bin/ranger-dtl-U'],
    ext_modules=[raxml_module]
    )


