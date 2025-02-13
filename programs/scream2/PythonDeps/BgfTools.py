#!/usr/bin/python

'''This module includes tools to manipulate BGF files.'''

import re, sys, os, shutil
import math
import PyAtom

BIOGRF_pat = re.compile(r'BIOGRF')
DESCRP_pat = re.compile(r'^DESCRP')
REMARK_pat = re.compile(r'^REMARK')
ATOM_pat = re.compile(r'^ATOM')
HETATM_pat = re.compile(r'^HETATM')
CONECT_pat = re.compile(r'^CONECT')
TER_pat = re.compile(r'^TER')
END_pat = re.compile(r'^END')

AminoAcids = {'A':'ALA', 'C':'CYS', 'D':'ASP', 'E':'GLU', 'F':'PHE', 'G':'GLY', 'H':'HIS', 'I':'ILE', 'K':'LYS', 'L':'LEU', 'M':'MET', 'N':'ASN', 'P':'PRO', 'Q':'GLN', 'R':'ARG', 'S':'SER', 'T':'THR', 'V':'VAL', 'W':'TRP', 'Y':'TYR', 'CYX':'CYX', 'HSE':'HSE', 'HSD':'HSD', 'HSP':'HSP'}

AminoAcids_321 = {'ALA': 'A', 'CYS' : 'C', 'ASP': 'D', 'GLU':'E', 'PHE':'F', 'GLY':'G', 'HIS':'H', 'ILE':'I', 'LYS':'K', 'LEU':'L', 'MET':'M','ASN':'N', 'PRO':'P', 'GLN':'Q','ARG':'R', 'SER':'S', 'THR':'T', 'VAL':'V','TRP':'W', 'TYR':'Y'}
                  

def make_PyAtom_list_from_bgf_file(bgf_file):
    (ATOM_lines, CONECT_lines) = return_ATOM_and_CONECT_lines(bgf_file)
    PyAtom_list = make_PyAtom_list(ATOM_lines)
    
    conect_PyAtom_list(CONECT_lines, PyAtom_list)
    
    return PyAtom_list

def make_PyAtom_list(bgf_lines):
    '''Returns a list of PyAtoms from bgf lines.'''
    py_atom_list = []
    for line in bgf_lines:
        py_atom = PyAtom.PyAtom()
        py_atom.bgf_line_populate(line)
        py_atom_list.append(py_atom)
    return py_atom_list

def conect_PyAtom_list(CONECT_lines, PyAtom_list):
    CONECT_hash = {}
    for l in CONECT_lines:
        lf = l.split()
        base_atom = int(lf[1])
        CONECT_hash[base_atom] = l

    for atom in PyAtom_list:
        CONECT_line = ''
        try:
            CONECT_line = CONECT_hash[atom.atom_n]
        except KeyError, e:
            print >>sys.stderr, 'Warning: atom %d has no CONECT info.' % atom.atom_n
            continue
        atom.bgf_CONECT_populate(CONECT_line)

#     CONECT_line_c = 0
#     for atom in PyAtom_list:
#         CONECT_n = atom.bgf_CONECT_populate(CONECT_lines[CONECT_line_c])
#         while CONECT_n < 2:
#             if CONECT_n == -1: # self.atom_n < base atom in CONECT_line
#                 atom.bonds = []
#                 break              # atom list needs to catch up
#             if CONECT_n == 1: # self.atom_n > base atom in CONECT_line
#                 CONECT_line_c += 1 # CONECT_line needs to catch up
#                 try:
#                     CONECT_n = atom.bgf_CONECT_populate(CONECT_lines[CONECT_line_c])
#                 except IndexError, e:
#                     print 'Warning: '
#                     print e
#                     break
#             if CONECT_line_c == len(CONECT_lines) -1:
#                 break

