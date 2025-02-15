#!/usr/bin/env python

# This module converts SCREAM atoms to OBMOL atoms and back.

import modbabel
import Py_Scream_EE

def InitOBMolFromScream (ScreamModel, OBMol):

    # Needs to be done:
    # Use OBtot functions to, 1) add new residue 2) add new atoms 3) take care of bonding info.

    OBMol.BeginModify()

    # Map each SCREAM atom into a new OBAtom, and make new residue along the way.
    ptn = ScreamModel.ptn # ptn stands for Protein.  A protein is the main data structure in SCREAM.
    screamAtomList = ptn.getNewAtomList()

    currentAtomNum = 0

    lastResNum = '_____'
    lastChain = '_____'
    currentResNum = '_____'
    currentChain = '_____'
    tmpObResidue = ''

    i = 0
    
    for atom in screamAtomList:
        i += 1
        #print i
        obAtom = OBMol.NewAtom()
        currentAtomNum = atom.n
        currentResNum = atom.getResNum()
        currentChain = atom.getChain()
        currentResName = atom.getResName()
        # Atom copying
        mapScreamAtomToOBAtom(atom,obAtom)

        # Residue making
        # if lastChain != currentChain and lastResNum != currentResNum:
#             obResidue = OBMol.NewResidue()
            
#             obResidue.SetName(currentResName)
#             obResidue.SetNum(currentResNum)
#             obResidue.SetChain(currentChain)
#             #obResidue.SetIdx(currentResNum)
#             obResidue.AddAtom(obAtom)

        # Do OBBonds
        scream_map = atom.connectivity_m

        for connectedAtom in scream_map:
            thisAtomNum = connectedAtom.n
            bondOrder = scream_map[connectedAtom]
            OBMol.AddBond(currentAtomNum, thisAtomNum, bondOrder)
            #print connectedAtom
            

    OBMol.EndModify()


def InitScreamFromOBMol (OBMol, ScreamModel):

    # Needs to be done:
    # Figure out exactly what needs to be initialized in ScreamModel.

    pass

def OBToSCREAM (ObTot, ScreamModel):

    # just map each OB atom to a scream atom
    pass


def SCREAMToOB (ScreamModel, OBTot):

    # just map each scream atom to an OB atom.  Initilization unnecessary.
    pass

def SCREAMToOB_xyz_only(ScreamModel, OBtot):

    scream_atom_list = ScreamModel.ptn.getNewAtomList()

    for i in scream_atom_list:
        atom_n = i.n
        obatom = OBtot.GetAtom(atom_n)

        x = i.getX()
        y = i.getY()
        z = i.getZ()

        obatom.SetVector(x, y, z)

    

def OBToSCREAM_xyz_only(OBtot, ScreamModel):
    
    natoms = OBtot.NumAtoms()

    scream_atom_list = ScreamModel.ptn.getNewAtomList()

    i=1
    while i<=natoms:
   	
	atom=OBtot.GetAtom (i)
	
	x=atom.GetX()
	y=atom.GetY()
	z=atom.GetZ()

        scream_atom_list[i-1].setX(x)
        scream_atom_list[i-1].setY(y)
        scream_atom_list[i-1].setZ(z)

        i = i + 1
                           
def mapScreamAtomToOBAtom (ScreamAtom, OBAtom):

    # map each SCREAM atom into a new OBAtom

    # following: all relevant set functions for an OBAtom
    
    OBAtom.SetIdx(ScreamAtom.n) # I.D.?
    
    #OBAtom.SetAtomicNum()

    OBAtom.SetVector(ScreamAtom.getX(), ScreamAtom.getY(), ScreamAtom.getZ())

    OBAtom.SetFixed(ScreamAtom.flags, ScreamAtom.flags, ScreamAtom.flags) # Fixed: 0 or 1 in OBMol?
    #OBAtom.SetTmp() # ?
    #OBAtom.SetTag() # ?
    OBAtom.SetLabel(ScreamAtom.getAtomLabel()) # Maybe use stripped_atomLabel instead
    OBAtom.SetFFType(ScreamAtom.getAtomType())
    OBAtom.SetGID(ScreamAtom.GLOBAL_ATOM_N) # Global ID?
    
    #OBAtom.SetPartialCharge() # ?
    OBAtom.SetCharge(ScreamAtom.getCharge()) # 
    #OBAtom.SetResidue(ScreamAtom.getResName()) # set residue done elsewhere
    # Is there a set chain name? Or is it expressed by "Molecule" structure for OBMol.
    
    pass
