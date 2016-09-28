#coding=utf-8
import nlpengine as ot
import src.io.iotool as it
import csv
import csv
import codecs
processAllReturn=it.processAllTxt(u'..\..\data\minicaibaosentence')
allwordseq=ot.allWordWithFlag (processAllReturn[1])
gram2seq=ot.bigramsWithFlag (processAllReturn[1])
gram3seq=ot.trigramsWithFlag (processAllReturn[1])
miseq=ot.mi2_2 (allwordseq,gram2seq)
miEntropyseq=ot.gram2entropy(miseq,gram3seq,gram2seq)
del miseq
documentgram2freq=ot.documentGram2FreqDist(processAllReturn[0])
MIEntropyDF=ot.documentFreq(miEntropyseq,documentgram2freq)
sortedseq=sorted(MIEntropyDF,key=lambda x:x[5],reverse=True)
f=open('allsave.csv','w')
csvwriter=csv.writer(f)

csvwriter.writerows([[s[0][0][0].encode('u8'),s[0][0][1],s[0][1][0].encode('u8'),s[0][1][1],s[1],s[2],s[3],s[4],s[5]]for s in sortedseq])
f.close()
# f= open('result.txt','txtw')
for s in sortedseq[:30]:
    # f.write(s[0][0][0],s[0][0][1],s[0][1][0],s[0][1][1],s[1],s[2],s[3],s[4],s[5])
	print s[0][0][0],s[0][0][1],s[0][1][0],s[0][1][1],s[1],s[2],s[3],s[4],s[5]
