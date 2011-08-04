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
# build source (developmental build)

cd python/raxml
swig -python raxml.i
cd ../../

python setup.py build_ext --inplace
mv _raxml.so python/

export PYTHONPATH=$PYTHONPATH:~/projects/raxml/python

#=============================================================================
# build source

cd python/raxml
swig -python raxml.i
cd ../../

python setup.py build
python setup.py install #--prefix=~/projects/raxml/sw

#=============================================================================
# cleanup

rm python/raxml/raxml_wrap.c
rm python/raxml/raxml.py
rm python/raxml/*.pyc
rm python/_raxml.so
rm -r build

#=============================================================================
# test

./examples/test_swig.py
./examples/test_mod.py

raxmlHPC -f h \
    -t ~/work/modencode-orth/0/0.pep.raxml.tree \
    -z ~/projects/raxml/tops.tree \
    -s ~/work/modencode-orth/0/0.pep.align.phylip \
    -m PROTGAMMAJTT -e 2.0 -n sh -#1
