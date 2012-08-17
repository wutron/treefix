# using RAxML-7.0.4 (modified source files)
cp ~/src/RAxML-7.0.4/*.h src/
cp ~/src/RAxML-7.0.4/*.c src/

#=============================================================================
# build C and swig interface separately (does not work)

cd src
make -f Makefile.gcc
cd ..

mkdir -p lib
gcc -o lib/raxml.so -shared src/*.o `gsl-config --libs`

#=============================================================================
# build swig library by itself
# (not necessary since now included in setup.py script)

cd python/treefix_raxml
swig -python raxml.i
cd ../../

#=============================================================================
# build source (developmental build)

python setup.py build_ext --inplace

export PYTHONPATH=$PYTHONPATH:~/projects/treefix_raxml/python

#=============================================================================
# build source

python setup.py build
python setup.py install #--prefix=<prefix>

#=============================================================================
# cleanup

rm python/treefix_raxml/raxml_wrap.c
rm python/treefix_raxml/raxml.py
rm python/treefix_raxml/*.pyc
rm python/treefix_raxml/_raxml.so
rm -r build

#=============================================================================
# test

./examples/test_swig.py \
    -T .nt.raxml.tree \
    -A .nt.align.phylip \
    examples/sim-fungi/0/0.nt.raxml.tree
./examples/test_mod.py \
    -T .nt.raxml.tree \
    -A .nt.align.phylip \
    examples/sim-fungi/0/0.nt.raxml.tree

raxmlHPC -f h \
    -t examples/sim-fungi/0/0.nt.raxml.tree \
    -z ~/projects/raxml/tops.tree \
    -s examples/sim-fungi/0/0.nt.align.phylip \
    -m GTRGAMMA -e 2.0 -n sh -#1
