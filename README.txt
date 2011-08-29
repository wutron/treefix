TreeFix
http://compbio.mit.edu/treefix/
Yi-Chieh Wu, with libraries contributed from Matthew Rasmussen

=============================================================================
ABOUT

TreeFix is a phylogenetic program that improves existing gene trees using
the species tree.

TreeFix citation: 
Wu, Rasmussen, Bansal, Kellis. TreeFix: improving existing gene tree reconstructions 
using the species tree. Genome Biology. In prep.

This package includes the Python source code of the TreeFix program
as well as several library interfaces for python.


=============================================================================
USAGE

Running treefix with no arguments will print out its command-line usage:

Usage: treefix [options] <gene tree> ...

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

  Cost Function:
    -D <dup cost>, --dupcost=<dup cost>
                        duplication cost (default: 1.0)
    -L <loss cost>, --losscost=<loss cost>
                        loss cost (default: 1.0)

  Likelihood Model:
    -m <module for tree calculations>, --module=<module for tree calculations>
                        module for tree calculations (default: "raxml")
    -e <extra arguments to module>, --extra=<extra arguments to module>
                        extra arguments to pass to program

  Likelihood Test:
    -t <test statistic>, --test=<test statistic>
                        test statistic for likelihood equivalence (default:
                        "SH")
    -p <p-value>, --pval=<p-value>
                        p-value threshold (default: 0.05)

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
    --debug             debug mode

#=============================================================================
# Likelihood Test

TreeFix requires a python module for computing the test statistic for
likelihood equivalence.  Any program (e.g. CONSEL) may be used for the actual
computation.  We have provided a module that uses RAxML at
http://compbio.mit.edu/treefix/index.html#raxml.

The module should have at least one variable and four commands:
    -- rooted
       True if module uses rooted trees.
    -- init()
       Initializes the module.
    -- cleanup()
       Performs any cleanup of the module.
    -- optimize_model(treefile, seqfile, extra)
       Optimizes the underlying model in the module given the tree, seq (alignment),
       and extra parameter arguments.
    -- compute_lik_test(tree, test statistic)
       Computes the test statistic for tree likelihood equivalence.
       Returns the p-value and Dlnl (delta lik = best lik - current lik).

#=============================================================================
# Examples

See examples/test.sh for an example of how to use TreeFix.
