import numpy as np
from numpy.linalg import norm

# Split list into list n-element lists.
def split_list(list, n):
    new = []
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(list), n):
        new.append(list[i:i + n])
    return new

# Get num of lines in a file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def squareDist(a,b):
    return np.power(norm(a-b,2),2)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1