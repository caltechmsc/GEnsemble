#!/usr/bin/python

'''This module includes the PyAtom class for easy info storage.'''

import re, math, sys

ions = ['na', 'cl', 'li', 'f', 'mg', 'cl', 'br', 'i', 'k', 'ca', 'sc', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'cd', 'ag', 'rb']

AminoAcids_321 = {'ALA': 'A', 'CYS' : 'C', 'CYX': 'C', 'ASP': 'D', 'APP': 'D', 'GLU':'E', 'GLP':'E', 'PHE':'F', 'GLY':'G', 'HSP': 'H', 'HSD':'H', 'HSE':'H', 'HIS':'H', 'ILE':'I', 'LYS':'K', 'LYN':'K','LEU':'L', 'MET':'M','ASN':'N', 'PRO':'P', 'GLN':'Q','ARG':'R', 'ARN':'R', 'SER':'S', 'THR':'T', 'VAL':'V','TRP':'W', 'TYR':'Y'}
Canonical_res_name = {'A': 'ALA', 'C' : 'CYS', 'D' : 'ASP', 'E':'GLU','F':'PHE','G':'GLY','H':'HIS', 'I':'ILE', 'K':'LYS', 'L':'LEU','M':'MET','N':'ASN','P':'PRO','Q':'GLN','R':'ARG','S':'SER','T':'THR','V':'VAL','W':'TRP','Y':'TYR'}

FASTA_map = {'HSE':'HIS', 'HSP':'HIS', 'HSD':'HIS', 'CYX':'CYS'}

class PyAtom:

    # Common section.  Don't want to make these global!
    # keyw = ''
#     atom_n = 0
#     atom_label = ''
#     res_name = ''
#     chain_name = ''
#     res_pstn = 0
#     x = 0.0
#     y = 0.0
#     z = 0.0
#     charge = 0.0

#     # topology section
#     bonds = []

#     # Particulars section.
#     DREIDII_type = ''
#     CHARMM_type = ''

#     num_of_bonds = 0
#     lone_pairs = 0
#     fixed = 0    
    
