# Great YT video + code: https://github.com/kamperh/lecture_dtw_notebook
import numpy as np

#If too slow, maybe try with this library: https://pypi.org/project/fastdtw/

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
    return dtw
