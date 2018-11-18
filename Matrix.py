import numpy as np
from scipy.linalg import null_space # null_space default: floating point eps * max(M,N).
from scipy.sparse.linalg import eigs
from Utils import split_list

'''I/O'''
# Read matrix from filename between rows f_ind (inclusive) and l_ind (exclusive).
def readMatrix(filename,f_ind,l_ind):
    mat = []
    with open(filename) as fp:
        for i, line in enumerate(fp):
            if i >= f_ind and i < l_ind:
                new_vec = line.rstrip().split(',')
                new_vec = list(map(float, new_vec))
                mat.append(new_vec)
            elif i >= l_ind:
                break
        fp.close()
    return np.array(mat, dtype="float64") # Numpy 2D array

# Write (append mode) matrix to filename.
def writeMatrix(filename, mat):
    mat = mat.tolist()
    thefile = open(filename, 'a')
    for item in mat:
        my_str = ','.join(map(str, item))
        thefile.write("%s\n" % my_str)
    thefile.close()

'''Preprocessing'''
# Preprocess a matrix by computing the subspace complement, then appending the vector z
def preprocess(mat):
    rows = mat.shape[0]
    subspace = mat[:rows - 1,] # Subspace is rows 1 to j
    #print("Subspace: ", subspace)
    displacement = mat[rows - 1,] # Displacement is row j+1
    #print("Displacement: ", displacement)
    complement = np.transpose(null_space(subspace))  # Find complement of subspace, returns orthogonalised columns
    #print("Complement: ", complement)
    offset = np.dot(complement, displacement)  # ans is (d-j) x 1
    disp_comp = split_list(offset, 1)
    f_subspace = np.concatenate([complement, disp_comp], axis=1)  # Append displacement onto normalised subspace complement as extra column
    #print("Final subspace: ", f_subspace)
    return f_subspace


'''Extra: Depreciated'''
# Get closest matrix in form xx^T with x[len(x)]=-1
def getClosestSymMatrix(M):
    val, vec = eigs(M, k=1)
    vec = np.real(vec)
    val = np.real(val)
    new_M = np.outer(np.multiply(vec,val), vec)
    m = 1/new_M[-1,-1]
    new_M = np.multiply(new_M, m)
    #print("new matrix: ", new_M)
    return new_M
