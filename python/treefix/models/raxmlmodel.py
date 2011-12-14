#
# Python module for SH test using RAxML likelihoods
# Requires raxml libraries (http://compbio.mit.edu/treefix/#raxml)
#

# treefix libraries
from treefix.models import StatModel

# raxml library
import raxml

# python libraries
import os, sys
import optparse

# rasmus libraries
from rasmus import util

class RAxMLModel(StatModel):
    """Computes test statistics using RAxML site-wise likelihoods"""
    
    def __init__(self):
        """Initializes the RAxML model"""
        self._raxml = raxml.RAxML()
        self.rooted = self._raxml.rooted

        parser = optparse.OptionParser(prog="RAxMLModel")
        parser.add_option("-m", "--model", dest="model",
                          metavar="<model>",
                          default="GTRGAMMA",
                          help="model of nucleotide or amino acid substitution (default: GTRGAMMA)")
        parser.add_option("-e", "--eps", dest="eps",
                          metavar="<eps>",
                          default=2.0, type="float",
                          help="model optimization precision in log likelihood units for final (default 2.0)")
        self.parser = parser

    def __del__(self):
        """Cleans up the RAxML model"""
        del self._raxml

    def optimize_model(self, gtree, seqfile, extra):
        """Optimizes the RAxML model"""
        StatModel.optimize_model(self, gtree, seqfile, extra)
        
        fd, treefile = util.temporaryfile.mkstemp('.tree')
        os.close(fd)
        gtree.write(treefile)
        
        self._raxml.optimize_model(treefile, seqfile,
                                   "-m %s -n test" % self.model)

        os.remove(treefile)
        
    def compute_lik_test(self, gtree, stat="SH"):
        """Computes the test statistic 'stat' using RAxML likelihoods"""
        return self._raxml.compute_lik_test(gtree, stat)
