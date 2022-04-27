# Methods used to read from the input files exercise.
import os
import exercise3_config as config


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
