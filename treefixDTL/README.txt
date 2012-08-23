TreeFixDTL
http://compbio.mit.edu/treefixDTL/
Yi-Chieh Wu,
with libraries contributed by Matthew Rasmussen
and executables contributed by Mukul Bansal

=============================================================================
ABOUT

TreeFixDTL is a phylogenetic program that improves existing gene trees using
the species tree.

TreeFixDTL citation: 
Bansal*, Wu*, Alm, Kellis. TreeFixDTL. In prep.

Additionally, please cite the respective paper corresponding to the module
you use for computing the test statistic for likelihood equivalence.
(See the README.txt files within their respective packages.)

This package includes the Python source code of the TreeFixDTL program
(including the TreeFix program and TreeFixDTL wrapper),
the ranger-dtl-U executable for Linux,
as well as several library interfaces for python.


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

See examples/test.sh for an example of how to use TreeFixDTL.

#=============================================================================
# Miscellaneous

TreeFixDTL is a simple wrapper around the TreeFix program that uses the 
ranger-dtl-U reconciliation model to determine the species tree aware cost.
It has different default options to deal with prokaryotic species and 
removes some functionality from TreeFix that are incompatible with the
ranger-dtl-U reconciliation model.  For more details on the underlying programs,
see

TreeFix    -- http://compbio.mit.edu/treefix/
RANGER-DTL -- http://compbio.mit.edu/ranger-dtl/

