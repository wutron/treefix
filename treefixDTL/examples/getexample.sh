path=~/work/treefixDTL

# get example from treefixDTL project (sim)
mkdir config
cp -L $path/config/strees/S1.stree config
cp -L $path/config/S.smap config

mkdir -p sim/G1
cp -L $path/data/sim/Seqlength173/lowDTL/height1/G1/G1{.tree,.pep.align,.pep.raxml.tree} sim/G1/
