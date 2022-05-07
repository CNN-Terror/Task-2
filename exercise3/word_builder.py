from word import Word, TestWord
from feature_extraction import ExtractFeatures


# Builds the lists of train and test words.
#
# The following code is not nice but it works because transcriptions and 
# train_words_per_image + test_words_per_image are in the same order.
#
# Input:
#  - transcriptions: list of transcriptions
#  - train_words_per_image: 
#  - test_words_per_image: 
# Output:
#  - train_words, test_words: list of Word object where only the following fields are set:
#     - id
#     - transcription
#     - image
#     - features
def BuildTrainAndTestWords(train_words_per_image, test_words_per_image, transcriptions, feature_extraction_methods, debug=False):
  train_words = []
  test_words = []
  
  index = 0
  for _, train_words_per_current_image in train_words_per_image.items():
    for train_word in train_words_per_current_image:
      if debug:
        print(f'Build train word {transcriptions[index][0]}')

      word = Word()
      word.image = train_word
      word.features = ExtractFeatures(train_word, feature_extraction_methods)
      word.id = transcriptions[index][0]
      word.transcription = transcriptions[index][1]
      index += 1
      train_words.append(word)

  for image_number, test_words_per_current_image in test_words_per_image.items():
    # TODO: remove once we use all files
    while transcriptions[index][0].split("-")[0] != image_number:
      index += 1
    for test_word in test_words_per_current_image:
      if debug:
        print(f'Build test word {transcriptions[index][0]}')

      word = TestWord()
      word.image = test_word
      word.features = ExtractFeatures(test_word, feature_extraction_methods)
      word.id = transcriptions[index][0]
      word.transcription = transcriptions[index][1]
      index += 1
      test_words.append(word)

  return train_words, test_words