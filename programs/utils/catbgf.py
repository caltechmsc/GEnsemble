#!/usr/bin/env python
import os,sys,string,math

def print_help():
   print '\nUser help for catbgf.py:'
   print 'Syntax: python catbgf.py file1.bgf file2.bgf merged.bgf'
   print 'file2 is catenated to the end of file1 and all of the atom'
   print 'numbers and connectivities are updated.'
   print 'The resulting file is written out to merged.bgf'
   print 'You can use any names you like for file1, file2, & merged.'
   sys.exit()
   
   
def catbgf(f1, f2, outfile):
   f = open(f1,'r')
   L = f.readlines()
   f.close()
   
   f = open(f2,'r')
   M = f.readlines()
   f.close()
  
   complex = []
   
   cL = 0    # line counter for L
   cM = 0    # line counter for M
   
   while string.find(L[cL],'ATOM') != 0 and string.find(L[cL],'HETATM') != 0:
      complex.append(L[cL])
      cL = cL + 1
   
   while string.find(L[cL],'ATOM') == 0 or string.find(L[cL],'HETATM') == 0:
      complex.append(L[cL])
      cL = cL + 1

   while string.find(M[cM],'ATOM') != 0 and string.find(M[cM],'HETATM') != 0:      
      cM = cM + 1
      
   atom_map = {}
   
   tmp = L[cL - 1][:]
   tmp = string.split(tmp)
   next_atom = string.atoi(tmp[1]) + 1  
   
   while string.find(M[cM],'ATOM') == 0 or string.find(M[cM],'HETATM') == 0:
      tmp = M[cM][:]
      tmp = string.split(tmp)
      atom_map[ tmp[1] ] = next_atom
      
      atom_chunk = '%5d' % next_atom
      M[cM] = M[cM][0:7] + atom_chunk + M[cM][12:]
      complex.append(M[cM])
      
      cM = cM + 1
      next_atom = next_atom + 1
      
   while string.find(L[cL],'END') != 0:
      complex.append(L[cL])
      cL = cL + 1
      
   while string.find(M[cM],'CONECT') != 0:
      cM = cM + 1
      
   while string.find(M[cM],'END') != 0:
      if string.find(M[cM],'CONECT') != 0:
         if string.find(M[cM],'ORDER') == 0:
            base = 'ORDER '
            tmp = M[cM][:]
            tmp = string.split(tmp)
            chunk = '%6d' % atom_map[ tmp[1] ]
            line = base + chunk + M[cM][12:]
            M[cM] = line
         complex.append(M[cM])
         cM = cM + 1
         continue
         
      tmp = M[cM][:]
      tmp = string.split(tmp)
      
      n = len(tmp)
      base = 'CONECT '
      
      for ii in range(n):
         if ii == 0: continue
         
         chunk = '%5d' % atom_map[ tmp[ii] ]
         base = base + chunk
         
      base = base + '\n'
      M[cM] = base
      complex.append(M[cM])
      
      cM = cM + 1
      
   complex.append('END\n')
   
   f = open(outfile,'w')
   f.writelines(complex)
   f.close()

# main starts here

args = sys.argv[1:]

if len(args) != 3: print_help()

file1 = args[0]
file2 = args[1]
output = args[2]

catbgf(file1,file2,output)


