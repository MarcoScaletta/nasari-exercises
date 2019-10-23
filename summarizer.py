
from preprocessor import Preprocessor
from document import Document
from nasari import Nasari
import numpy as np
import math

class Summarizer:

    def __init__(self, nasari, preprocessor,filename):
        self.nasari :Nasari = nasari
        self.last_summarization = None
        self.preprocessor = preprocessor
        self.document = Document(filename, self.preprocessor)
        self.init_no_weights()

    def title_summarize(self):
        pass

    def init_no_weights(self):
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
        self.sorted_paragraphs = list(np.argsort(par_val))
        self.sorted_paragraphs.reverse()

    def init_weights(self):
        # nasari_context = [[word, 0] self.document.title_bow]
        self.init_vectors()
        
    def summarize(self, percentage):
        tot_lines = int(len(self.document.lines)*percentage)
        if tot_lines < 1:
            tot_lines = 1
            print("WARNING: TOO FEW LINES! SUMMARIZE TO SINGLE LINE")
        elif tot_lines >= len(self.document.paragraphs):
            print("ALERT: NO SUMMARIZATION NEEDED")
            return range(len(self.document.paragraphs))
        else:
            print("Summarizing to", tot_lines, "lines")
        new_lines = self.sorted_paragraphs[:tot_lines]
        new_lines.sort()
        return [self.document.paragraphs[i] for i in new_lines]

    
    def best_nasari_vector_id(self, word):
        vectors = self.nasari_vectors(word)
        # l = list(vectors.keys())
        # l.sort()
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

    def init_vectors(self):
        self.vectors_id = dict()
        for word in self.document.text_bow:
            best_vector_id = self.best_nasari_vector_id(word)
            if best_vector_id is not None:
                self.vectors_id[word] = best_vector_id

    # def wo(self, v1, v2):
    #     wo = 0
    #     if v1 is not None and v2 is not None:
    #         print(v1)
    #         print(v2)
    #         overlap_dimensions = list(set(v1.keys()).intersection(set(v2.keys())))
    #         rank_sum = 0
    #         index_sum = 0
    #         for i in range(len(overlap_dimensions)):
    #             q = overlap_dimensions[i]
    #             rank_sum += float(1)/float(v1[q] + v2[q])
    #             if i > 0:
    #                 index_sum += float(1)/float(2*i)
    #         index_sum += float(1)/float(2*len(overlap_dimensions))
    #         print(rank_sum)
    #         print(index_sum)
    #         if len(overlap_dimensions) > 0:
    #             wo = rank_sum/index_sum
    #     return wo

    # def sim(self, w1, w2):
    #     # if w1 == w2:
    #     #     return 1
    #     # else:
    #     max_sim = 0
    #     w1_vectors = self.nasari_vectors(w1)
    #     w2_vectors = self.nasari_vectors(w2)
    #     if w1_vectors is None or w2_vectors is None:
    #         return 0
    #     for v1 in w1_vectors:
    #         for v2 in w2_vectors:
    #             # sim = math.sqrt(self.wo(w1_vectors[v1], w2_vectors[v2]))
    #             sim = math.sqrt(self.wo(w1_vectors[v1], w2_vectors[v2]))
    #             if sim > max_sim:
    #                 max_sim = sim
    #     return sim
            
