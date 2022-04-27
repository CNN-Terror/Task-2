class Word:
  id = None
  transcription = None # string
  image = None # PIL.Image
  features = None 


class TestWord(Word):
  closest_train_word = None # Word