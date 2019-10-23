
class Nasari:

    def __init__(self, nasari_filename):
        self.concepts = dict()
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
            
            words = dict([[w.split('_')[0], float(w.split('_')[1])] for w in elem_line[index_first_word:] if len(w) > 0 and '_' in w])
            self.concepts[word][bn_id]= words
                
            i+=1