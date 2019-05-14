import spacy as sp

class SpacyWrapper:
   def __init__(self):
      self.nlp = sp.load('en_core_web_lg')

   def process(self, word):
      return self.nlp(word)

   def compare(self, word, header):
      return word.similarity(header)