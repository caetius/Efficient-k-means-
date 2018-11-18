import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import time

cutoff = 10 # For the summary to indicate the relative sizes of cells.

def getSignVectors(normals, sample, k, alpha, plot):
    t = time.time()
    prod = (normals).dot(np.transpose(sample))
    signs = prod > 0
    elapsed = time.time() - t
    print(">", len(signs), " Signs computed in ", elapsed)
    idx = getSummary(signs, k, plot, alpha)
    return idx

def getSummary(signs, k, plot, alpha):
    t = time.time()
    combos = []     # Summarized rows
    weights = []       # Weight vector
    indexes = []
    for i in range(len(signs[0])):
        found = False
        # Check vector is not in list of found vectors
        for x in range(len(combos)):
            if (combos[x] == signs[:,i]).all():
                found = True
        # If it is not found, we count
        if not found:
            count = 0
            for j in range(len(signs[0])):
                if (signs[:,j] == signs[:,i]).all():
                    count = count + 1
            weights.append(count)
            indexes.append(i)
            combos.append(signs[:,i])

    elapsed = time.time() - t
    print("> Cells summarized in ", elapsed)

    order = np.argsort(weights)[::-1][:alpha*k]
    top = signs[:,order[0]]

    # Uncomment to get all the points in the largest cell.
    '''
    top_indexes = []
    for j in range(len(signs[0])):
        if (signs[:, j] == top).all():
            top_indexes.append(j)
    '''
    indexes = [indexes[i] for i in order]
    # Plot
    if plot:
        weights.sort(reverse=True)
        plot_res(weights)
    return indexes    # Return top k sign vectors

# Plot results
def plot_res(reps):
    N = len(reps)
    cuts = sum(i > cutoff for i in reps)
    print(">Total Cells with over ", cutoff, " occurrences: ", cuts)
    x = range(1, N + 1)
    plt.bar(x, reps, align='center', alpha=0.5)
    plt.ylabel('Occurrences')
    plt.title('Frequency of sphere points in each cell')
    plt.show()
