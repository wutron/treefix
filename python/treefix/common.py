import sys
from rasmus import treelib, util

#=============================
# input

def add_common_options(parser,
                       infiles=False ,reroot=False,
                       stree=False, smap=False,
		       treeext=False, alignext=False,
		       clade=False):
    if infiles:
        parser.add_option("-i", "--input", dest="input",
                          action="append",
                          metavar="<input file>",
			  help="list of input files, one per line")
    if reroot:
        parser.add_option("-r", "--reroot", dest="reroot",
                          action="store_true", default=False,
                          metavar="<reroot tree>",
			  help="whether to reroot the input tree")
    if stree:
       parser.add_option("-s", "--stree", dest="stree",
                         metavar="<species tree>",
			 help="species tree file in newick format")
    if smap:
       parser.add_option("-S", "--smap", dest="smap",
                         metavar="<species map>",
                         help="gene to species map")
    if treeext:
	parser.add_option("-T","--treeext", dest="treeext",
                          metavar="<tree file extension>",
                          default=".tree",
	                  help="tree file extension (default: \".tree\")")
    if alignext:
        parser.add_option("-A","--alignext", dest="alignext",
			  metavar="<alignment file extension>",
			  default=".align",
			  help="alignment file extension (default: \".align\")")
    if clade:
            parser.add_option("-c", "--clade", dest="clade",
	                      metavar="<clade file>",
			      help="clade file")

def move_option(parser, opt_str, opt_grp):
    """Move option 'opt_str' from 'parser' to 'opt_grp'"""
    if parser.has_option(opt_str):
        opt = parser.get_option(opt_str)
        parser.remove_option(opt_str)
        opt_grp.add_option(opt)

def check_req_options(parser, options,
                      species=True, clade=True):
    if species and ((not options.stree) or (not options.smap)):
        parser.error("--stree and --smap are required")
    if clade and (not options.clade):
        parser.error("--clade is required")

def get_input_files(parser, options, args):
    # determine input files from options
    infiles = []
    if options.input:
        for arg in options.input:
            if arg == "-":
                infiles.append(sys.stdin)
            else:
                infiles.append(open(arg))

    # determine all input lines
    files = args
    for infile in infiles:
        files.extend(map(lambda fn:fn.rstrip("\n"),infile.readlines()))
    if len(files) == 0:
        parser.error("must specify input file(s)")
        
    return files

#=============================
# clades

def get_clade(names, stree):
    nodes = [stree.nodes[name] for name in names]
    head = treelib.lca(nodes)
    clade = [head] + head.descendants()
    return clade

def read_clades(cladefile, stree):
    clades = {}
    for line in util.open_stream(cladefile):
        toks = line.rstrip().split()
	name = toks[0]
	sps = toks[1].split(',')
	assert all(sp in stree.nodes for sp in sps)
        clade = get_clade(sps, stree)
        clades[name] = clade
    return clades

