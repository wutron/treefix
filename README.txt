TreeFix
http://compbio.mit.edu/treefix/
Yi-Chieh Wu, with libraries contributed from Matthew Rasmussen

=============================================================================
ABOUT

TreeFix is a phylogenetic program that improves existing gene trees using
the species tree.

TreeFix citation: 
Wu, Rasmussen, Bansal, Kellis. TreeFix: statistically informed 
gene tree error correction using species trees. Systematic Biology. Accepted.

Additionally, please cite the respective paper corresponding to the module
you use for computing the test statistic for likelihood equivalence.
(See the README.txt files within their respective packages.)

This package includes the Python source code of the TreeFix program
as well as several library interfaces for python.


=============================================================================
USAGE

Running treefix with no arguments will print out its command-line usage:

Usage: treefix [options] <gene tree> ...

Options:
  --version             show program's version number and exit

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
    --seed=<seed>       seed value for random generator
    --niter=<# iterations>
                        number of iterations (default: 100)
    --nquickiter=<# quick iterations>
                        number of subproposals (default: 50)
    --freconroot=<fraction reconroot>
                        fraction of search proposals to reconroot (default:
                        0.05)

  Information:
    -V <verbosity level>, --verbose=<verbosity level>
                        verbosity level (0=quiet, 1=low, 2=medium, 3=high)
    -l <log file>, --log=<log file>
                        log filename.  Use '-' to display on stdout.
    -h, --help          show this help message and exit

  Debug:
    --cached            set to cache likelihoods and costs
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
    SH test statistic with RAxML sitewise likelihoods.

    Any program (e.g. CONSEL) may be used for the actual computation.
    We have provided a module that uses RAxML
    (requires a python wrapper around RAxML, available at
    http://compbio.mit.edu/treefix/index.html#raxml).

(2) computing the species tree aware cost
    This should inherit treefix.models.CostModel.
    See treefix.models.duplossmodel.DupLossModel for an example using
    the duplication/loss cost.

We have also provided a helper function (treefix_compute) for testing these modules.

#=============================================================================
# Examples

See examples/test.sh for an example of how to use TreeFix.
