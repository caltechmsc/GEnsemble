from chempy import Atom,Bond
from chempy.models import Indexed
from pymol import cmd
from copy import deepcopy
import time
#
# dotmae (.mae) file reader

import re,string

# regular expressions for parsing

_trunc_comment_re = re.compile(r'\n\s*#[^\n]*\n')
_trunc_quote_re = re.compile(r'"[^"]*"')
_match_quote_re = re.compile(r'"([^"]*)"')
_nuke_esc_quote_re = re.compile(r'\\"')
_unsupp_label_re = re.compile("\%HP|\%TY|\%NM|\%NE|\%CY") # unsupported labels

_crlf_re = re.compile(r"\r\n|\r")

_p2sym = { 1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N',
    8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si',
    15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc',
    22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28:
    'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se',
    35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41:
    'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag',
    48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54:
    'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd',
    61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67:
    'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta',
    74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80:
    'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn',
    87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U', 93:
    'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es',
    100: 'Fm', 101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db',
    106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg',
    }

_ss2ss = { 0: 'L', 1: 'H', 2: 'S' }

_colors = [(1,(0,0,0)),(2,(160,160,160)),(3,(0,0,180)),
           (4,(30,30,225)),(5,(100,100,225)),(6,(112,219,147)),(7,(173,234,234)),
           (8,(0,255,127)),(9,(0,100,0)),(10,(30,225,30)),(11,(50,204,50)),
           (12,(153,204,30)),(13,(225,225,30)),(14,(234,130,50)),
           (15,(142,35,107)),(16,(225,30,30)),(17,(255,152,163)),
           (18,(234,173,234)),(19,(225,30,225)),(20,(159,95,159)),
           (21,(255,255,255)),(22,(165,42,42)),(23,(225,127,80)),
           (24,(105,105,105)),(25,(225,193,37)),(26,(225,105,180)),
           (27,(107,142,35)),(28,(205,133,63)),(29,(160,82,45)),(30,(70,130,180)),
           (31,(216,191,216)),(32,(245,222,179)),(33,(7,7,255)),(34,(15,15,255)),
           (35,(23,23,255)),(36,(31,31,255)),(37,(39,39,255)),(38,(47,47,255)),
           (39,(55,55,255)),(40,(63,63,255)),(41,(71,71,255)),(42,(79,79,255)),
           (43,(87,87,255)),(44,(95,95,255)),(45,(103,103,255)),
           (46,(111,111,255)),(47,(119,119,255)),(48,(127,127,255)),
           (49,(135,135,255)),(50,(143,143,255)),(51,(151,151,255)),
           (52,(159,159,255)),(53,(167,167,255)),(54,(175,175,255)),
           (55,(183,183,255)),(56,(191,191,255)),(57,(199,199,255)),
           (58,(207,207,255)),(59,(215,215,255)),(60,(223,223,255)),
           (61,(231,231,255)),(62,(239,239,255)),(63,(247,247,255)),
           (64,(255,255,255)),(65,(255,7,7)),(66,(255,15,15)),(67,(255,23,23)),
           (68,(255,31,31)),(69,(255,39,39)),(70,(255,47,47)),(71,(255,55,55)),
           (72,(255,63,63)),(73,(255,71,71)),(74,(255,79,79)),(75,(255,87,87)),
           (76,(255,95,95)),(77,(255,103,103)),(78,(255,111,111)),
           (79,(255,119,119)),(80,(255,127,127)),(81,(255,135,135)),
           (82,(255,143,143)),(83,(255,151,151)),(84,(255,159,159)),
           (85,(255,167,167)),(86,(255,175,175)),(87,(255,183,183)),
           (88,(255,191,191)),(89,(255,199,199)),(90,(255,207,207)),
           (91,(255,215,215)),(92,(255,223,223)),(93,(255,231,231)),
           (94,(255,239,239)),(95,(255,247,247)),(96,(255,255,255)),
           (97,(44,60,60)),(98,(0,0,128)),(99,(34,139,34)),(100,(0,255,255)),
           (101,(220,20,60)),(102,(210,127,36)),(103,(192,192,192)),
           (104,(224,224,224)),(105,(255,30,0)),(106,(255,60,0)),(107,(255,90,0)),
           (108,(255,120,0)),(109,(255,150,0)),(110,(255,180,0)),
           (111,(255,210,0)),(112,(255,240,0)),(113,(255,255,0)),
           (114,(204,255,0)),(115,(153,255,0)),(116,(102,255,0)),(117,(51,255,0)),
           (118,(0,204,51)),(119,(0,153,102)),(120,(0,102,153)),(121,(0,51,204)),
           (122,(0,0,255)),(123,(15,0,255)),(124,(30,0,255)),(125,(45,0,255)),
           (126,(60,0,255)),(127,(75,0,255)),(128,(90,0,255)),(129,(255,0,31)),
           (130,(223,63,0)),(131,(191,127,25)),(132,(255,191,51)),
           (133,(223,223,0)),(134,(191,255,51)),(135,(159,255,0)),
           (136,(127,191,25)),(137,(95,255,51)),(138,(63,191,76)),
           (139,(31,255,102)),(140,(0,191,127)),(141,(159,255,191)),
           (142,(159,210,255)),(143,(255,223,159)),(144,(191,159,255)),
           (145,(95,63,255)),(146,(0,31,191)),(147,(191,0,191)),(148,(255,0,159)),
           (149,(0,255,51)),
           (150,    (   0,   255,       102)),
           (151,    (   0,   255,       153)),
           (152,    (   0,   255,       204)),
           (153,    (   0,   204,       255)),
           (154,    (   0,   153,       255)),
           (155,    (   0,   102,       255)),
           (156,    (   0,    51,       255)),
           (157,    ( 120,     0,       255)),
           (158,    ( 180,     0,       255)),
           ]