#     FSM_type = 0
#     FSM_area = -1
    def __init__(self, bgf_line=None):
        self.__init_default()
        if bgf_line is None:
            pass
        else:
            self.bgf_line_populate(bgf_line)

    def __init_default(self):
        # Common section.
        self.keyw = ''
        self.atom_n = 0
        self.atom_label = ''
        self.res_name = ''
        self.chain_name = ''
        self.res_pstn = 0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.charge = 0.0
        
        # topology section
        self.bonds = []
        
        # Particulars section.
        self.DREIDII_type = ''
        self.CHARMM_type = ''
        
        self.num_of_bonds = 0
        self.lone_pairs = 0
        self.fixed = 0    
        
        self.FSM_type = 0
        self.FSM_area = -1
  
    # Copy functions.
    def copy_bgf_attributes(self, atom2):
        '''Copies all bgf attributes related of atom2 into self.'''
        self.keyw = atom2.keyw
        self.atom_n = atom2.atom_n
        self.atom_label = atom2.atom_label
        self.res_name = atom2.res_name
        self.chain_name = atom2.chain_name
        self.res_pstn = atom2.res_pstn
        self.x = atom2.x
        self.y = atom2.y
        self.z = atom2.z
        self.DREIDII_type = atom2.DREIDII_type
        self.num_of_bonds = atom2.num_of_bonds
        self.lone_pairs = atom2.lone_pairs
        self.charge = atom2.charge

        self.bonds = []
        for b in atom2.bonds:
            self.bonds.append(b)

    def copy_coords(self, atom2):
        self.x = atom2.x
        self.y = atom2.y
        self.z = atom2.z

    # Bond manipulation functions.
    def add_bond(self, atom2):
        if atom2.atom_n == self.atom_n:
            print 'Can\'t make bond to self!'
            return
        if not atom2.atom_n in self.bonds:
            self.bonds.append(atom2.atom_n)
        if not self.atom_n in atom2.bonds:
            atom2.bonds.append(self.atom_n)

    def delete_bond(self, atom2):
        success = 0
        if atom2.atom_n == self.atom_n:
            print 'Can\'t delete bond to self!'
            return
        if atom2.atom_n in self.bonds:
            self.bonds.remove(atom2.atom_n)
            success += 1 
        if self.atom_n in atom2.bonds:
            atom2.bonds.remove(self.atom_n)
            success += 1

        if success == 2:
            return 1
        else:
            return 0
    # Population functions.
    def bgf_line_populate(self, bgf_line):
        #self.__init_default()
        new_line = bgf_line.strip()

        self.keyw = new_line[0:6]
        self.atom_n = int(new_line[6:12])
        self.atom_label = new_line[13:18]
        self.res_name = new_line[19:22]
        self.chain_name = new_line[23:24]
	#        self.res_pstn = int(new_line[25:29])
	self.res_pstn = int(new_line[25:30])
        self.x = float(new_line[30:40])
        self.y = float(new_line[40:50])
        self.z = float(new_line[50:60])
        self.DREIDII_type = new_line[61:66]
        self.num_of_bonds = int(new_line[68:69])
        self.lone_pairs = int(new_line[70:71])
        self.charge =  float(new_line[72:80])

        if len(new_line) > 80:
            try:
                self.fixed = int(new_line[81:82])
            except ValueError, e:
                print >>sys.stderr, 'Bgf readline error: on line'
                print >>sys.stderr, bgf_line
                print >>sys.stderr, e
                pass

    def bgf_CONECT_populate(self, conect_line_in):
        # Return value of 0: means populate unsuccessful, error in CONECT_line.
        # Return value of -1, 1: means only base atom value in CONECT_line.  -1: self.atom_n < base atom.  1: base atom < self.atom_n
        # Return value of >= 2: # of atoms connected to base atom plus 1 (plus 1 comes from base atom)
        self.bonds = []

        # first process conect line.  only the first 70 columns taken.
        conect_line = conect_line_in[0:70]
        
        conect_f = conect_line.split()
        
        if len(conect_f) == 1:
            # impossible: means line consists is "CONECT" and no atom n info
            return 0
        elif len(conect_f) == 2:
            # means only base atom in CONECT line; okay.
            if self.atom_n != int(conect_f[1]):
                #print 'Error: CONECT line base atom doesn\'t correspond to this atom\'s atom number.'
                if self.atom_n < int(conect_f[1]):
                    return -1
                else:
                    return 1
            else:
                return len(conect_f)
            
        elif len(conect_f) >= 3:
            # legit conect line
            if self.atom_n != int(conect_f[1]):
                #print 'Error: CONECT line base atom doesn\'t correspond to this atom\'s atom number.'
                if self.atom_n < int(conect_f[1]):
                    return -1
                else:
                    return 1

            for i in range(2, len(conect_f)):
                self.bonds.append(int(conect_f[i]))

                
            return len(conect_f)

    def pdb_CONECT_populate(self, l):
        s = l.strip()[6:]
        while s != '':
            n = int(s[0:5])
            s = s[5:]
            if n == self.atom_n:
                continue
            self.bonds.append(n)
        
    
    def pdb_line_populate(self, line):
        # 01234567890123456789012345678901234567
        # ATOM    730  CG  LEU A  91      68.164  69.007  14.320
        TER_pat = re.compile(r'^TER')
        if TER_pat.search(line):
            print 'Warning: Pdb Line is a TER flagged line.'
            # return 0
        else:
            self.keyw = line[0:6]
            self.atom_n = int(line[6:11])
            self.atom_label = line[11:16]
            self.res_name = line[17:20]
            self.chain_name = line[21:22]
            self.res_pstn = int(line[22:26])
            self.x = float(line[30:38])
            self.y = float(line[38:46])
            self.z = float(line[46:54])
            
        #     if len(line) > 72:
        #                 self.chain_name = line[72:74]
    def return_SCREAM_label(self):
        one_letter = self.return_one_letter_aa_for_FASTA()
        if one_letter == '':
            print 'This res_name %s is not a standard amino acid: ' % self.res_name
            return ''
        s = '%s%i_%s' % (one_letter, self.res_pstn, self.chain_name)
        return s
        
    def return_atom_label(self):
        return self.atom_label.strip()

    def return_xyz(self):
        return [self.x, self.y, self.z]

    def return_canonical_res_name(self):
        canon_name = 'UNDEFINED'
        try:
            canon_name = Canonical_res_name[AminoAcids_321[self.res_name]]
        except KeyError, e:
            print 'Warning: in return_canonical_res_name(): '
            print e
            print 'Res Name is %s ' % self.res_name
            canon_name = self.res_name
        return canon_name
                
    def return_bgf_line(self):
        #line = '%6s%6d %4.4s  %3s %1.1s %4d %10.5f%10.5f%10.5f %5s  %1d %1d %8.5f'
        #line = '%6s%6d %4.4s  %3s %1c %4d %10.5f%10.5f%10.5f %-5s  %1d %1d %8.5f'
        line = '%6s%6d %4.4s  %3s %1c %4d %10.5f%10.5f%10.5f %-5s  %1d %1d %8.5f'
        atom_label_formatted = ''
        if self.keyw == 'HETATM':
            atom_label_formatted = self.atom_label
        else:
            atom_label_formatted = fix_atom_label(self.atom_label)
        #print "Chain name: ", self.chain_name
        #        line %= (self.keyw, self.atom_n, self.atom_label, self.res_name, self.chain_name, self.res_pstn, self.x, self.y, self.z, self.DREIDII_type, self.bonds, self.lone_pairs, self.charge)
        line %= (self.keyw, self.atom_n, atom_label_formatted, self.res_name, self.chain_name, self.res_pstn, self.x, self.y, self.z, self.DREIDII_type, self.num_of_bonds, self.lone_pairs, self.charge)
        return line

    def return_bgf_line_with_fixed(self):
        line = self.return_bgf_line()
        if self.fixed == 1:
            line = line + ' 1   0'
        else:
            line = line + ' 0   0'
        return line

    def return_bgf_conn_line(self):
        if len(self.bonds) == 0:
            return ''

        conect_line = 'CONECT'
        base_atom = '%6d' % self.atom_n
        conect_line += base_atom
        
        for bonded_atom in self.bonds:
            token = '%6d' % bonded_atom
            conect_line += token
        return conect_line
            

    def return_pdb_conn_line(self):
        if len(self.bonds) == 0:
            return ''

        conect_line = 'CONECT'
        base_atom = '%5d' % self.atom_n
        conect_line += base_atom

        for bonded_atom in self.bonds:
            token = '%5d' % bonded_atom
            conect_line += token
        return conect_line

    def return_pdb_line(self):
        #0123456789012345678901234567890123456789012345678901234567890
        #ATOM    310  CD1 LEU A  38      65.355  40.077  25.458
        #ATOM   1597  CZ  ARG A 226      96.119  38.077  33.389
        line = '%6s%5d %4.4s %3s %1s%4d    %8.3f%8.3f%8.3f'

        atom_label_formatted = fix_atom_label(self.atom_label)

        line %= (self.keyw, self.atom_n, atom_label_formatted, self.res_name, self.chain_name, self.res_pstn, self.x, self.y, self.z)
        return line

    def return_SCWRL_pdb_line(self):
        line = '%6s%5d %4.4s %3s %1s%4d    %8.3f%8.3f%8.3f'
        atom_label_formatted = fix_atom_label(self.atom_label)
        faster_res_name = self.res_name
        if self.res_name in FASTA_map.keys():
            faster_res_name = FASTA_map[self.res_name]
        line %= (self.keyw, self.atom_n, atom_label_formatted, faster_res_name, self.chain_name, self.res_pstn, self.x, self.y, self.z)
        return line
        

    def return_one_letter_aa_for_FASTA(self):
        one_letter = ''
        try:
            one_letter = AminoAcids_321[self.res_name]
        except KeyError,e:
            print 'This res_name %s is not a standard amino acid: ' % self.res_name
        return one_letter

    def fsm_atom_area_line_populate(self, line):
        #  0123456789012345678901234567890
        # 'Atom:     10 Area:      17.05'
        self.atom_n = int(line[5:12])
        self.fsm_area = float(line[18:29])

    def distance(self, atom2):
        x1 = self.x
        y1 = self.y
        z1 = self.z

        x2 = atom2.x 
        y2 = atom2.y
        z2 = atom2.z

        dist = math.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
        return dist

    def within(self, atom2, epsilon):
        if self.distance(atom2) <= epsilon:
            return 1
        else:
            return 0

    def closest_distance(self, atom_list):
        min_dist = 99999
        for a in atom_list:
            dist = self.distance(a)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def is_Hydrogen(self):
        stripped_atom_label = self.atom_label.strip()
        if stripped_atom_label[0] == 'H':
            return 1
        elif stripped_atom_label[0].isdigit() \
            and stripped_atom_label[1] == 'H':
            return 1
        else:
            return 0

    def is_Oxygen(self):
        if self.atom_label.strip()[0] == 'O':
            return 1
        else:
            return 0

    def is_Nitrogen(self):
        if self.atom_label.strip()[0] == 'N':
            return 1
        else:
            return 0

    def is_Sulfur(self):
        if self.atom_label.strip()[0] == 'S':
            return 1
        else:
            return 0
        

    def is_HeavyAtom(self):
        if self.is_Hydrogen():
            return 0
        else:
            return 1
        
    def is_BackBoneAtom(self):
        BackBoneAtomList = ['N', 'HN', 'CA', 'HCA', 'C', 'O', 'HT1', 'HT2', 'HT3', 'HA', 'HA1', 'HA2']
        stripped_atom_label = self.atom_label.strip()
        
        if stripped_atom_label in BackBoneAtomList:
            return 1
        else:
            return 0

    def is_SideChainAtom(self):
        if self.is_BackBoneAtom() or self.is_TermOxygenAtom():
            return 0
        elif self.keyw == 'HETATM':
            return 0
        else:
            return 1


    def is_TermOxygenAtom(self):
        TermOxygenAtomList = ['OXT', 'OT1', 'OT2']
        stripped_atom_label = self.atom_label.strip()
        
        if stripped_atom_label in TermOxygenAtomList:
            return 1
        else:
            return 0

    def is_new_residue(self, other_atom):
        if self.res_pstn != other_atom.res_pstn or self.chain_name != other_atom.chain_name:
            return 1
        else:
            return 0
        


