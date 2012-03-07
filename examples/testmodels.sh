#============================================================================
# raxml likelihood

treefix_compute --type likelihood -m treefix.models.raxmlmodel.RAxMLModel \
    -s config/fungi.stree -S config/fungi.smap \
    -A .nt.align -U .nt.raxml.tree \
    sim-fungi/0/0.tree

#============================================================================
# dup/loss cost

treefix_compute --type cost -m treefix.models.duplossmodel.DupLossModel \
    -r -s config/fungi.stree -S config/fungi.smap \
    -o .nt.raxml.tree \
    sim-fungi/0/0.nt.raxml.tree

treefix \
    --seed 1024 \
    -s config/fungi.stree \
    -S config/fungi.smap \
    -A .nt.align \
    -o .nt.raxml.tree \
    -n .nt.raxml.treefix.tree \
    -U .tree \
    -V2 -l sim-fungi/0/0.nt.raxml.treefix.log \
    sim-fungi/0/0.nt.raxml.tree

#============================================================================
# spimap cost
# fungi: lambda = 0.000732, mu = 0.000859
# params:
#    /home/unix/yjw/projects/spimap/examples/config/sim/fungi.params
#    real (RY): /seq/compbio/rasmus/work/spimap/train/param/fungi.ry.param
#    real (nt): /seq/compbio/rasmus/work/spimap/train/param/fungi.param
#    sim: /seq/compbio/rasmus/work/spimap/train/param/fungi-sim.param (retrained on simulations)

treefix_compute --type cost -m treefix.models.spimapmodel.SpimapModel \
    -r -s config/fungi.stree -S config/fungi.smap \
    -o .nt.raxml.tree \
    -e  "-a sim-fungi/0/0.nt.align -p /seq/compbio/rasmus/work/spimap/train/param/fungi-sim.param -D 0.000732 -L 0.000859" \
    sim-fungi/0/0.nt.raxml.tree

treefix \
    --freconroot 1 \
    --seed 1024 \
    -M treefix.models.spimapmodel.SpimapModel \
    -E "-a sim-fungi/0/0.nt.align -p /seq/compbio/rasmus/work/spimap/train/param/fungi-sim.param -D 0.000732 -L 0.000859" \
    -s config/fungi.stree \
    -S config/fungi.smap \
    -A .nt.align \
    -o .nt.raxml.tree \
    -n .nt.raxml.treefix.spimap.tree \
    -U .tree \
    -V2 -l sim-fungi/0/0.nt.raxml.treefix.spimap.log \
    sim-fungi/0/0.nt.raxml.tree

#============================================================================
# deep coalescence

treefix_compute --type cost -m treefix.models.coalmodel.CoalModel \
    -r -s config/fungi.stree -S config/fungi.smap \
    -o .nt.raxml.tree \
    sim-fungi/0/0.nt.raxml.tree

treefix \
    --freconroot 1 \
    --seed 1024 \
    -M treefix.models.coalmodel.CoalModel \
    -s config/fungi.stree \
    -S config/fungi.smap \
    -A .nt.align \
    -o .nt.raxml.tree \
    -n .nt.raxml.treefix.coal.tree \
    -U .tree \
    -V2 -l sim-fungi/0/0.nt.raxml.treefix.coal.log \
    sim-fungi/0/0.nt.raxml.tree

#============================================================================
# DTL

treefix_compute --type cost -m treefix.models.dtlmodel.DTLModel \
    -r -s config/fungi.stree -S config/fungi.smap \
    -o .nt.raxml.tree \
    sim-fungi/0/0.nt.raxml.tree

treefix \
    --freconroot 1 \
    --seed 1024 \
    -M treefix.models.dtlmodel.DTLModel \
    -s config/fungi.stree \
    -S config/fungi.smap \
    -A .nt.align \
    -o .nt.raxml.tree \
    -n .nt.raxml.treefix.dtl.tree \
    -U .tree \
    -V2 -l sim-fungi/0/0.nt.raxml.treefix.dtl.log \
    sim-fungi/0/0.nt.raxml.tree

#============================================================================
# cleanup
for fn in sim-fungi/0/*.*; do
    if [ "$fn" == "sim-fungi/0/0.nt.align" ] || \
       [ "$fn" == "sim-fungi/0/0.tree" ] || [ "$fn" == "sim-fungi/0/0.nt.raxml.tree" ]; then
        :
    else
	rm $fn
    fi
done
