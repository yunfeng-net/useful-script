import re
import os
import string

root = 'c:\\nobackup\\'
path = root+'dir-epub'
rd = open(root+'hdshsh.txt')
lines = rd.readlines()
rd.close()

if not os.path.isdir(path):
     os.mkdir(path)
#char = ur'集\u96c6' #+'篇'.decode('gbk')+'章\u7ae0'.decode('gbk')
def split_lines(lines):
    index = 0
    start = 0
    finish = len(lines)
    if start>=finish:
        return
    (i,j) = (0, start)
    while j<len(lines):
##        if re.findall(ur'^[ \u3000\t]*[\u4e00\u4e09\u56db\u4e8c\u516d'+
##                  ur'\u4e03\u4e94\u516b\u4e5d\u96f6\u767e\u5343\u5341]+'+
##                  ur'[ \u3000\t]+', lines[j].decode('utf')):
##            lines[j] = "<h2>"+lines[j]+"</h2>"
        if re.findall(ur'^[ \u3000\t]*\u7b2c[0-9]+', lines[j].decode('utf')):
            if re.findall(ur'\u7ae0[\r\n]*$', lines[j].decode('utf')):
                mat = re.findall(ur'([^\uff0c\uff1a\u2026\u3002\uff01]*)[\uff0c\u3002\uff1a\u2026\uff01]+', lines[j+1].decode('utf'))
                if mat:
                    line = re.sub(ur'[\n\r]', '', lines[j].decode('utf'))
                    lines[j] = "<h2>"+line.encode('utf')+mat[0].encode('utf')+"</h2>"
                else:
                    lines[j] = "<h2>"+lines[j]+"</h2>"
            else:
                lines[j] = "<h2>"+lines[j]+"</h2>"
            #print lines[j]
            i += 1
        else:
            lines[j] = "<p>"+lines[j]+"</p>"
        if i>10 or j+1>=len(lines):
               print "page", index
               id = "%03d.html" % (index)
               ww = open(path+'\\'+id, 'w')
               index += 1
               ww.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" \
xmlns:xml="http://www.w3.org/XML/1998/namespace">\
                        <head></head><body><meta http-equiv=\
\"Content-Type\" content=\"text/html; charset=utf-8\" />'.encode("UTF-8"))
               stop = j
               if j+1>=len(lines): # last line
                   stop = j+1
               for k in range(start, j):
                    ww.write(lines[k])                    
               ww.write("</body></html>".encode("UTF-8"))
               ww.close()
               start = j
               i = 1
        j += 1

split_lines(lines)


