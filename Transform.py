import numpy as np
from itertools import combinations
from math import acos, sqrt, pow, pi, cos, sin
import Matrix


'''Projections along dimensions: (d+1)->(d+1)^2 and back'''
# Project subspace into high dimensional vector. Input: 2D NP array. Output: 1D NP Array.
def pComp(A):
    interim = np.matmul(A.transpose(),A)    # Matrix product (yields (d+1)x(d+1) when A is (d-j)x(d+1))
    return np.reshape(interim,-1)           # Reshape as vector

def qDecomp(q, d):
    xxT = Matrix.getClosestSymMatrix(np.reshape(q, (d, d)))
    x = -xxT[d - 1]                         # Take negative of bottom row
    return x

def qComp(x):
    interim = np.outer(x,x)  # Matrix product (yields (d+1)x(d+1) when A is (d-j)x(d+1))
    return np.reshape(interim, -1)

'''Cartesian -> Spherical '''

# Given is that r=1. (Unit n-sphere)
def cartesianToSpherical(x):
    d = len(x)
    phi = np.zeros((d-1))
    d_ = len(phi)

    sum_squares = pow(x[d_],2) + pow(x[d_-1],2)
    last_angle = acos(x[d_-1]/(sqrt(sum_squares)))
    if x[d_] >= 0:
        phi[d_-1] = last_angle
    else:
        phi[d_-1] = 2*pi-last_angle

    for k in range(d_-2,-1,-1):
        sum_squares = sum_squares + pow(x[k],2)
        phi[k] = acos(x[k]/sqrt(sum_squares))

    return phi


'''Spherical -> Cartesian '''

# Given is that r=1. (Unit n-sphere)
def sphericalToCartesian(phi):
    dim = len(phi)
    x = np.zeros(dim+1)
    sins = 1
    for i in range(0,dim):
        x[i] = sins*cos(phi[i])
        sins *= sin(phi[i])
    x[dim] = sins
    return x

'''Alternative Code: Appendix method'''


'''P-Q: Appendix Version'''
# Project subspace into high dimensional vector. Input: 2D NP array. Output: 1D NP Array.
# Version as shown in Appendix 1.
def pCompAlt(A,j):
    d = len(A[0,:])
    p = np.array([])

    p_1 = np.reshape(np.multiply(A, A), (1, A.shape[0] * A.shape[1]))
    p = np.append(p, p_1)

    index = range(d + 1)
    comb = list(combinations(index, 2))
    for i in range(d - j):
        p_2 = 2 * np.multiply(A[i, [x[0] for x in comb]], A[i, [x[1] for x in comb]])
        p = np.append(p, p_2)

    return p

# Decomposition as shown in Appendix 1.
def qDecompAlt(q, d, j):
    x_ = np.sqrt(np.abs(q[0:d]))  # Elementwise square root
    signs = q[d * (d - j):d * (d - j) + d - 1]
    x = np.zeros(d)
    x[0] = np.absolute(x_[0])  # Assume first entry is positive.
    for i in range(1, len(x_)):
        if (signs[i - 1] < 0):
            x[i] = -np.absolute(x_[i])
        else:
            x[i] = np.absolute(x_[i])

    return x  # First candidate solution center in input dim (second is negative of this vec)
