#
# Python module for ranger-dtl cost
#

# treefix libraries
from treefix.models import CostModel

# python libraries
import optparse
import os, sys, subprocess
import re
import tempfile

# rasmus libraries
from rasmus import treelib, util

#=============================================================================
# command

# uses ranger-dtl-U v1.0
##cmd = os.path.join(os.path.realpath(os.path.dirname(__file__)),
##                   "ranger-dtl-U.linux")
cmd = "ranger-dtl-U.linux"

patt = "The minimum reconciliation cost is: (?P<cost>\d+) \(Duplications: (?P<D>\d+), Transfers: (?P<T>\d+), Losses: (?P<L>\d+)\)"

#============================================================================

class DTLModel(CostModel):
    """Computes DTL costs"""

    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)

        self.VERSION = "0.1.0"
        self.mincost = 0

        parser = optparse.OptionParser(prog="DTLModel")
        parser.add_option("-D", "--dupcost", dest="dupcost",
                          metavar="<dup cost>",
                          default=2, type="int",
                          help="duplication cost (default: 2)")
        parser.add_option("-T", "--transfercost", dest="transfercost",
                          metavar="<transfer cost>",
                          default=3, type="int",
                          help="transfer cost (default: 3)")
        parser.add_option("-L", "--losscost", dest="losscost",
                          metavar="<loss cost>",
                          default=1, type="int",
                          help="loss cost (default: 1)")
        self.parser = parser

        CostModel._parse_args(self, extra)

        # make temporary file
        fd, self.treefile = tempfile.mkstemp()
        os.close(fd)

    def __del__(self):
        """Cleans up the model"""
        # delete temporary file
        os.remove(self.treefile)

    def recon_root(self, gtree, newCopy=True, returnCost=False):
        """
        Returns input gene tree and min DTL cost.

        Note: The optimally rooted gene tree from ranger-dtl-U
              contains species names, so this function does NOT reroot.
              It simply delegates to compute_cost.
        """
        if newCopy:
            gtree = gtree.copy()

        if returnCost:
            mincost = self.compute_cost(gtree)
            return gtree, mincost
        else:
            return gtree

    def compute_cost(self, gtree):   
        """Returns the DTL cost"""

        # write species tree and gene tree using species map
        treeout = util.open_stream(self.treefile, 'w')
        self.stree.write(treeout, oneline=True, writeData=lambda x: "")
        treeout.write("\n[&U]")
        gtree.write(treeout, namefunc=lambda name: self.gene2species(name),
                    oneline=True, writeData=lambda x: "")
        treeout.write("\n")
        treeout.close()

        # execute command
        proc = subprocess.Popen([cmd,
                                 '-i', self.treefile,
                                 '-D', str(self.dupcost),
                                 '-T', str(self.transfercost),
                                 '-L', str(self.losscost)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        ret = proc.wait()
        if ret != 0:
            raise Exception("ranger-dtl-U failed with returncode %d" % ret)
        
        # parse output
        cost = None
        for line in proc.stdout:
            m = re.match(patt, line)
            if m:
                cost = int(m.group("cost"))
                break
        assert cost is not None
        
        return cost
