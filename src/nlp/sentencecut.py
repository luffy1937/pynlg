#coding=UTF-8
import codecs
import re
import glob
import os
#对中文进行分句
def sentencecut(text):
    pattern=re.compile(u'[ 【】（）()《》？、：；，,\]\[。’\\\/‘“”！]+')
    return pattern.split(text)
#读取一个文件夹下的所有文件，分句结果存进新文件
def sentencesave():
    for filename in glob.glob(r'..\..\data\testtxt\*.txt'):
        fr=codecs.open(filename,'r','u8')
        fw=codecs.open(filename+'.txt','w','u8')
        fw.writelines([line+'\n' for line in sentencecut(fr.read())])
        fr.close()
        fw.close()
if __name__=='__main__':
    for dirt,dirtnam,filenames in os.walk('..\..\data\caibao'):
        for filename in filenames:
            if filename.endswith('.txt'):
                with codecs.open(os.path.join(dirt,filename),'r','u8') as fr:
                    with codecs.open(os.path.join(dirt,'..\\caibaosentence\\'+filename),'w','u8') as fw:
                        fw.writelines([line+'\n' for line in sentencecut(fr.read())])


