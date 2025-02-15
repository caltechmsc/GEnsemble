#!/usr/bin/python

''' This program converst atom label formatting in bgf file to one that SCREAM accepts (prior to SCREAM debugging).'''

import re, sys
import BgfTools, SCREAM_ConversionTools, PyAtom

def Make_SCREAM_compatible_Bgf_usage():
    message = 'This script takes in a bgf file, and converts all atom labels to one that SCREAM rotamer libraries would recognize. \n\nUsage: ' + sys.argv[0] + ' <in_bgf_file> <out_bgf_file>\n\n'
    print message

def Make_SCREAM_compatible_Bgf(input, output, cnv_file):
    (atom_lines, conect_lines) = BgfTools.return_ATOM_and_CONECT_lines(input)
    
    SCREAM_CNV = SCREAM_ConversionTools.SCREAM_ConversionInfo(cnv_file)
    converted_atom_lines = []
    for l in atom_lines:
        new_line = SCREAM_CNV.bgf_line_conversion(l)
        if BgfTools.get_keyw(new_line) == 'HETATM' and BgfTools.get_atom_label(new_line).strip().lower() in PyAtom.ions:
            new_line = new_line[0:23] + ' ' + new_line[24:]
        converted_atom_lines.append(new_line)
    OUTPUT = open(output, 'w')
    BgfTools.reproduce_all_but_atom_lines(input, converted_atom_lines, OUTPUT)
    OUTPUT.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 1:
        Make_SCREAM_compatible_Bgf_usage()
        sys.exit(2)
    else:
        in_file = args[0]
        out_file = args[1]
        default_cnv_file = '/ul/victor/ForceFieldFiles/SCREAM.cnv'
        
        Make_SCREAM_compatible_Bgf(in_file, out_file, default_cnv_file)

        

