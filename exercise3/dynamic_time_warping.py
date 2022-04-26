# Great YT video + code: https://github.com/kamperh/lecture_dtw_notebook
import numpy as np

#If too slow, maybe try with this library: https://pypi.org/project/fastdtw/

#To get the path from cost matrix: https://towardsdatascience.com/an-intuitive-approach-to-dtw-dynamic-time-warping-f660ccb77ff4
def trace_path(cost_matrix, i, j):
    path = [(i, j)]
    while ((i>0) | (j>0)):
        path_min = np.argmin([cost_matrix[i-1, j-1], cost_matrix[i-1, j], cost_matrix[i, j-1]])   
        if path_min==0:
            i=i-1
            j=j-1
        elif path_min==1:
            i=i-1
        else:
            j=j-1
        path.append((i, j)) 
    return path[::-1] ## return after reversing the list

#Dynamic time warping: Align two sequences, along a common time axis with Euclidean cost
#Sakoe-Chiba Band: Reduce the number of paths to consider in DTW by adding a window constraint
#https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd
def dtwWindow(vector1, vector2, window):
    n, m = len(vector1), len(vector2)
    dtw = np.array(np.ones((n+1, m+1)) * np.inf)
    dtw[0][0] = 0 

    #Adapt window size if necessary 
    window = np.max([window, np.abs(n-m)])

    for i in range(1, n+1):
        for j in range(np.max([1, i-window]), np.min([m, i+window])+1):
            dtw[i][j] = 0
            
    for i in range(1, n+1):
        for j in range(np.max([1, i-window]), np.min([m, i+window])+1):
            cost = abs(vector1[i-1]-vector2[j-1])
            dtw[i, j] = cost + np.min([dtw[i-1, j], dtw[i, j-1], dtw[i-1, j-1]])
    finalCost = dtw[n][m]
    path = trace_path(dtw, n, m)
    return dtw, finalCost, path #Return the matrix cost, the final cost and the best path to take
