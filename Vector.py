import numpy as np
import credentials
import time

'''I/O'''
def readVector(filename, index):
    vec = []
    with open(filename) as fp:
        for count, line in enumerate(fp):
            if count == index:
                vec = line.rstrip().split(',')
                vec = list(map(np.float64, vec))
                break
        fp.close()
    return np.array(vec)

def writeVector(filename, vec):
    thefile = open(filename, 'a')
    my_str = ','.join(map(str, vec.tolist()))
    thefile.write("%s\n" % my_str)
    thefile.close()

'''Check if one point is in a cell given by normals with the signs specified.'''
def isInsideCell(point, sign_vec):
    is_inside = True

    for i in range(len(sign_vec)):
        next = readVector(credentials.hd_normals, i)
        next = sign_vec[i] * next
        res = np.dot(next, point)
        if res <= 0:
            is_inside = False
    return is_inside

def generateNPoints(beta,d):
    t = time.time()
    v = np.random.uniform(-2,2,size=(d, beta))
    v = v / np.sqrt(np.sum(v ** 2, 0))
    elapsed = time.time() - t
    print(">",beta," points generated in ", elapsed)
    return np.transpose(v)