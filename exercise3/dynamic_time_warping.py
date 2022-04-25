# Great YT video + code: https://github.com/kamperh/lecture_dtw_notebook
import numpy as np

# TODO: Sakoe-Chiba Band: Reduce the number of paths to consider

#Dissimilarity between two feature vector sequences
#Dynamic time warping aligns two sequences, along a common time axis usually with Euclidean cost
#https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd
def dtw(vector1, vector2):
    n, m = len(vector1), len(vector2)
    dtw = np.array(np.ones((n+1, m+1)) * np.inf)
    dtw[0][0] = 0  
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(vector1[i-1]-vector2[j-1])
            dtw[i, j] = cost + np.min([dtw[i-1, j], dtw[i, j-1], dtw[i-1, j-1]])
    print(dtw)
    return dtw

#To test
v1 = [1, 2, 3]
v2 = [2, 2, 2, 3, 4]
dtw(v1, v2)