def bgf_coord_lines_from_PyAtom_list(PyAtom_list, FixedFlag = 0):
    '''Returns a list of bgf-formatted atom lines.  if FixedFlag == 1, also prints MPSim style Fixed/Moveable line.'''
    bgf_coord_lines = []
    for atom in PyAtom_list:
        #print atom.atom_n
        bgf_coord_line = ''
        if FixedFlag == 0:
            bgf_coord_line = atom.return_bgf_line()
        if FixedFlag == 1:
            bgf_coord_line = atom.return_bgf_line_with_fixed()
        bgf_coord_line += '\n'
        bgf_coord_lines.append(bgf_coord_line)
    return bgf_coord_lines


def bgf_coord_lines_with_fixed_from_PyAtom_list(PyAtom_list):
    '''Returns a list of bgf-formatted atom lines.'''
    bgf_coord_lines = []
    for atom in PyAtom_list:
        #print atom.atom_n
        bgf_coord_line = atom.return_bgf_line_with_fixed()
        bgf_coord_line += '\n'
        bgf_coord_lines.append(bgf_coord_line)
    return bgf_coord_lines


def bgf_connectivity_lines_from_PyAtom_list(PyAtom_list):
    '''Returns a list of bgf-formatted connectivity lines.'''
    bgf_conn_lines = []
    for atom in PyAtom_list:
        bgf_conn_line = atom.return_bgf_conn_line()
        if bgf_conn_line != '':
            bgf_conn_line += '\n'
            bgf_conn_lines.append(bgf_conn_line)
    return bgf_conn_lines

def distance(atom_line1, atom_line2):
    '''Calculates the distance between two atoms.  Takes two bgf format lines as input.'''
    a1 = atom_line1
    a2 = atom_line2
    
    x1 = get_x_coord(a1)
    y1 = get_y_coord(a1)
    z1 = get_z_coord(a1)

    x2 = get_x_coord(a2)
    y2 = get_y_coord(a2)
    z2 = get_z_coord(a2)

    dist = math.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
    return dist


def translate_atom(atom_line, x_shift, y_shift, z_shift):
    '''Returns an atom_line with x, y and z coordinates shifted.'''
    x = get_x_coord(atom_line) + float(x_shift)
    y = get_y_coord(atom_line) + float(y_shift)
    z = get_z_coord(atom_line) + float(z_shift)

    x_fm = '%10.5f' % x
    y_fm = '%10.5f' % y
    z_fm = '%10.5f' % z

    translated_line = atom_line[0:30] + x_fm + y_fm + z_fm + atom_line[60:]
    return translated_line

def translate_atom_lines(atom_lines, x_shift, y_shift, z_shift):
    '''Return a list of atom lines with x, y z coordinates shifted.'''
    new_lines = []
    for l in atom_lines:
        new_line = translate_atom(l, x_shift, y_shift, z_shift)
        new_lines.append(new_line)
    return new_lines

def return_residues(atom_lines):
    '''Takes in a list of atom lines and splits them into a list of residues.  Each residue is represented by its atom lines.'''
    previous_line = ''
    current_line = ''

    residue_lines = []
    residue_list = []
    
    for line in atom_lines:
        previous_line = current_line
        current_line = line
        
        if is_new_residue(current_line, previous_line):
            if len(residue_lines) != 0:
                residue_list.append(residue_lines)
                residue_lines = []
                residue_lines.append(current_line)
                continue
                
            elif len(residue_lines) == 0:  # start condition
                residue_lines.append(line)
                continue
        else:  # not a new residue; middle of residue
            residue_lines.append(current_line)
            continue
    
    # end condition
    residue_list.append(residue_lines)

    return residue_list

