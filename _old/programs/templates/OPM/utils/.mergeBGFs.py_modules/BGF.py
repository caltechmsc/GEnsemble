#!/exec/python/python-2.4.2/bin/python
"""
BGF.py
Aug 12 2004 -(c)- caglar tanrikulu

Module containing BGF-file specific tools including:
(*) BgfAtom class:
        Stores atom information
(*) BgfFile class:
        Stores all components of a bgf file
        The structural information is stored as a sequence of 'BgfAtom's

 040812 # module for managing bgf file information.
 040901 # stable version with BgfAtom and BgfFile classes.
 041030 # work on BgfSeln class for selection over multiple BgfFiles
 050827 # added functions for fixing/freeing atoms & __cmp__() to the BgfAtom
           class
          added the resIDs field and getAtom() to the BgfFile class
 050829 # added functions for formatting BgfFile's for 2/3/4xx formats
          added BgfFile.format field (contains 2/3/4)
 071105 # added the copy function to the BgfFile class
          renamed function BgfFile.getAtom() to BgfFile.getAtomByIndex()
          renamed function BgfAtom.isHydrogen() to BgfAtom.is_hydrogen()
          added the functions getAtom(), getResidue() and getChain() to BgfFile,
           in order to return atoms, residues or chains as BgfAtom or BgfFile
           objects based on external atomNos, resIDs or chainIDs. 
 071107 # added a list of approved protein residue names as aminoAcidResNames
 071113 # added functions angle() and dihedral() and to make this function
           possible, also added a_dot_b(), a_cross_b() and rad2deg() 
 071201 # added totalCharge() and BgfFile.charge()
 071204 # added the 'safe' flag to BgfFile.readBgfFromLines()
          function BgfFile.setBgfVersion() is now called BgfFile.setVersion()
 071220 # also added the 'safe' flag to BgfFile.readBgf() and BgfFile._init_()
          functions formatFile3xx(), formatFile4xx(), formatFor3xx(),
           formatFor4xx() and isHydrogen() are removed
 080120 # added the rmsd() function to calculate RMSD between two BgfFiles
          added the BgfFile.getSidechain() function to retrieve sidechain atoms
           from a BgfFile
 080123 # reads the biogroup versions of caglar's modules
"""

import os, sys, re, string, math, copy
if '/project/Biogroup/scripts/python/.caglarsPythonModules' not in sys.path:
    sys.path.append('/project/Biogroup/scripts/python/.caglarsPythonModules')
import cutils as cu

#
#

version = '080120p'

#
# - BGF file constants:
#

# atoms names assumed to be backbone:
backboneAtomList = [' N   ', \
                    'HN   ', \
                    ' CA  ', \
                    'HCA  ', \
                    ' C   ', \
                    ' O   ', \
                    ' OXT ', \
                    'HOXT ']

# default values for the optional fields:
defaultBgfFields = {'fixed':0, 'field1':0, 'fsmA':0.0, 'fsmT':0 }
    
# dictionary for translating AA3 to A
aas_3to1 = {"ALA":'A', "CYS":'C', "ASP":'D', "GLU":'E', "PHE":'F', \
            "GLY":'G', "HIS":'H', "ILE":'I', "LYS":'K', "LEU":'L', \
            "MET":'M', "ASN":'N', "PRO":'P', "GLN":'Q', "ARG":'R', \
            "SER":'S', "THR":'T', "VAL":'V', "TRP":'W', "TYR":'Y', \
            "HSP":'B', "HSE":'J' };

# dictionary for translating A to AA3
aas_1to3 = {}
for aaa in aas_3to1.keys():
    aas_1to3[ aas_3to1[aaa] ] = aaa
del aaa

