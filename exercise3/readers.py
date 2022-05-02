# Methods used to read from the input files exercise.
import os
import exercise3_config as config
from image_preprocessing import CropAllWordImages
from word_builder import BuildTrainAndTestWords
from ipynb.fs.full.binarization import ApplyOtsu


# Applies binarization on the original image, then crops the words using the given mask.
def ExtractWordImagesFromOriginalImage(original_image_path, mask_path):
  image_after_binarization = ApplyOtsu(original_image_path)
  return CropAllWordImages(image_after_binarization, mask_path)


# Extracts all words needed for train and test
# Output:
#  - train_words_per_image: dict containing all train words
#  - testt_words_per_image: dict containing all test words
# Entries in the output dictionaries are like dict[page_number] = list_of_words
def ExtractTrainAndTestWords(train_images_numbers, train_jpg_paths, train_svg_paths,
                             test_images_numbers, test_jpg_paths, test_svg_paths):
  train_words_per_image = {}
  # for index in range(len(train_images_numbers)):
  # TODO: iterate over all images. we can leave it like this for now for testing
  for index in range(1):
    train_words_per_image[train_images_numbers[index]] = ExtractWordImagesFromOriginalImage(train_jpg_paths[index], train_svg_paths[index])

  test_words_per_image = {}
  # for index in range(len(test_images_numbers)):
  # TODO: iterate over all images. we can leave it like this for now for testing
  for index in range(1):
    test_words_per_image[test_images_numbers[index]] = ExtractWordImagesFromOriginalImage(test_jpg_paths[index], test_svg_paths[index])

  return train_words_per_image, test_words_per_image


# Output:
#  - list of size n containing image numbers
#  - list of size n containing paths to original jpg images
#  - list of size n containing paths to svg masks
def ExtractImagePaths(text_file_path):
  images_numbers = []
  jpg_paths = []
  svg_paths = []

  with open(text_file_path) as file:
    for image_number in file.readlines():
      images_numbers.append(str(int(image_number)))
      jpg_image_path = os.path.join(config.DATA_ROOT_DIR, 'images/' + str(int(image_number)) + '.jpg')
      jpg_paths.append(jpg_image_path)
      svg_image_path = os.path.join(config.DATA_ROOT_DIR, 'ground-truth/locations/' + str(int(image_number)) + '.svg')
      svg_paths.append(svg_image_path)

  return images_numbers, jpg_paths, svg_paths


# Extracts transcriptions.
# Output:
#  - transcriptions: dict. transcriptions[keyword_id] = (transcription, index in the doc)
def ExtractTranscriptionsAsDictionary():
  transcriptions = {}

  transcriptions_path = os.path.join(config.DATA_ROOT_DIR, 'ground-truth/transcription.txt')
  index = 0
  current_file = None
  with open(transcriptions_path) as transcriptions_file:
    for line in transcriptions_file.readlines():
      keyword_id, keyword_transcription = line.strip().split(sep=" ")
      keyword_file = keyword_id.split(sep="-")[0]
      if keyword_file != current_file:
        current_file = keyword_file
        index = 0
      transcriptions[keyword_id] = (keyword_transcription, index)
      index += 1

  return transcriptions


# Extracts transcriptions.
# Output:
#  - transcriptions: list of (keyword_id, keyword_transcription)
def ExtractTranscriptionsAsList():
  transcriptions = []

  transcriptions_path = os.path.join(config.DATA_ROOT_DIR, 'ground-truth/transcription.txt')
  with open(transcriptions_path) as transcriptions_file:
    for line in transcriptions_file.readlines():
      keyword_id, keyword_transcription = line.strip().split(sep=" ")
      transcriptions.append((keyword_id, keyword_transcription))

  return transcriptions


# Extracts keywords.
# Output:
#  - keywords_to_search: list of strings (transcriptions)
def ExtractKeywords():
  keywords_to_search = []

  keywords_path = os.path.join(config.DATA_ROOT_DIR, 'task/keywords.txt')
  with open(keywords_path) as keywords_file:
    for line in keywords_file.readlines():
      keywords_to_search.append(line.strip())

  return keywords_to_search


# Reads all input data and processes it.
def GetProcessedInputData(feature_extraction_methods):
  transcriptions_as_list = ExtractTranscriptionsAsList()
  keywords_to_search = ExtractKeywords()

  # Extract paths for train and test files
  train_images_numbers, train_jpg_paths, train_svg_paths = \
    ExtractImagePaths(os.path.join(config.DATA_ROOT_DIR, 'task/train.txt'))
  test_images_numbers, test_jpg_paths, test_svg_paths = \
    ExtractImagePaths(os.path.join(config.DATA_ROOT_DIR, 'task/valid.txt'))

  train_words_per_image, test_words_per_image = \
    ExtractTrainAndTestWords(train_images_numbers, train_jpg_paths, train_svg_paths,
                            test_images_numbers, test_jpg_paths, test_svg_paths)

  train_words, test_words = \
    BuildTrainAndTestWords(train_words_per_image, test_words_per_image, transcriptions_as_list, feature_extraction_methods)
  
  return transcriptions_as_list, keywords_to_search, train_words, test_words