def fix_residue_atom_ordering(residue_lines):
    '''Fixes atom ordering in residues for mutate.pl relates scripts.  I.e. N, HN, CA, HCA, C, O, then sidechain.  Returns a list of PyAtoms, so that the mapping can still be traced.'''


    # First, instantiate a bunch of PyAtoms.
    PyAtom_List = make_PyAtom_list(residue_lines)

    # If not amino acid, don't fix.

    AA_3letter = AminoAcids.values()
    residue_name = get_res_name(residue_lines[0])
    if not residue_name in AA_3letter:
        return PyAtom_List

    # Secondly, separate the BackBone, SideChain and Term Oxygen portions.
    BackBone_PyAtom_list = []
    SideChain_PyAtom_list = []
    TermOxygen_PyAtom_list = []

    for atom in PyAtom_List:
        if atom.is_BackBoneAtom():
            BackBone_PyAtom_list.append(atom)
        elif atom.is_SideChainAtom():
            SideChain_PyAtom_list.append(atom)
        elif atom.is_TermOxygenAtom():
            TermOxygen_PyAtom_list.append(atom)  # should have a max of 1 element.
    

    # Thirdly, put them in the right order.  Only BackBone atoms need to be done, sidechain atoms ASSUMED to be in right order.  Currently doing this manually.  Is there a better way?
    # Ahh!  Indeed.  Use a comparison function.  Perhaps tricky, but it's smart.
    # Below: Nested function.
    def _backbone_atom_order_cmp(py_atom1, py_atom2):
        atom_order = ['N', 'HN', 'HT1', 'HT2', 'HT3', 'CA', 'HCA', 'HA', 'HA1', 'HA2', 'C', 'O']
        label1 = py_atom1.atom_label.strip()
        label2 = py_atom2.atom_label.strip()
        label1_index = atom_order.index(label1)
        label2_index = atom_order.index(label2)

        if label1_index < label2_index:
            return int(-1)
        elif label1_index == label2_index:
            return int(0)
        else:
            return int(1)


    BackBone_PyAtom_list.sort(_backbone_atom_order_cmp)

    # Done!

    final_output_atoms = []
    final_output_atoms.extend(BackBone_PyAtom_list)
    final_output_atoms.extend(SideChain_PyAtom_list)
    final_output_atoms.extend(TermOxygen_PyAtom_list)

    return final_output_atoms


def calc_min_dist_between_residues(residue_lines1, residue_lines2):
    r1 = residue_lines1
    r2 = residue_lines2

    min_dist = 999999

    for a1 in r1:
        for a2 in r2:
            dist = distance(a1, a2)
            if dist < min_dist:
                min_dist = dist
    return min_dist

def calc_min_dist_between_residues_wo_H(residue_lines1, residue_lines2):
    r1 = residue_lines1
    r2 = residue_lines2

    min_dist = 999999

    for a1 in r1:
        if is_Hydrogen(a1):
            continue
        for a2 in r2:
            if is_Hydrogen(a2):
                continue
            
            dist = distance(a1, a2)
            if dist < min_dist:
                min_dist = dist
    return min_dist

def calc_min_distance_between_atom_residue(atom_line, residue_lines1):
    r1 = residue_lines1
    min_dist = 999999

    for a in r1:
        dist = distance(atom_line, a)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def calc_min_distance_between_atom_residue_wo_H(atom_line, residue_lines1):
    r1 = residue_lines1
    min_dist = 999999

    for a in r1:
        if is_Hydrogen(a):
            continue
        dist = distance(atom_line, a)
        if dist < min_dist:
            min_dist = dist
            
    return min_dist


    
def is_new_residue(current_line, previous_line):
    if previous_line == '':
        return 1

    current_res_pstn = get_res_pstn(current_line)
    previous_res_pstn = get_res_pstn(previous_line)

    current_chain = get_chain_name(current_line)
    previous_chain = get_chain_name(previous_line)

    if current_res_pstn != previous_res_pstn or current_chain != previous_chain:
        return 1

def collapse_atoms(atom_list, shift_n = 1):
    '''collapses atom numbering to begin at number 1.  makes changes in place.'''
    atom_mapping = {}
    for i in range(0,len(atom_list)):
        atom_n = atom_list[i].atom_n
        atom_mapping[atom_n] = i + shift_n
    # Collapse atoms.
    for a in atom_list:
        a.atom_n = atom_mapping[a.atom_n]
        for i in range(0,len(a.bonds)):
            a.bonds[i] = atom_mapping[a.bonds[i]]

