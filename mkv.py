#!/usr/bin/env python
import multiprocessing
import time,os,sys
 

def func(msg):
    os.system(msg)
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=2)
    i = 1
    while i<len(sys.argv):
        print "task : %s" % sys.argv[i]
        pool.apply_async(func, (sys.argv[i], ))
        i += 1
    pool.close()
    pool.join()
