#coding=UTF-8
import codecs
import glob
import os
from src.nlp import nlpengine as ot
import csv
import math
import copy

#将所在文件夹下的.txt.txt文件中的内容读取并存入一个.txt.txt
def toOneTxt():
    fw=codecs.open(r'.\total.txt.txt','w','u8')
    for filename in glob.glob(r'.\*.txt.txt'):
        fr=codecs.open(filename,'r','u8')
        fw.writelines([line for line in fr.read()])
        fr.close()
    fw.close()

def processAllTxt(path):
    """
    将所在文件夹下的.txt文件中的内容读取,返回一个二元组，
    二元组第一个元素结构是[[[(word,flag),(word,flag)...],[句子]],[文档]]
    二元组第二个元素结构是[[(word,flag),(word,flag)...],[句子]]  不区分文档

    @param path:
    @return:
    """
    #区分文档
    item1=[]
    #不区分文档
    item2=[]
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path,filename)) and filename.endswith('.txt'):
            sentenceseq=ot.readline('u8',os.path.join(path,filename))
            possegcutseq=ot.cut(sentenceseq)
            cutresultsaved=ot.saveCutResult (possegcutseq)

            for i in cutresultsaved:
                item2.append(i)
            item1.append(cutresultsaved)
    return (item1,item2)
def readsavecsv(filepath):
    """
    读save.csv文件
    @param filepath:
    @return:
    """
    returnseq=[]
    def decodeu8(str):
        return codecs.decode(str,'u8')

    f=open(filepath,'r')
    type=[decodeu8,str,decodeu8,str,float,int,float,float,int]
    cr=csv.reader(f)
    for r in cr:
        returnseq.append([convert(value) for convert,value in zip(type,r)])
    f.close()
    return returnseq
def readmilogcsv(filepath):
    """
    读milogdf.csv文件
    @param filepath:
    @return:
    """
    returnseq=[]
    def decodeu8(str):
        return codecs.decode(str,'u8')

    f=open(filepath,'r')
    type=[decodeu8,str,decodeu8,str,float,float]
    cr=csv.reader(f)
    cr.next()
    for r in cr:
        returnseq.append([convert(value) for convert,value in zip(type,r)])
    f.close()
    return returnseq
def filer(mi,logdf,seq):
    returnseq=[item for item in seq if item[4]>mi and item[5]>logdf]
    # f=open('fiter.csv','w')
    # csvwriter=csv.writer(f)
    # csvwriter.writerow(['Word1','Flag1','Word2','Flag2','MI','logDF'])
    # csvwriter.writerows([i[0].encode('u8'),i[1],i[2].encode('u8'),i[3],i[4],i[5]] for i in returnseq)
    # f.close()
    return returnseq
def fiterbystopword(seq):
    stop=['f','p','c','u','y','uj']
    returnseq=[item for item in seq if item[1] not in stop and item[3] not in stop ]
    f=open('fiter.csv','w')
    csvwriter=csv.writer(f)
    csvwriter.writerow(['Word1','Flag1','Word2','Flag2','MI','logDF'])
    csvwriter.writerows([i[0].encode('u8'),i[1],i[2].encode('u8'),i[3],i[4],i[5]] for i in returnseq)
    f.close()
    return returnseq
if __name__ == '__main__':
    # a=processAllTxt()
    s=readmilogcsv(u'E:\\实验室资料\\nlg\\pynlg\src\\io\\milogdf.csv')
    fs=filer(2,6,s)

    print len(fs)
    print(len(fiterbystopword(fs)))