def collapse(atom_lines, conect_lines):
    '''collapse(atoms_lines, conect_lines): collapses atom numbering to begin at number 1.'''
    atom_mapping = {}
    new_atom_lines = []
    new_conect_lines = []
    for i in range(1,len(atom_lines)+1):
        atom_n = get_atom_n(atom_lines[i-1])
        atom_mapping[atom_n] = i          # Creates a map from original numbering to collapsed numbering
    # Collapse atom lines
    for atom_line in atom_lines:
        atom_n = get_atom_n(atom_line)
        atom_n_fm = '%6d' % atom_mapping[atom_n]
        new_atom_line = atom_line[0:6] + atom_n_fm + atom_line[12:]
        new_atom_lines.append(new_atom_line)
    # Collapse conect lines
    for conect_line in conect_lines:
        new_conect_line = 'CONECT'
        first_entry_flag = 1
        for entry in conect_line.split():
            if entry == 'CONECT':
                pass
            else:
                try:
                    atom_n = atom_mapping[int(entry)]
                except KeyError, e:
                    print >>sys.stderr, 'Warning: atom number %d appearing in CONECT not appearing in ATOM.  Proceeding.' % int(entry)
                    if first_entry_flag == 1:
                        first_entry_flag = 2 # meaning skip over this CONECT line entry.
                        break
                    else:
                        continue
                atom_n_fm = '%6d' % atom_n
                new_conect_line += atom_n_fm
                first_entry_flag = 0
        
        if first_entry_flag != 2:
            new_conect_line += '\n'
            new_conect_lines.append(new_conect_line)
    
    return (new_atom_lines, new_conect_lines)


def renumber_from_PyAtom_list(atom_list):
    '''This routine renumbers according to the order in which atoms appear in list.  Replacement in-line.'''
    atom_n_map = {}
    for i in range(1, len(atom_list) +1):
        atom_n_map[atom_list[i-1].atom_n] = i
    for a in atom_list:
        a.atom_n = atom_n_map[a.atom_n]
        new_bonds = []
        for n in a.bonds:
            new_bonds.append(atom_n_map[n])
        a.bonds = []
        a.bonds = new_bonds
    

def renumber(bgf_file):
    (atom_lines, conect_lines) = return_ATOM_and_CONECT_lines(bgf_file)
    return renumber_from_lines(atom_lines, conect_lines)


def renumber_from_lines(atom_lines, conect_lines):
    '''This routine renumbers according to the order in which atoms appear in atom lines.'''
    atom_n_map = {}
    for i in range(1, len(atom_lines) +1):
        atom_n_map[get_atom_n(atom_lines[i-1])] = i   # atom_lines start from 0
        
    new_atom_lines = []
    new_conect_lines = []

    # populate new atom lines
    for line in atom_lines:
        atom_n_fm = '%6d' % atom_n_map[get_atom_n(line)]
        new_line = line[0:6] + atom_n_fm + line[12:]
        new_atom_lines.append(new_line)

    # populate new conect lines
    for line in conect_lines:
        new_line = 'CONECT'
        for disordered_atom_n in get_conect_line_atoms(line):
            atom_n_fm = '%6d' % atom_n_map[disordered_atom_n]
            new_line += atom_n_fm
        new_line += '\n'
        new_conect_lines.append(new_line)


    # sort these conect lines for friendlier output
    sorted_conect_lines = new_conect_lines
    sorted_conect_lines.sort(conectLineSort)

    return (new_atom_lines, sorted_conect_lines)

def return_ATOM_lines(bgf_file):
    try:
        file = open(bgf_file)
    except IOError, e:
        print e
        print 'Filename', bgf_file, 'does not exist!'
        sys.exit(2)

    atom_lines = []

    for line in file.readlines():
        if ATOM_pat.search(line) or HETATM_pat.search(line):
            atom_lines.append(line)
            continue
        if CONECT_pat.search(line):
            break

    return atom_lines
    

