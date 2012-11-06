#
# Python module for RAXML library
#

import sys,os

# import RAXML SWIG module
import raxml

# load rasmus libraries if available
def load_deps(dirname="deps"):
    sys.path.append(os.path.realpath(
        os.path.join(os.path.dirname(__file__), dirname)))

# add pre-bundled dependencies to the python path,
# if they are not available already
try:
    import rasmus, compbio
except ImportError:
    load_deps()
    import rasmus, compbio
from rasmus import treelib

# normal distribution
try:
    # scipy libraries
    from scipy.stats import norm
    sf = norm.sf
except ImportError:
    # use approximation from rasmus stats library
    from rasmus import stats
    sf = lambda x: 1-stats.normalCdf(x, (0,1))

#=============================================================================

class RAxML:
    """Wrapper for RAxML functions"""
    
    #=========================================
    # constructors/destructors
    
    def __init__(self):
        self.rooted = False # RAxML uses unrooted trees
        self.adef = raxml.new_analdef()
        raxml.init_adef(self.adef)
        self.tr = raxml.new_tree()
        self.optimal = False
        self.best_LH = None; self.weight_sum = None; self.best_vector = None

    def __del__(self):
        raxml.delete_analdef(self.adef)
        raxml.delete_tree(self.tr)
        if self.best_vector is not None:
            raxml.delete_best_vector(self.best_vector)

    #=========================================
    # utilities
    
    def read_tree(self, tree):
        """Read treelib tree to raxml tr"""
        r,w = os.pipe()
        fr,fw = os.fdopen(r, 'r'), os.fdopen(w, 'w')

        tree.write(fw, oneline=True); fw.write('\n')
        fw.close()

        raxml.read_tree(fr, self.tr, self.adef)
        fr.close()    

    def draw_raxml_tree(self, *args, **kargs):
        """Draw raxml tr -- adef and tr must have been previously defined"""
        treestr = raxml.tree_to_string(self.tr, self.adef)
        tree = treelib.parse_newick(treestr)
        treelib.draw_tree(treelib.unroot(tree), *args, **kargs)

    #=========================================
    # model optimization
    
    def optimize_model(self, treefile, seqfile, extra="-m GTRGAMMA -n test"):
        """Optimizes the RAXML model"""

        # initialize parameters based on input
        cmd = "raxmlHPC -t %s -s %s %s" %\
              (treefile, seqfile, extra)
        raxml.init_program(self.adef, self.tr, cmd.split(' '))

        # optimize
        raxml.optimize_model(self.adef, self.tr)

        # reset best LH
        if self.best_vector is not None:
            raxml.delete_best_vector(self.best_vector)
        self.best_vector, self.best_LH, self.weight_sum = raxml.compute_best_LH(self.tr)

        # set flags
        self.optimal = True

    #=========================================    
    # test statistics
    
    def compute_lik_test(self, tree, test="SH", report="both"):
        """
        Computes the test statistic, returning the pvalue and Dlnl
        report -- "under":  one-sided test, i.e. H0: LH_{tree} > LH_{optimal} v H1: LH_{tree} < LH_{optimal}
                  "over": one-sided test, i.e. H0: LH_{tree} < LH_{optimal} v H1: LH_{tree} > LH_{optimal}
                  "both":  two-sided test, i.e. H0: LH_{tree} == LH_{optimal} v H1: LH_{tree} != LH_{optimal}
        """
        ##use scipy.stats to determine whether zscore is significant
        ##sf = 1 - cdf, zprob = cdf
        ##>>> stats.norm.sf(2)*2      # two-sided
        ##0.045500263896358417
        ##>>> (1-stats.zprob(2))*2    # two-sided
        ##0.045500263896358417
        ##>>> stats.zprob(2)
        ##0.97724986805182079
        ##>>> stats.norm.cdf(2)
        ##0.97724986805182079
        
        if test == "SH":
            if not self.optimal:
                raise Exception("The model is not optimized: call optimize_model.\n")

            self.read_tree(tree)
            zscore, Dlnl = raxml.compute_LH(self.adef, self.tr,
                                            self.best_LH, self.weight_sum, self.best_vector)

            # really should just use pval = sf(zscore) if one of the trees is the ML tree,
            # but SH test compares two a priori trees (to determine if T_x and T_y
            # are equally good explanations of the data), so raxml uses two-sided test
            if report == "under":
                # high zscore => low pval => statistically worse tree
                return sf(zscore), Dlnl
            elif report == "over":
                # low zscore => low pval => statistically better tree
                return 1-sf(zscore), Dlnl
            elif report == "both":
                # high abs(zscore) => low pval => statistically nonequivalent tree
                return sf(abs(zscore))*2, Dlnl
            else:
                raise Exception("report must be 'over', 'under', or 'both': %s" % report)

        raise Exception("%s test statistic not implemented" % test)
