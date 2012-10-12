#
# Python module for dup-loss-ils cost
#

# treefix libraries
from treefix.models import CostModel

# python libraries
import optparse

# import random (and numpy.random if available)
import random
try:
    from numpy import random as nprnd
    NUMPY = True
except:
    NUMPY = False

# rasmus libraries
from rasmus import treelib
from compbio import phylo

#=============================================================================

class DLCModel(CostModel):
    """Computes Dup/Loss/Coal cost
    
    Note: This model is HIGHLY LIKELY to overfit the gene tree
    (inferring ILS over dup/loss).  It also does not correctly handle
    daughter lineages (for duplications) and therefore may violate
    bounded coalescent assumptions."""
    
    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)
        
        self.VERSION = "0.1.0"
        self.mincost = 0

        parser = optparse.OptionParser(prog="DLCModel")
        parser.add_option("-D", "--dupcost", dest="dupcost",
                          metavar="<dup cost>",
                          default=1.0, type="float",
                          help="duplication cost (default: 1.0)")
        parser.add_option("-L", "--losscost", dest="losscost",
                          metavar="<loss cost>",
                          default=1.0, type="float",
                          help="loss cost (default: 1.0)")
        parser.add_option("-C", "--coalcost", dest="coalcost",
                          metavar="<(deep) coalescence cost>",
                          default=1.0, type="float",
                          help="deep coalescence cost (default: 1.0)")
        parser.add_option("-o", "--output", dest="output",
                          metavar="<locus tree output file>",
                          help="locus tree output file")

        grp_search = optparse.OptionGroup(parser, "Search Options")
        grp_search.add_option("--niter", dest="niter",
                              metavar="<# iterations>",
                              default=1000, type="int",
                              help="number of search iterations (for locus tree) (default: 1000)")
        grp_search.add_option("--freconroot", dest="freconroot",
                              metavar="<fraction reconroot>",
                              default=0.05, type="float",
                              help="fraction of search proposals to reconroot (default: 1.0)")
        grp_search.add_option("--seed", dest="seed",
                              metavar="<seed>",
                              type="int",
                              help="seed value for random generator")
        grp_search.add_option("--rf", dest="rf",
                              metavar="<RF error threshold>",
                             default=0.5, type="float",
                             help="Robinson-Foulds error threshold between gene tree and locus tree")
        parser.add_option_group(grp_search)
    
        self.parser = parser

        CostModel._parse_args(self, extra)

        self.locustree = None

    def optimize_model(self, gtree, stree, gene2species):
        """Optimizes the model"""
        CostModel.optimize_model(self, gtree, stree, gene2species)

        # check arguments
        if self.dupcost < 0:
            self.parser.error("-D/--dupcost must be >= 0: " + str(self.dupcost))
        if self.losscost < 0:
            self.parser.error("-L/--losscost must be >= 0: " + str(self.losscost))
        if self.coalcost < 0:
            self.parser.error("-C/--coalcost must be >= 0: " + str(self.coalcost))
        #if self.output is None:
        #    self.parser.error("-o/--output must be specified")
        
        if self.niter < 1:
            self.parser.error("--niter must be >= 1: %d" % options.niter)
        if self.rf < 0 or self.rf > 1:
            self.parser.error("--rf must be in [0,1]: " + str(self.rf))

        # copy over tree topology
        ltree = treelib.Tree(nextname=gtree.nextname)
        def walk(node):
            # copy of node
            newnode = treelib.TreeNode(node.name)
            
            # recurse
            for child in node.children:
                ltree.add_child(newnode, walk(child))
                
            return newnode
        if gtree.root:
            walk(gtree.root)
            ltree.root = ltree.nodes[gtree.root.name]
        else:
            raise Exception("input gene tree must be rooted")
        self.locustree = ltree

        # search functions
        self.search = phylo.TreeSearchMix(None)
        self.search.add_proposer(phylo.TreeSearchNni(None), 0.5)
        self.search.add_proposer(phylo.TreeSearchSpr(None), 0.5)
        
    def compute_cost(self, gtree):
        """Returns the duplication-loss-coalescence cost"""
        
        # start with locus tree equal to gene tree
        ltree = self.locustree
        treelib.set_tree_topology(ltree, gtree)

        # initialize search
        self.search.set_tree(ltree)
        treehash = phylo.hash_tree(ltree)
        uniques = set([treehash])

        # initalize optimal locus tree and DLC cost
        ntrees = 0
        minltree = ltree
        mincost = self._compute_cost_helper(gtree, ltree)

        # random values
        random.seed(self.seed)
        randvec = nprnd.random(self.niter)
        if NUMPY:
            nprnd.seed(self.seed)
            randvec = [random.random() for _ in xrange(self.niter)]

        # search locus trees
        for i in xrange(self.niter):
            # propose locus tree
            ltree = self.search.propose()
            treehash = phylo.hash_tree(ltree)
            if treehash in uniques and ntrees >= 0.1*i:
                self.search.revert()
                continue
            if phylo.robinson_foulds_error(gtree, ltree) > self.rf:
                self.search.revert()
                continue

            # save tree
            if treehash not in uniques:
                uniques.add(treehash)
            ntrees += 1

            # reconroot (some percentage of the time depending on freconroot)
            if randvec[i] < self.freconroot:
                ltree, dlcost = phylo.recon_root(ltree, self.stree, self.gene2species,
                                                 newCopy=True,
                                                 keepName=True, returnCost=True,
                                                 dupcost=self.dupcost, losscost=self.losscost)
                coalcost = self._compute_coalcost(gtree, ltree)
                cost = dlcost + coalcost
            else:
                cost = self._compute_cost_helper(gtree, ltree)
            
            # update min cost and decide how to continue proposals from here
            if cost < mincost:
                minltree = ltree if randvec[i] < self.freconroot else ltree.copy()
                mincost = cost
            else:
                self.search.revert()

        # set optimal locus tree
        self.locustree = minltree
        self.locustree.write(self.output)

        return mincost

    def _compute_cost_helper(self, gtree, ltree):
        """Helper function to compute DLC cost from coalescent tree (gene tree) -> locus tree -> species tree"""
        return self._compute_coalcost(gtree, ltree) + self._compute_duplosscost(ltree)
    
    def _compute_coalcost(self, gtree, ltree):
        """Returns deep coalescent cost from coalescent tree (gene tree) to locus tree

        Note: uses Zhang (RECOMB 2000) result that C = L - 2*D
        """
        cost = 0
        if self.coalcost > 0:
            recon = phylo.reconcile(gtree, ltree)
            events = phylo.label_events(gtree, recon)
            cost = (phylo.count_loss(gtree, ltree, recon) - 2*phylo.count_dup(gtree, events)) * self.coalcost
        return cost

    def _compute_duplosscost(self, ltree):
        """Returns dup/loss cost from locus tree to species tree"""
        cost = 0
        if self.dupcost > 0 or self.losscost > 0:
            recon = phylo.reconcile(ltree, self.stree, self.gene2species)
            events = phylo.label_events(ltree, recon)
            if self.dupcost != 0:
                cost += phylo.count_dup(ltree, events) * self.dupcost
            if self.losscost != 0:
                cost += phylo.count_loss(ltree, self.stree, recon) * self.losscost
        return cost
