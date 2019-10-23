
class Document:
    
    def __init__(self, filename, preprocessor):
        f = open(filename)
        self.preprocessor = preprocessor
        self.lines = [line.replace("\n", "") for line in f.readlines() if not line.startswith("#") and not line.startswith("\n")]
        self.title = self.lines[0].lower()
        self.paragraphs = self.lines[1:]
        self.title_bow = self.preprocessor.preprocess_sentence_lemming(self.title)       
        self.text_bow = set()
        self.paragraphs_bow = list()

        for i in range(len(self.paragraphs)):
            self.paragraphs_bow.append(self.preprocessor.preprocess_sentence_lemming(self.paragraphs[i].lower()))