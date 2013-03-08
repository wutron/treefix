TreeFix
http://compbio.mit.edu/treefix/
Yi-Chieh Wu

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

Running treefix with no arguments will print out its command-line usage:

Usage: treefix [options] <gene tree> ...

Options:
  Input/Output:
    -i <input file>, --input=<input file>
                        list of input files, one per line
    -r, --reroot        set to reroot the input tree
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
    -B <bootstrap trees file extension>, --boottreeext=<bootstrap trees file extension>
                        bootstrap trees file extension (default:
                        ".treefix.boot.trees")

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
                        (default: "treefix.models.duplossmodel.DupLossModel")
    -E <extra arguments to module>, --sextra=<extra arguments to module>
                        extra arguments to pass to program

  Search Options:
    -b <# bootstraps>, --boot=<# bootstraps>
                        number of bootstraps to perform (default: 1)
    --seed=<seed>       seed value for random generator
    --niter=<# iterations>
                        number of iterations (default: 100)
    --nquickiter=<# quick iterations>
                        number of subproposals (default: 50)
    --freconroot=<fraction reconroot>
                        fraction of search proposals to reconroot (default:
                        0.05)

  Information:
    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -V <verbosity level>, --verbose=<verbosity level>
                        verbosity level (0=quiet, 1=low, 2=medium, 3=high)
    -l <log file>, --log=<log file>
                        log filename.  Use '-' to display on stdout.

  Debug:
    --debug=<debug mode>
                        debug mode (octal: 0=normal, 1=skips likelihood test,
                        2=skips cost filtering on pool, 4=computes likelihood
                        for all trees in pool)

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
