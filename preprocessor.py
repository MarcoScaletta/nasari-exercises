from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import nltk
from nltk.corpus import wordnet as wn


class Preprocessor:

    def __init__(self, stop_words_filename, method):
        f = open(stop_words_filename)
        self.stop_words = set(f.read().splitlines())
        self.lemmatizer = WordNetLemmatizer()
        self.pos_tags = {}
        if method is "stemming":
            self.preprocess_sentence = self.preprocess_sentence_stemming
        elif method is "lemming":
            self.preprocess_sentence = self.preprocess_sentence_lemming
        else:
            self.preprocess_sentence = None

    def wn_relevant_words_tags(self, sentence):
        tokens = word_tokenize(sentence)
        tokens_pos_tags = nltk.pos_tag(tokens, lang='eng')
        pairs = [(pair[0], self.wn_pos(pair[1])) for pair in tokens_pos_tags
                 if pair[0] not in self.stop_words and self.wn_pos(pair[1]) is not "X"]
        return pairs

    def preprocess_sentence_lemming(self, sentence):
        relevant_words_tags = self.wn_relevant_words_tags(sentence)
        lemma_set = set(map(lambda x: self.lemmatizer.lemmatize(x[0], pos=x[1]), relevant_words_tags))
        return lemma_set

    def preprocess_sentence_stemming(self, sentence):
        relevant_words_tags = self.wn_relevant_words_tags(sentence)
        stems_set = set(map(lambda x: PorterStemmer().stem(x[0]), relevant_words_tags))
        return stems_set

    def preprocess_word(self, word, stem=False):
        cleaned_word = self.clean_string(word)
        if stem:
            return PorterStemmer().stem(cleaned_word)
        return cleaned_word

    @staticmethod
    def wn_pos(tag):
        if tag.startswith('NN'):
            return wn.NOUN
        elif tag.startswith('VB'):
            return wn.VERB
        elif tag.startswith('JJ'):
            return wn.ADJ
        elif tag.startswith('RB'):
            return wn.ADV
        else:
            return 'X'

    @staticmethod
    def clean_string(raw_string):
        return raw_string.replace("\n", "").translate(str.maketrans('', '', string.punctuation))
