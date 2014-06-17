#-*- coding: utf-8 -*-  
   
import urllib
from urllib.parse import urlparse
from urllib.parse import ParseResult
from urllib.request import urlopen
from urllib.request import urlretrieve

import re  
import time

web = "http://www.arft.net/jpkj/jrkc/skjy/a.html"
webres = urlparse(web)
root = "c:\\nobackup\\dir-5\\"

class Page:
    pass
class Spider:
    def __init__(self):
        self.file_id = 1
        self.to_fetch = {}
        self.ready = {}

    def add_url(self, url, parent, res = None):
        if res is None:
            url, res = self.parse(url, parent)
        if url in self.to_fetch:
            return self.to_fetch[url]
        if url in self.ready:
            return self.ready
        isHtml = True
        if res.path.find(".html")<0:
            if res.path.find(".jpg")<0:
                return None
            else:
                isHtml = False
        page = Page()
        page.isHtml = isHtml
        page.name = re.sub(r'/', '.', res.path)
        if page.name[0]=='.':
            page.name = page.name[1:]
        self.to_fetch[url] = page
        #print("add", url, res, page.name)
        return page
    
    def load(self):
        myUrl = list(self.to_fetch.keys())[0]
        page = self.to_fetch[myUrl]
        print(u"加载", myUrl)
        myResponse = urlopen(myUrl)  
        myPage = myResponse.read()
        page.html = myPage.decode("gbk")
        parent = urlparse(myUrl)
        self.get_anchor_pic(page, parent)
        self.get_anchor_html(page, parent)
        del self.to_fetch[myUrl]
        self.ready[myUrl] = page
        page.todo = False
        
    def get_anchor_pic(self, page, respar):
        myItems = re.findall('src="(.*?)\"',page.html,re.S)
        for item in myItems:
            #print("url", item)
            url, res = self.parse(item, respar)
            #print("pic", url, res)
            page = self.filter_out(url, res)
            if page and url in self.to_fetch:
                del self.to_fetch[url]
                self.ready[url] = page
                urlretrieve(url, root+page.name)

    def parse(self, url, respar):
        res = urlparse(url)
        nl = res.path
        if respar.path.rfind("/")>=0:
            nl = respar.path[0:respar.path.rfind("/")+1] + res.path
        res2 = ParseResult(scheme = res.scheme or respar.scheme,
                          netloc = res.netloc or respar.netloc,
                          path = nl,
                           params='', query='', fragment='')
        url = res2.geturl()
        #print("parse", url, res2, respar)
        return (url, res2)
        
    def get_anchor_html(self, page, respar):
        """ for each anchor, add the new url"""    
        myItems = re.findall('href="(.*?)\"',page.html,re.S)
        for item in myItems:
            url, res = self.parse(item, respar)
            #print("html", url, res)
            page = self.filter_out(url, res)
            #print(url, res, page)

    def filter_out(self, url, res):
        if res.netloc!=webres.netloc: # ignore page in the other root
            return None
        if url in self.to_fetch:
            return self.to_fetch[url]
        if url in self.ready: 
            return self.ready[url]
        return self.add_url(url, None, res)
    
    def save_anchor(self, html, respar):
        # for each anchor -> name
        myItems = re.findall('href="(.*?)\"', html,re.S)
        myPics = re.findall('src="(.*?)\"', html,re.S)
        myItems.extend(myPics)
        for item in myItems:
            url, res = self.parse(item, respar)
            if self.filter_out(url, res) is None:
                continue
            print("url", item)
            target = self.ready[url].name
            if res.fragment:
                target += '#'+res.fragment
            if url in self.ready:
                html = re.sub(item, target, html)
        return html
    
    def save(self):
        for url in self.ready:
            page = self.ready[url]
            res2 = urlparse(url)
            if page.isHtml:
                #print("save", root+page.name)
                #continue
                ww = open(root+page.name, 'w')
                html = self.save_anchor(page.html, res2)
                ww.write(html)
                ww.close()
    
    def run(self):
        while len(self.to_fetch)>0:
            self.load()
        if len(self.ready)>0:
            self.save()

mySpider = Spider()
for i in range(1,2):
    mySpider.add_url("cha_%d_1.html" % i, webres)
mySpider.run()