def return_ATOM_and_CONECT_lines(bgf_file):
    
    try:
        file = open(bgf_file)
    except IOError, e:
        print e
        print 'Filename', bgf_file, 'does not exist!'
        sys.exit(2)

    atom_lines = []
    conect_lines = []

    for line in file.readlines():
        if ATOM_pat.search(line) or HETATM_pat.search(line):
            atom_lines.append(line)
        if CONECT_pat.search(line):
            conect_lines.append(line)
        
    return (atom_lines, conect_lines)


def print_BGF(PyAtom_list, out_fh):
    bgf_header_lines = make_header()
    bgf_coord_lines = bgf_coord_lines_from_PyAtom_list(PyAtom_list)
    bgf_conn_lines = bgf_connectivity_lines_from_PyAtom_list(PyAtom_list)

    print_lines(out_fh, bgf_header_lines)
    print_lines(out_fh, bgf_coord_lines)
    print_conect(out_fh)
    print_lines(out_fh, bgf_conn_lines)
    print_end(out_fh)

def print_MPSIM_BGF(PyAtom_list, out_fh):
    bgf_header_lines = make_header()
    bgf_coord_lines = bgf_coord_lines_from_PyAtom_list(PyAtom_list, 1)
    bgf_conn_lines = bgf_connectivity_lines_from_PyAtom_list(PyAtom_list)

    print_lines(out_fh, bgf_header_lines)
    print_lines(out_fh, bgf_coord_lines)
    print_conect(out_fh)
    print_lines(out_fh, bgf_conn_lines)
    print_end(out_fh)
    

def print_BGF_with_fixed(PyAtom_list, out_fh):
    bgf_header_lines = make_header()
    bgf_coord_lines = bgf_coord_lines_with_fixed_from_PyAtom_list(PyAtom_list)
    bgf_conn_lines = bgf_connectivity_lines_from_PyAtom_list(PyAtom_list)

    print_lines(out_fh, bgf_header_lines)
    print_lines(out_fh, bgf_coord_lines)
    print_conect(out_fh)
    print_lines(out_fh, bgf_conn_lines)
    print_end(out_fh)
    

def make_header():
    '''Make a random header, and return lines.'''

    header_lines = []
    header_lines.append('BIOGRF 332\n')
    header_lines.append('REMARK\n')
    header_lines.append('FORCEFIELD DREIDING\n')
    header_lines.append('FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,i2,i4,f10.5,1x,i3)\n')

    return header_lines
                     

def print_header(fh, bgf_version, *remarks):
    '''print_header(fh, bgf_version, *remarks).  fh: filehandle.  bgf_version: integer.  *remarks: goes into REMARK lines'''
    
    print >>fh, 'BIOGRF', bgf_version
    for remark in remarks:
        print >>fh, 'REMARK', remark
    print >>fh, 'FORCEFIELD DREIDING'
    print >>fh, 'FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,i2,i4,f10.5,1x,i3)'

def reproduce_header(fh, filename):
    '''reproduces header of a bgf file'''
    file = open(filename)
    for line in file.readlines():
        if not (ATOM_pat.search(line) or HETATM_pat.search(line)):
            print >>fh, line,
        if (ATOM_pat.search(line) or HETATM_pat.search(line)):
            break
    
def reproduce_all_but_atom_lines(bgf_file, atom_lines, OUTPUT):
    try:
        BGF_FILE = open(bgf_file)
    except IOError, e:
        print e
        print 'Can\'t open bgf_file!'
        sys.exit(2)
    bgf_lines = BGF_FILE.readlines()
    BGF_FILE.close()

    printed_flag = 0

    for line in bgf_lines:
        if not (ATOM_pat.search(line) or HETATM_pat.search(line)):
            print >>OUTPUT, line,
        elif printed_flag == 0:
            printed_flag = 1
            for l in atom_lines:
                print >>OUTPUT, l,

