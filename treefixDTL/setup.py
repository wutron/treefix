#!/usr/bin/env python
# 
# setup for TreeFixDTL library packages
#
# use the following to install:
#   python setup.py install
#

from distutils.core import setup, Extension

VERSION = '1.0.0'

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
              'treefix.deps.compbio'],
    py_modules=[],
    scripts=['bin/treefix', 'bin/treefixDTL'],
    #ext_modules=[
    #    Extension(
    #        '', 
    #        [],
    #        include_dirs=[],
    #        libraries=[]
    #        )]
    )


