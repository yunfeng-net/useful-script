
# -*- coding: utf-8 -*-  
   
import urllib2  
import urllib  
import re  
import thread  
import time  

#web = "http://blog.nosqlfan.com/html/"
#top = "3537.html"
web = "http://www.arft.net/jpkj/jrkc/skjy/"
top = "cha_9_1.html"
root = "c:\\nobackup\\dir-5\\"

class Spider:  
      
    def __init__(self):
        self.file_id = 1
        self.pages = {}
#        self.myTool = HTML_Tool()  
  
    # 将所有的网页都扣出来，添加到列表中并且返回列表  
    def GetPage(self,page):
        if self.pages[page]:
            return
        myUrl = page
        print u"加载", myUrl
        myResponse = urllib2.urlopen(myUrl)  
        myPage = myResponse.read()  
        #encode的作用是将unicode编码转换成其他编码的字符串  
        #decode的作用是将其他编码的字符串转换成unicode编码  
        unicodePage = myPage.decode("gbk")
  
        # 找出所有class="content"的div标记  
        #re.S是任意匹配模式，也就是.可以匹配换行符  
#        myItems = re.findall('('+web+'.*?)[\"\']',unicodePage,re.S)  
        myItems = re.findall('href="(.*?)\"',unicodePage,re.S)
        for item in myItems:
            url = web+item
            if url not in self.pages:
                self.pages[url] = ""
        myItems = re.findall('src="(.*?)\"',unicodePage,re.S)
        for item in myItems:
            it = re.sub("images[\\/]", "", item);
            urllib.urlretrieve(web+item, root+it)
        # TODO save as file
        name = "%d.html"%self.file_id
        sub = re.findall('(cha.*)', page)
        if len(sub)>0:
            name = sub[0]
            self.pages[page] = name
            print page, name
            self.file_id += 1
            ww = open(root+name, 'w')
            item = re.sub("images[\\/]", "", unicodePage.encode("gbk"))
            ww.write(item)
            ww.close()
        else:
            self.pages[page] = "ok"

    def addPage(self, page):
        self.pages[page] = ""
    # 用于加载新的网页  
    def LoadPage(self):
        ok = True
        while ok:
            ok = False
            items = []
            for page in self.pages:
                if len(self.pages[page])<=0:
                    items.append(page)
            for item in items:
                self.GetPage(item)
                ok = True # to do
            #print self.pages
          
    def Start(self, html):
        self.pages[html] = ""
        # thread.start_new_thread(self.LoadPage,())
        self.LoadPage()
          
mySpider = Spider()
for i in range(1,9):
    mySpider.addPage(web+"cha_%d_1.html" % i)
mySpider.Start(web+top) 

