# Finds the closest known word for the given unknwon_word.
# Input:
#  - unknown_word: Word object
#  - known_words: list of Word object
#  - distances: dict
def FindClosestKnownWord(unknwon_word, known_words, distances):
  smallest_distance_to_word = None
  closest_word = None

  for known_word in known_words:
    if closest_word is None or distances[known_word.id][unknwon_word.id] < smallest_distance_to_word:
      smallest_distance_to_word = distances[known_word.id][unknwon_word.id]
      closest_word = known_word
  
  return closest_word


# Find all test images whose closest train word has the given transcription 
# Input:
#  - keyword_transcription: string following the ground-truth/transcription.txt file's format
#  - transcriptions: dict. transcriptions[keyword_id] = transcription
# Output:
#  - 
def SpotKeyword(keyword_transcription, test_words):
  return [test_word for test_word in test_words \
          if test_word.closest_train_word.transcription == keyword_transcription]
