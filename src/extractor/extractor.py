#coding=utf-8
import requests as req
import re
import matplotlib.pyplot as plt
DBUG   = 0

reBODY = r'<body.*?>([\s\S]*?)<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG  = r'<[\s\S]*?>|[ \t\r\f\v]'

reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
'''
正文抽取算法
block为行块半径
timeout超时时间
image是否下载图片链接
'''
class Extractor():
    '''
    初始化
    '''
    def __init__(self, url = "", blockSize=3, timeout=5, image=False,encode='gb2312'):
        self.url       = url
        self.blockSize = blockSize
        self.timeout   = timeout
        self.saveImage = image
        self.rawPage   = ""
        self.ctexts    = []
        self.cblocks   = []
        self.encode    =encode
    '''
    得到url页面的字符
    '''
    def getRawPage(self):
        try:
            resp = req.get(self.url, timeout=self.timeout)
        except Exception as e:
            raise e

        if DBUG: print(resp.encoding)
        #指定页面编码
        resp.encoding = self.encode

        return resp.status_code, resp.text
    #过滤掉tag
    def processTags(self):
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "" ,re.sub(reTRIM.format("style"), "", self.body))
        self.body = re.sub(reTRIM.format("STYLE"),"",self.body)
        # self.body = re.sub(r"[\n]+","\n", re.sub(reTAG, "", self.body))
        self.body = re.sub(reTAG, "", self.body)

    def processBlocks(self):
        #以换行符将文档分行（可能含有空行）
        self.ctexts   = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]

        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))

        maxTextLen = max(self.cblocks)

        if DBUG: print(maxTextLen)
        #找到骤升、骤降点
        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1
        #得到网页正文
        return "".join(self.ctexts[self.start:self.end])

    def processImages(self):
        self.body = reIMG.sub(r'{{\1}}', self.body)

    def getContext(self):
        code, self.rawPage = self.getRawPage()
        self.body = re.findall(reBODY, self.rawPage)[0]

        if DBUG: print(code, self.rawPage)

        if self.saveImage:
            self.processImages()
        self.processTags()
        return self.processBlocks()
        # print(len(self.body.strip("\n")))
class ExtractorPlot(Extractor):
    def processTags(self):
        print "*******过滤标签前*******"
        print(self.body)
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "" ,re.sub(reTRIM.format("style"), "", self.body))
        self.body = re.sub(reTRIM.format("STYLE"),"",self.body)
        # self.body = re.sub(r"[\n]+","\n", re.sub(reTAG, "", self.body))
        self.body = re.sub(reTAG, "", self.body)
        
        raw_input()
        print "*****过滤后的内容*****"
        print(self.body) 
    def processBlocks(self):
        #以换行符将文档分行（可能含有空行）
        self.ctexts   = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]
        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))
        raw_input()
        print "******折线图******"
        plt.plot(self.cblocks)
        plt.show()
        raw_input()
        maxTextLen = max(self.cblocks)
        if DBUG: print(maxTextLen)
        #找到骤升、骤降点
        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1
        print "骤升点:",self.start,"骤降点:",self.end
        raw_input()
        print "*******抽取的网页正文************"
        #得到网页正文
        return "".join(self.ctexts[self.start:self.end])
if __name__ == '__main__':
    ext = Extractor(url="http://tech.163.com/12/0816/06/890RDCT1000915BF.html",blockSize=5, image=False,encode='gb2312')
    print(ext.getContext())
