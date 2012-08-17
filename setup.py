#!/usr/bin/env python
# 
# setup for TreeFix library packages
#
# use the following to install:
#   python setup.py install
#

from distutils.core import setup, Extension

VERSION = '1.1.4'

setup(
    name='treefix',
    version=VERSION,
    description='TreeFix',
    long_description = """
            """,
    author='Yi-Chieh Wu',
    author_email='yjw@mit.edu',
#    url='http://compbio.mit.edu/treefix/',
#    download_url='http://compbio.mit.edu/pub/treefix/treefix-%s.tar.gz' % VERSION,
    
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
    scripts=['bin/treefix', 'bin/treefix_compute'],
    #ext_modules=[
    #    Extension(
    #        '', 
    #        [],
    #        include_dirs=[],
    #        libraries=[]
    #        )]
    )


