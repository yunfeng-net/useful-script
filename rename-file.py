# -*- coding: utf-8 -*-
import os
import re
from pprint import pprint
p = re.compile('.*jpg$', re.IGNORECASE) # the suffix here
prefix = 'Hall.'; # modify the prefix here
width = len(prefix)

def rename_files(root):
  for root, dirs, files in os.walk(root):
      os.chdir(root)
      for file in files:
        if p.match(file):
          print file[9:]
#          idx = file.find(prefix)
#          if idx>=0:
#            print file[idx+width:]
          try:
              os.rename(file, file[9:])
          except:
              print "error", file
rename_files('C:\\nobackup\\book\\Bression') # directory here


