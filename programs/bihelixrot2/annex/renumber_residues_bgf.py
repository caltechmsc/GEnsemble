import os,sys,string,math

def print_help():
   print '\nHelp notes for renumber_residue_bgf.py:\n'
   print 'Syntax: python renumber_residue_bgf.py input.bgf output.bgf\n'
   print 'input.bgf is read in and residue numbers are reset'
   print 'to #1 starting with the first residue.  output.bgf is' 
   print 'created.  This has been used to renumber minimized .bgf'
   print 'files that do not start with residue #1 before conversion'
   print 'to .mol2 (using bgf2mol2_protein.py).  The program GRID'
   print 'will not accept protein substructures that do not have'
   print 'continuous residue numbers starting from 1.\n'
   sys.exit()
   
args = sys.argv[1:]

if len(args) != 2: print_help()

input_file = args[0]
output_file = args[1]

f = open(input_file,'r')
L = f.readlines()
f.close()

count = 0

while string.find(L[count],'ATOM') != 0 and string.find(L[count],'HETATM') != 0:
   count = count + 1
   
has_chain = 0
if L[count][23] != ' ': has_chain = 1

cur_resno = 1
line = string.split(L[count])
cur_resname = line[4 + has_chain]

while string.find(L[count],'FORMAT') != 0:
   line = string.split(L[count])
   
   if line[4 + has_chain] != cur_resname: 
      cur_resno = cur_resno + 1
      cur_resname = line[4 + has_chain]
      
   start = L[count][0:26]
   end = L[count][29:]
   newres = '%3d' % cur_resno
   L[count] = start + newres + end
   
   count = count + 1

f = open(output_file,'w')
f.writelines(L)
f.close()
