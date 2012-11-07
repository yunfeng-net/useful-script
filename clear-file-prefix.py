# -*- coding: utf-8 -*-
import os
import re
from pprint import pprint
p = re.compile('.*pdf$', re.IGNORECASE) # the suffix here
prefix = 'Hall.'; # modify the prefix here
width = len(prefix)

def rename_files(root):
  for root, dirs, files in os.walk(root):
      os.chdir(root)
      for file in files:
        if p.match(file):
          idx = file.find(prefix)
          if idx>=0:
            print file[idx+width:]
            try:
              os.rename(file, file[idx+width:])
            except:
              print "error", file
rename_files('C:\\nobackup\\My Ref\\math') # directory here