def reproduce_all_but_atom_and_conect_lines(bgf_file, atom_lines, conect_lines, OUTPUT):
    try:
        BGF_FILE = open(bgf_file)
    except IOError, e:
        print e
        print 'Can\'t open bgf_file!'
        sys.exit(2)
    bgf_lines = BGF_FILE.readlines()
    BGF_FILE.close()

    atom_line_printed_flag = 0
    conect_line_printed_flag = 0

    for line in bgf_lines:
        if not ( ATOM_pat.search(line) or HETATM_pat.search(line) or TER_pat.search(line) or END_pat.search(line) or CONECT_pat.search(line) ):
            print >>OUTPUT, line,
        elif ( ATOM_pat.search(line) or HETATM_pat.search(line) or TER_pat.search(line))  and atom_line_printed_flag == 0:
            atom_line_printed_flag = 1
            for l in atom_lines:
                print >>OUTPUT, l,
        elif CONECT_pat.search(line) and conect_line_printed_flag == 0:
            conect_line_printed_flag = 1
            for l in conect_lines:
                print >>OUTPUT, l,
        elif END_pat.search(line) and conect_line_printed_flag == 0:
            conect_line_printed_flag = 1
            for l in conect_lines:
                print >>OUTPUT, l,
            #print >>OUTPUT, line,
        elif END_pat.search(line) and conect_line_printed_flag == 1:
            print >>OUTPUT, line,
            
    if len(bgf_lines) == 0: # i.e. empty file
        print >>OUTPUT, 'BIOGRF 321'
        print >>OUTPUT, 'FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,f10.5)'
        for l in atom_lines:
            print >>OUTPUT, l,
        print >>OUTPUT, 'FORMAT CONECT (a6,14i6)'
        print >>OUTPUT, 'FORMAT ORDER (a6,i6,13f6.3)'
        for l in conect_lines:
            print >>OUTPUT, l,
        print >>OUTPUT, 'END'

def make_conect_lines():
    conect_lines = []
    conect_lines.append('FORMAT CONECT (a6,14i6)\n')
    conect_lines.append('FORMAT ORDER (a6,i6,13f6.3)\n')

    return conect_lines
                        

def print_conect(fh):
    print >>fh, 'FORMAT CONECT (a6,14i6)'
    print >>fh, 'FORMAT ORDER (a6,i6,13f6.3)'

def make_end_line():
    end_line = ['END\n']
    return end_line

    
def print_end(fh):
    print >>fh, 'END'
    if fh != sys.stdout:
        fh.close()

def print_conect_line(fh,*args):
    conect_line = 'CONECT'
    for atom_n in args:
        token = '%6d'
        print atom_n
        token %= atom_n
        conect_line += token
    print >>fh, conect_line

def print_lines(fh, lines):
    for line in lines:
        print >>fh, line,
    pass

def make_conect_line(args):
    conect_line = 'CONECT'
    for atom_n in args:
        atom_n = int(atom_n)
        token = '%6d'
        token %= atom_n
        conect_line += token
    return conect_line


def get_conect_line_atoms(conect_line):
    '''This function returns a list of atoms that is contained in a conect line bgf format.'''
    atom_list = []
    line = conect_line.strip()

    index = 6
    while index < len(line):
        start_i = index
        end_i = index+6
        atom_n = int(conect_line[start_i:end_i])
        atom_list.append(atom_n)
        index += 6
    return atom_list
                     

def get_keyw(atom_line):
    return atom_line[0:6]

def get_atom_n(atom_line):
    return int(atom_line[6:12])
    
def get_atom_label(atom_line):
    return atom_line[13:17]

def get_res_name(atom_line):
    return atom_line[19:22]

def get_chain_name(atom_line):
    return atom_line[23:24]

def get_res_pstn(atom_line):
    return int(atom_line[25:29])

def get_x_coord(atom_line):
    return float(atom_line[30:40])

def get_y_coord(atom_line):
    return float(atom_line[40:50])

def get_z_coord(atom_line):
    return float(atom_line[50:60])

def get_ff_type(atom_line):
    return atom_line[61:66]

def get_hybridization(atom_line):
    return int(atom_line[68:69])

def get_lone_pairs(atom_line):
    return int(atom_line[70:71])

