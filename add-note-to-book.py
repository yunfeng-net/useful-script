# -*- coding: utf-8 -*-
import os
import re
from urllib import urlopen  
from pprint import pprint
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring
from xml.etree.ElementTree import parse
import cgi

def add_note(note, book_file):
    url = note.find('annotation/url')
    t = find_book_by_note(url.text)
    for book in book_file:
        for child in book.getchildren():
            if child.tag=='link'>0 and t==child.text:
                print child.text
                ele = Element('note')
                ele.text = cgi.escape(note.find('annotation/content').text)
                book.append(ele)

url = "http://book.douban.com/annotation/22115997/"
prefix = "href=\"http://book.douban.com/subject/"
def find_book_by_note(url):
    doc = urlopen(url).read()
    n = doc.find(prefix)
    if n<0:
        return None
    m = doc.find('/',n+len(prefix))
    s = doc[n+6:m+1]
    return s

note_name = 'c:\\nobackup\\philip.xml' # input the note file name
book_name = 'c:\\nobackup\\book2.xml' # input the book file name
notes = parse(note_name)
db = parse(book_name)
note = notes.findall('book')
for page in note:
    add_note(page, db.findall('book'))
db.write('c:\\nobackup\\db.xml', 'utf-8')
print "finished"
#print find_book_by_note(url)
