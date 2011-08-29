#!/bin/sh python
#
# This is an example of how to use TreeFix to correct a tree topology.
#

# Make sure tools are compiled and installed before running the commands in 
# this tutorial.  See INSTALL.txt for more information.

# Or you can run from the source directory:

export PATH=$PATH:../bin
export PYTHONPATH=$PYTHONPATH:../python

#=============================================================================
# Compute the SH statistics for variations on an original gene trees.

# show help information
treefix -h

# Usage: treefix [options] <gene tree> ...
#
# Options:
#   Input/Output:
#     -s <species tree>, --stree=<species tree>
#                         species tree file in newick format
#     -S <species map>, --smap=<species map>
#                         gene to species map
#     -A <alignment file extension>, --alignext=<alignment file extension>
#                         alignment file extension (default: ".align")
#     -o <old tree file extension>, --oldext=<old tree file extension>
#                         old tree file extension (default: ".tree")
#     -n <new tree file extension>, --newext=<new tree file extension>
#                         new tree file extension (default: ".treefix.tree")
#
#   Information:
#     -V <verbosity level>, --verbose=<verbosity level>
#                         verbosity level (0=quiet, 1=low, 2=medium, 3=high)
#     -l <log file>, --log=<log file>
#                         log filename.  Use '-' to display on stdout.

treefix \
    -s config/fungi.stree \
    -S config/fungi.smap \
    -A .nt.align.phylip \
    -o .nt.raxml.tree \
    -n .nt.raxml.treefix.tree \
    -V2 -l sim-fungi/0/0.nt.raxml.treefix.log \
    sim-fungi/0/0.nt.raxml.tree

#=============================================================================
# Clean up

rm sim-fungi/0/0.nt.raxml.treefix{.tree,.log}

