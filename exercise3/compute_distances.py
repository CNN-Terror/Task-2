import csv
import os
from dtaidistance import dtw
from fastdtw import fastdtw
from feature_extraction import Method
import exercise3_config as config
from readers import GetProcessedInputData
from scipy.spatial.distance import euclidean


# Calculates the distance from the given word to all the other words.
# Input:
#  - word: Word
#  - other_words: list of Word
def ComputeDistance(word, other_words, debug=False):
  distances = {}
  for other_word in other_words:
    # if debug:
    #   print(f'Compute distances for test word {other_word.id}')
    #distances[other_word.id] = \
    #  dtw.distance(word.features, other_word.features)
    distances[other_word.id], _ = \
      fastdtw(word.features, other_word.features, dist=euclidean)

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


def ReadDistances(filepath):
  distances = {}
  with open(filepath, 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
      test_word_id = row[0]
      while test_word_id[0] == '0':
        test_word_id = test_word_id[1:]
      distances[test_word_id] = row[1]
  return distances


def ReadAllDistances(root_dir):
  all_files = [os.path.join(root, file) for root, _, files in os.walk(root_dir) for file in files if file.split('.')[-1] == 'csv']
  distances = {}
  for file in all_files:
    train_word_id = (file.split('/')[-1]).split('.')[0]
    distances[train_word_id] = ReadDistances(file)
  return distances


# We'll store distances in an output dir using csv files as follows
# {output_dir_name}/{feature}/{page_number}/{word_id}.csv = output/BLACK_PIXEL_RATIO/270/270-01-01.csv
if __name__ == "__main__":
  # distancces = ReadAllDistances(config.OUTPUT_DIR)
  try:
    os.mkdir(os.path.join(config.OUTPUT_DIR))
  except OSError as error: 
    # Directory already exists
    pass

  # Single method only!
  feature_extraction_methods = \
    [Method.BLACK_PIXEL_RATIO, Method.BLACK_PIXEL_RATIO_LC_UP, Method.LOWER_CONTOUR, Method.UPPER_CONTOUR]
  transcriptions_as_list, keywords_to_search, train_words, test_words = \
    GetProcessedInputData(feature_extraction_methods, debug=True)

  try:
    os.mkdir(os.path.join(config.OUTPUT_DIR, feature_extraction_methods[0].name))
  except OSError as error: 
    # Directory already exists
    pass

  for train_word in train_words:
    print('====================================================================================================')
    print(f'Train word id: {train_word.id}')
    train_page_id = train_word.id.split('-')[0]

    try:
      os.mkdir(os.path.join(config.OUTPUT_DIR, feature_extraction_methods[0].name, train_page_id))
    except OSError as error: 
      # Directory already exists
      pass

    filepath = os.path.join(config.OUTPUT_DIR, feature_extraction_methods[0].name, train_page_id, f'{train_word.id}.csv')
    distances = ComputeDistances([train_word], test_words, debug=True)
    __WriteToFile(filepath, distances[train_word.id])
