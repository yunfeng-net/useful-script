import re

file_object = open('c:\\nobackup\\4.txt')
ww = open('c:\\nobackup\\3.txt', 'w')

for line in file_object:
     if len(re.findall(u'F\xb7A\xb7\u54c8\u8036\u514b \u300a\u81f4\u547d\u7684\u81ea\u8d1f\u300b', line.decode('utf')))==0:
         ww.write(line)

file_object.close( )
ww.close()
