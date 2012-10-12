#!/bin/sh python
#
# This is an example of how to use TreeFixDTL to correct a tree topology.
#

# Make sure tools are compiled and installed before running the commands in 
# this tutorial.  See INSTALL.txt for more information.

# Or you can run from the source directory:

cd ..
python setup.py build_ext --inplace

# if using Linux
cp bin/ranger-dtl-U.linux bin/ranger-dtl-U
# if using Mac
cp bin/ranger-dtl-U.mac bin/ranger-dtl-U

cd examples
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
#   Likelihood Model:
#     -e <extra arguments to module>, --extra=<extra arguments to module>
#                         extra arguments to pass to program
#
#   Information:
#     -V <verbosity level>, --verbose=<verbosity level>
#                         verbosity level (0=quiet, 1=low, 2=medium, 3=high)
#     -l <log file>, --log=<log file>
#                         log filename.  Use '-' to display on stdout.

treefixDTL \
    -s config/S1.stree \
    -S config/S.smap \
    -A .pep.align \
    -o .pep.raxml.boot.tree \
    -n .pep.raxml.treefixDTL.tree \
    -U .tree \
    -e "-m PROTGAMMAJTT -e 2.0" \
    -V1 -l sim/G1/G1.pep.raxml.treefixDTL.log \
    sim/G1/G1.pep.raxml.boot.tree

# By default, the RAxML likelihood module assumes a GTRGAMMA model of evolution
# and optimizes log likelihood units to a precision of 2.0.
# If you want to use other options, use '-e "<options>"'.
# See also "test RAxML module" below and the RAxML manual.

# By default, the RANGER-DTL reconciliation module assumes that the RANGER-DTL executable 
# is in the system path and can be executed by running "ranger-dtl-U".
# If you want to use a different executable, use '-E "--cmd <command>"'.
# See also "test RANGER-DTL module" below and the RANGER-DTL manual.

#=============================================================================
# Clean up

rm sim/G1/G1.pep.raxml.treefixDTL{.tree,.log}



#=============================================================================
# Helper executable to test various (likelihood and cost) modules

# show help information
treefix_compute -h

#=============================
# test RAxML module

# show help
treefix_compute --type likelihood -m treefix.models.raxmlmodel.RAxMLModel --show-help

# compute pval and Dlnl for true tree using RAxML tree to optimize
treefix_compute --type likelihood -m treefix.models.raxmlmodel.RAxMLModel \
    -A .pep.align -U .pep.raxml.boot.tree \
    -e "-m PROTGAMMAJTT -e 2.0" \
    sim/G1/G1.tree

# clean up
rm sim/G1/G1.output

#=============================
# test RANGER-DTL module

# show help
treefix_compute --type cost -m treefix.models.rangerdtlmodel.DTLModel --show-help

# compute cost for RAxML tree
treefix_compute --type cost -m treefix.models.rangerdtlmodel.DTLModel \
    -s config/S1.stree -S config/S.smap \
    -o .pep.raxml.boot.tree \
    sim/G1/G1.pep.raxml.boot.tree

# compute cost for true tree
treefix_compute --type cost -m treefix.models.rangerdtlmodel.DTLModel \
    -s config/S1.stree -S config/S.smap \
    -o .tree \
    sim/G1/G1.tree

# clean up
rm sim/G1/G1.output
