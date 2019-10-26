
class Nasari:

    def __init__(self, nasari_filename):
        self.concepts = dict()
        self.concepts_bn = dict()
        f = open(nasari_filename)
        i = 0
        for line in f:  
            elem_line = line.replace("\n", "").split(';')
            bn_id = elem_line[0]
            word = elem_line[1].lower()
            index_first_word = 2
            if not "_" in elem_line[2]:
                word += elem_line[2]
                index_first_word = 3

            if not word in self.concepts:
                self.concepts[word] = dict()
            self.concepts_bn[bn_id] = dict()
            first_score = elem_line[index_first_word].split('_')[1]
            words = dict([[w.split('_')[0], float(w.split('_')[1])] for w in elem_line[index_first_word:] if len(w) > 0 and '_' in w])
            self.concepts[word][bn_id] = words
            self.concepts_bn[bn_id]['vector'] = words
            self.concepts_bn[bn_id]['max_score'] = first_score
            i+=1
    
    def sim_concept_word(self, bn_id, word):
        vector = self.concepts_bn[bn_id]['vector']
        max_score = self.concepts_bn[bn_id]['max_score']
        if word in vector:
            return float(vector[word])/float(max_score)
        else:
            return 0

    def sim_concepts(self, bn_id1, bn_id2):
        sim = 0
        words_bn_id1 = set(self.concepts_bn[bn_id1]['vector'].keys())
        words_bn_id2 = set(self.concepts_bn[bn_id2]['vector'].keys())
        overlap = words_bn_id1.intersection(words_bn_id2)
        for word in overlap:
            sim += self.sim_concept_word(bn_id1, word)
            sim += self.sim_concept_word(bn_id2, word)
        return sim


    def sim(self, w1, w2):
        if not w1 in self.concepts or not w2 in self.concepts:
            return 0
        w1_concept = self.concepts[w1]
        w2_concept = self.concepts[w2]
        max_sim = 0
        for bn_id_w1 in w1_concept:
            for bn_id_w2 in w2_concept:
                sim = self.sim_concepts(bn_id_w1, bn_id_w2)
                if sim > max_sim:
                    max_sim = sim
        return max_sim

    def nearness(self, bow1, bow2):
        nearness = 0
        for w1 in bow1:
            for w2 in bow2:
                nearness += self.sim(w1,w2)
        return nearness


