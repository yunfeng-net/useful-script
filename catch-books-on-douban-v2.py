# -*- coding: utf-8 -*-
import os
import re
from urllib import urlopen  
from pprint import pprint
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring
import cgi

db = ElementTree(Element('root'))
#root = ET.parse('c:\\nobackup\\douban4.xml')
ns0 = "{http://www.w3.org/2005/Atom}"
ns1="{http://a9.com/-/spec/opensearchrss/1.0/}"
ns2="{http://www.douban.com/xmlns/}"
ns3="{http://schemas.google.com/g/2005}"
show = { 'wish' : 0,  'read' : 2,  'reading' : 1 }


def load_subject(child, node):
    for x in child.getchildren():
        if x.tag.rfind('title')>0:
            ele = Element('title')
            ele.text = x.text
            node.append(ele)
        if x.tag.rfind('link')>0:
            if x.get('rel')=='alternate':
                ele = Element('id')
                ele.text
                s = x.get('href')
                s = s[0:len(s)-1]
                ele.text = s[s.rfind('/')+1:]
                node.append(ele)

def load_books(books, db):
    for book in books:
        node = Element('book')
        db.getroot().append(node)
        for child in book.getchildren():
            if child.tag.rfind('subject')>0:
                load_subject(child, node)                     
            if child.tag.rfind('tag')>0 and child.get('name'):
                ele = Element('tag')
                ele.text = child.get('name')
                node.append(ele)

user_id = "60284471"
url = "http://api.douban.com/people/"+user_id
url += "/collection?cat=book&max-results=1000&start-index="

n = 0
for i in range(100):
    url2 = url + str(i*50+1)
    print url2
    ++n
    doc = urlopen(url2).read()
    root = fromstring(doc)
    books = root.findall(ns0+'entry')
    if len(books)>0:
        load_books(books, db)
    else:
        break
    
db.write('H:\\e.xml', 'utf-8')
#testFile = open('c:\\nobackup\\douban4.txt','w')
#testFile.write(doc)
#testFile.close()
