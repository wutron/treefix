#
# Python module for SPIMAP cost
# Requires SPIMAP libraries (http://compbio.mit.edu/spimap)
#

# treefix libraries
from treefix.models import CostModel

# spidir libraries
import spidir

# python libraries
import optparse

# rasmus libraries
from rasmus import treelib, util
from compbio import phylo, fasta, alignlib

#=============================================================================

class SpimapModel(CostModel):
    """Computes SPIMAP costs"""
   
    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)

        self.VERSION = "0.1.0"
        self.mincost = -util.INF
       
        parser = optparse.OptionParser(prog="SpimapModel")
        parser.add_option("-a", "--align", dest="align",
                          metavar="<alignment fasta>",
                          help="sequence alignment in fasta format")
        parser.add_option("-p", "--param", dest="params",
                          metavar="<params file>",
                          help="substitution rate parameters file")
        parser.add_option("--simplereroot", dest="simplereroot",
                          metavar="<simple reroot>",
                          default=False, action="store_true",
                          help="set to reroot using dup/loss cost")

        grp_seq = optparse.OptionGroup(parser, "Sequence evolution model")
        grp_seq.add_option("-k", "--kappa", dest="kappa",
                           metavar="<transition/transversion estimate>",
                           default=-1.0, type="float",
                           help="used for HKY model (default: estimate)")
        grp_seq.add_option("-f", "--bgfreq", dest="bgfreq",
                           metavar="<A freq>,<C freq>,<G freq>,<T freq>",
                           help="background frequencies (default: estimate)")
        parser.add_option_group(grp_seq)

        grp_duploss = optparse.OptionGroup(parser, "Dup/loss evolution model")
        grp_duploss.add_option("-D", "--duprate", dest="duprate",
                               metavar="<duplication rate>",
                               default=0.1, type="float",
                               help="rate of gene duplication (default: 0.1)")
        grp_duploss.add_option("-L", "--lossrate", dest="lossrate",
                               metavar="<loss rate>",
                               default=0.1, type="float",
                               help="rate of gene loss (default: 0.1)")
        grp_duploss.add_option("-P", "--pretime", dest="pretime",
                               metavar="<pre-speciation time parameter>",
                               default=1.0, type="float",
                               help="lambda param of pre-speciation distribution (default: 1.0)")
        parser.add_option_group(grp_duploss)
                
        self.parser = parser

        CostModel._parse_args(self, extra)
    
    def optimize_model(self, gtree, stree, gene2species):
        """Optimizes the model"""
        CostModel.optimize_model(self, gtree, stree, gene2species)
        
        #=============================
        # read sequences
        if not self.align:
            self.parser.error("--align must be specified")
        self.align = fasta.read_fasta(self.align)

        #=============================
        # read SPIDIR parameters
        if not self.params:
            self.parser.error("--param must be specified")
        self.params = spidir.read_params(self.params)

        #=============================
        # determine background base frequency
        if self.bgfreq:
            # use supplied frequency
            vals = map(float, self.bgfreq.split(","))
            if len(vals) != 4:
                self.parser.error("invalid --bgfreq: %s" % self.bgfreq)
            self.bgfreq = vals
        else:
            # compute frequency from alignment
            self.bgfreq = alignlib.compute_bgfreq(self.align)

        #=============================
        # branch lengths
        if self.kappa >= 0:
            # use supplied kappa
            self.kappa = self.kappa
        else:
            # compute kappa from alignment
            # from spidir.find_ml_kapp_hky
            minkappa = 0.4; maxkappa = 5.0; stepkappa = 0.1
            maxlk = -util.INF
            maxk = minkappa

            for k in util.frange(minkappa, maxkappa, stepkappa):
                l = spidir.find_ml_branch_lengths_hky(gtree, self.align, self.bgfreq, k, maxiter=1,
                                                      parsinit=True if k == minkappa else False)
                if l > maxlk:
                    maxlk = l
                    maxk = k

            self.kappa = maxk
            
    def recon_root(self, gtree, newCopy=True, returnCost=False):
        """
        Reroots the tree by minimizing the duplication/loss cost
        Note, may NOT minimize the cost function
        """
        if self.simplereroot:
            tree = phylo.recon_root(gtree, self.stree, self.gene2species,
                                    newCopy = newCopy,
                                    keepName = True, returnCost = False)
            if returnCost:
                return tree, self.compute_cost(tree)
            else:
                return tree
        else:
            return CostModel.recon_root(self, gtree, newCopy, returnCost)

    def compute_cost(self, gtree):
        """
        Returns -log [P(topology) + P(branch)],
        min cost = min neg log prob = max log prob = max prob
        """
        recon = phylo.reconcile(gtree, self.stree, self.gene2species)
        events = phylo.label_events(gtree, recon)

        # optimize branch lengths
        spidir.find_ml_branch_lengths_hky(gtree, self.align, self.bgfreq, self.kappa,
                                          maxiter=10, parsinit=False)

        branchp = spidir.branch_prior(gtree, self.stree, recon, events,
                                      self.params, self.duprate, self.lossrate, self.pretime)
        topp = spidir.calc_birth_death_prior(gtree, self.stree, recon,
                                             self.duprate, self.lossrate, events)
        return -(topp + branchp)
