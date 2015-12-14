# -*- coding: utf-8 -*-
import os,time,stat

def group_files(root):
  for root, dirs, files in os.walk(root):
      os.chdir(root)
      print(root)
      for file in files:
          ft = os.stat(file)
          dt = time.strftime("%Y-%m-%d",time.localtime(ft[stat.ST_MTIME]))
          try:
              os.mkdir(root+os.sep+dt);
          except FileExistsError:
              pass
          try:
              os.symlink(root+os.sep+file, root+os.sep+dt+os.sep+file)
          except FileExistsError:
              pass
          print(file, dt)
      return    # only one directory
              
group_files('C:\\nobackup\\51') # directory here
