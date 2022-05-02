import csv
import os
from dtaidistance import dtw
from feature_extraction import Method
import exercise3_config as config
from readers import GetProcessedInputData


# Calculates the distance from the given word to all the other words.
# Input:
#  - word: Word
#  - other_words: list of Word
def ComputeDistance(word, other_words, debug=False):
  distances = {}
  for other_word in other_words:
    if debug:
      print(f'Compute distances for test word {other_word.id}')
    distances[other_word.id] = \
      dtw.distance(word.features, other_word.features)
  return distances


# Compute distances between the first set of words and the second set of words.
# Output:
#  - distances: matrix stored as dict of size n x m, 
#    where n = len(first_set_of_words) and m = len(second_set_of_words)
def ComputeDistances(first_set_of_words, second_set_of_words, debug=False):
  distances = {}
  for first_word in first_set_of_words:
    if debug:
      print(f'Compute distances for train word {first_word.id}')
    distances[first_word.id] = ComputeDistance(first_word, second_set_of_words, debug)
  return distances


# Input:
#  - filepath: string
#  - distances: dictionary. distances[x] = y, where x is a word id and y a float number
def __WriteToFile(filepath, distances):
  with open(filepath, 'w') as f:
    csv_writer = csv.writer(f, delimiter=',')
    for entry in distances.items():
      csv_writer.writerow([entry[0], entry[1]])



# We'll store distances in an output dir using csv files as follows
# {output_dir_name}/{feature}/{page_number}/{word_id}.csv = output/BLACK_PIXEL_RATIO/270/270-01-01.csv
if __name__ == "__main__":
  try:
    os.mkdir(os.path.join(config.OUTPUT_DIR))
  except OSError as error: 
    # Directory already exists
    pass

  # Single method only!
  feature_extraction_methods = [Method.BLACK_PIXEL_RATIO]
  transcriptions_as_list, keywords_to_search, train_words, test_words = GetProcessedInputData(feature_extraction_methods)

  for train_word in train_words:
    print('====================================================================================================')
    print(f'Train word id: {train_word.id}')
    train_page_id = train_word.id.split('-')[0]

    try:
      os.mkdir(os.path.join(config.OUTPUT_DIR, train_page_id))
    except OSError as error: 
      # Directory already exists
      pass

    filepath = os.path.join(config.OUTPUT_DIR, feature_extraction_methods[0].name, train_page_id, f'{train_word.id}.csv')
    distances = ComputeDistances([train_word], test_words, debug=True)
    __WriteToFile(filepath, distances[train_word.id])
