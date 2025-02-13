#!/usr/bin/python



import re
import PyResidue, PyAtom

atom_area_start_pat = re.compile(r'Breakdown of Area/Volume/Cavity results by atom')
atom_area_end_pat = re.compile(r'Maximum number of neighbors')



def get_atom_area(atom_area_filename):
    '''
    Input: FSM output file.  I.e. the output that has atom area information in it.
    Output: returns a list of PyAtoms that contains atom area info.
    Dcrptn: Gets all area of atoms and puts them into a list of PyAtoms.
    '''

    fh = open(atom_area_filename)
    
    lines = fh.readlines()
    PyAtom_list = []
    
    atom_area_flag = 0
    for line in lines:
        l = line.strip()
        if l == '':
            continue
        if atom_area_start_pat.search(l):
            atom_area_flag = 1
            continue
        if atom_area_end_pat.search(l):
            atom_area_flag = 0
            break
        if atom_area_flag:
            atom = PyAtom.PyAtom()
            atom.fsm_atom_area_line_populate(l)
            PyAtom_list.append(atom)

    return PyAtom_list



def residue_area(atom_area_list, bgf_atom_list):
    '''
    Input:
    Output: texts with residue area.
    Dcrptn: 
    '''
    assert(len(atom_area_list) == len(bgf_atom_list))
    PyAtom.copy_pyatom_lists_bgf_attributes(atom_area_list, bgf_atom_list)

    residue_list = PyResidue.make_PyResidue_list_with_fsm_area(atom_area_list)
    text_lines = []

    for res in residue_list:
        text = '%3s %5d %1s : %10.5f' % (res.res_name, res.res_pstn, res.chain_name, res.surface_area)
        text_lines.append(text)

    return text_lines

def return_residue_list_with_area_info(atom_area_list, bgf_atom_list):

#     print "atom_area_list"
#     for a in atom_area_list:
#         print a.return_bgf_line()
#     print "bgf_atom_list"
#     for a in bgf_atom_list:
#         print a.return_bgf_line()
    
    assert(len(atom_area_list) == len(bgf_atom_list))
    PyAtom.copy_pyatom_lists_bgf_attributes(atom_area_list, bgf_atom_list)

    residue_list = PyResidue.make_PyResidue_list_with_fsm_area(atom_area_list)
    return residue_list
