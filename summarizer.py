
from preprocessor import Preprocessor
from document import Document
from nasari import Nasari
import numpy as np
import math

class Summarizer:

    def __init__(self, nasari, preprocessor,filename, method=['NEARNESS']):
        self.nasari :Nasari = nasari
        self.last_summarization = None
        self.preprocessor = preprocessor
        self.document = Document(filename, self.preprocessor)
        self.sorted_paragraphs_dict = dict()
        self.method = method
        if 'NEARNESS' in self.method:
            self.init_nearness()
        if 'TITLE' in self.method:
            self.init_by_title()

    def title_summarize(self):
        pass

    def init_by_title(self):
        nasari_context = self.document.title_bow
        par_val = []
        for word in self.document.title_bow:
            nasari_vector = self.nasari_vectors(word)
            if not nasari_vector is None:
                vector_id = self.best_nasari_vector_id(word)
                nasari_context = nasari_context.union(self.nasari.concepts[word][vector_id].keys())

        for i in range(len(self.document.paragraphs)):
            bow = self.document.paragraphs_bow[i]
            overlap = bow.intersection(nasari_context)
            par_val.append(len(overlap))
            # print("->", bow)
        self.sorted_paragraphs_dict['TITLE'] = list(np.argsort(par_val))
        self.sorted_paragraphs_dict['TITLE'].reverse()

    def summarize(self, percentage):
        if len(self.method) < 1:
            print("ERROR, NO METHOD")
            return None

        tot_lines = int(len(self.document.lines)*percentage)
        if tot_lines < 1:
            tot_lines = 1
            print("WARNING: TOO FEW LINES! SUMMARIZE TO SINGLE LINE")
        elif tot_lines >= len(self.document.paragraphs):
            print("ALERT: NO SUMMARIZATION NEEDED")
            return range(len(self.document.paragraphs))
        else:
            print("Summarizing to", tot_lines, "lines")

        best_paragraph = np.zeros(len(self.document.paragraphs))

        print("methods:", self.method)
        for method in self.sorted_paragraphs_dict:
            for i in range(len(best_paragraph)):
                best_paragraph[i] += self.sorted_paragraphs_dict[method][i]
        
        best_paragraph = list(np.argsort(best_paragraph))
        best_paragraph.reverse()

        new_lines = best_paragraph[:tot_lines]
        new_lines.sort()

        return [self.document.paragraphs[i] for i in new_lines]

    
    def best_nasari_vector_id(self, word):
        vectors = self.nasari_vectors(word)
        if vectors is None:
            return None
        if len(vectors) == 1:
            return list(vectors.keys())[0]
        max_overlap = 0

        best_vector_id = list(vectors.keys())[0]

        for bn_id in vectors:
            overlap = self.overlap_nasari_vector(vectors[bn_id])
            len_overlap = len(overlap)
            if len_overlap > max_overlap:
                max_overlap = len_overlap
                best_vector_id = bn_id

        return best_vector_id

    def nasari_vectors(self, word):
        if word in self.nasari.concepts:
            return self.nasari.concepts[word]
        return None

    def overlap_nasari_vector(self, nasari_vector):
        doc_bow = self.document.text_bow
        return doc_bow.intersection(set(nasari_vector.keys()))

    def init_nearness(self):
        self.nearness_list = list(np.zeros(len(self.document.paragraphs_bow)))
        title_bow = self.document.title_bow
        for i in range(len(self.document.paragraphs_bow)):
            bow_i = self.document.paragraphs_bow[i]
            nearness = self.nasari.nearness(bow_i, title_bow)
            self.nearness_list[i] += nearness
            for j in range(len(self.document.paragraphs_bow)):
                if i < j:
                    bow_j = self.document.paragraphs_bow[j]
                    nearness = self.nasari.nearness(bow_i, bow_j)
                    self.nearness_list[i] += nearness
                    self.nearness_list[j] += nearness
        
        self.sorted_paragraphs_dict['NEARNESS'] = list(np.argsort(self.nearness_list))
        self.sorted_paragraphs_dict['NEARNESS'].reverse()
