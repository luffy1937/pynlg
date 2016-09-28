#coding=utf-8
#读一个文件，返回一个列表，文件中每行对应列表的一个元素
import codecs
import math
import jieba
import jieba.posseg as pseg
def ngram(seqtogram,n):
    """

    @param seqtogram:
    @param n:
    @return:
    """
    seqlen=len(seqtogram)
    if seqlen<n:
        return []
    else :
        return [zip(seqtogram[:seqlen-n+2],seqtogram[seqlen-1])]

def readline(encode,filename):
    fr=codecs.open(filename,'r',encode)
    returnseq=[]
    for line in fr:
        returnseq.append(line[:-1])#最后一个字符是"\n"
    fr.close()
    return returnseq

#分词及词性标注，参数是句子（或者短语）的列表，返回jieba对每一句话的分词结果序列
def cut(seq):
    jieba.initialize()
    returnseq=[pseg.cut(item) for item in seq]
    return returnseq
#读取停用词文件，返回停用词列表
def readstopwords():
    fr=codecs.open('..\data\stopwords.txt','r','u8')
    stopwords=[]
    for line in fr:
        stopwords.append(line[:-1])
    fr.close()
    return stopwords
def saveCutResultWithoutStopword(possegcutseq):
    """
        遗留的方法
        将jieba的分词及词性标注结果（迭代器的形式），存起来并且用了词性过滤以及通用词过滤
        目前看来这种方法不好
        过滤应该在形成词组后再过滤，否则会破坏词间的关系（原来停用词隔开的词）
        @param possegcutseq: jieba分词方法返回的迭代器
        @return:
        """
    returnseq=[]
    stopword=readstopwords()
    stopflag=['x','uj','u','f','p','c','y']
    # "stopwords num:",len(stopword),repr(stopword[0]),repr(stopword[1100])
    for j in possegcutseq:
        tempseq=[]
        for i in j:
            if i.word not in stopword and i.flag not in stopflag:
                tempseq.append((i.word,i.flag))
        if len(tempseq)!=0:
            returnseq.append(tempseq)
    #returnseq=[[(i.word,i.flag) for i in j if i.word not in stopword] for j in possegcutseq]
    # print returnseq[1: 10]
    return returnseq
def saveCutResult(possegcutseq):
    """
    遍历jieba的分词结果，并存起来
    @param possegcutseq:
    @return:
    """
    returnseq=[]
    for j in possegcutseq:
        tempseq=[(i.word,i.flag) for i in j]
        if len(tempseq)!=0:
            returnseq.append(tempseq)
    return returnseq

#根据jieba返回的分词结果序列。将所有词的词性组合，组成一个列表返回(需要修改为以saveCutResult返回值为参数)
def cixingrules(cutseq):
    returnseq=[]
    for item in cutseq:
        cixing=""
        for w in item:
            cixing=cixing+'/'+w.flag
        returnseq.append(cixing)
    return returnseq
#根据jieba返回的分词结果序列。将所有的分词结果（word,flag）组成一个列表返回
def allWordWithFlag(possegcutseq):
    returnseq=[]
    for p in possegcutseq:
        for item in p:
            returnseq.append(item)
    return returnseq
    
#将字典变为二元组链表的形式（为了排序）
def dict2seq(d):
    returnseq=[]
    for item in d:
        returnseq.append((item,d[item]))
    return returnseq
#从列表s中取前n个元素，组成字典返回
def seq2dict(s,n):
    returndict={}
    for cixing,num in s[1:n+1]:
        returndict[cixing]=num
    return returndict

import nltk
#根据jieba对句子列表的词性标注结果（也是一个列表），返回所有可能的二元组合（bigrams）
def bigramsWithFlag(possegcutseq):
    returnseq=[]
    for j in possegcutseq:
        # returnseq+=ngram(j,2)
        returnseq+=nltk.bigrams(j)
    return returnseq
#返回可能的三元组合
def trigramsWithFlag(possegcutseq):
    returnseq=[]
    for j in possegcutseq:
        # returnseq+=ngram(j,3)
        returnseq+=nltk.trigrams(j)
    return returnseq
