# ...
# Input:
#  - keyword_transcription: string following the ground-truth/transcription.txt file's format
#  - transcriptions: dict. transcriptions[keyword_id] = transcription
# Output:
#  - 
def SpotKeyword(keyword_transcription, train_words, test_words, distances):
  # Find all test images 
  test_keywords = [word for word in test_words if word.transcription == keyword_transcription]
  
  
  spotted_keywords = [] 

  # Iterate over all train words
  # for train_word in train_words:
    
  return spotted_keywords