from dtaidistance import dtw


# Calculates the distance from the given word to all the other words.
# Input:
#  - word: Word
#  - other_words: list of Word
def ComputeDurations(word, other_words):
  distances = {}
  for other_word in other_words:
    distances[other_word.id] = \
      dtw.distance(word.features, other_word.features)


# Compute distances between the first set of words and the second set of words.
# Output:
#  - distances: matrix stored as dict of size n x m, 
#    where n = len(first_set_of_words) and m = len(second_set_of_words)
def ComputeDistances(first_set_of_words, second_set_of_words):
  distances = {}
  for first_word in first_set_of_words:
    distances[first_word.id] = ComputeDurations(first_word, second_set_of_words)
  return distances