def fix_atom_label(atom_label):
    stripped_label = atom_label.strip()
    new_label = ''
    if stripped_label[0].isdigit():
        if stripped_label[1] == 'H':
            new_label = '%-4.4s'

    elif stripped_label[0:1] == 'H':
        new_label = '%-4.4s'

    else:
        new_label = ' %-3.3s'

    return new_label %stripped_label
    

def copy_pyatom_lists_bgf_attributes(list1, list2):
    '''Copies bgf contents of one list to another.  list1: to be populated.  list2: reference list.'''

    assert(len(list1) == len(list2))
    if len(list1) == 0:
        return

    for i in range(0, len(list1)):
        list1[i].copy_bgf_attributes(list2[i])


def make_PyAtom_n_map(PyAtom_list):
    '''Makes a map from atom_n to atom.'''
    atom_map = {}
    for a in PyAtom_list:
        atom_map[a.atom_n] = a
    return atom_map

def angle(a1, a2, a3):
    '''Calculates the angle a1-a2-a3.  Always between 0 and 180.'''
    v1 = [a1.x-a2.x, a1.y-a2.y, a1.z-a2.z]
    v2 = [a3.x-a2.x, a3.y-a2.y, a3.z-a2.z]

    v1v2dot = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
    v1v2norm = math.sqrt((v1[0]*v1[0] + v1[1]*v1[1] + v1[2]*v1[2]) * (v2[0]*v2[0] + v2[1]*v2[1] + v2[2]*v2[2]))

    angle = math.acos(v1v2dot / v1v2norm) * 180 / math.pi

    return angle

    
    
#01234567890123456789012345678901234567890123456789012345678901234567890123456789012345
#ATOM      21  C    ILE B    5  -18.90354  13.45419   0.97836 C_R    3 0  0.51000 0   0
#ATOM      10   N   ARG E  226   94.46000  41.33500  27.46800        0 0 -0.47000
#ATOM       7 HA2   GLY E  225   93.74400  41.75700  24.97700        0 0  0.09000
        
#        1          2          3            4      5        6          7
#01234567890123456789012345678901234567890123456789012345678901234567890123
#ATOM      1  N   GLY   225      92.103  42.564  25.823  1.00  0.00      E1  
