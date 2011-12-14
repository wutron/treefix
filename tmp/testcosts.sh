#==========================================================
# cost functions from Mukul

# Both programs takes as input a single input file containing first the species tree and then one or more gene trees, on separate lines and in newick format. All trees must be rooted. The leaf labels of the gene tree must be the same as the leaf labels used on the species tree. The trees may or may not have branch lengths (any branch length information will be ignored). An example input file is attached.

# deep coalescence cost
# Uses EITHER dup/loss model or deep coalescence model.
# The -t g specifies that the program should output the costs for the individual input gene trees (not the sum of all costs).
genetreereport.linux -t g -i inputfile

# duplication-transfer-loss cost
# Here -D, -T and -L are used to specify the costs of duplication, transfer and loss. These costs must be whole numbers.
DTL.linux -i inputfile -D 2 -T 3 -L 1
