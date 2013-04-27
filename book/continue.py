import re

file_object = open('c:\\nobackup\\2.txt')
ww = open('c:\\nobackup\\3.txt', 'w')
text = file_object.read()
text = re.sub(ur'([^\u3002])\n([^ \n])', ur'\1\2', text.decode('utf'))
ww.write(text.encode('utf-8'))

file_object.close( )
ww.close()
