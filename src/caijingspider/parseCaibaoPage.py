#coding=utf-8
import requests
import re
import codecs
import src.extractor.extractor
import thread
url="http://tech.163.com/caibao"
r=r'<a href="(\S+)">\D\d\D\D</a>'
def getRawPage(url,en):
    try:
        resp=requests.get(url,timeout=5)
    except Exception as e:
        raise e
    resp.encoding=en
    return resp.text
def geturl(text):
    m=re.compile(r)
    urls=re.findall(m,text)
    return urls

def download(urls,en,tag):
    """
       @param urls:要下载的url列表
       @param encode:网页编码  
       @param tag:给下载的文档加一个标识
    """
    count=0;
    for u in urls:
       # print u,count
        try:
            count=count+1;
            temp=src.extractor.extractor.Extractor(url=u, blockSize=5, image=False, encode=en)
            fw=codecs.open(r'..\..\data\caibao\\'+tag+str(count)+'.txt','w','u8')
            fw.write(temp.getContext())
            fw.close()
        except:
            print "Error: unable to download:"+u+"  with tag"+tag
    return count
def downloadController(urls,encode):
    """将urls链表分给线程"""
    l=len(urls)
    count=0
    while count+50<l:
        try:
            thread.start_new_thread(download, (urls[count:count+50],encode,str(count)+"_"+str(count+50)+"_",))
        except:
            print "unable start thread :"+str(count)+"_"+str(count+50)+"_"
            break
        print("start thread:"+str(count)+"_"+str(count+50)+"_")
        count+=50
    try:
        thread.start_new_thread(download, (urls[count:l],encode,str(count)+"_"+str(l)+"_",))
    except:
        print("unable start thread:"+str(count)+"_"+str(l)+"_")
    print ("start thread:"+str(count)+"_"+str(l)+"_")
    #可能出现的bug是：线程还没创建，就退出了
    while thread._count()!=0:
        pass
    print "all threads exit"
urls=geturl(getRawPage(url,'gb2312'))
downloadController(urls, 'gb2312')

