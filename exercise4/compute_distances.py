from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


# Calculates the distance from the given signature to all the other signatures.
# Input:
#  - signature: array of features
#  - other_signatures: list of signature
def ComputeDistance(signature, other_signatures):
  distances = {}
  for other_signature in other_signatures:
    if signature[0][:3] == other_signature[0][:3]:
      distances[other_signature[0]], _ = \
        fastdtw(signature[1], other_signature[1], dist=euclidean)

  return distances


# Compute distances between the first set of signatures and the second set of signatures.
# Output:
#  - distances: matrix stored as dict of size n x m, 
#    where n = len(first_set_of_signatures) and m = len(second_set_of_signatures)
def ComputeDistances(first_set_of_signatures, second_set_of_signatures):
  distances = {}
  for first_signature in first_set_of_signatures:
    distances[first_signature[0]] = ComputeDistance(first_signature, second_set_of_signatures)
  return distances
