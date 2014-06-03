TreeFix
http://compbio.mit.edu/treefix/
Yi-Chieh Wu, with libraries contributed from Matthew Rasmussen

=============================================================================
ABOUT

TreeFix is a phylogenetic program that improves existing gene trees using
the species tree.

TreeFix citation:
Wu, Rasmussen, Bansal, Kellis. TreeFix: Statistically Informed
Gene Tree Error Correction Using Species Trees.
Systematic Biology (62)1:110-120, 2013.



By default, TreeFix uses p-values based on the SH test statistic,
as computed by RAxML.  If you use this default, please also cite

Stamatakis. RAxML-VI-HPC: Maximum Likelihood-based Phylogenetic Analyses
with Thousands of Taxa and Mixed Models. Bioinformatics, 22(21):2688-2690, 2006

The original RAxML source code (v7.0.4) is written by Alexandros Stamatakis
and available at http://sco.h-its.org/exelixis/software.html.



This package includes the Python source code of the TreeFix program,
modified RAxML source code, and several library interfaces for Python.


=============================================================================
USAGE

Running 'treefix -h' will print out its command-line usage.


#=============================================================================
# File formats

TreeFix expects trees to be in newick format and alignments in fasta format.


#=============================================================================
# Likelihood Test and Species Tree Aware Cost Functions

TreeFix requires python modules for

(1) testing likelihood equivalence
    This should inherit treefix.models.StatModel.
    See treefix.models.raxmlmodel.RAxMLModel for an example using the
    SH test statistic with RAxML site-wise likelihoods.

    Any program (e.g. CONSEL) may be used for the actual computation.

(2) computing the species tree aware cost
    This should inherit treefix.models.CostModel.
    See treefix.models.duplossmodel.DupLossModel for an example using
    the duplication/loss cost.

We have also provided a helper function (treefix_compute) for testing these modules.

#=============================================================================
# Examples

See examples/test.sh for an example of how to use TreeFix.
