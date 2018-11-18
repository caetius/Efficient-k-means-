#Standard Lib
import os
from sys import argv

# Non-Standard
from itertools import combinations
from itertools import product
import numpy as np

#Local
from CheckInputs import checkInputs, getopts
import Matrix
import Vector
import credentials
import Transform
import Sampler


'''
Parse Args
'''
myargs = getopts(argv)                                                      # Parse inputs
j,k,d,n, alpha, beta, input_file,output_file = checkInputs(myargs)                        # Raise any input issues
dir_path = os.path.dirname(os.path.realpath(__file__))



'''
PREPROCESSING: 
One by one read the subspaces (including displacement), take orthogonal compliment, append offset vector and store this in preprocessed file.
'''
for index in range(n):
    if j > 0:
        mat = Matrix.readMatrix(input_file, index*(j+1),index*(j+1)+(j+1)) # Read python matrix from file. Matrix is (j+1)*n x d dimensional.
        mat = Matrix.preprocess(mat)
        Matrix.writeMatrix(credentials.preprocessed, mat)                  # Save complement of subspace to file
print("Stage 1/4-- Preprocessing Completed: ", n, " input subspaces found.\n")

'''
TAKE TO PROJECTIVE SPACE: 
Generate the combinations of all pairs of n subspaces. 
For every pair of subspaces as defined by 'comb', compute HD normal (affine) and store in file HD_normals.
'''
comb = list(combinations(range(n), 2))    #Get all 2-element combinations of the subspaces (over indexes [0,n-1])
hd_dim = (d+1)**2
hp_size = d-j
rho_normals = np.zeros((len(comb),hd_dim));
for col in range(len(comb)):
    i_1 = comb[col][0]
    i_2 = comb[col][1]
    hyp_1 = Matrix.readMatrix(credentials.preprocessed,i_1*hp_size,i_1*hp_size+hp_size)
    hyp_2 = Matrix.readMatrix(credentials.preprocessed,i_2*hp_size,i_2*hp_size+hp_size)
    p_1 = Transform.pComp(hyp_1)                                            # Transform A_i and A_j to p_i-p_j
    p_2 = Transform.pComp(hyp_2)
    rho = p_1 - p_2
    rho = rho / np.linalg.norm(rho,2)                                       # Normalise so rho is a point on the n-sphere.
    rho_normals[col] = rho
    Vector.writeVector(credentials.hd_normals, rho)                         # Save high dim normal (normalised).
print("Stage 2/4-- High-Dim Normals Computed. Total (nC2)=", len(comb), ", Projective Dim= ", hd_dim)


'''
Generate a sample of points on the hypersphere in d+1 and project to high dimensional space. 
Use these points to find the largest cells in the high dimensional arrangement and return the best points.
'''
num_smart_samples = beta*hd_dim
points = Vector.generateNPoints(num_smart_samples,d+1)     # Generate points in the input space
Matrix.writeMatrix(credentials.temp, points)
hd_points = np.zeros((points.shape[0], hd_dim))
for i in range(points.shape[0]):
    hd_points[i,:] = Transform.qComp(points[i,:])
best_idx = Sampler.getSignVectors(rho_normals, hd_points, k, alpha, credentials.plot)
best_points = points[best_idx,:]
Matrix.writeMatrix(credentials.candidates, best_points)
print("Stage 3/4-- ", num_smart_samples, "Samples taken / sign vectors generated.")


'''
For every input, measure the distance to the k candidates and assign the closest point as cluster. 
'''
comb = list(combinations(range(len(best_idx)), k))
min_score = 100000
best_comb = []
iii = 0
for col in range(len(comb)):
    scores = np.zeros((n, k))
    selected_comb = best_points[comb[col],:]
    for i in range(n):
        h = Matrix.readMatrix(credentials.preprocessed, i * hp_size, i * hp_size + hp_size)
        count = 0
        for row in selected_comb:
            scores[i,count] = np.sum(np.abs(np.dot(h,row)))**2
            count = count + 1
    clusters = np.argmin(scores, axis=1)
    total_score = np.sum(np.min(scores,axis=1))
    if total_score < min_score:
        min_score = total_score
        best_comb = clusters
    #print(clusters)
    #print(total_score)
    iii += 1
Vector.writeVector(credentials.clusters, best_comb)
print()
print(best_comb)
print("Stage 4/4-- ", k, "clusters computed with error score=", min_score)
