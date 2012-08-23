#!/bin/sh python
#
# This is an example of how to use TreeFixDTL to correct a tree topology.
#

# Make sure tools are compiled and installed before running the commands in 
# this tutorial.  See INSTALL.txt for more information.

# Or you can run from the source directory:

export PATH=$PATH:../bin
export PYTHONPATH=$PYTHONPATH:../python

#=============================================================================
# Compute the corrected gene tree using RAxML SH statistics and ranger-dtl-U cost model

# show help information
treefixDTL -h

# Usage: treefixDTL [options] <gene tree> ...
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
#     -U <user tree file extension>, --usertreeext=<user tree file extension>
#                         check if user tree is visited in search
#
#   Information:
#     -V <verbosity level>, --verbose=<verbosity level>
#                         verbosity level (0=quiet, 1=low, 2=medium, 3=high)
#     -l <log file>, --log=<log file>
#                         log filename.  Use '-' to display on stdout.

treefix \
    -s config/S1.stree \
    -S config/S.smap \
    -A .pep.align \
    -o .pep.raxml.tree \
    -n .pep.raxml.treefixDTL.tree \
    -U .tree \
    -V1 -l sim/G1/G1.pep.raxml.treefixDTL.log \
    sim/G1/G1.pep.raxml.tree

#=============================================================================
# Clean up

rm sim/G1/G1.pep.raxml.treefixDTL{.tree,.log}

