#!/usr/bin/env python
# 
# setup for TreeFix-DTL library packages
# (if TreeFix has already been installed)
#
# use the following to install:
#   python setup.py install
#

import os, sys, shutil
from distutils.core import setup, Extension

# version control
sys.path.insert(0, os.path.realpath(
            os.path.join(os.path.dirname(__file__), "python")))
from treefix import treefixDTL
VERSION = treefixDTL.PROGRAM_VERSION_TEXT

setup(
    name='treefixDTL',
    version=VERSION,
    description='TreeFix-DTL',
    long_description = """
            """,
    author='Yi-Chieh Wu',
    author_email='yjw@mit.edu',
#    url='http://compbio.mit.edu/treefix-dtl/',
#    download_url='http://compbio.mit.edu/treefix-dtl/pub/sw/treefixDTL-%s.tar.gz' % VERSION,
    
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
    packages=[],
    py_modules=['treefix.treefixDTL', 'treefix.models.rangerdtlmodel'],
    scripts=['bin/treefixDTL'],
    ext_modules=[]
    )


