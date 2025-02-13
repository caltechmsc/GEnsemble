#!/usr/bin/python

'''This moduel includes tools to manipulate residues.'''

import PyAtom
import re, copy, math, sys
import vector

AminoAcids_321_SCREAM = {'ALA': 'A', 'CYS' : 'C', 'ASP': 'D', 'APP': 'D', 'GLU':'E', 'GLP':'E', 'PHE':'F', 'GLY':'G', 'HSP': 'B', 'HSD':'H', 'HSE':'J', 'HIS':'H', 'ILE':'I', 'LYS':'K', 'LYN':'K', 'LEU':'L', 'MET':'M','ASN':'N', 'PRO':'P', 'GLN':'Q','ARG':'R', 'ARN':'R', 'SER':'S', 'THR':'T', 'VAL':'V','TRP':'W', 'TYR':'Y', 'CYX':'X'}

AminoAcids_321_FASTA = {'ALA': 'A', 'CYS' : 'C', 'ASP': 'D', 'GLU':'E', 'PHE':'F', 'GLY':'G', 'HSP': 'H', 'HSD':'H', 'HSE':'H', 'HIS':'H', 'ILE':'I', 'LYS':'K', 'LEU':'L', 'MET':'M','ASN':'N', 'PRO':'P', 'GLN':'Q','ARG':'R', 'SER':'S', 'THR':'T', 'VAL':'V','TRP':'W', 'TYR':'Y', 'CYX': 'C'}

Canonical_res_name = {'A': 'ALA', 'C' : 'CYS', 'D' : 'ASP', 'E':'GLU','F':'PHE','G':'GLY','H':'HIS', 'I':'ILE', 'K':'LYS', 'L':'LEU','M':'MET','N':'ASN','P':'PRO','Q':'GLN','R':'ARG','S':'SER','T':'THR','V':'VAL','W':'TRP','Y':'TYR'}

# 
value_map = {}
#  Backbone.
value_map["N"] = 1
value_map["NT"] = 1
value_map["HN"] = 2
value_map["HN1"] = 2.1
value_map["HN2"] = 2.2
value_map["HN3"] = 2.3
value_map["CA"] = 3
value_map["HCA"] = 4
value_map["HA1"] = 4.1
value_map["HA2"] = 4.2
value_map["C"] = 5
value_map["O"] = 6

#value_map["C"] = 500
#value_map["O"] = 600

#  SideChain.
value_map["CB"] = 11
value_map["HCB"] = 12
value_map["HB1"] = 12.1
value_map["HB2"] = 12.2
value_map["HB3"] = 12.3

value_map["CG"] = 21
value_map["HCG"] = 21.5
value_map["OG1"] = 22
value_map["HOG1"] = 22.5
value_map["CG1"] = 23
value_map["HCG1"] = 24
value_map["CG2"] = 25
value_map["HCG2"] = 26 #  plus all those HG11, etc.  put these in later.
value_map["SG"] = 27
value_map["HSG"] = 28
value_map["OG"] = 29
value_map["HOG"] = 30

value_map["CD"] = 31
value_map["HCD"] = 32
value_map["ND1"] = 33
value_map["HND1"] = 34
value_map["CD1"] = 35
value_map["HCD1"] = 36
value_map["CD2"] = 37
value_map["HCD2"] = 38
value_map["OD1"] = 39
value_map["HOD1"] = 39.5 # APP
value_map["OD2"] = 40
value_map["HOD2"] = 40.5
value_map["ND2"] = 41
value_map["HND2"] = 42
value_map["SD"] = 43

value_map["CE"] = 51
value_map["HCE"] = 52
value_map["NE"] = 53
value_map["HNE"] = 54
value_map["NE1"] = 55
value_map["HNE1"] = 56
value_map["CE1"] = 57
value_map["HCE1"] = 58
value_map["OE1"] = 59
value_map["HOE1"] = 59.5 # GLP
value_map["OE2"] = 60
value_map["HOE2"] = 60.5
value_map["CE1"] = 61
value_map["HCE1"] = 62
value_map["NE2"] = 63
value_map["HNE2"] = 64
value_map["CE2"] = 65
value_map["HCE2"] = 66
value_map["CE3"] = 67
value_map["HCE3"] = 68

value_map["CZ"] = 81
value_map["HCZ"] = 82
value_map["NZ"] = 83
value_map["HNZ"] = 84
value_map["CZ2"] = 85
value_map["HCZ2"] = 86
value_map["CZ3"] = 87
value_map["HCZ3"] = 88

