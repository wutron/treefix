#
# Python module for deep coalescence cost
#

# treefix libraries
from treefix.models import CostModel

# python libraries
import os, sys, subprocess
import re

# rasmus libraries
from rasmus import treelib, util

#=============================================================================
# command

cmd = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                   'genetreereport.linux')

#============================================================================

class CoalModel(CostModel):
    """Computes deep coalescence costs"""
    
    def __init__(self):
        """Initializes the model"""
        self.mincost = 0
        self.parser = None
        
        # make temporary file
        fd, self.treefile = util.temporaryfile.mkstemp()
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
        self.stree.write(treeout, oneline=True)
        edges = []
        for gtree, edge in self._reroot_helper(gtree, newCopy=newCopy, returnEdge=True):
            gtree.write(treeout, namefunc=lambda name: self.gene2species(name), oneline=True)
            edges.append(edge)
        treeout.close()

        # execute command
        proc = subprocess.Popen([cmd,
                                 '-i', self.treefile],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
                
        # parse output
        i = None
        n = len(edges)
        costs = [None]*n
        while True:
            line = proc.stdout.readline()
            if line == '':
                break
            
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
        self.stree.write(treeout, oneline=True)
        gtree.write(treeout, namefunc=lambda name: self.gene2species(name), oneline=True)
        treeout.close()

        # execute command
        proc = subprocess.Popen([cmd,
                                 '-i', self.treefile],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
                
        # parse output
        cost = None
        while True:
            line = proc.stdout.readline()
            if line == '':
                break
            
            toks = line.split(':')
            if toks[0] == "deep coalecense":
                cost = int(toks[1])
                break
        assert cost is not None

        return cost