# names of approved amino acids in proteins (includes neutral residues)
aminoAcidResNames = ['ALA', 'APP', 'ARG', 'ARN', 'ASN', 'ASP', 'CYS', 'CYX', 'GLN', 'GLP', 'GLU', 'GLY', 'HIS', 'HOH', 'HSD', 'HSE', 'HSP', 'ILE', 'LEU', 'LYN', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']


#
# - General BGF file utilities:
#

def getAtomNumberFromLine(bgfline):
    """
getAtomNumberFromLine(bgfline):
    returns the atom number form a BGF ATOM/HETATM/CONECT/ORDER line
    """
    return int(bgfline[7:12])


# ----------------------------
#
# - Define the BgfAtom object:
#

class BgfAtom:
    """
    BgfAtom object stores atom information contained in the
    ATOM/HETATM, CONECT and ORDER lines
    """

    def __init__(self, *lines):
        """
    __init__(self, *lines):
        initialize atom with empty fields, or data from atom lines
        as provided

        attributes of the BgfAtom class are:
        self.aTag   = 0       # atom tag, 0->'ATOM  ', 1-> 'HETATM'
        self.aNo    = 0       # atom number
        self.aName  = ''      # atom name
        self.rName  = ''      # residue name
        self.chain  = ''      # chain name
        self.rNo    = 0       # residue number
        self.x      = 0.0     # x coordinate
        self.y      = 0.0     # y coordinate
        self.z      = 0.0     # z coordinate
        self.ffType = '     ' # forcefield type
        self.bonds  = 0       # number of connected bonds
        self.lpair  = 0       # number of lone pairs
        self.charge = 0.0     # atom charge
    
        the following fields have -ve default values in order to 
        differentiate between their initialized and unitintialized states
        self.fixed  = -1      # movable rec., 0-> free, 1-> fixed
        self.field1 = -1      # unknown field 1
    
        self.fsmA   = -1.0    # fsm atomic weight
        self.fsmT   = -1      # fsm solvation type
        
        self.CONECT =[]       # list of connected atoms
        self.ORDER  =[]       # bond order for connected atoms """
        
        # atom attributes
        # initialized to default values:
        self.aTag   = 0       # atom tag, 0->'ATOM  ', 1-> 'HETATM'
        self.aNo    = 0       # atom number
        self.aName  = ''      # atom name
        self.rName  = ''      # residue name
        self.chain  = ''      # chain name
        self.rNo    = 0       # residue number
        self.x      = 0.0     # x coordinate
        self.y      = 0.0     # y coordinate
        self.z      = 0.0     # z coordinate
        self.ffType = '     ' # forcefield type
        self.bonds  = 0       # number of connected bonds
        self.lpair  = 0       # number of lone pairs
        self.charge = 0.0     # atom charge

        # the following fields have -ve default values in order to 
        #  differentiate between their initialized and unitintialized states
        self.fixed  = -1      # movable rec., 0-> free, 1-> fixed
        self.field1 = -1      # unknown field 1

        self.fsmA   = -1.0    # fsm solvation per area (?)
        self.fsmT   = -1      # fsm solvation type (?)
        
        self.CONECT =[]       # list of connected atoms
        self.ORDER  =[]       # bond order for connected atoms

        # if BGF lines are provided, read them:
        if lines:
            for line in lines:  self.readBgfLine(line)

        
    def ATOMline(self):
        """
    ATOMline(self):
        returns a string: the BGF ATOM line """
        
        if self.aTag:
            output = 'HETATM'
        else:
            output = 'ATOM  '

        output += ' %5d %5s %3s %1s %4d %10.5f%10.5f%10.5f %5s%3d%2d %8.5f' % \
                  (self.aNo  ,\
                  self.aName ,\
                  self.rName ,\
                  self.chain ,\
                  self.rNo   ,\
                  self.x     ,\
                  self.y     ,\
                  self.z     ,\
                  self.ffType,\
                  self.bonds ,\
                  self.lpair ,\
                  self.charge)

        if self.fixed >= 0:
            output += '%2d%4d' % (self.fixed, self.field1)

            if self.fsmA > 0:
                output += '  %8.4f %3d' % (self.fsmA, self.fsmT)

        output += '\n'
        
        # return
        return output


    def CONECTline(self):
        """
    CONECTline(self):
        returns a string: the BGF CONECT line """
        output = ''
        
        if self.CONECT:
            output  = 'CONECT %5d' + ('%6d' * len(self.CONECT)) + '\n'
            output %= tuple([self.aNo] + self.CONECT)

        # return
        return output


    def ORDERline(self):
        """
    ORDERline(self):
        returns a string: the BGF ORDER line """
        output = ''

        if self.ORDER:
            output  = 'ORDER  %5d' + ('%6d' * len(self.ORDER)) + '\n'
            output %= tuple([self.aNo] + self.ORDER)
        
        # return
        return output


    def __str__(self):
        """
    __str__(self):
        prints atom lines """
        return self.ATOMline() + self.CONECTline() + self.ORDERline()

        
    def readBgfLine(self,line):
        """
    readBgfLine(self,line):
        enters info from ATOM/HETATM, CONECT and ORDER lines into a BgfAtom object """

        line = line.strip()
        
        if line[0:6] == 'ATOM  ' or line[0:6] == 'HETATM':

            if line[0:6] == 'HETATM':  self.aTag = 1

            self.aNo    =   int(line[ 7:12])  # atom numbers cannot be greater than 99999
            self.aName  =       line[13:18]
            self.rName  =       line[19:22]
            self.chain  =       line[23:24]
            self.rNo    =   int(line[25:29])  # doesn't support alternate placements of a residue
            self.x      = float(line[30:40])
            self.y      = float(line[40:50])
            self.z      = float(line[50:60])
            self.ffType =       line[61:66]
            self.bonds  =   int(line[66:69])
            self.lpair  =   int(line[69:71])
            self.charge = float(line[72:80])

            if len(line) > 80:  # if 332
                self.fixed  = int(line[80:82])
                self.field1 = int(line[82:86])
                
                if len(line) > 86:  # if 400
                    self.fsmA = float(line[88: 96])
                    if line[97:100]:
                        self.fsmT = int(line[97:100])
                    else:
                        self.fsmT = 0
            
        elif line[0:6] == 'CONECT' or line[0:6] == 'ORDER ':
            if not self.aNo:
                cu.die('readBgfLine:  Cannot read CONECT/ORDER data prior to ATOM data!')

            elif int(line[7:12]) != self.aNo:
                cu.die('readBgfLine:  The line read does not refer to the atom, "%d":\n%s' % (self.aNo, line))

            else:       # using re.split is OK in the following lines since aNo cannot be 6 digits
                if line[0:6] == 'CONECT':
                    conectInfoString = line[12:].strip()
                    if conectInfoString:
                        self.CONECT = cu.list2intList( re.split(r'\s+', conectInfoString) )
                
                else:   #elif line[0:6] == 'ORDER ':
                    if not self.CONECT:
                        cu.die('readBgfLine:  Cannot read ORDER data prior to CONECT data!')                        
                    else:
                        self.ORDER  = cu.list2intList( re.split(r'\s+', line[12:].strip()) )

                        if len(self.CONECT) != len(self.ORDER):
                            cu.die('readBgfLine:  CONECT and ORDER line elements do not match:\n%s%s' % \
                                (self.CONECTline(), line) )
            
        else:
            cu.die('readBgfLine:  Line provided does not carry any atom information:\n%s' % (line,))


    def __cmp__(self,other):
        """
    __cmp__(self,other):
        compares the atom with another atom to see if they are similar.
        comparison is done on the basis of:
        - residue ID and name
        - atom name
        - forcefield type
        returns 0 if similar, 1 if not"""
        if (self.rName == other.rName) and \
           (self.rNo == other.rNo) and \
           (self.chain == other.chain) and \
           (self.aName == other.aName) and \
           (self.ffType == other.ffType):
            return 0
        else:
            return 1

           
    def copy(self):
        """
    copy(self):
        returns a (deep)copy of the atom object """
        return copy.deepcopy(self)


    def element(self):
        """
    element(self):
        gets which element the atom is from its ff-type and returns it """
        elm =  self.ffType[0:2].replace('_','')
        if len(elm) == 2:
            elm = elm[0] + elm[1].lower()
        return elm
    
    
    def resID(self):
        """
    resID(self):
        returns the residue ID {res.no.}{chain} of the atom """
        return str(self.rNo) + self.chain

    def aaCode(self):
        """
    aaCode(self):
        returns the single-letter amino acid code of the atom """
        return aas_3to1.get(self.rName,'X')

    def free(self):
        """
    free(self):
        sets the movable rec. of the atom to 0"""
        self.fixed = 0
    
    def fix(self):
        """
    fix(self):
        sets the movable rec. of the atom to 1"""
        self.fixed = 1

    def setFormat(self, format=3):
        """
    setFormat(self, format=3):
        sets the atom line format to 'format' (2, 3, or 4) 
        """
        if format == 2:
            self.fixed = -1
            self.field1 = -1
            self.fsmA = -1.0
            self.fsmT = -1
        elif format == 3:
            if self.fixed  < 0:  self.fixed  = defaultBgfFields['fixed']
            if self.field1 < 0:  self.field1 = defaultBgfFields['field1']
            self.fsmA = -1.0
            self.fsmT = -1
        elif format == 4:
            if self.fixed  < 0:  self.fixed  = defaultBgfFields['fixed']
            if self.field1 < 0:  self.field1 = defaultBgfFields['field1']
            if self.fsmA < 0:  self.fsmA = defaultBgfFields['fsmA']
            if self.fsmT < 0:  self.fsmT = defaultBgfFields['fsmT']
        else:
            cu.die("BgfAtom.setFormat does not recognize the format: %d"%format)

        
    # ... checking atom properties:

    def is_hydrogen(self):
        """
    is_hydrogen(self):
        returns true if atom is a hydrogen atom """
        if self.ffType[0:2] == 'H_':
            return 1
        else:
            return 0
        

    def is_free(self):
        """
    is_free(self):
        returns true if atom is free"""
        if not self.fixed:   return 1
        else:                return 0
    
    def is_fixed(self):
        """
    is_fixed(self):
        returns true if atom is fixed"""
        if self.fixed:   return 1
        else:            return 0

    def is_backbone(self):
        """
    is_backbone(self):
        returns true if the atom is backbone (atom name is in the backbone atoms list)"""
        if self.aName in backboneAtomList:   return 1
        else:   return 0
        
    def is_sidechain(self):
        """
    is_sidechain(self):
        returns true if the atom is a 'sidechain' atom
        (atom name is not in the backbone atoms list)"""
        return (not self.is_backbone())
    
    # end of BgfAtom class #

        
#
# - Functions/Operations using the atom object:
#

# ... changing atom attributes:

def setFree(atom):
    """
setFree(atom):
    sets the movable rec. of the atom to 0
    """
    atom.fix()
    
def setFixed(atom):
    """
setFixed(atom):
    sets the movable rec. of the atom to 1
    """
    atom.free()


# ... checking atom properties:

def is_free(atom):
    """
is_free(atom):
    returns true if atom is free
    """
    return atom.is_free()
    
def is_fixed(atom):
    """
is_fixed(atom):
    returns true if atom is fixed
    """
    return atom.is_fixed()

def is_backbone(atom):
    """
is_backbone(atom):
    returns true if the atom is backbone (atom name is in the backbone
    atoms list)
    """
    return atom.is_backbone()

def is_sidechain(atom):
    """
is_sidechain(atom):
    returns true if the atom is 'sidechain' (atom name is not in the
    backbone atoms list)
    """
    return atom.is_sidechain()


# ... changing atom formatting/BGF version:
    
def guessBGFformat(atom):
    """
guessBGFformat(atom):
    returns the first integer of the BIOGRF version, based on the line length
    """
    if atom.fixed < 0:
        return 2
    elif atom.fsmA < 0:
        return 3
    else:
        return 4


# ... evaluating properties of two atoms:

def is_bonded(atom1, atom2):
    """
is_bonded(atom1, atom2):
    returns true if atoms are bonded
    """
    return is_12(atom1,atom2)


def is_12(atom1, atom2):
    """
is_12(atom1, atom2):
    returns true if atoms are bonded
    """
    for i in atom1.CONECT:
        if i == atom2.aNo:
            return 1
    else:
        return 0


def sqrDistance(atom1, atom2):
    """
sqrDistance(atom1, atom2):
    returns the distance squared (r^2) between two atoms
    """
    #return ( (atom2.x - atom1.x) ** 2 +\
    #         (atom2.y - atom1.y) ** 2 +\
    #         (atom2.z - atom1.z) ** 2  )
    # define vector a:
    a = ( (atom2.x-atom1.x), (atom2.y-atom1.y), (atom2.z-atom1.z) ) #1->2
    return a_dot_b(a,a)

def distance(atom1, atom2):
    """
distance(atom1, atom2):
    returns the distance r (in A) between two atoms
    """
    return math.sqrt( sqrDistance(atom1, atom2) )


def angle(atom1, atom2, atom3, radians=0):
    """
angle(atom1, atom2, atom3, radians=0):
    returns the angle theta (in degrees unless radians=1) between three 
    atoms around central atom, atom2
    """
    # define vectors a and b
    a = ( (atom1.x-atom2.x), (atom1.y-atom2.y), (atom1.z-atom2.z) ) #2->1
    b = ( (atom3.x-atom2.x), (atom3.y-atom2.y), (atom3.z-atom2.z) ) #2->3
    
    #                   a . b
    #  theta = arccos ( ------ )
    #                   |a||b|
    theta = math.acos( a_dot_b(a,b) / (math.sqrt(a_dot_b(a,a))*math.sqrt(a_dot_b(b,b))) )
    if radians:
        return theta
    else:
        return rad2deg(theta)     


def dihedral(atom1, atom2, atom3, atom4, radians=0):
    """
dihedral(atom1, atom2, atom3, atom4, radians=0):
    returns the torsion angle theta (in degrees unless radians=1) around 
    the bond between atom2 and atom3, assuming that the atoms are bonded 
    as 1-2-3-4
    """
    # define vectors a, b, and c between the atoms
    a = ( (atom2.x-atom1.x), (atom2.y-atom1.y), (atom2.z-atom1.z) ) #1->2
    b = ( (atom3.x-atom2.x), (atom3.y-atom2.y), (atom3.z-atom2.z) ) #2->3
    c = ( (atom4.x-atom3.x), (atom4.y-atom3.y), (atom4.z-atom3.z) ) #3->4

    # normal vectors to the planes defined by vectors a&b and b&c:
    bc = a_cross_b(a,b)
    ab = a_cross_b(b,c)
    
    # calculate magnitude of the angle between these two normal vectors:
    #                   ab . bc
    #  theta = arccos ( -------- )
    #                   |ab||bc|
    theta = math.acos( a_dot_b(ab,bc) / (math.sqrt(a_dot_b(ab,ab))*math.sqrt(a_dot_b(bc,bc))) )
    
    # to get the sign, we look at the direction of the vector abXbc =(ab x bc) and compare
    # it with vector b.  if the two vectors are in the same direction, the sign is negative
    abXbc = a_cross_b(ab,bc)
    if a_dot_b(b, abXbc) > 0:
        theta = -theta
    if radians:
        return theta     
    else:
        return rad2deg(theta)     


# mathematical functions used in the measurements between atoms

def a_dot_b(a,b): 
    """ 
a_dot_b(a,b): 
    returns the dot product of vector a=(ax,ay,az) with vector b=(bx,by,bz) 
    """  
    return float( (a[0]*b[0]) + (a[1]*b[1]) + (a[2]*b[2]) ) 

def a_cross_b(a,b): 
    """ 
a_cross_b(a,b): 
    calculates c, the cross product of vector a=(ax,ay,az) with b=(bx,by,bz) 
    returns vector c = a x b = (cz,cy,cz) as a tuple
    """  
    return ( (a[1]*b[2])-(a[2]*b[1]), \
             (a[2]*b[0])-(a[0]*b[2]), \
             (a[0]*b[1])-(a[1]*b[0]) )

def rad2deg(radians):
    """
rad2deg(radians):
    converts radians to degrees
    """
    return 180*(radians/math.pi)




# ---------------------------
#
# - Define the BgfFile class:
#

class BgfFile:
    """
    Class to contain collections of BgfAtoms.
    Each object contains a list of atoms, which are indexed consecutively
    starting from zero, as well as indexing information that relates chains
    and residues to these atoms.
    """

    def __init__(self, file=0, safe=0):
        """
    __init__(self, file=0, safe=0):
        creates a new, empty bgf-file object and, if a file is specified,
        populates this object with the contents of the file.
        if 'safe' is set, information after the charges is not read. 
        self.BIOGRF = ''    # Biograf version 
        self.DESCRP = 'bgf' # file descriptor
        self.REMARK = []    # REMARK list
        self.FF     = 'FORCEFIELD DREIDING'
        self.FORMAT = {'ATOM'  :'FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,i2,i4,f10.5)',
                       'CONECT':'FORMAT CONECT (a6,14i6)',
                       'ORDER' :'FORMAT ORDER (a6,i6,13f6.3)'}
        self.OTHER  = []    # a list of unresolved/unknown lines

        # file info:
        self.source  = ''   # file source
        self.nlines  = 0    # number of lines in file
        self.format  = 0    # bgf format: 2/3/4

        # atoms:
        self.a = []         # index of first atom in file is 0
        self.natoms  = 0    # number of atoms

        # bookkeeping:
        self.a2i = {}       # translates actual atomNo (a) to internal atomNo (i) 
                            # the following information is obtained from self.a2i: 
        self.max_aNo = 0    #  largest atom number in the file
        self.min_aNo = 99999#  smallest atom number in the file

        # compilation populates the data structures below:
          this allows the information to be reached in the order

              chains --> resIDs ---,-> internal atom numbers --,-> atom numbers
               (c)        (r)     /       (i)                 /      (a)
              resIDs ------------'                           /
              internal atom numbers ------------------------'

          however it is not possible to reach atom numbers directly.
    
        self.compiled = 0   # tells if the res/chain range info is compiled or not
        self.r2i = {}       # translates resID to atom ranges
        self.c2i = {}       # translates chain to atom ranges

                            # for .chains and .residues below: 
                            # (I'm assuming that chains may be broken in the BGF file,
                            # but that residues won't be broken) 

        self.chains = []    # keeps a list of chains
        self.residues = {}  # unlike .chains, .residues is a dictionary, where each 
                            #  chain name points to an array of resID's in that chain
        self.resIDs  = []   # keeps a list of residues
        self.nres    = 0    # number of residues
        self.nchains = 0    # number of chains """
        
        # bgf lines with default values:
        self.BIOGRF = ''    # Biograf version 
        self.DESCRP = 'bgf' # file descriptor
        self.REMARK = []    # REMARK list
        self.FF     = 'FORCEFIELD DREIDING'
        self.FORMAT = {'ATOM'  :'FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,i2,i4,f10.5)', \
                       'CONECT':'FORMAT CONECT (a6,14i6)', \
                       'ORDER' :'FORMAT ORDER (a6,i6,13f6.3)'}
        self.OTHER  = []    # a list of unresolved/unknown lines

        # file info:
        self.source  = ''   # file source
        self.nlines  = 0    # number of lines in file
        self.format  = 0    # bgf format: 2/3/4
        
        # atoms:
        self.a = []         # index of first atom in file is 0
        self.natoms  = 0    # number of atoms

        # bookkeeping:
        self.a2i = {}       # translates actual atomNo (a) to internal atomNo (i) 
                            # the following information is obtained from self.a2i: 
        self.max_aNo = 0    #  largest atom number in the file
        self.min_aNo = 99999#  smallest atom number in the file

        # compilation populates the data structures below:
        self.compiled = 0   # tells whether the res/chain range information is compiled or not
        self.r2i = {}       # translates resID to atom ranges
        self.c2i = {}       # translates chain to atom ranges

                            # for .chains and .residues below: 
                            # ( I'm assuming that chains may be broken in the BGF file,
                            # but that residues won't be broken) 

        self.chains = []    # keeps a list of chains
        self.residues = {}  # unlike .chains, .residues is a dictionary, where each chain
                            #  name points to an array of resID's in that chain
        self.resIDs  = []   # keeps a list of residues
        self.nres    = 0    # number of residues
        self.nchains = 0    # number of chains

        # if a filename is specified, read the file in:
        if file:  self.readBGF(file,safe)


    def __len__(self):
        """
    __len__(self):
        returns the number of atoms in the BgfFile object"""
        return self.natoms
    

    def __str__(self):
        """
    __str__(self):
        prints self as a .bgf file """
        lines = self.writeBgfToLines()
        return string.join(lines,'')


    def copy(self):
        """
    copy(self):
        returns a (deep)copy of the BgfFile object """
        return copy.deepcopy(self)
        


    def compile(self, forceCompile=0):
        """
    compile(self, forceCompile=0):
        compiles the chain and residue information on a BgfFile object
          (warns if recompiling without forceCompile set to true)
        by doing this, we have all the information on:
        - which residues are in the file       : self.r2i.keys()
        -   and where they start and end       : self.r2i
        - which chains are in the file         : self.chains
        -   and where they start and end       : self.c2i
        -   and which residues they contain    : self.resIDs
        -   and residues by chain              : self.residues
        - how many residues and chains we have : self.nres and self.nchains"""

        # warn if already compiled:
        if self.compiled and not forceCompile:
            cu.warn("BgfFile.compile(): BgfFile already compiled!")
        
        # go line by line to determine where chains are:
        start = 0                        # initialize for the 
        lastChain = self.a[0].chain      #   first atom and 
        self.c2i[lastChain] = []         #   its chain
        self.chains.append(lastChain)    #
        
        for i in range(self.natoms):
            
            curChain = self.a[i].chain

            if curChain != lastChain:    # chain has changed, need to enter range data!
                self.c2i[lastChain].append( (start, i) )   # save data for the prior chain
                start = i                                  # note the starting atom for the current chain
                
                if curChain not in self.chains:  # this is a brand new chain!
                    self.chains.append(curChain)    # write new chain into chain list
                    self.c2i[curChain] = []         #   and create a range array for it.

            lastChain = curChain

        self.c2i[curChain].append( (start, self.natoms) )  # record the last segment  
        self.nchains = len(self.chains)  # record the number of chains   


        # parse each chain and find residues:
        for chain in self.chains:               # for each chain:
            self.residues[chain] = []
            
            for sstart, sstop in self.c2i[chain]:   # for each segment in this chain:

                start = sstart                          # initialize for the 
                lastRes = self.a[sstart].resID()        #   first atom in this 
                self.residues[chain].append(lastRes)    #   range and its residue

                for i in range(sstart, sstop):          # for each atom in this range:
                    curRes = self.a[i].resID()

                    if curRes != lastRes:                   # if we started a new residue:
                        self.r2i[lastRes] = (start,i)           # save data for the prior residue
                        
                        start = i                               # note the starting atom for the current residue
                        self.residues[chain].append(curRes)     # write new residue into the res[chain] list

                    lastRes = curRes

                self.r2i[curRes] = (start, sstop)       # record the last segment  
                self.nres = len(self.r2i)               # record the number of residues   

            self.resIDs += self.residues[chain]

        # now we have finished compiling the residue/chain information:
        self.compiled = 1

        # done
        

    def readBgfFromLines(self,lines,safe=0):
        """
    readBgfFromLines(self,lines,safe=0):
        reads a list of BGF lines and populates basic fields
        if 'safe' is set, data after the charges are not read """

        aCount = 0          # counts atoms
                
        for line in lines:
            tag = re.split(r'\s+', line)[0]

            if tag == 'ATOM' or tag == 'HETATM':

                if safe:
                    line = line[:80] # do not read anything after 80 chars
                
                atom = BgfAtom()
                atom.readBgfLine(line.strip())
                self.format = max(self.format, guessBGFformat(atom))
                self.a.append(atom)
                
                self.a2i[atom.aNo] = aCount
                self.max_aNo = max(atom.aNo, self.max_aNo)
                self.min_aNo = min(atom.aNo, self.min_aNo)

                aCount += 1

            elif tag == 'CONECT' or tag == 'ORDER':
                aNo = getAtomNumberFromLine(line)
                self.a[ self.a2i[aNo] ].readBgfLine(line)

            elif tag == 'REMARK':
                self.REMARK.append( line.strip()[7:] )

            elif tag == 'FORMAT':
                if re.search(r'^FORMAT ATOM', line):
                    self.FORMAT['ATOM'] = line.strip()                    
                elif re.search(r'^FORMAT CONECT', line):
                    self.FORMAT['CONECT'] = line.strip()                    
                elif re.search(r'^FORMAT ORDER', line):
                    self.FORMAT['ORDER'] = line.strip()                    
                else:
                    cu.die("readBgfFromLines: Unkown FORMAT line:\n%s" % line)

            elif tag == 'DESCRP':
                self.DESCRP = line[7:].strip()

            elif tag == 'BIOGRF':
                self.BIOGRF = line[7:].strip()

            elif tag == 'FORCEFIELD':
                self.FF = line.strip()

            elif tag == 'REM' or \
                 tag == 'PHI' or \
                 tag == 'PSI':       # these are fields in the rotamer library
                self.OTHER.append(line)

            elif tag == 'END':
                break

            else:
                cu.warn("readBgfFromLines: Encountered unkown field:\n%s" % line)
                line = line.strip()
                if line:
                    self.OTHER.append(line)
        else:
            if self.source[-4:] != '.lib':
                cu.warn("readBgfFromLines:  Did not see the 'END' tag at the end of file, %s!" % self.source)

        self.natoms  = aCount


    def readBGF(self,file,safe=0):
        """
    readBGF(self,file,safe=0):
        reads a .bgf file into self
        if 'safe' is set, data after the charges are not read """

        # read bgf file:
        lines = cu.readLinesFromFile(file)
        
        # modify bgf info fields:
        self.source = file
        self.DESCRP = file[0:8]    
        self.nlines = len(lines)
        
        # read structure information:
        self.readBgfFromLines(lines,safe)


    def writeBgfToLines(self):
        """
    writeBgfToLines(self):
        writes self into a list of lines and returns it """
        lines = []

        lines.append("BIOGRF  %s\n" % self.BIOGRF)    # Biograf version
        lines.append("DESCRP %s\n"  % self.DESCRP)    # File descriptor

        for entry in self.OTHER:                      # Unknown entries that are not 
            lines.append("%s\n" % entry)              #  empty lines

        for entry in self.REMARK:                     # Remarks
            lines.append("REMARK %s\n" % entry)

        lines.append("%s\n" % self.FF)                # Forcefield line

        lines.append("%s\n" % self.FORMAT['ATOM'])    # FORMAT ATOM line

        for atom in self.a:                           # ATOM lines
            lines.append(atom.ATOMline())

        lines.append("%s\n" % self.FORMAT['CONECT'])  # FORMAT CONECT line
        lines.append("%s\n" % self.FORMAT['ORDER'])   # FORMAT ORDER line        

        for atom in self.a:                           # CONECT and ORDER lines
            lines.append(atom.CONECTline())
            lines.append(atom.ORDERline())

        lines.append('END\n')                         # END

        # return
        return lines
    

    def saveBGF(self,file):
        """
    saveBGF(self,file):
        writes self into a file """
        # write bgf file into text:
        lines = self.writeBgfToLines()    
        
        # save structure information:
        cu.writeLinesToFile(lines,file)



    def addAtom(self,atom):
        """
    addAtom(self,atom):
        adds a new atom to self; renumbers atom if necessary """
        atom = atom.copy()   # create a copy (not reference)
        self.a.append(atom)  # add new atom

        if self.a2i.has_key(atom.aNo):   # aNo exists, need to renumber this atom:
            atom.aNo = self.max_aNo + 1
            
        self.a2i[atom.aNo] = self.natoms            #
        self.max_aNo = max(atom.aNo, self.max_aNo)  #
        self.min_aNo = min(atom.aNo, self.min_aNo)  # ... fill in the rest ...
                                                    #
        self.natoms += 1                            #

        if self.compiled:
            # need to update the compiled records
            # at this point!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.compiled = 0
        # done


    def delAtom(self,index):
        """
    delAtom(self,index):
        deletes one atom from self, and updates all x2i information """
        if index < 0 and index >= self.natoms:  # if atom doesn't exist: 
            cu.die('BgfFile.delAtom: Atom at index "%d" does not exist' % index)

        del self.a2i[self.a[index].aNo]     # delete the a2i record
        del self.a[index]                   # delete the atom

        self.natoms -= 1                    # update no.of atoms

        for i in range(index, self.natoms): # decrement/update all the a2i 
            atom = self.a[i]                #  records that come after this
            self.a2i[atom.aNo] = i           #  index number

        if self.compiled:
            # need to update the compiled records
            # at this point!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.compiled = 0

        self.max_aNo = max( self.a2i.keys() ) # ... update constants ...
        self.min_aNo = min( self.a2i.keys() ) #
        # done


    def delRange(self, iRange):
        """
    delRange(self, iRange):
        deletes atoms indicated by a range of indices from self """
        if iRange[1] > self.natoms:
            cu.die('BgfFile.delAtom:  Range (%d,%d) extends outside the current atom list!' % iRange)

        for index in range(iRange):
            del self.a2i[self.a[index].aNo]     # delete the a2i record
            del self.a[index]                   # delete the atom            
            self.natoms -= 1                    # update no.of atoms

        for i in range(iRange[0], self.natoms): # decrement/update all the a2i 
            atom = self.a[i]                    #  records that come after this
            self.a2i[atom.No] = i               #  index number

        if self.compiled:
            # need to update the compiled records
            # at this point!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.compiled = 0

        self.max_aNo = max( self.a2i.keys() ) # ... update constants ...
        self.min_aNo = min( self.a2i.keys() ) #
        # done


    def addAtoms(self,atoms):
        """
    addAtoms(self,atoms):
        adds a list of atoms to self """
        for atom in atoms:  self.addAtom(atom)


    def delAtoms(self,indices):
        """
    delAtoms(self,indices):
        deletes atoms indicated by a list of indices from self """
        for index in indices:  self.delAtom(index)

        
    def __add__(self,other):
        """
    __add__(self,other):
        merges two bgf files into one BgfFile object
        dereferences all information when moving it to the newly created object
        returns the new BgfFile object """
        result = copy.deepcopy(self)
        # !!! in the future:  instead of deepcopy, keep atom list as a reference
        # !!!  and deepcopy all other fields like the res.lists and stuff...

        # figure out whether to renumber other's atom numbers before merging:
        if self.max_aNo < other.min_aNo:
            increment = 0
        else:
            increment = self.max_aNo - other.min_aNo + 1

        # renumber atoms of other, adding them the increment
        #  and add these atoms to sum:
        for atom in copy.deepcopy(other.a):
            if increment:
                atom.aNo += increment
                for i in range(len(atom.CONECT)):   atom.CONECT[i] += increment

            result.a.append(atom)               # not using the addAtom() function here
            result.a2i[atom.aNo] = result.natoms#  so that we don't check for renumbering
            result.natoms += 1                  #  each time we read a line from the file

        # adjust the remaining variables:
        result.max_aNo = max( result.a2i.keys() )
        result.min_aNo = min( result.a2i.keys() )
        
        # return:
        return result 


    def __radd__(self,other):
        """
    __radd__(self,other):
        reverse __add__ """
        return BgfFile.__add__(other, self)


    def renumber(self,start=1):
        """
    renumber(self,start=1):
        renumbers all atom numbers (.aNo) in the BgfFile starting from 'start' """
        old2new_aNo = {}
        a2i = {}
        
        # renumber ATOM lines:
        for i in range(self.natoms):
            cur_aNo = i + start

            old2new_aNo[ self.a[i].aNo ] = cur_aNo
            self.a[i].aNo = cur_aNo

            a2i[cur_aNo] = i

        # save new a2i array
        self.a2i = a2i

        # renumber CONECT lines:
        for i in range(self.natoms):
            newConectList = []
            myConectList = self.a[i].CONECT

            for j in range(len( myConectList )):
                connectedAtom = myConectList[j]
                if old2new_aNo.has_key(connectedAtom):
                    newConectList.append(old2new_aNo[connectedAtom])
            self.a[i].CONECT = newConectList
 
            if (len(newConectList) != len(myConectList)) and self.a[i].ORDER:
                newOrderList = []
                myOrderList  = self.a[i].ORDER
                for j in range(len( myConectList )):
                    connectedAtom = myConectList[j]
                    if old2new_aNo.has_key(connectedAtom):
                        newOrderList.append(myOrderList[j])
                self.a[i].ORDER  = newOrderList
        # done


    def aaCode3(self, resID):
        """
    aaCode3(self, resID):
        returns the 3-letter a.a. code of the current residue """
        if not self.compiled:
            self.compile()

        start,stop = self.r2i.get(resID, (-1,-1))

        # return:
        if start < 0:
            cu.die("aaCode: No such resID, %s, in BgfFile object!" % resID)
        else:
            return self.a[start].rName


    def aaCode(self, resID):
        """
    aaCode(self, resID):
        returns the 1-letter a.a. code of the current residue """
        return aas_3to1[ self.aaCode3(resID) ]


    def setFormat(self, format=3):
        """
    setFormat(self, format=3):
        sets the BgfFile atom line format to 'format' (2, 3, or 4) for each atom"""
        for i in range(self.natoms):
            self.a[i].setFormat(format)

    def setVersion(self,version):
        """
    setVersion(self,version):
        sets the BIOGRF line to 'version' and formats all atom lines accordingly"""
        version = str(version).strip()
        self.BIOGRF = version
        
        if version[0] == '4':
            self.setFormat(4)
        elif version[0] == '3':
            self.setFormat(3)
        elif version[0] == '2':
            self.setFormat(2)
        else:
            pass
        # done

    
    def charge(self):
        """
    charge(self):
        returns the sum of the charges of all atoms in the BgfFile object"""
        totalCharge = 0.0
        for i in range(self.natoms):
            totalCharge += self.a[i].charge
        
        return totalCharge


    def getAtomByIndex(self,intAtomNo=0):
        """
    getAtomByIndex(self,intAtomNo=0):
        returns the atom object indicated by the internal atom no (intAtomNo)"""
        return self.a[intAtomNo]


    # functions to return atoms, residues, chains without the need to deal with atom indices

    def getAtom(self, atomNo):
        """
    getAtom(self, atomNo):
        returns the BgfAtom specified by the atom number"""
        index = self.a2i.get(atomNo, (-1))

        # return:
        if index < 0:
            cu.die("getAtom: No such atom number, %s, in BgfFile object!" % atomNo)
        else:
            return self.a[index]
        
    
    def getResidue(self, resID):
        """
    getResidue(self, resID):
        returns the residue specified by the residue ID as a BgfFile object"""
        if not self.compiled:
            self.compile()

        start,stop = self.r2i.get(resID, (-1,-1))

        if start < 0:
            cu.die("getResidue: No such resID, %s, in BgfFile object!" % resID)

        myResidue = BgfFile()
        for index in range(start,stop):
            myResidue.addAtom( self.a[index] )

        myResidue.BIOGRF = self.BIOGRF
        
        # return:
        return myResidue
    
    
    def getChain(self, chainID):
        """
    getChain(self, chainID):
        returns the chain specified by the residue ID as a BgfFile object"""
        if not self.compiled:
            self.compile()

        atomRangeList = self.c2i.get(chainID,[])
        if not atomRangeList:
            cu.die("getChain: No such chainID, %s, in BgfFile object!" % chainID)
                
        myChain = BgfFile()
        for (start,stop) in atomRangeList:
            for index in range(start,stop):
                myChain.addAtom( self.a[index] )

        myChain.BIOGRF = self.BIOGRF

        # return:
        return myChain
    

    def getSidechain(self, resID=''):
        """
    getSidechain(self, resID=''):
        returns the sidechain atoms in the BgfFile as a BgfFile object.
        if resID is defined, only the sidechain atoms in that residue are returned."""
        if not self.compiled:
            self.compile()

        if resID:
            mybgf = self.getResidue(resID)
        else:
            mybgf = self

        sidechainAtoms = BgfFile()
        for index in range(mybgf.natoms):
            if mybgf.a[index].is_sidechain():
                sidechainAtoms.addAtom( mybgf.a[index] )
                
        sidechainAtoms.BIOGRF = self.BIOGRF
        
        # return:
        return sidechainAtoms
    
    
    ### end of BgfFile class ###



#
# - functions using BgfFiles:
#

def saveBGF(bgffile, filename):
    """
saveBGF(bgffile, filename):
    same as BgfFile.saveBGF
    """
    bgffile.saveBGF(filename)

def readBGF(filename):
    """
readBGF(filename):
    returns a BgfFile object read from 'filename'
    """
    return BgfFile(filename)


def guessFileFormat(myBGF):
    """
guessFileFormat(myBGF):
    based on the values read its atoms, evaulates the format
    of the BgfFile myBGF:  returns 2, 3, or 4
    *** BgfFile(filename).format makes this obsolete ***    
    """
    for i in range(myBGF.natoms):
        if myBGF.a[i].field1 >= 0:
            break
    else:
        return 2

    for i in range(myBGF.natoms):
        if myBGF.a[i].fsmT >= 0:
            break
    else:
        return 3
    return 4
    

def totalCharge(myBGF):
    """
totalCharge(myBGF):
    returns the sum of the charges of all atoms in the BgfFile object
    """
    return myBGF.charge()


def rmsd(myBGF1,myBGF2):
    """
rmsd(myBGF1,myBGF2):
    returns the RMSD (in A) between the two BgfFile objects, myBGF1 and myBGF2,
    that share the same structure
    """
    natoms = myBGF1.natoms
    if natoms != myBGF2.natoms:  # check natoms
        cu.die("BGF: rmsd: BgfFile objects don't contain the same number of atoms: %d =/= %d"%(natoms,myBGF2.natoms))

    sumOfSqrDist = 0.0
    for i in range(natoms):
        if myBGF1.a[i] != myBGF2.a[i]:  # check atoms
            cu.die("BGF: rmsd: Atom number %d refers to different atoms in the BgfFile objects provided."%i)
        sumOfSqrDist += sqrDistance(myBGF1.a[i], myBGF2.a[i])

    myRMSD = math.sqrt(sumOfSqrDist / natoms)

    return myRMSD




# --------------------------------
#
# - Define the BgfSeln class:
#     for handling selections within BGF files
# 

# ... first need to define functions dealing with atom ranges:

#def reduce_iRanges(*iRanges):
#    """ """
#    # nothing here yet....
#    return new_iRanges


# ... now define the class:

class BgfSeln:
    """
    Class to store selections of atoms over multiple BgfFile objects.
    Each object contains a list of BgfFiles, and start/stop ranges for
    each selected atom/group of atoms. 
    """
    
    def __init__(self):
        """
    __init__(self):
        creates a new empty BgfSeln object:
        self.files     = [] # stores the BgfFile objects in the selection 
        self.nfiles    = 0  # stores the number of files in the current selection
        self.selection = [] # stores an array of atom ranges (start,stop) for each file"""

        # empty object attributes:
        self.files     = [] # stores the BgfFile objects in the selection 
        self.nfiles    = 0  # stores the number of files in the current selection
        self.selection = [] # stores an array of atom ranges, e.g. (start, stop) for each file



    def addFile(self, bgffile, SelnList=None):
        """
    addFile(self, bgffile, SelnList =None):
        adds a new BgfFile to the self.files list and selects the range(s) in the
        SelnList if specified, or all atoms otherwise"""
        # check for bgffile in seln:
        if self.fileInSeln(bgffile): 
            cu.die("BgfSelection.addFile: Cannot add BgfFile to selection, BgfFile already in the file list!")

        # add new file:
        bgffile.compile()
        self.files.append(bgffile)
        self.nfiles += 1
        if SelnList == None:
            self.selection.append( [ (0, bgffile.natoms) ] )
        else:
            self.selection.append( SelnList )

        

    def addFiles(self, List):
        """
    addFiles(self, List):
        adds the BgfFiles in the List to the self.files list and selects
        all atoms in these files """
        for bgffile in List:
            self.addFile(bgffile)


    def rmFile(self, bgffile):
        """
    rmFile(self, bgffile):
        remove a BgfFile from the selection"""
        # check for bgffile in seln:
        index = self.fileInSeln(bgffile)
        if not index:
            cu.warn("BgfSelection.addFile: Cannot remove BgfFile from the selection: BgfFile not in the file list!")
        else:
            # remove file:
            del self.files[index]
            del self.selection[index]
            self.nfiles -= 1
        

    def rmFiles(self, List):
        """
    rmFiles(self, List):
        remove the BgfFiles in the List from the selection"""
        for bgffile in List:
            self.rmFile(bgffile)


    def assignDefaultFile(self):
        """
    assignDefaultFile(self):
        returns the first BgfFile in the self.files list if it exists"""
        if self.nfiles:
            return self.files[0]
        else:
            cu.die('BgfSelection.assignDefaultFile:  Cannot operate on empty selection!')
            

############## SHOULD THIS BE LIKE THIS???? ################
    def addAtom(self, atomNo, bgffile=None):
        """
    addAtom(self, atomNo, bgffile=None):
        add a single atom by its atom number from bgffile to the selection"""
        if not bgffile:
            bgffile = self.assignDefaultFile()   # default BgfFile
            fileIndex = 0
        else:
            fileIndex = self.fileInSeln(bgffile) # BgfFile already here
            if fileIndex == None:
                self.addFile(bgffile,[])         # brand new BgfFile
                fileIndex = self.nfiles - 1
                
        # get internal atom number
        atomIndex = bgffile.a2i(atomNo)
        range     = (atomIndex, atomIndex+1)
        self.selection[index] = addRangeToRanges(range, self.selection[index])


    def addAtoms(self, atoms, file=0):
        """"""
        if not file:   file = self.assignDefaultFile()


    def addResidue(self, residue, file=0):
        """"""
        if not file:   file = self.assignDefaultFile()

    def addResidues(self, residues, file=0):
        """"""
        if not file:   file = self.assignDefaultFile()



    def addChain(self, chain, file=0):
        """"""
        if not file:   file = self.assignDefaultFile()

    def addChains(self, chains, file=0):
        """"""
        if not file:   file = self.assignDefaultFile()


    def fileInSeln(self, bgffile, dieIfAbsent=0):
        """
    fileInSeln(self, bgffile, dieIfAbsent=0):
        returns the (negative) index of the file if it is in selection, None if
        not if dieIfAbsent is true, run will die if file is not in selection"""
        count = self.nfiles * -1
        for file in self.files:
            count += 1
            if file == bgffile:
                cu.warn("BgfSelection.addFile: Cannot add BgfFile to selection, BgfFile already in the file list!")
                # return file index: file in selection 
                return count    
        # return False: file not in selection
        if dieIfAbsent:
            cu.die("BgfSelection.fileInSeln: No such BgfFile in selection!")
        else:
            return None


############## SHOULD THIS BE LIKE THIS???? ################
    def setupBgfFile(self, bgffile):
        """
    setupBgfFile(self, bgffile):
        for an arbitrary BgfFile entered, returns the BgfFile and its index back
        """
        if not bgffile:
            bgffile = self.assignDefaultFile()   # default BgfFile
            fileIndex = 0
        else:
            fileIndex = self.fileInSeln(bgffile) # BgfFile already here
            if fileIndex == None:
                self.addFile(bgffile,[])         # brand new BgfFile (empty selection)
                fileIndex = self.nfiles - 1
        
        # return BgfFile, index of BgfFile in self.files
        return bgffile, index


    def limitToResID(self, resIDs):
        """"""

    def limitToFFtype(self, ffTypes):
        """"""

    def limitToMovable(self):
        """"""

    def limitToMovable(self):
        """"""

    def limitToSidechain(self):
        """"""

    def limitToBackbone(self):
        """"""



    ### end of BgfSelection class ###


#
# Functions using selections:
#







#-------------------------------------
#
# - Print information
#
if __name__ == '__main__':

    # get directory:
    directory = dir()

    # set imported stuff we don't want to see:
    imported = ['os', 'sys', 'math', 'string', 'copy', 're', 'cu']

    # print __doc__ for the module:
    print
    print ( '-'*60 )
    if 'version' not in directory:  version = '??????'
    print "%-45s%15s" % (os.path.basename(sys.argv[0]), 'ver: '+version)

    print ( '-'*60 )
    print __doc__


    # import types:
    import types

    # create hash-table:
    hashtable = {}
    for item in directory:
        actual_item = eval(item)
        if item in imported:
            # don't show imported stuff:
            pass
        elif type(actual_item) is types.ModuleType:
            # don't discuss other modules:
            pass
        elif type(actual_item) is types.FunctionType:
            # show __doc__s for functions:
            hashtable[item] = actual_item.__doc__
        elif type(actual_item) is types.ClassType:
            # show __doc__s for classes:
            title = item+' class: '
            hashtable[item] = title +  ( '-' * (60-len(title)) )
            hashtable[item] += actual_item.__doc__

            # show __doc__s for class elements:
            for classItem in dir(actual_item):
                actual_class_item = eval(item+'.'+classItem)
                if type(actual_class_item) is types.ModuleType:
                    # don't discuss other modules:
                    pass
                elif type(actual_class_item) is types.UnboundMethodType \
                         or type(actual_class_item) is types.MethodType:
                    # show __doc__s for functions:
                    hashtable[item] += actual_class_item.__doc__ + '\n'

                elif classItem in ['__doc__','__module__']:
                    pass
                else:
                    # for other stuff show the value:
                    hashtable[item] += '\n'+classItem+' = '+str(actual_class_item)+'\n'

            hashtable[item] +=  ( '-'*60 )+'\n\n'
            
        elif item[0] != '_':
            # for other stuff show the value:
            hashtable[item] = '\n'+item+' = '+str(actual_item)+'\n'

    # print info out
    keys = hashtable.keys()
    keys.sort()
    
    print 'Contents:'
    print ( '-'*60 )
    for item in keys:
        #print ( '--- '*6 ),
        #print ' ', 
        print hashtable[item],

    print
    print ( '-'*60 )
    print 'contact:  caglar@wag.caltech.edu'
    print ( '-'*60 )
    print
    
    # done!
