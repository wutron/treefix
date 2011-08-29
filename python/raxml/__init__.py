#
# Python module for RAXML library
#

import sys,os

# import RAXML SWIG module
import raxml

# scipy libraries
from scipy.stats import norm

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


#=============================================================================
# globals

_GLOBAL = None
rooted = False	# RAxML uses unrooted trees

class Globals:
    def __init__(self):
        self.adef = raxml.new_analdef()
        self.tr = raxml.new_tree()
        self.optimal = False
        self.best_LH = None; self.weight_sum = None; self.best_vector = None

    def __del__(self):
        raxml.delete_analdef(self.adef)
        raxml.delete_tree(self.tr)
        if self.best_vector is not None:
            raxml.delete_best_vector(self.best_vector)

#=============================================================================
# init/cleanup

def init():
    """Initializes internal variables"""
    global _GLOBAL
    if _GLOBAL is None:
        _GLOBAL = Globals()
    else:
        raise Exception("Are you trying to reinitialize?  Call cleanup first.")

def cleanup():
    """Cleans up internal variables"""
    global _GLOBAL
    if _GLOBAL is None:
        pass
    del _GLOBAL
    _GLOBAL = None

def globalRAXML():
    global _GLOBAL
    if _GLOBAL is None:
        init()
    return _GLOBAL        

#=============================================================================
# model optimization

def optimize_model(treefile, seqfile, extra="-m GTRGAMMA -n test"):
    """Optimizes the RAXML model"""
    myraxml = globalRAXML()
    
    cmd = "raxmlHPC -t %s -s %s %s" %\
          (treefile, seqfile, extra)
    raxml.init_program(myraxml.adef, myraxml.tr, cmd.split(' '))

    raxml.optimize_model(myraxml.adef, myraxml.tr)
    myraxml.optimal = True
    
#=============================================================================
# SH test

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
   
def compute_lik_test(tree, test="SH"):
    """Computes the test statistic, returning the pvalue and Dlnl"""
    if test == "SH":
        myraxml = globalRAXML()
    
        if not myraxml.optimal:
            raise Exception("The model is not optimized: call optimize_model.\n")
        if myraxml.best_LH is None:
            myraxml.best_vector, myraxml.best_LH, myraxml.weight_sum = raxml.compute_best_LH(myraxml.tr)
            
        read_tree(tree)
        zscore, Dlnl = raxml.compute_LH(myraxml.adef, myraxml.tr,
                                        myraxml.best_LH, myraxml.weight_sum, myraxml.best_vector)
        if Dlnl <= 0:
            return 1.0, Dlnl
        
        # really should just use pval = norm.sf(zscore) if one of the trees is the ML tree, 
	# but SH test compares two a priori trees (to determine if T_x and T_y
	# are equally good explanations of the data), so raxml uses two-sided test
        return norm.sf(zscore)*2, Dlnl

    raise Exception("%s test statistic not implemented" % test)

#=============================================================================
# utilities

def read_tree(tree):
    """Read treelib tree to raxml tr"""
    myraxml = globalRAXML()
    
    r,w = os.pipe()
    fr,fw = os.fdopen(r, 'r'), os.fdopen(w, 'w')

    tree.write(fw, oneline=True); fw.write('\n')
    fw.close()

    raxml.read_tree(fr, myraxml.tr, myraxml.adef)
    fr.close()    

def draw_raxml_tree(*args, **kargs):
    """Draw raxml tr -- adef and tr must have been previously defined"""
    myraxml = globalRAXML()
    treestr = raxml.tree_to_string(myraxml.tr, myraxml.adef)
    tree = treelib.parse_newick(treestr)
    treelib.draw_tree(treelib.unroot(tree), *args, **kargs)
