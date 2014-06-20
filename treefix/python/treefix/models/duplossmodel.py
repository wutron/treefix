#
# Python module for duploss cost
#

# treefix libraries
from treefix.models import CostModel

# python libraries
import optparse

# rasmus libraries
from rasmus import treelib

# compbio libraries
from compbio import phylo

#=============================================================================

class DupLossModel(CostModel):
    """Computes Dup/Loss costs"""

    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)

        self.VERSION = "1.0.1"
        self.mincost = 0

        parser = optparse.OptionParser(prog="DupLossModel")
        parser.add_option("-D", "--dupcost", dest="dupcost",
                          metavar="<dup cost>",
                          default=1.0, type="float",
                          help="duplication cost (default: 1.0)")
        parser.add_option("-L", "--losscost", dest="losscost",
                          metavar="<loss cost>",
                          default=1.0, type="float",
                          help="loss cost (default: 1.0)")
        self.parser = parser

        CostModel._parse_args(self, extra)

    def optimize_model(self, gtree, stree, gene2species):
        """Optimizes the model"""
        CostModel.optimize_model(self, gtree, stree, gene2species)

        if self.dupcost < 0:
            self.parser.error("-D/--dupcost must be >= 0")
        if self.losscost < 0:
            self.parser.error("-L/--losscost must be >= 0")

        # ensure gtree and stree are both rooted and binary
        if not (treelib.is_rooted(gtree) and treelib.is_binary(gtree)):
            raise Exception("gene tree must be rooted and binary")
        if not (treelib.is_rooted(stree) and treelib.is_binary(stree)):
            raise Exception("species tree must be rooted and binary")
        try:
            junk = phylo.reconcile(gtree, stree, gene2species)
        except:
            raise Exception("problem mapping gene tree to species tree")

    def recon_root(self, gtree, newCopy=True, returnCost=False):
        """Reroots the tree by minimizing the duplication/loss cost"""
        return phylo.recon_root(gtree, self.stree, self.gene2species,
                                newCopy = newCopy,
                                keepName = True, returnCost = returnCost,
                                dupcost = self.dupcost, losscost = self.losscost)

    def compute_cost(self, gtree):
        """Returns the duplication-loss cost"""
        recon = phylo.reconcile(gtree, self.stree, self.gene2species)
        events = phylo.label_events(gtree, recon)
        cost = 0
        if self.dupcost != 0:
            cost += phylo.count_dup(gtree, events) * self.dupcost
        if self.losscost != 0:
            cost += phylo.count_loss(gtree, self.stree, recon) * self.losscost
        return cost
