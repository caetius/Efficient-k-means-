import Vector
import os
import credentials

dirname = os.path.dirname(__file__)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

'''
Check arguments
cluster.py
 -i : Input file containing n*(j+1) rows of length d representing n j-subspaces in R^d.
 -o : Output file to store k clusters.
 -j : Dimensionality of subspaces in the input.
 -k : Number of clusters to solve for.
'''
def checkInputs(myargs):
    if len(myargs) != 6:
        raise ValueError(
            'Wrong number of inputs: \nUsage: python Algorithm.py -i input_filename -o output_filename -j j -k k -alpha alpha -beta -beta')

    if '-j' in myargs:
        j = int(myargs['-j'])
    else:
        raise ValueError('Dimensionality of the subspaces not defined.')

    if '-i' in myargs:
        input_name = os.path.join(dirname, myargs['-i'])
        # Define dimension of input space
        d = len(Vector.readVector(input_name, 0).tolist())

        num_lines = file_len(input_name)  # Check dimensions of input file data
        if num_lines % (j + 1) != 0:
            raise ValueError('Dimensions of input matrix inconsistent with value j')

        n = int(num_lines / (j + 1))  # Safe operation

    else:
        raise ValueError('Input file not found or not specified')

    if '-o' in myargs:
        output_name = os.path.join(dirname, myargs['-o'])
    else:
        raise ValueError('No output file specified')

    if '-k' in myargs:
        k = int(myargs['-k'])
    else:
        raise ValueError('Number of clusters not specified')

    if '-alpha' in myargs:
        alpha = int(myargs['-alpha'])
    else:
        raise ValueError('Cell sampling coefficient alpha not set.')

    if '-beta' in myargs:
        beta = int(myargs['-beta'])
    else:
        raise ValueError('Point sampling coefficient beta not set.')
    '''
    Check k,j are positive
    '''
    if (k <= 0 or j < 0 or d <= 0):
        raise ValueError('d > 0, k > 0, and j >= 0 required')


    '''
    Remove Trace from Prev. Runs
    '''
    try:
        os.remove(credentials.hd_normals)
        print("Removed 1/4 Old Files")
    except:
        print("Removed 1/4 Old Files (Absent)")
    try:
        os.remove(credentials.candidates)
        print("Removed 2/4 Old Files")
    except:
        print("Removed 2/4 Old Files (Absent)")
    try:
        os.remove(credentials.preprocessed)
        print("Removed 3/4 Old Files")
    except:
        print("Removed 3/4 Old Files (Absent)")
    try:
        os.remove(credentials.clusters)
        print("Removed 4/4 Old Files")
    except:
        print("Removed 4/4 Old Files (Absent)")

    return j,k,d,n, alpha, beta, input_name,output_name