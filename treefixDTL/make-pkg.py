#!/usr/bin/env python
# package treefixDTL

files = ["src",
         "python",
         "examples",

         "setup.py",
         "setup_DTL.py",
         "setup_TreeFixDTL.py",
         "README.txt",
	 "INSTALL.txt",
	 "LICENSE.txt",
	 "CHANGES.txt"]

exclude = ["examples/getexample\.sh",
           ".*\.linux$", ".*\.pyc$", ".*\.so$",
           "python/treefix_raxml/raxml_wrap\.c",
	   "python/treefix_raxml/raxml\.py",
	   "python/treefix/[^/]*\.py",
           "python/treefix/models/.*"]

include = ["bin/treefix", "bin/treefix_compute",
           "bin/treefixDTL",
           "bin/ranger-dtl-U.linux",
	   "bin/ranger-dtl-U.mac",
	   "bin/ranger-dtl-U.exe",
	   "python/treefix/__init__.py",
	   "python/treefix/common.py",
	   "python/treefix/treefixDTL.py",
           "python/treefix/models/__init__.py",
           "python/treefix/models/raxmlmodel.py",
	   "python/treefix/models/rangerdtlmodel.py"]

#=============================================================================

import os, sys, re, shutil
from subprocess import call, Popen, PIPE

pkgdir = sys.argv[1]

if os.path.exists(pkgdir):
    shutil.rmtree(pkgdir)

exclude_expr = "|".join(exclude)

p = Popen(["find", "-L"] + files, stdout=PIPE)
all_files = [x.rstrip("\n") for x in p.stdout.readlines()]
all_files = [x for x in all_files
             if not re.match(exclude_expr, x)] + include

for f in all_files:
    dest = os.path.join(pkgdir, f)
    destdir = os.path.dirname(dest)
    print f, "-->", dest

    if os.path.isfile(f):
        # copy file
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        shutil.copy(f, dest)
    else:
        # make dir
        if not os.path.exists(dest):
            os.makedirs(dest)

# tar
basename = os.path.basename(pkgdir)
print ' '.join(["tar", "-C", os.path.dirname(pkgdir), "-zcvf",
                pkgdir + ".tar.gz", basename])
call(["tar", "-C", os.path.dirname(pkgdir), "-zcvf",
      pkgdir + ".tar.gz", basename])

