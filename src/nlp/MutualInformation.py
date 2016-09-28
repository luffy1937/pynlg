import nlpengine as ot
sentenceseq=ot.readline('u8',"./testtxt/1.txt.txt")
possegcutseq=ot.saveCutResult(ot.cut(sentenceseq))
allwordseq=ot.allWordWithFlag(possegcutseq)
gram2seq=ot.bigramsWithFlag(possegcutseq)
gram3seq=ot.trigramsWithFlag(possegcutseq)
miseq=ot.mi2_2(allwordseq,gram2seq)
entropyseq=ot.gram2entropy(miseq,gram3seq,gram2seq)
sortmiseq=sorted(entropyseq,key=lambda x:x[3],reverse=True)
for s in sortmiseq[:30]:
	print s[0][0][0],s[0][0][1],s[0][1][0],s[0][1][1],s[1],s[2],s[3],s[4]
