TreeFix-RAxML (Python Wrapper for RAxML for use with TreeFix)
http://compbio.mit.edu/treefix/index.html#raxml
Yi-Chieh Wu

=============================================================================
ABOUT

RAxML is a popular phylogenetic program for gene tree reconstruction.
TreeFix-RAxML simply uses SWIG to provide a Python wrapper.

RAxML citation:
Stamatakis. RAxML-VI-HPC: Maximum Likelihood-based Phylogenetic Analyses 
with Thousands of Taxa and Mixed Models. Bioinformatics 22(21):2688-2690, 2006

TreeFix-RAxML citation: 
Wu, Rasmussen, Bansal, Kellis. TreeFix: statistically informed
gene tree error correction using species trees. Systematic Biology. Accepted.

The original RAxML source code (v7.0.4) is written by Alexandros Stamatakis
and available at http://wwwkramer.in.tum.de/exelixis/software.html.

This package includes modified C source of the RAxML program and
a SWIG interface and Python module for calling RAxML functions from Python.
Currently, you can optimize the RAxML model and compute the SH statistic.
Further functions in RAxML may be exposed in the wrapper at a future
date.

To test the RAxML module, additional libraries contributed by Matthew Rasmussen
are also provided.

#=============================================================================
# Examples

See examples/test.sh for an example of how to use TreeFix-RAxML.
