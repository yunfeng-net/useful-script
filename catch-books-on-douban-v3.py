# -*- coding: utf-8 -*-
import os
import re
from urllib import urlopen  
from pprint import pprint
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring
import cgi
from datetime import date
import json

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

def get_url(year, month):
    user_id = "60284471"
    url = "https://api.douban.com/v2/book/user/"+user_id
    url += "/collections?status=read"
    begin = date(year, month, 1)
    end = date(year, month, 28)
    try:
        end = end.replace(day=29)
        try:
            end = end.replace(day=30)
            try:
                end = end.replace(day=31)
            except:
                n = 1
        except:
            n = 2
    except:
        n = 3
    url += "&from=" + begin.isoformat() + "T00:00:01+08:00" \
           + "&to=" + end.isoformat() + "T23:59:59+08:00"
    #print url
    return (url, begin, end)

def get_books(year, month, start):
    (url2, begin, end) = get_url(year, i+1)
    url2 += "&start=" + str(start)
    #print url2
    doc = urlopen(url2).read()
    books = json.loads(doc)
    total = books["total"]
    return (books, total)

def get_stat(books, stat):
    ary = books["collections"] 
    for book in ary:
        tag = book["tags"][0]
        #print tag, tag[0:2]==u'娱乐'
        if tag==u'社科-心理学':
            stat["society"] += 1
        elif tag[0:2]==u'艺术' or tag[0:2]==u'摄影' or tag[0:2]==u'社科':
            stat["spirit"] += 1
        else:
            stat["knowledge"] += 1
n = 0
m = 0
year = 2013
stat = {"knowledge":0, "spirit":0, "society":0}
for i in range(3):
    start = 0
    stat = {"knowledge":0, "spirit":0, "society":0}
    while True:
        (books, total) = get_books(year, i+1, start)
        if start==0:
            print year, i+1, total
        if total>0:
            count = min(books["count"], total-books["start"])
            m += count
            get_stat(books, stat)
            #load_books(books, db)
            if(books["count"]+books["start"]<total):
                start += books["count"]
            else:
                break
        else:
            break
    print stat
print "books : ", m

#db.write('c:\\nobackup\\e.xml', 'utf-8')

