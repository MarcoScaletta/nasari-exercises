
from nasari import Nasari
from preprocessor import Preprocessor
from sentence_ranker import SentenceRanker
from summarizer import Summarizer

preprocessor = Preprocessor("stop_words", "lemming")

nasari = Nasari("dd-small-nasari-15.txt")
filename = []
filename.append("Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt")
filename.append("People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt")
filename.append("The-Last-Man-on-the-Moon--Eugene-Cernan-gives-a-compelling-account.txt")

new_sizes = [0.1, 0.2, 0.3]

results = open("results", "w")

for f in filename:
    summarizer = Summarizer(nasari, preprocessor, f, ['TITLE','NEARNESS'])
    print()
    results.write("\n")
    print("TITLE:", summarizer.document.title.upper())
    results.write("TITLE:"+ summarizer.document.title.upper())
    print()
    results.write("\n")
    results.write("\n")

    for new_size in new_sizes:
        summarized_doc_lines = summarizer.summarize(new_size)
        for i in range(len(summarized_doc_lines)):
            print(str(i+1)+".", summarized_doc_lines[i])
            results.write(str(i+1)+"."+ str(summarized_doc_lines[i]))
            results.write("\n")
        print()
        results.write("\n")
