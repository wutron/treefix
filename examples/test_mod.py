#!/usr/bin/env python

# python libraries
import os,sys
import optparse

# raxml library
import raxml

# rasmus libraries
from rasmus import treelib, util
from rasmus.bio import phylo

#=============================
# parser

usage = "usage: %prog [options] <gene tree>"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-T", "--treeext", dest="treeext",
                  metavar="<tree file extension>",
                  default=".tree",
                  help="tree file extension (default: \".tree\")")
parser.add_option("-A", "--alignext", dest="alignext",
                  metavar="<alignment file extension>",
                  default=".align",
                  help="alignment file extension (default: \".align\")")
parser.add_option("--niter", dest="niter",
                  metavar="<# iterations>",
                  default=5, type="int",
                  help="number of iterations (default: 5)")
parser.add_option("-e", "--extra", dest="extra",
                  metavar="<extra arguments to initialize RAxML>",
                  default="-m PROTGAMMAJTT -n test -e 2.0",
                  help="extra arguments to pass to program")
parser.add_option("-p", "--pval", dest="pval",
                  metavar="<p-value>",
                  default=0.05, type="float",
                  help="p-value threshold (default: 0.05)")
parser.add_option("-o", "--output", dest="output",
                  metavar="<output file>",
                  default="-")

options, args = parser.parse_args()

#=============================
# check arguments

if options.niter < 1:
    parser.error("--niter must be >= 1: %d" % options.niter)

if len(args) != 1:
    parser.error("must specify input file")
    
#=============================
# main file

treefile = args[0]
seqfile = util.replace_ext(treefile, options.treeext, options.alignext)
out = util.open_stream(options.output, 'w')

util.tic("Initializing RAXML and optimizing...")
raxml.init()
raxml.optimize_model(treefile, seqfile, options.extra)
util.toc()

tree = treelib.read_tree(treefile)
for node in tree: node.dist = 0
treehash = phylo.hash_tree(treelib.unroot(tree, newCopy=True))
treehashes = set([treehash])

for i in xrange(options.niter):
    while treehash in treehashes:
        util.log("random spr")
        node1, node2 = phylo.propose_random_spr(tree)
        phylo.perform_spr(tree, node1, node2)
        treehash = phylo.hash_tree(treelib.unroot(tree, newCopy=True))

    treehashes.add(treehash)
    tree.write(out, oneline=True); out.write('\n'); out.flush()

    util.tic("Computing LH...")
    p, Dlnl = raxml.compute_lik_test(tree)
    util.log("pvalue: %.3f, Dlnl: %.3f" % (p, Dlnl))
    util.toc()

    if Dlnl <= 0:
        util.log("worse likelihood?: %s" % False)  # better topology (higher likelihood)
    else:
        util.log("worse likelihood?: %s" % True)   # worse topology (higher likelihood)
        
        if p < options.pval:
            util.log("significant?: %s" % True)    # statistically significant (significantly worse likelihood)
        else:
            util.log("significant?: %s" % False)   # statistically insignificant (equivalent likelihood)

    util.log('\n')

# cleanup
out.close()
raxml.cleanup()
