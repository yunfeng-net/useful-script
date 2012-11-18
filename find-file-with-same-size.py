# -*- coding: utf-8 -*-
import os
import re
from pprint import pprint
from os.path import join, getsize

p = re.compile('.*pdf$', re.IGNORECASE) # the suffix here
prefix = 'Hall.'; # modify the prefix here
width = len(prefix)
dic = {}
def rename_files(root):
  for root, dirs, files in os.walk(root):
      os.chdir(root)
      for file in files:
        if p.match(file):
          name = join(root, file)
          try:
            size = getsize(name)
          except:
            print "fail to open ", name
          if size not in dic:
            dic[size] = (root, file)
          else:
            if dic[size][1]==file:
              print 'duplicated file : ', file
              p2 = root
              path = dic[size][0]
              if len(path)>len(root):
                p2 = path
                path = root
              os.remove(join(path, file))
              #print 'remove %s keep %s' %(path, p2)
            else:
              print 'conflict %s with %s' % (name, join(dic[size][0],dic[size][1]))
print 'finished'
rename_files('C:\\nobackup\\My Ref') # directory here


