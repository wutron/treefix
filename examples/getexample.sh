path=~/work/treefix

# get example from treefix project (sim-fungi)
mkdir config
cp -L $path/config/fungi{.stree,.smap} config/

mkdir -p sim-fungi/0
cp -L $path/data/sim-fungi/1-1/0/0{.tree,.nt.align,.nt.align,.nt.raxml.tree} sim-fungi/0/