#返回n元组合
def ngramsWithFlag(possegcutseq,n):
    returnseq=[]
    for j in possegcutseq:
        # returnseq+=nltk.ngrams(j,n)
        returnseq+=ngram(j,n)
    return returnseq
#返回二元组合（不包括Flag）
def bigrams(jiebaseq):
    returnseq=[]
    for j in jiebaseq:
        tempseq=[i.word for i in j]
        returnseq+=nltk.bigrams(tempseq)
    return returnseq
#计算互信息 2-gram Mutual Information(以每篇为单位计算MI和词频)
def mi2(allwordseq,gram2seq):
    returnMIseq=[]
    fd=nltk.FreqDist(gram2seq)
    gram2set=set(gram2seq)
    fw1=0
    fw2=0
    for g2 in gram2set:
        fw1=allwordseq.count(g2[0])
        fw2=allwordseq.count(g2[1])
        returnMIseq.append((g2,float(fd[g2])/(fw1+fw2-fd[g2]),fd[g2]))
    return  returnMIseq
def mi2_2(allwordseq,gram2seq):
    """
    互信息
    @param allwordseq:
    @param gram2seq:
    @return:
    """
    returnMIseq=[]
    gram2set=set(gram2seq)
    fw1=0
    fw2=0
    fw12=0
    allwordslen=len(allwordseq)
    gram2len=len(gram2seq)
    for g2 in gram2set:
        fw1=float(allwordseq.count(g2[0]))/ allwordslen
        # print allwordseq.count(g2[0]),len(allwordseq),fw1
        fw2=float(allwordseq.count(g2[1]))/ allwordslen
        #print allwordseq.count(g2[1]),len(allwordseq),fw2
        fw12=float(gram2seq.count(g2))/gram2len
        # print fd[g2],len(gram2seq),fw12
        #print g2[0][0],g2[1][0],allwordseq.count(g2[0]),allwordseq.count(g2[1]),fd[g2],len(allwordseq),len(gram2seq),math.log(fw12/(fw1*fw2),2)
        returnMIseq.append((g2,math.log(fw12/(fw1*fw2),2),gram2seq.count(g2)))
    return returnMIseq
def gram2entropy(mi2_2_return,trigramsWithFlag_return,bigramsWithFlag_return):
    returnseq=[]
    cfdright=nltk.ConditionalFreqDist([((item[0],item[1]),item[2]) for item in trigramsWithFlag_return])
    cfdleft=nltk.ConditionalFreqDist([((item[1],item[2]),item[0]) for item in trigramsWithFlag_return])
    
    for item in mi2_2_return:
        leftEntropy=0.0
        rightEntropy=0.0
        fdright=cfdright[item[0]]
        fdleft=cfdleft[item[0]]
        pitem=bigramsWithFlag_return.count(item[0])
        #print pitem
        if fdright.N()!=0:
            p=0
            for f in fdright:
                p=float(fdright[f])/pitem
                rightEntropy-=p*math.log(p,2)
        if fdleft.N()!=0:
            p=0
            for f in fdleft:
                p=float(fdleft[f])/pitem
                leftEntropy-=p*math.log(p,2)
        #print leftEntropy,rightEntropy
        returnseq.append((item[0],item[1],item[2],leftEntropy,rightEntropy))
    return returnseq
#根据processAllTxtTxt_return[0],返回每个二元组的DF [((word,flag),(word,flag)):num,((word,flag),(word,flag)):num...]
def documentGram2FreqDist(processAllTxtTxt_return_0):
    tempseq=[]#[set(文档gram2),set(文档gram2)...]
    for d in processAllTxtTxt_return_0:
        tempseq+=list(set(bigramsWithFlag(d)))
    return nltk.FreqDist(tempseq)
#计算DF
def documentFreq(gram2entropy_return,documentGram2Freq_return):
    returnseq=[]
    for g in gram2entropy_return:
        returnseq.append((g[0],g[1],g[2],g[3],g[4],documentGram2Freq_return[g[0]]))
    return returnseq