value_map["CH2"] = 91  #  TRP
value_map["HCH2"] = 92
value_map["OH"] = 93 #  TYR
value_map["HOH"] = 94
value_map["NH1"] = 95 #  ARG
value_map["HNH1"] = 96
value_map["HH11"] = 96.1 # ARN
value_map["NH2"] = 97
value_map["HNH2"] = 98
value_map["HH21"] = 98.1
value_map["HH22"] = 98.2

value_map["OX"] = 997  
value_map["HC"] = 998
value_map["OXT"] = 999
value_map["HOXT"] = 999.1


class PyResidue:
    # Member parameters.
    res_name = ''
    chain_name = ''
    res_pstn = ''

    surface_area = -1
    
    is_AA_residue = 1
    
    pyatom_list = []

    def __init__(self):
        self.pyatom_list = []

    def __getitem__(self, index):
        return self.pyatom_list[index]

    def _cmp(self, other):
        value = 0
        if self.chain_name < other.chain_name:
            value = -1
        elif self.chain_name == other.chain_name:
            if self.res_pstn < other.res_pstn:
                value = -1
            elif self.res_pstn == other.res_pstn:
                value = 0
            elif self.res_pstn > other.res_pstn:
                value = 1
        elif self.chain_name > other.chain_name:
            value = 1

        return value

    def initialize(self):
        '''Initilizes attributes from atoms stored in pyatom_list'''
        if len(self.pyatom_list) != 0:
            self.res_name = self.pyatom_list[0].res_name.strip()
            self.chain_name = self.pyatom_list[0].chain_name
            self.res_pstn = self.pyatom_list[0].res_pstn
        else:
            print 'Warning: pyatom_list is empty!  in pyresidueinitialize()'

        # self.is_AA_residue = 
        # Initializing surface area. 
        
    def initialize_with_fsm_area(self):
        self.initialize()
        self.surface_area = 0
        
        for atom in self.pyatom_list:
            assert(atom.fsm_area != -1)
            if atom.is_SideChainAtom():
                self.surface_area += atom.fsm_area

    def total_charge(self):
        charge = 0
        for atom in self.pyatom_list:
            charge += atom.charge
        if math.fabs(charge) <= 0.000001:
            return 0
        else:
            return charge

    def return_sc_heavy_atoms(self):
        sc_heavy_atoms = []
        for atom in self.pyatom_list:
            if atom.is_SideChainAtom() and atom.is_HeavyAtom():
                sc_heavy_atoms.append(atom)
        return sc_heavy_atoms
            
    def closest_distance(self, res2):
        closest_distance = 99999
        for atom1 in self.pyatom_list:
            for atom2 in res2.pyatom_list:
                dist = atom1.distance(atom2)
                if dist < closest_distance:
                    closest_distance = dist
        return closest_distance

    def CRMS_distance(self, res2):
        '''
        Calculates heavy atom CRMS between two sidechains.  CRMS:  i.e. RMSD, root-mean-square deviation.
        Remark: CRMS distance is corrected through PHE, TYR ring flips and ASP, GLU OXT flips, and ARG N1 - N2 flips.
        '''

        equivalent_atoms_map = {}
        flipped_atoms_map = {}
        CRMS = 999999
        
        # take care of Gly.
        if self.res_name == "GLY":
            return 0
        if self.res_name != res2.res_name:
            if (self.res_name == "HIS" or self.res_name == "HSP" or self.res_name == "HSE") and (res2.res_name == "HIS" or res2.res_name == "HSP" or res2.res_name == "HSE"):
                pass
            elif (self.res_name == "CYS" or self.res_name == "CYX"):
                pass
            else:
                print "Comparing residue CRMS of different type!  Error.  Quitting."
                print self.res_name, self.res_pstn
                print res2.res_name, res2.res_pstn
                sys.exit(2)
        
        # First associate the equivalent atoms.
        for atom in self.pyatom_list:
            if atom.is_SideChainAtom() and atom.is_HeavyAtom() and atom.atom_label.strip() != 'CB': #and atom.DREIDII_type.strip() != 'H_': #
                mapped_atom = res2.return_atom_with_atom_label(atom.atom_label)
                equivalent_atoms_map[atom] = mapped_atom

        if len(equivalent_atoms_map.keys()) == 0:
            return 0.00
        assert (len(equivalent_atoms_map.keys()) != 0)
        # Then actually do the CRMS distance calculation.
        pyatom_list1 = equivalent_atoms_map.keys()
        pyatom_list2 = map(lambda x: equivalent_atoms_map[x], pyatom_list1)
        
        CRMS = calc_CRMS_from_two_PyAtom_lists(pyatom_list1, pyatom_list2)
        if not (self.res_name == 'PHE' or self.res_name == 'TYR' or self.res_name == 'ASP' or self.res_name == 'GLU' or self.res_name == 'ARG'):
            return CRMS

        # Flip residue if necessary.
        for atom in self.pyatom_list:
            if atom.is_SideChainAtom() and atom.is_HeavyAtom() and atom.atom_label.strip() != 'CB':
                mapped_atom = res2.return_atom_with_flipped_atom_label(atom.atom_label)
                flipped_atoms_map[atom] = mapped_atom
        
        assert(len(flipped_atoms_map.keys()) != 0)
        pyatom_list1_flipped = flipped_atoms_map.keys()
        pyatom_list2_flipped = map(lambda x: flipped_atoms_map[x], pyatom_list1_flipped)

        CRMS_flipped = calc_CRMS_from_two_PyAtom_lists(pyatom_list1_flipped, pyatom_list2_flipped)
        if CRMS_flipped < CRMS:
            return CRMS_flipped
        else:
            return CRMS

    def is_polar(self):
        aa = self.return_one_letter_aa_for_SCREAM()
        AminoAcids_321_SCREAM = {'ALA': 'A', 'CYS' : 'C', 'ASP': 'D', 'APP': 'D', 'GLU':'E', 'GLP':'E', 'PHE':'F', 'GLY':'G', 'HSP': 'B', 'HSD':'H', 'HSE':'J', 'HIS':'H', 'ILE':'I', 'LYS':'K', 'LYN':'K', 'LEU':'L', 'MET':'M','ASN':'N', 'PRO':'P', 'GLN':'Q','ARG':'R', 'ARN':'R', 'SER':'S', 'THR':'T', 'VAL':'V','TRP':'W', 'TYR':'Y', 'CYX':'X'}

        polar_res = ['D', 'E', 'B', 'H', 'J', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y']
        if aa in polar_res:
            return 1
        else:
            return 0

    def is_canonical_amino_acid(self):
        if AminoAcids_321_SCREAM.has_key(self.res_name):
            return 1
        else:
            return 0

    def return_SCREAM_string(self):
        aa = self.return_one_letter_aa_for_SCREAM()
        if aa == '':
            return ''
        else:
            s = aa + str(self.res_pstn) + '_' + self.chain_name
        return s

    def return_FASTA_mutInfo_string(self):
        aa = self.return_one_letter_aa_for_FASTA()
        if aa == '':
            return ''
        else:
            s = aa + str(self.res_pstn) + '_' + self.chain_name
        return s

    def return_one_letter_aa_for_SCREAM(self):
        one_letter_AA = ''
        try:
            one_letter_AA = AminoAcids_321_SCREAM[self.res_name]
        except KeyError, e:
            pass
            #print self.res_name, 'isn\'t a valid residue name!'
        return one_letter_AA

    def return_canonical_res_name(self):
        canon_name = 'UNDEFINED'
        try:
            canon_name = Canonical_res_name[AminoAcids_321_SCREAM[self.res_name]]
        except KeyError, e:
            print 'Warning: in return_canonical_res_name(): '
            print e
            print 'Res Name is %s ' % self.res_name
            canon_name = self.res_name
        return canon_name

    def return_one_letter_aa_for_FASTA(self):
        one_letter_AA_FASTA = ''
        try:
            one_letter_AA_FASTA = AminoAcids_321_FASTA[self.res_name]
        except KeyError, e:
            pass
            #print self.res_name, 'isn\'t a valid residue name!'
        return one_letter_AA_FASTA
            

    def return_atom_with_atom_label(self, atom_label):
        '''Finds first instance of atom with atom label name.  Does not guard against residues with atoms with multiple atom labels.'''
        a = 0
        for atom in self.pyatom_list:
            if atom.atom_label.strip() == atom_label.strip():
                return atom
        return a

    def return_atom_with_atom_label_multiple(self, atom_label):
        '''Finds all atoms with atom label name.  Output in a list.'''
        list = []
        for atom in self.pyatom_list:
            if atom.atom_label.strip() == atom_label.strip():
                list.append(atom)
        return list

    def return_multiple_H_connected_to_heavy_atom_label(self, heavy_atom_label):
        '''Find all H\'s that are connected to atom_label.  Heuristics are used.  Output in a list.'''
        list = []
        H_atom_label = 'H' + heavy_atom_label.strip()
        list = self.return_atom_with_atom_label_multiple(H_atom_label)

        if len(list) == 0:
            # try HB1, HZ3 nomenclatures.  will implement other nomenclatures.
            heavy_atom_core = heavy_atom_label[1:] # rid of leading heavy atom element name
            H_atom_label_core = 'H' + heavy_atom_core.strip()
            H_pat = re.compile(H_atom_label_core)
            print 'H_atom_label_core',  H_atom_label_core
            for a in self.pyatom_list:
                label = a.atom_label.strip()
                if H_pat.match(label):  # match: search beginning of string.  e.g. HZ matches HZ1, HZ2, etc.
                    list.append(a)
        return list
            
        

    def return_NeutralToCharged_HAddedOrRemoved(self):
        '''Returns a list of charged atoms for ASP, GLU, ARG and LYS.  Not HIS.'''
        AddRemove = []
        #canRes = self.return_canonical_res_name()
        canRes = self.res_name
        #if canRes == 'ASP':
        if canRes == 'APP':
            # Also needs to remove connectivity.
            HOD1 = self.return_atom_with_atom_label('HOD1')
            HOD2 = self.return_atom_with_atom_label('HOD2')

            if HOD1 == 0:
                return ['REMOVE',HOD2]
            else:
                return ['REMOVE',HOD1]

                
        #elif canRes == 'GLU':
        elif canRes == 'GLP':
            HOE1 = self.return_atom_with_atom_label('HOE1')
            HOE2 = self.return_atom_with_atom_label('HOE2')

            if HOE1 == 0:
                return ['REMOVE',HOE2]
            else:
                return ['REMOVE',HOE1]

        #elif canRes == 'ARG':
        elif canRes == 'ARN':
            H = self._return_added_ARG_H_added()
            return ['ADD', H]

        #elif canRes == 'LYS':
        elif canRes == 'LYN':
            H = self._return_added_LYN_H_added()
            return ['ADD', H]
        
        else:
            pass
        return AddRemove

    def _return_added_LYN_H_added(self):
        HNZ_l = self.return_atom_with_atom_label_multiple('HNZ')
        NZ = self.return_atom_with_atom_label('NZ')
        CE = self.return_atom_with_atom_label('CE')

        new_HNZ = PyAtom.PyAtom()
        new_HNZ.copy_bgf_attributes(HNZ_l[0])

        HNZ1_v = vector.vector([HNZ_l[0].x, HNZ_l[0].y, HNZ_l[0].z])
        HNZ2_v = vector.vector([HNZ_l[1].x, HNZ_l[1].y, HNZ_l[1].z])
        NZ_v = vector.vector([NZ.x, NZ.y, NZ.z])
        CE_v = vector.vector([CE.x, CE.y, CE.z])

        CE_NZ = (NZ_v - CE_v).normalized()
        NHZ1_NZ = (NZ_v - HNZ1_v).normalized()
        NHZ2_NZ = (NZ_v - HNZ2_v).normalized()

        NZ_NHZ3 = (CE_NZ + NHZ1_NZ + NHZ2_NZ).normalized() * 0.97
        HNZ3_v = NZ_NHZ3 + NZ_v

        new_HNZ.x = HNZ3_v[0]
        new_HNZ.y = HNZ3_v[1]
        new_HNZ.z = HNZ3_v[2]

        # don't need to change atom label.  atom connectiviy is actually right at this point.
        
        return new_HNZ 

    def _return_added_ARG_H_added(self):
        HNH1_l = self.return_atom_with_atom_label_multiple('HNH1')
        HNH2_l = self.return_atom_with_atom_label_multiple('HNH2')

        HH11 = self.return_atom_with_atom_label('HH11')
        HH12 = self.return_atom_with_atom_label('HH12')
        HH21 = self.return_atom_with_atom_label('HH21')
        HH22 = self.return_atom_with_atom_label('HH22')

        if len(HNH1_l) == 0:
            if HH11 != 0:
                HNH1_l.append(HH11)
            if HH12 != 0:
                HNH1_l.append(HH12)
        if len(HNH2_l) == 0:
            if HH21 != 0:
                HNH2_l.append(HH21)
            if HH22 != 0:
                HNH2_l.append(HH22)

        HNH = ''
        NH = ''
        CZ = self.return_atom_with_atom_label('CZ')
        
        if len(HNH1_l) == 1:
            NH = self.return_atom_with_atom_label('NH1')
            HNH = self.return_atom_with_atom_label('HNH1')
            if HNH == 0:
                HNH = self.return_atom_with_atom_label('HH11')
            if HNH == 0:
                HNH = self.return_atom_with_atom_label('HH12')
            
        else:
            NH = self.return_atom_with_atom_label('NH2')
            HNH = self.return_atom_with_atom_label('HNH2')
            if HNH == 0:
                HNH = self.return_atom_with_atom_label('HH21')
            if HNH == 0:
                HNH = self.return_atom_with_atom_label('HH22')

        HNH_v = vector.vector([HNH.x, HNH.y, HNH.z])
        NH_v = vector.vector([NH.x, NH.y, NH.z])
        CZ_v = vector.vector([CZ.x, CZ.y, CZ.z])

        HNH_NH = (NH_v - HNH_v).normalized()
        CZ_NH = (NH_v - CZ_v).normalized()

        NH_HNH_new = (HNH_NH + CZ_NH).normalized() * 0.97
        new_HNH = NH_v + NH_HNH_new

        H = PyAtom.PyAtom()
        H.copy_bgf_attributes(HNH)
        H.x = new_HNH[0]
        H.y = new_HNH[1]
        H.z = new_HNH[2]

        # no need to change connectivities yet--reflects already in the other HNH.atom labels will be taken care of later.

        return H


    def _return_removed_APP_GLP_H_removed(self, H_label):
        pass

    def Fix_Atom_Labels(self):
        res_name = self.res_name
        if res_name == 'ARN':
            self._fix_ARN_labels()
        elif res_name == 'LYN':
            self._fix_LYN_labels()
        elif res_name == 'APP':
            self._fix_APP_labels()
        elif res_name == 'GLP':
            self._fix_GLP_labels()
        else:
            pass


    def _fix_ARN_labels(self):
        # HNH1 should have 1 hydrogen.
        NH1 = ''
        NH1_H_list = []
        NH2 = ''
        NH2_H_list = []

        
        NE = ''
        CZ = ''
        HH11 = ''
        HH21 = ''
        HH22 = ''
        
        for atom in self.pyatom_list:
            atom_label = atom.return_atom_label()
            if atom_label == 'NE':
                NE = atom
            elif atom_label == 'CZ':
                CZ = atom
            elif atom_label == 'NH1':
                NH1 = atom
            elif atom_label == 'NH2':
                NH2 = atom
            elif atom_label == 'HNH1' or atom_label[0:3] == 'HH1':
                NH1_H_list.append(atom)
            elif atom_label == 'HNH2' or atom_label[0:3] == 'HH2':
                NH2_H_list.append(atom)

        if len(NH1_H_list) == 1:
            HH21 = NH2_H_list[0]
            HH22 = NH2_H_list[1]
            
            pass
        else: # if NH1_H_list == 2.
            NH1.atom_label = ' NH2'
            NH2.atom_label = ' NH1'
            NH1_H_list[0].atom_label = 'HNH2'
            NH1_H_list[1].atom_label = 'HNH2'
            NH2_H_list[0].atom_label = 'HH11'

            HH21 = NH1_H_list[0]
            HH22 = NH1_H_list[1]
            NH2 = NH1 # loses info
        

        # Now: NH2-HH22
        #      /
        #    HH21
        # determine which one is HH21 and which one is HH22

        NE_v = vector.vector([NE.x, NE.y, NE.z])
        CZ_v = vector.vector([CZ.x, CZ.y, CZ.z])

        NE_CZ = CZ_v - NE_v

        NH2_v = vector.vector([NH2.x, NH2.y, NH2.z])
        HH21_v = vector.vector([HH21.x, HH21.y, HH21.z])
        HH22_v = vector.vector([HH22.x, HH22.y, HH22.z])

        v21 = HH21_v - NH2_v
        v22 = HH22_v - NH2_v
        
        if vector.dot(NE_CZ, v21) > 0:
            HH21.atom_label = 'HH22'
            HH22.atom_label = 'HH21'
        else:
            HH21.atom_label = 'HH21'
            HH22.atom_label = 'HH22'

    def _fix_LYN_labels(self):
        # only need to check if HZ1 and HZ2 are the names; if not, name them to HZ1 and HZ2.
        HZ_l = self.return_multiple_H_connected_to_heavy_atom_label('NZ')
        if len(HZ_l) == 2:
            HZ_l[0].atom_label = 'HZ1'
            HZ_l[1].atom_label = 'HZ2'
            

    def _fix_APP_labels(self):
        # OD1 should have HOD1
        OD1 = ''
        HOD1 = ''
        OD2 = ''

        atom_map = {}
        
        for atom in self.pyatom_list:
            atom_map[atom.return_atom_label()] = atom

        if atom_map.has_key('HOD1'):
            pass
        else:
            OD1 = atom_map['OD1']
            OD2 = atom_map['OD2']
            HOD1 = atom_map['HOD2']
            OD1.atom_label = ' OD2'
            OD2.atom_label = ' OD1'
            HOD1.atom_label = 'HOD1'
    

    def _fix_GLP_labels(self):
        # OE1 should have HOE1
        OE1 = ''
        HOE1 = ''
        OE2 = ''

        atom_map = {}
        
        for atom in self.pyatom_list:
            atom_map[atom.return_atom_label()] = atom

        if atom_map.has_key('HOE1'):
            pass
        else:
            OE1 = atom_map['OE1']
            OE2 = atom_map['OE2']
            HOE1 = atom_map['HOE2']
            OE1.atom_label = ' OE2'
            OE2.atom_label = ' OE1'
            HOE1.atom_label = 'HOE1'
        
    def return_atom_with_flipped_atom_label(self, atom_label):
        '''
        Returns atom with atom label that corresponds to a flipped residue like Phe, Tyr, Asp, Glu, Arg.
        '''

        # Atoms that need to be flipped.
        atom_label = atom_label.strip()
        if self.res_name == 'PHE' or self.res_name == 'TYR':
            if atom_label == 'CD1':
                return self.return_atom_with_atom_label('CD2')
            elif atom_label == 'CD2':
                return self.return_atom_with_atom_label('CD1')
            elif atom_label == 'CE1':
                return self.return_atom_with_atom_label('CE2')
            elif atom_label == 'CE2':
                return self.return_atom_with_atom_label('CE1')
            
        elif self.res_name == 'ASP':
            if atom_label == 'OD1':
                return self.return_atom_with_atom_label('OD2')
            elif atom_label == 'OD2':
                return self.return_atom_with_atom_label('OD1')
            
        elif self.res_name == 'GLU':
            if atom_label == 'OE1':
                return self.return_atom_with_atom_label('OE2')
            elif atom_label == 'OE2':
                return self.return_atom_with_atom_label('OE1')
            
        elif self.res_name == 'ARG':
            if atom_label == 'NH1':
                return self.return_atom_with_atom_label('NH2')
            elif atom_label == 'NH2':
                return self.return_atom_with_atom_label('NH1')
        
        # Atoms that stay who they are.
        return self.return_atom_with_atom_label(atom_label)

    def sort_standard(self):
        canName = self.return_canonical_res_name()
        try:
            AminoAcids_321_SCREAM[canName]
            self.pyatom_list.sort(self._cmp_AA_atom_order)
        except KeyError, e:
            print 'Warning: in .sort_standard(), can\'t sort because not a natural amino acid: %s' % canName
            
    def return_MutInfo(self):
        mutInfo = '%s%d_%s' % (AminoAcids_321_SCREAM[self.res_name], self.res_pstn, self.chain_name)
        return mutInfo

    def add_atom(self, atom):
        self.pyatom_list.append(atom)

    def clear(self):
        self.pyatom_list = []

    def size(self):
        return len(self.pyatom_list)

    def _cmp_AA_atom_order(self, a1, a2):
        a1_atom_label = a1.atom_label.strip()
        a2_atom_label = a2.atom_label.strip()

        a1_value = ''
        a2_value = ''

        try:
            a1_value = value_map[a1_atom_label]
            a2_value = value_map[a2_atom_label]
        except KeyError, e:
            print e
            print 'One of these atom label values don\'t exist!'
            print a1_atom_label
            print a1.return_bgf_line()
            print a2_atom_label
            print a2.return_bgf_line()
            sys.exit(2)

        if a1_value < a2_value:
            return -1
        elif a1_value > a2_value:
            return 1
        else:
            a1_n = a1.atom_n
            a2_n = a2.atom_n
            if a1_n < a2_n:
                return -1
            elif a1_n > a2_n:
                return 1
            else:
                return 0



def make_PyResidue_list(atom_list):

    previous_atom = PyAtom.PyAtom()
    current_atom = PyAtom.PyAtom()

    previous_atom.res_pstn = -1
    current_atom.res_pstn = -1
    previous_atom.chain_name = ''
    current_atom.chain_name = ''

    residue_list = []
    this_res = PyResidue()
    
    for pyatom in atom_list:
        previous_atom.res_pstn = current_atom.res_pstn
        current_atom.res_pstn = pyatom.res_pstn
        previous_atom.chain_name = current_atom.chain_name
        current_atom.chain_name = pyatom.chain_name

        if current_atom.is_new_residue(previous_atom):
            # start condition
            if this_res.size() == 0:
                pass
            # main (body) condition
            else:
                this_res.initialize()
                residue_list.append(this_res)
                this_res = PyResidue()

            # execute the following under all conditions (in this if-else control)
            this_res.add_atom(pyatom)
                
        else:
            # execute under all conditions (in this if-else control)
            this_res.add_atom(pyatom)

    # end condition
    this_res.initialize()
    residue_list.append(this_res)

    return residue_list


def make_PyResidue_list_with_fsm_area(atom_list):

    previous_atom = PyAtom.PyAtom()
    current_atom = PyAtom.PyAtom()

    residue_list = []
    this_res = PyResidue()
    
    for pyatom in atom_list:
        previous_atom = copy.deepcopy(current_atom)
        current_atom = copy.deepcopy(pyatom)
        
        if current_atom.is_new_residue(previous_atom):
            # start condition
            if this_res.size() == 0:
                pass
            # main (body) condition
            else:
                this_res.initialize_with_fsm_area()
                residue_list.append(this_res)
                this_res = PyResidue()

            # execute the following under all conditions (in this if-else control)
            this_res.add_atom(pyatom)
                
        else:
            # execute under all conditions (in this if-else control)
            this_res.add_atom(pyatom)

    # end condition
    this_res.initialize_with_fsm_area()
    residue_list.append(this_res)

    return residue_list



def calc_CRMS_from_two_PyAtom_lists(atom_list1, atom_list2):
    '''
    Calculates CRMS distance from 2 atom lists, matching atoms given by the equivalent atoms map.
    if equivalent_atoms_map is empty, does comparison sequentially.
    '''
    CRMS_squared_sum = 0
    
    assert(len(atom_list1) == len(atom_list2) )
    for index in range(0, len(atom_list1) ):
        atom1 = atom_list1[index]
        atom2 = atom_list2[index]

        CRMS_squared_sum += (atom1.distance(atom2))**2
                
    total_atoms = len(atom_list1)
    CRMS = math.sqrt(CRMS_squared_sum / total_atoms)
    return CRMS


def get_PyResidue_from_PyResidue_list(list, pstn, chn):
    residue = ''
    for res in list:
        if res.res_pstn == pstn and res.chain_name == chn:
            residue = res
            break
    if residue == '':
        print 'Residue with chain name' , chn, ', position' , pstn, 'not found in PyResidue list!'
    return res

    
def make_FASTA_file(residue_list, filename, keyw_list):
    FASTA = open(filename, 'w')

    count = 0
    
    for res in residue_list:
        char_to_be_printed = ''

        for keyw in keyw_list:
            k = keyw.split("_")
            chain = k[-1]
            res_name = k[0][0]
            pstn = int(k[0][1:])
            
            if (res.chain_name == chain):
                if (res.res_pstn == pstn):
                    char_to_be_printed = res_name.upper()
                    break
                else:
                    char_to_be_printed = res.return_one_letter_aa_for_FASTA().lower()

            else:
                pass # don't do anything if not matching Chain
        
        FASTA.write(char_to_be_printed)

        count += 1
        if (count % 80 == 0):
            print >>FASTA
            #print 
            # FASTA format: line contains 80 characters

    print >>FASTA
    FASTA.close()


def Fix_HIS_type(PyRes):
    HIS_defn_h = {0:'HDD',1:'HIS',2:'HSE',3:'HSP'}
    HIS_type = 0
    for a in PyRes.pyatom_list:
        atom_label = a.return_atom_label()
        if atom_label == 'HND1' or \
           atom_label == 'HD1':
            HIS_type = HIS_type +1
        if atom_label == 'HNE2' or \
           atom_label == 'HE2':
            HIS_type = HIS_type +2
        
    for a in PyRes.pyatom_list:
        a.res_name = HIS_defn_h[HIS_type]

    PyRes.res_name = HIS_defn_h[HIS_type]

def Fix_CYS_type(PyRes):
    CYS_defn_h = {0:'CYX',1:'CYS'}
    CYS_type = 0
    for a in PyRes.pyatom_list:
        if a.return_atom_label() == 'HSG':
            CYS_type += 1

    for a in PyRes.pyatom_list:
        a.res_name = CYS_defn_h[CYS_type]

    PyRes.res_name = CYS_defn_h[CYS_type]

def Fix_ASP_type(PyRes):
    ASP_defn_h = {0:'ASP', 1:'APP'}
    ASP_type = 0

    Need_Fix_Flag = 0
    
    for a in PyRes.pyatom_list:
        if a.return_atom_label() == 'HOD1':
            ASP_type += 1
        if a.return_atom_label() == 'HOD2':
            ASP_type += 1
            Need_Fix_Flag = 1

    for a in PyRes.pyatom_list:
        a.res_name = ASP_defn_h[ASP_type]

    # Now fix OD1, OD2 and HOD1 nonmenclature.
    if Need_Fix_Flag == 1:
        OD1 = PyRes.return_atom_with_atom_label('OD1')
        OD2 = PyRes.return_atom_with_atom_label('OD2')
        HOD2 = PyRes.return_atom_with_atom_label('HOD2')

        OD1.atom_label = 'OD2'
        OD2.atom_label = 'OD1'
        HOD2.atom_label = 'HOD1'

    PyRes.res_name = ASP_defn_h[ASP_type]

def Fix_GLU_type(PyRes):
    GLU_defn_h = {0:'GLU', 1:'GLP'}
    GLU_type = 0

    Need_Fix_Flag = 0
    
    for a in PyRes.pyatom_list:
        if a.return_atom_label() == 'HOE1':
            GLU_type += 1
        if a.return_atom_label() == 'HOE2':
            GLU_type += 1
            Need_Fix_Flag = 1

    for a in PyRes.pyatom_list:
        a.res_name = GLU_defn_h[GLU_type]

    # Now fix OD1, OD2 and HOD1 nonmenclature.
    if Need_Fix_Flag == 1:
        OE1 = PyRes.return_atom_with_atom_label('OE1')
        OE2 = PyRes.return_atom_with_atom_label('OE2')
        HOE2 = PyRes.return_atom_with_atom_label('HOE2')

        OE1.atom_label = 'OE2'
        OE2.atom_label = 'OE1'
        HOE2.atom_label = 'HOE1'

        #OD1.

    PyRes.res_name = GLU_defn_h[GLU_type]
 
def Fix_ARG_type(PyRes):
    ARG_defn_h = {3:'ARN', 4:'ARG'}
    ARG_type = 0
    for a in PyRes.pyatom_list:
        atom_label = a.return_atom_label()
        if atom_label == 'HNH1':
            ARG_type += 1
        if atom_label == 'HNH2':
            ARG_type += 1
        if atom_label[0:2] == 'HH':
            ARG_type += 1

    for a in PyRes.pyatom_list:
        try:
            a.res_name = ARG_defn_h[ARG_type]
        except KeyError, e:
            print a.return_bgf_line()
            
    PyRes.res_name = ARG_defn_h[ARG_type]

def Fix_LYS_type(PyRes):
    LYS_defn_h = {2:'LYN', 3:'LYS'}
    LYS_type = 0
    for a in PyRes.pyatom_list:
        if a.return_atom_label() == 'HNZ' or \
           a.return_atom_label() == 'HZ1' or \
           a.return_atom_label() == 'HZ2' or \
           a.return_atom_label() == 'HZ3':
            LYS_type += 1
    if LYS_type != 2 and LYS_type != 3:
        print 'Incompatible LYS type!  Only ' + str(LYS_type) + ' number of HNZ atoms.  Missing NZ atom?'
        PyRes.res_name = 'LYS'
    else:
        for a in PyRes.pyatom_list:
            a.res_name = LYS_defn_h[LYS_type]

        PyRes.res_name = LYS_defn_h[LYS_type]

def Fix_Residue_type(PyRes):
    special_types = ['CYS','HIS', 'ASP', 'APP', 'GLU', 'GLP', 'ARG', 'ARN', 'LYS', 'LYN']
    name = PyRes.pyatom_list[0].return_canonical_res_name()
    if name in special_types:
        if name == 'CYS':
            Fix_CYS_type(PyRes)
        elif name in ['HIS']:
            Fix_HIS_type(PyRes)
        elif name in ['ASP', 'APP']:
            Fix_ASP_type(PyRes)
        elif name in ['GLU', 'GLP']:
            Fix_GLU_type(PyRes)
        elif name in ['ARG', 'ARN']:
            Fix_ARG_type(PyRes)
        elif name in ['LYS', 'LYN']:
            Fix_LYS_type(PyRes)

