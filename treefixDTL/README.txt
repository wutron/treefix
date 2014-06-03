TreeFix-DTL
http://compbio.mit.edu/treefix-dtl/
Yi-Chieh Wu,
with libraries contributed by Matthew Rasmussen
and executables contributed by Mukul Bansal

=============================================================================
ABOUT

TreeFix-DTL is a phylogenetic program for reconstructing highly
accurate prokaryotic gene trees.  TreeFix-DTL uses the species tree
topology to guide the reconstruction of the gene tree and balanaces
sequence and species tree information through a statistical hypothesis
testing framework.  TreeFix-DTL operates under the assumption that
multiple gene tree topologies are "statistically equivalent" (as
evaluated using a likelihood ratio test), and the optimal topology
among this set is one that is most parsimonious (where the cost of the
topology is dependent on the inferred gene duplication, horizontal
gene transfer, and gene loss events).  Specifically, given a (maximum
likelihood) gene tree, a multiple sequence alignment, and a rooted
species tree, TreeFix-DTL finds an alternative gene tree topology that
minimizes the duplication-transfer-loss reconciliation cost while
still being supported by the sequence data.

TreeFix-DTL citation:
Bansal*, Wu*, Alm, Kellis. Improving the Accuracy of Gene Tree Reconstruction
in Prokaryotes: Strategies and Impact. Submitted.



By default, TreeFix-DTL uses p-values based on the SH test statistic,
as computed by RAxML.  If you use this default, please also cite

Stamatakis. RAxML-VI-HPC: Maximum Likelihood-based Phylogenetic Analyses
with Thousands of Taxa and Mixed Models. Bioinformatics 22(21):2688-2690, 2006

The original RAxML source code (v7.0.4) is written by Alexandros Stamatakis
and available at http://sco.h-its.org/exelixis/software.html.



This package includes the Python source code of the TreeFix-DTL program
(including the TreeFix program and TreeFix-DTL wrapper),
modified RAxML source code, the ranger-dtl-U executable,
as well as several library interfaces for Python.


=============================================================================
DETAILS

TreeFix-DTL is a wrapper around the TreeFix program that uses the
ranger-dtl-U reconciliation model (v1.0) to determine the species tree aware cost.
It has different default options to deal with prokaryotic species and
removes some functionality from TreeFix that are incompatible with the
ranger-dtl-U reconciliation model.  Note also that using default modules,
TreeFix-DTL returns an *unrooted* gene tree (though all trees used by the program
are expected to be written as rooted trees in newick format).

For more details on the underlying programs, see
TreeFix    -- http://compbio.mit.edu/treefix/
RANGER-DTL -- http://compbio.mit.edu/ranger-dtl/


=============================================================================
USAGE

Running treefixDTL with no arguments will print out its command-line usage:

Usage: treefixDTL [options] <gene tree> ...

Options:
  Input/Output:
    -i <input file>, --input=<input file>
                        list of input files, one per line
    -s <species tree>, --stree=<species tree>
                        species tree file in newick format
    -S <species map>, --smap=<species map>
                        gene to species map
    -A <alignment file extension>, --alignext=<alignment file extension>
                        alignment file extension (default: ".align")
    -U <user tree file extension>, --usertreeext=<user tree file extension>
                        check if user tree is visited in search
    -o <old tree file extension>, --oldext=<old tree file extension>
                        old tree file extension (default: ".tree")
    -n <new tree file extension>, --newext=<new tree file extension>
                        new tree file extension (default: ".treefix.tree")

  Likelihood Model:
    -m <module for likelihood calculations>, --module=<module for likelihood calculations>
                        module for likelihood calculations (default:
                        "treefix.models.raxmlmodel.RAxMLModel")
    -e <extra arguments to module>, --extra=<extra arguments to module>
                        extra arguments to pass to program

  Likelihood Test:
    -t <test statistic>, --test=<test statistic>
                        test statistic for likelihood equivalence (default:
                        "SH")
    --alpha=<alpha>     alpha threshold (default: 0.05)
    -p <alpha>, --pval=<alpha>
                        same as --alpha

  Species Tree Cost Model:
    -M <module for species tree aware cost calculations>, --smodule=<module for species tree aware cost calculations>
                        module for species tree aware cost calculations
                        (default: "treefix.models.rangerdtlmodel.DTLModel")
    -E <extra arguments to module>, --sextra=<extra arguments to module>
                        extra arguments to pass to program

  Search Options:
    --seed=<seed>       seed value for random generator
    --niter=<# iterations>
                        number of iterations (default: 1000)
    --nquickiter=<# quick iterations>
                        number of subproposals (default: 100)

  Information:
    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -V <verbosity level>, --verbose=<verbosity level>
                        verbosity level (0=quiet, 1=low, 2=medium, 3=high)
    -l <log file>, --log=<log file>
                        log filename.  Use '-' to display on stdout.

#=============================================================================
# Examples

See examples/test.sh for an example of how to use TreeFix-DTL.