def get_charge(atom_line):
    return float(atom_line[72:80])

def get_fixed_flag(atom_line):
    if len(line) > 80:
        return int(atom_line[81:82])
    else:
        print 'Line not BGF 400 format.'

def get_base_atom(conect_line):
    return int(conect_line[6:12])

def get_atom(atom_lines, atom_n):
    '''Takes in atom lines and returns the line with atom number atom_n (argument).'''
    atom_line = ''
    for l in atom_lines:
        if get_atom_n(l) == atom_n:
            atom_line = l
            break
    if atom_line == '':
        print 'Atom', atom_n, 'not found!'
        return 0
    return atom_line
    

def get_residue(atom_lines, residue_info):
    '''Takes in a list of atom_lines, a residue_info (like C123_X) and returns atom lines that correspond to the residue that matches the info.'''
    residue_list = return_residues(atom_lines)
    chain_name = residue_info[-1]
    res_PSTN_pat = re.compile(r'(\d+)_')
    residue_pstn = int(res_PSTN_pat.search(residue_info).group(1))

    residue_wanted = []

    for r in residue_list:
        first_line = r[0]
        r_pstn = get_res_pstn(first_line)
        r_chain = get_chain_name(first_line)

        if r_pstn == residue_pstn and r_chain == chain_name:
            residue_wanted = r
            break

    if len(residue_wanted) == 0:
        print 'Residue', residue_info, 'not found!'
        return 0
    else:
        return residue_wanted

def is_Hydrogen(atom_line):
    atom_label = get_atom_label(atom_line)
    atom_label = fix_atom_label(atom_label)

    if atom_label[0] == 'H':
        return 1
    else:
        return 0


def is_BackBoneAtom(atom_line):
    '''The atom lines passed in need to be verified to be part of a peptide.  Else unpredictable results.'''
    BackBoneAtomList = ['N', 'HN', 'CA', 'HCA', 'C', 'O', 'HT1', 'HT2', 'HT3', 'HA', 'HA1', 'HA2']
    atom_label = get_atom_label(atom_line)
    if atom_label in BackBoneAtomList:
        return True
    else:
        return False


def is_SideChainAtom(atom_line):
    if is_BackBoneAtom(atom_line) or is_TermOxygenAtom(atom_line):
        return False
    else:
        return True

def is_TermOxygenAtom(atom_line):
    TermOxygenAtomList = ['OXT', 'OT1', 'OT2']
    atom_label = get_atom_label(atom_line)
    if atom_label in TermOxygenAtomList:
        return True
    else:
        return False

def fix_atom_label(atom_label):
    stripped_label = atom_label.strip()
    
    if stripped_label[0:1] == 'H':
        new_label = '%-4.4s'
        return new_label % stripped_label
    else:
        new_label = ' %-3.3s'
        return new_label %stripped_label

def fix_ff_type(ff_type):
    stripped_ff_type = ff_type.strip()

    new_ff_type = '%-5.5s'
    return new_ff_type % stripped_ff_type

def change_atom_n(line, atom_n):
    atom_n_fm = '%6d' % atom_n
    return line[0:6] + atom_n_fm + line[12:]

def change_charge(line, charge):
    new_charge = '%8.5f' % charge
    return line[0:72] + new_charge + line[80:]

def change_res_pstn(line, res_pstn):
    atom_res_pstn_fm = '%4d' % res_pstn
    return line[0:25] + atom_res_pstn_fm + line[29:]

def change_chain_name(line, chain_name):
    new_chain = '%1s' % chain_name.strip()
    return line[0:23] + new_chain + line[24:]

def conectLineSort(conect_line1, conect_line2):
    line1_baseAtom_n = get_conect_line_atoms(conect_line1)[0]
    line2_baseAtom_n = get_conect_line_atoms(conect_line2)[0]

    if line1_baseAtom_n < line2_baseAtom_n:
        return -1
    elif line1_baseAtom_n == line2_baseAtom_n:
        return 0
    elif line1_baseAtom_n > line2_baseAtom_n:
        return 1
