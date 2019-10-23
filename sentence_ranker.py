
from preprocessor import Preprocessor

class SentenceRanker:

    def __init__(self, nasari):
        self.nasari = nasari
    
    def score_bow(self, bag_of_words,sentence):
        
        score = 0
        for word in bag_of_words:
            score += sentence.count(word)
        return score