import re
import os
import string

root = 'c:\\nobackup\\'
path = root+'dir-4'
rd = open(root+'4.txt')
lines = rd.readlines()
rd.close()

if not os.path.isdir(path):
     os.mkdir(path)

def split_lines(lines):
     index = 0
     start = 0
     finish = len(lines)
     if start>=finish:
          return
     (i,j) = (0, start)
     while j<len(lines):
          if string.find(lines[j], "----")>=0:
               lines[j] = "</p>"+lines[j]+"<p>"
               i += 1
          j += 1
          if i>30 or j>=len(lines):
               print "page", index
               id = "%03d.html" % (index)
               ww = open(path+'\\'+id, 'w')
               index += 1
               ww.write("<html><head></head><body><meta http-equiv=\
\"Content-Type\" content=\"text/html; charset=utf-8\" /><p>".encode("UTF-8"))
               for k in range(start, j):
                    ww.write(lines[k])                    
               ww.write("</p></body></html>".encode("UTF-8"))
               ww.close()
               start = j
               i = 0

split_lines(lines)