_color_dict = {}

_atom_rep = { 0:0x881, 2:0x802, 3:0x883 } # non-bonded + lines, sphere, ball & stick

_cartoon_rep = { 1:0x20, 2:0x20, 3:0x20, 4:0x30, 5:0x40, 6:0x40, 7:0x40 }

_bond_rep = { 0:0xF72, 1:0xFF2, 2:0xF71, 3:0xF73 } 


def prime_colors():
    for (key,rgb) in _colors:
        trgb = eval("0x%02x%02x%02x"%rgb)
        _color_dict[key] = trgb
        _color_dict[-key] = trgb        
        _color_dict[-1000-key] = trgb
        
class MAEReaderException(Exception):

    def __init__(self,value):
        self.value = value
    def __str__(self):
        return `self.value`
    
class MAEReader:

    def __init__(self):
        self.full_count = 0
        prime_colors()
        
    def next_quote(self):
        result = _match_quote_re.search(self.mae_st,self.quote_pos)
        if result != None:
            self.quote_pos = result.end()
        return result.group(1)

    def open_brace(self,tok):
        if self.stack[-1:] == ['f_m_ct']:
            self.full_bond_block = None
            self.full_atom_block = None
        self.meta_stack.append( (self.stack,self.spec) )
        self.stack = []
        self.spec = []
        
    def triple_colon(self,tok):
        if self.spec == []:
            self.spec = self.stack
            self.stack = []

    def parse_atom_block(self,count,spec,data,full):
        handler = {
            'i_m_mmod_type' : lambda x,a:setattr(a,'numeric_type',int(x)),
            'r_m_x_coord' : lambda x,a:a.coord.__setitem__(0,float(x)),
            'r_m_y_coord' : lambda x,a:a.coord.__setitem__(1,float(x)),
            'r_m_z_coord' : lambda x,a:a.coord.__setitem__(2,float(x)),
            'i_m_residue_number' : lambda x,a:setattr(a,'resi',x),
            'i_m_insertion_code' : lambda x,a:setattr(a,'ins_code',x),
#            's_m_mmod_res' : lambda x,a:setattr(a,'mmod_res',x),
            's_m_chain_name' : lambda x,a:setattr(a,'chain',x),
            'i_m_color' : lambda x,a:setattr(a,'trgb',_color_dict.get(int(x),16777215)),
            'r_m_charge1' : lambda x,a:setattr(a,'partial_charge',float(x)),
#            'r_m_charge2' : lambda x,a:setattr(a,'',x),
            's_m_pdb_residue_name' : lambda x,a:setattr(a,'resn',x),
            's_m_pdb_atom_name' : lambda x,a:setattr(a,'name',x),
#            's_m_grow_name' : lambda x,a:setattr(a,'',x),
            'i_m_atomic_number' : lambda x,a:setattr(a,'symbol',_p2sym.get(int(x),'X')),
            'i_m_formal_charge' : lambda x,a:setattr(a,'formal_charge',int(x)),
#            's_m_atom_name' : lambda x,a:setattr(a,'mae_name',x),
            'i_m_secondary_structure' : lambda x,a:setattr(a,'ss',_ss2ss.get(int(x),'L')),
            's_m_label_format' : lambda x,a:setattr(a,'label_format',x),
            'i_m_label_color' : lambda x,a:(
            setattr(a,'label_trgb',_color_dict.get(int(x),16777215))),
            's_m_label_user_text' : lambda x,a:setattr(a,'label_user_text',x),
            'i_m_ribbon_style' : lambda x,a:(
            setattr(a,'visible',a.visible|_cartoon_rep.get(int(x),0))),
            'i_m_representation' : lambda x,a:(
            setattr(a,'visible',a.visible|_atom_rep.get(int(x),0))),
            'i_m_ribbon_color' : lambda x,a:(
            setattr(a,'ribbon_trgb',_color_dict.get(int(x),16777215)),
            setattr(a,'cartoon_trgb',_color_dict.get(int(x),16777215))),                      
#            setattr(a,'cartoon_trgb',_rib_color(int(x)))),
            'i_m_visibility' : lambda x,a:setattr(a,'visibility',int(x)),
            'r_m_pdb_tfactor' : lambda x,a:setattr(a,'b',x),
#            'i_m_pdb_convert_problem' : lambda x,a:setattr(a,'',x),
            }
        fn_list = [ lambda x,a:setattr(a,'id',int(x)) ]
        for code in spec:
            fn_list.append(handler.get(code,lambda x,a:0))
        data.reverse()
        if full != None:
            count = len(data)/len(fn_list)
            atom_list = deepcopy(full)
        else:
            atom_list = []
        for a in xrange(count):
            if full == None:
                at = Atom()
                at.coord = [0.0,0.0,0.0]
                at.visible = 0
                at.mask = -1
                at.hetatm = 0
                atom_list.append(at)
            else:
                at = atom_list[int(data[-1])-1] # trusting index
            if 'i_m_representation' in spec: # representation information provided
                at.visible = 0
            elif full == None:
                at.visible = 0x880 # default: show nonbonded and lines by
            for fn in fn_list: 
                apply(fn,(data.pop(),at))
            if hasattr(at,'visibility'): # obey atom visibility flag
                if not at.visibility:
                    at.visible = at.visible & 0x70 # filter out all but cartoon
            if (at.visible & 0x3) == 0x3: 
                at.sphere_scale = 0.18 # default ball & stick scaling
            else:
                at.sphere_scale = 0.85 # default schrodinger CPK scaling
            if hasattr(at,'label_format'):
                if at.label_format != "%OF":
                    label = _unsupp_label_re.sub('',at.label_format)
                    label = label.replace("%UT",at.label_user_text)
                    label = label.replace("%RT",at.resn)
                    label = label.replace("%RN",at.resi)
                    label = label.replace("%CH",at.chain)                    
                    label = label.replace("%EL",at.symbol)
                    label = label.replace("%NU",str(at.id))
                    if at.formal_charge==0:
                        label = label.replace("%FC","")
                    elif at.formal_charge>0:
                        label = label.replace("%FC","+%d"%at.formal_charge)
                    else:
                        label = label.replace("%FC","%d"%at.formal_charge)                    
                    if len(label.replace(" ","")):
                        at.visible = 0x08 | at.visible # labels
                        at.label = label
                    elif hasattr(at,'label_trgb'):
                        del at.label_trgb
                del at.label_format
                
        for atom in atom_list:
            if hasattr(atom,'ins_code'):
                atom.resi=atom.resi+atom.ins_code
                del atom.ins_code
                
        return atom_list
    
    def parse_bond_block(self,count,spec,data,full):
        handler = {
            'i_m_from' : lambda x,a:a.index.__setitem__(0,int(x)-1),
            'i_m_to' : lambda x,a:a.index.__setitem__(1,int(x)-1),
            'i_m_order' : lambda x,a:setattr(a,'order',int(x)),
            'i_m_from_rep': lambda x,a:setattr(a,'from_rep',int(x)),
            'i_m_to_rep': lambda x,a:setattr(a,'to_rep',int(x)),            
            }
        fn_list = [ lambda x,a:setattr(a,'id',int(x)) ]
        for code in spec:
            fn_list.append(handler.get(code,lambda x,a:0))
        if full != None:
            count = len(data)/len(fn_list)
            bond_list = deepcopy(full)
        else:
            bond_list = []
        data.reverse()
        try:
            for a in xrange(count):
                if full == None:
                    bd = Bond()
                    bd.index = [0,0]
                    bond_list.append(bd)
                else:
                    bd = bond_list[int(data[-1])-1] # trusting index
                for fn in fn_list:
                    apply(fn,(data.pop(),bd))
        except IndexError:
            pass
        return bond_list

    def parse_ct_block(self,spec,data):
        handler = {
            's_m_title'   : lambda x,a:setattr(a,'title',x),
            'chempy_atoms' : lambda x,a:setattr(a,'atom',x),
            'chempy_bonds' : lambda x,a:setattr(a,'bond',x),
            's_m_entry_name' : lambda x,a:setattr(a,'name',x), 
            }
        fn_list = [ ]
        for code in spec:
            fn_list.append(handler.get(code,lambda x,a:0))
        bond_list = []
        data.reverse()
        mdl = Indexed()
        for fn in fn_list:
            apply(fn,(data.pop(),mdl))
        return mdl

    def close_brace(self,tok):
        (spec,data) = (self.spec,self.stack)
        (self.stack,self.spec) = self.meta_stack.pop()
        if len(self.stack):
            tag = self.stack.pop()
            if cmd.is_string(tag):
                if tag[0:7]=='m_atom[' and tag[-1:]==']':
                    self.spec.append('chempy_atoms')
                    cur_atom_block = self.parse_atom_block(int(tag[7:-1]),
                                                           spec,
                                                           data,
                                                           self.full_atom_block)
                    self.stack.append( cur_atom_block )
                    if self.full_atom_block == None:
                        self.full_atom_block = cur_atom_block
                elif tag[0:7]=='m_bond[' and tag[-1:]==']':
                    self.spec.append('chempy_bonds')
                    expected_length = int(tag[7:-1])
                    cur_bond_block = self.parse_bond_block( int(tag[7:-1]),spec,
                                                            data,
                                                            self.full_bond_block)
                    if self.full_bond_block == None:
                        self.full_bond_block = cur_bond_block
                    bond_list = filter(lambda x:x.index[0]<x.index[1],cur_bond_block)
                    self.stack.append( bond_list )
                elif tag[0:6]=='f_m_ct':
                    self.spec.append('f_m_ct')
                    self.full_count = self.full_count + 1
                    rec = self.parse_ct_block(spec,data)
                    if rec:
                        rec.mae_record = 'f_m_ct'
                    self.stack.append( rec )
                elif tag[0:6]=='p_m_ct':
                    self.spec.append('p_m_ct')
                    rec = self.parse_ct_block(spec,data)
                    if rec:
                        rec.mae_record = 'p_m_ct'
                    self.stack.append( rec )
            else:
                self.stack.append(tag)
                
    def push(self,tok):
        if tok=='"':
            self.stack.append(self.next_quote())
        else:
            self.stack.append(tok)
    
    def listFromStr(self,mae_st):
        self.quote_pos = 0
        self.stack = []
        self.spec = []
        self.meta_stack = []
        self.full_atom_block = None
        self.full_bond_block = None
        
        if mae_st.find('\r'):
            mae_st = _crlf_re.sub('\n',mae_st)
        mae_st = _trunc_comment_re.sub('\n',mae_st)
        mae_st = _nuke_esc_quote_re.sub("",mae_st) # gotta do better than this!
        mae_st = string.replace(mae_st,"<>","0")
        self.mae_st = mae_st
        tq_st = _trunc_quote_re.sub('"',mae_st)
        _dispatch = {
            '{' : self.open_brace,
            ':::' : self.triple_colon,
            '}' : self.close_brace,
            }
        for tok in string.split(tq_st):
            if tok == '"':
                tok = self.next_quote()
            apply(_dispatch.get(tok,self.push),(tok,))
        return self.stack
        
    def fix_bond_reps(self,mdl):
        atom = mdl.atom
        for bond in mdl.bond:
            if hasattr(bond,'from_rep') and hasattr(bond,'to_rep'):
                from_mask = _bond_rep.get(bond.from_rep,0)
                to_mask = _bond_rep.get(bond.to_rep,0)
                to_rep = bond.to_rep
                from_at = atom[bond.index[0]]
                to_at = atom[bond.index[1]]
                
                if from_at.mask != -1:
                    from_at.mask = (from_at.mask | from_mask | to_mask)
                else:
                    from_at.mask = (from_mask | to_mask)

                if to_at.mask != -1:
                    to_at.mask = (to_at.mask | from_mask | to_mask)
                else:
                    to_at.mask = (from_mask | to_mask)

                if (from_at.mask|to_at.mask) & 0x2:
                    bond.stick_radius = 0.18 
                    if (from_at.mask|to_at.mask) & 0x1:
                        from_at.sphere_scale = 0.18
                        
        for at in mdl.atom:
            at.visible = at.visible & at.mask
