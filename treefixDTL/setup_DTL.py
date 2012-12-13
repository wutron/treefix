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

# find correct ranger-dtl-U executable
if not os.path.exists('bin/ranger-dtl-U'):
    if sys.platform == 'darwin':
        ranger_dtl_script = 'bin/ranger-dtl-U.mac'
    elif sys.platform == 'cygwin':
        ranger_dtl_script = 'bin/ranger-dtl-U.exe'
    else:
        ranger_dtl_script = 'bin/ranger-dtl-U.linux'
    shutil.copy(ranger_dtl_script, 'bin/ranger-dtl-U')

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
    scripts=['bin/treefixDTL', 'bin/ranger-dtl-U'],
    ext_modules=[]
    )


