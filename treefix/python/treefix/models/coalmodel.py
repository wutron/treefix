#
# Python module for deep coalescence cost
#

# treefix libraries
from treefix.models import CostModel

# python libraries
import os, sys, subprocess
import re
import tempfile

# rasmus libraries
from rasmus import treelib, util

#=============================================================================
# command

##cmd = os.path.join(os.path.realpath(os.path.dirname(__file__)),
##                   'genetreereport.linux')
cmd = "genetreereport.linux"

#============================================================================

class CoalModel(CostModel):
    """Computes deep coalescence costs"""
    
    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)

        self.VERSION = "0.1.0"
        self.mincost = 0

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
        Returns the rerooted tree with min deep coalescence cost
        Generalizes compute_cost to multiple trees.
        """

        # write species tree and gene tree using species map
        treeout = util.open_stream(self.treefile, 'w')
        self.stree.write(treeout, oneline=True, writeData=lambda x: "")
        treeout.write('\n')
        edges = []
        for gtree, edge in self._reroot_helper(gtree, newCopy=newCopy, returnEdge=True):
            gtree.write(treeout, namefunc=lambda name: self.gene2species(name),
	                oneline=True, writeData=lambda x: "")
            treeout.write('\n')
            edges.append(edge)
        treeout.close()

        # execute command
        proc = subprocess.Popen([cmd,
                                 '-i', self.treefile],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        ret = proc.wait()
        if ret != 0:
            raise Exception("genetreereport failed with returncode %d" % ret)
                
        # parse output
        i = None
        n = len(edges)
        costs = [None]*n
        for line in proc.stdout:
            m = re.match("\[ gene tree #(\d+) \]", line)
            if m:
                i = int(m.groups()[0]) - 1

            if i is not None:
                m = re.match("\[ deep coalecense: (\d+) \]", line)
                if m:
                    costs[i] = int(m.groups()[0])
        assert all(map(lambda x: x is not None, costs))

        # find minimum cost tree    
        ndx, mincost = min(enumerate(costs), key=lambda it:it[1])
        minroot = edges[ndx]
        if edge != minroot:
            node1, node2 = minroot
            if node1.parent != node2:
                node1, node2 = node2, node1
            assert node1.parent == node2
            treelib.reroot(gtree, node1.name, newCopy=False, keepName=True)

        if returnCost:
            return gtree, mincost
        else:
            return gtree
 
    def compute_cost(self, gtree):   
        """Returns the deep coalescence cost"""
       
        # write species tree and gene tree using species map
        treeout = util.open_stream(self.treefile, 'w')
        self.stree.write(treeout, oneline=True, writeData=lambda x: "")
        treeout.write('\n')
        gtree.write(treeout, namefunc=lambda name: self.gene2species(name),
	            oneline=True, writeData=lambda x: "")
        treeout.write('\n')
        treeout.close()

        # execute command
        proc = subprocess.Popen([cmd,
                                 '-i', self.treefile],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        ret = proc.wait()
        if ret != 0:
            raise Exception("genetreereport failed with returncode %d" % ret)
                
        # parse output
        cost = None
        for line in proc.stdout:
            toks = line.split(':')
            if toks[0] == "deep coalecense":
                cost = int(toks[1])
                break
        assert cost is not None

        return cost
