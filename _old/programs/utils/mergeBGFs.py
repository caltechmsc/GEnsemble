#!/exec/python/python-2.4.2/bin/python
"""
mergeBGFs.py
Aug 26 2007 -(c)- caglar tanrikulu 

Merges a series of BGF files into a single BGF file.

(see printHelp() for usage info)

 070826 # quick version
 080123 # full version
        # reads the centralized versions of caglar's modules
        
"""

import os, sys, re
from getopt import gnu_getopt

modulePath = os.path.dirname(sys.argv[0])+'/.'+os.path.basename(sys.argv[0])+'_modules'
sys.path.append(modulePath)

import BGF
import cutils as cu


#
# - program information
#

version = '080123p'

def printHeader(version):
    """ prints header """
    cu.printHeader('mergeBGFs.py','Aug 26 2007',version)
    
def printHelp():
    """ print usage info and exit """
    # print header
    printHeader(version)
    
    # print help
    print '''
   Reads a series of BGF files, and merges them into a single
     BGF file in the order they are entered
   
 contact:  
   caglar@its.caltech.edu

 options and [defaults]:
   -o <merged-bgf-file>
      : sets the filename the merged BGF file will be written to
      : *** use of this option is mandatory ***
   -s, --silent
      : do not print any output
      
 usage:
   %s  <bgf-files...> -o <merged-bgf-file>
''' % sys.argv[0]

    # exit
    sys.exit()


# --------------------
#
# - Main program body:
#

def mergeBGFs(bgfFiles, outbgf, silent=0):
    """ Merges all the BGF files listed in 'bgfFiles' and writes them out to 'outbgf' """
    # start-up:
    if not silent:
        printHeader(version)

    if not silent:
        print " ... reading:    %s" % bgfFiles[0]
    mergedBGF = BGF.BgfFile(bgfFiles[0])
    
    for mybgffile in bgfFiles[1:]:
        if not silent:
            print " ... reading:    %s" % mybgffile
        mergedBGF += BGF.BgfFile(mybgffile)
        
    if not silent:
        print " ... writing merged BGF file:    %s" % outbgf
    mergedBGF.saveBGF(outbgf)

    # done
    if not silent:
        print " ... done!"
        print


# --------------------
#
# - Execute Program
#
if __name__ == '__main__':

    # set defaults
    silent = 0
    outbgf = ''
    
    # check for input:
    opts, argv = gnu_getopt(sys.argv[1:], 'o:sh')
    
    # if no input, print help and exit
    if len(argv) < 2:
        printHelp()

    # read options
    for opt, arg in opts:
        if opt == '-s':                 # -s: don't print any output 
            silent = 1
        elif opt == '-o':               # -o: output bgf filename
            outbgf = arg
            
        elif opt == '-h':               # -h: print help
            printHelp()
            
    if not outbgf:
        cu.die("No output file name specified. Please use '-o <merged-bgf-file>'")

    # read argv:
    bgfFiles = argv

    # execute:
    mergeBGFs(bgfFiles, outbgf, silent)
    
    # exit
    sys.exit(0)

