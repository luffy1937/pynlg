import nlpengine as ot
import nltk.collocations as cl


sentenceseq=ot.readline('u8',u"../data/caibao/1.txt.txt")
possegcutseq=ot.saveCutResult(ot.cut(sentenceseq))
allwordseq=ot.allWordWithFlag(possegcutseq)
gram2seq=ot.bigramsWithFlag(possegcutseq)
#bcf=cl.BigramCollocationFinder(nltk.FreqDist([i[0] for i in allwordseq]),nltk.FreqDist([(i[0][0],i[1][0]) for i in gram2seq]))
bcf=cl.BigramCollocationFinder.from_words([a[0] for a in allwordseq])
bm=cl.BigramAssocMeasures()
for bigram in bcf.score_ngrams(bm.pmi)[:30]:
    print bigram[0][0],bigram[0][1],bigram[1]

                           
