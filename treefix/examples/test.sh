#!/bin/sh python
#
# This is an example of how to use TreeFix to correct a tree topology.
#

# Make sure tools are compiled and installed before running the commands in 
# this tutorial.  See INSTALL.txt for more information.

# Or you can run from the source directory:

cd ..
python setup.py build_ext --inplace

cd examples
export PATH=$PATH:../bin
export PYTHONPATH=$PYTHONPATH:../python

#=============================================================================
# Compute the corrected gene tree using RAxML SH statistics and dup/loss cost model

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
#     -U <user tree file extension>, --usertreeext=<user tree file extension>
#                         check if user tree is visited in search
#
#   Information:
#     -V <verbosity level>, --verbose=<verbosity level>
#                         verbosity level (0=quiet, 1=low, 2=medium, 3=high)
#     -l <log file>, --log=<log file>
#                         log filename.  Use '-' to display on stdout.

treefix \
    -s config/fungi.stree \
    -S config/fungi.smap \
    -A .nt.align \
    -o .nt.raxml.tree \
    -n .nt.raxml.treefix.tree \
    -U .tree \
    -V1 -l sim-fungi/0/0.nt.raxml.treefix.log \
    sim-fungi/0/0.nt.raxml.tree

#=============================================================================
# Clean up

rm sim-fungi/0/0.nt.raxml.treefix{.tree,.log}



#=============================================================================
# Using other parameters in the likelihood or reconciliation cost modules

# By default, the likelihood module used by TreeFix assumes a GTRGAMMA model of 
# sequence evolution and a model optimization precision of eps=2.0.  
# To change this, add the following to the treefix command:
#     -e '-m <model> -e <eps>'
# The specified model must be supported by RAxML.

# By default, the reconciliation cost module used by TreeFix assumes equal costs 
# (D=1, L=1) for inferred (duplication-loss) events.  
# To change this, add the following to the treefix command:
#     -E '-D <dup cost> -L <loss cost>'
# The costs must be non-negative.

# Be sure to watch the quotes.  The '-e' ('-E') switch tells treefix to pass the 
# following options to the module used for likelihood (reconciliation cost) calculation.
# See also "test RAxML module" and "test dup/loss module" below.



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
    -A .nt.align -U .nt.raxml.tree \
    sim-fungi/0/0.tree

# clean up
rm sim-fungi/0/0.output

#=============================
# test dup/loss module

# show help
treefix_compute --type cost -m treefix.models.duplossmodel.DupLossModel --show-help

# compute cost for RAxML tree
treefix_compute --type cost -m treefix.models.duplossmodel.DupLossModel \
    -r -s config/fungi.stree -S config/fungi.smap \
    -o .nt.raxml.tree \
    sim-fungi/0/0.nt.raxml.tree

# compute cost for true tree
treefix_compute --type cost -m treefix.models.duplossmodel.DupLossModel \
    -r -s config/fungi.stree -S config/fungi.smap \
    -o .tree \
    sim-fungi/0/0.tree

# clean up
rm sim-fungi/0/0.output
