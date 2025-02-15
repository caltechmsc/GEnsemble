#!/usr/bin/env python

import sys, timing, os, random, math
from Py_Scream_EE import *

'''Module for stuff involved in BiHelix calculations.
Assumptions: Input bgf file only has 2 chains, and they are chain A and chain B.
Output: 

MutInfoEnergies:'Res', 'Intern', 'Tot_EL', 'V_EL', 'C_EL', 'H_EL', 'Tot_ScSc', 'V_ScSc', 'C_ScSc', 'H_ScSc', 'Total'

BiHelixEnergies: 'Res', 'Intern', 'Tot_EL', 'EL_AA', 'EL_AB', 'Tot_Scsc', 'Scsc_AA', 'Scsc_AB', 'Total'

'''

def Print_Bihelix_Final_Residue_Energy_Breakdown_from_scratch(bgf_file, scream_par_file, output_file):
    # This function reads in new par file and calls Print_BiHelix_Final_Residue_Energy_Breakdown by supplying a new scream_EE.
    SCREAM_MODEL = ScreamModel(scream_par_file)
    (SCREAM_PARAMS, BGF_HANDLER, ptn, scream_EE) = (SCREAM_MODEL.scream_parameters, SCREAM_MODEL.HANDLER, SCREAM_MODEL.ptn, SCREAM_MODEL.scream_EE)

    SCREAM_MODEL2 = ScreamModel(scream_par_file)

    # No need to read in libraries.
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    # scream_EE init.
    _just_BiHelix_for_from_scratch_init_Scream_EE(scream_EE, SCREAM_PARAMS, ptn)


    # determine internal energy for sidechains on ptn (only those that are specified in scream_par_file)
    _find_ptn_internal_energies(SCREAM_MODEL, SCREAM_MODEL2)

    # Now call Print_BiHelix_Final_Residue_Energy_Breakdown
    Print_BiHelix_Final_Residue_Energy_Breakdown(SCREAM_MODEL, scream_EE, output_file)


def _find_ptn_internal_energies(SCREAM_MODEL_orig, SCREAM_MODEL2):
    ptn = SCREAM_MODEL_orig.ptn
    ptn2 = SCREAM_MODEL2.ptn

    (Libraries_Dict, mutInfo_rotConnInfo_Dict, Ntrl_Orig_Rotamer_Dict) = initRotlibs_no_orig_rot(SCREAM_MODEL2.scream_parameters, ptn2)
    print Ntrl_Orig_Rotamer_Dict.keys()
    # Now figure out RMSD
    for mIString in Ntrl_Orig_Rotamer_Dict.keys():
        print '##############################' , mIString, '###################################'
        crntRotlib = Libraries_Dict[mIString]
        
        mI = MutInfo(mIString)
        (chn, pstn) = (mI.getChn(), mI.getPstn() )
        crntRotlib.reset_pstn() # doesn't sort
        crntRotamer = crntRotlib.get_next_rot()

        while (crntRotamer != None):
            ptn2.ntrlRotamerPlacement(chn, pstn, crntRotamer)
            CRMS = ptn.sc_CRMS(chn, pstn, ptn2)
            if CRMS <= 0.001:
                internal_energy = crntRotamer.get_preCalc_TotE()
                ptn.setPreCalcEnergy(chn, pstn, internal_energy)
                print internal_energy
                break
            else:
                crntRotamer = crntRotlib.get_next_rot()
                continue
                
        if crntRotlib == None:
            print 'No matching rotamer found for %s %d.  QUitting.' % (chn, pstn)
            sys.exit(2)

            

def _just_BiHelix_for_from_scratch_init_Scream_EE(scream_EE, SCREAM_PARAMS, ptn):
    '''
    Inits scream_EE using a protein structure and a SCREAM_PARAMs structure.
    '''
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    if ntrlMutInfo_list.size() == 1 and ntrlMutInfo_list[0] == 'DESIGN':
        ntrlMutInfo_list = []
    elif ntrlMutInfo_list.size() == 1 and ntrlMutInfo_list[0] == 'BINDING_SITE':
        ntrlMutInfo_list = []

    for mutInfo in ntrlMutInfo_list:
        mI = MutInfo(mutInfo)
        scream_EE.addMutInfoRotConnInfo(mI)

    ff_file = SCREAM_PARAMS.getOneEnergyFFParFile()
    scream_delta_file = SCREAM_PARAMS.getDeltaParFile()

    if SCREAM_PARAMS.getUseRotamerNeighborList() == 'YES':
        scream_EE.init_after_addedMutInfoRotConnInfo_neighbor_list(ptn, SCREAM_PARAMS)
    else:
        scream_EE.init_after_addedMutInfoRotConnInfo_on_the_fly_E(ptn, SCREAM_PARAMS)

    # Then, init FULL pre-initialization.
    _initScreamAtomDeltaValuePy(scream_EE, SCREAM_PARAMS)



def Print_BiHelix_Final_Residue_Energy_Breakdown(SCREAM_MODEL, scream_EE, output_file):
    ptn = SCREAM_MODEL.ptn
    SCREAM_PARAMS = SCREAM_MODEL.scream_parameters

    OUTPUT = open(output_file, 'w')
    #print >>OUTPUT, '%7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s' % ('Res', 'Intern', 'Tot_EL', 'EL_AA', 'EL_AA_V', 'EL_AA_C', 'EL_AA_H', 'EL_AB', 'EL_AB_V', 'EL_AB_C', 'EL_AB_H', 'Tot_Ss', 'Ss_AA', 'Ss_AA_V', 'Ss_AA_C', 'Ss_AA_H', 'Ss_AB', 'Ss_AB_V', 'Ss_AB_C', 'Ss_AB_H', 'Tot_E')
    clashCollection = ClashCollection(15)
    scream_EE.addClashCollection(clashCollection)
    
    scream_EE.resetFlags(1)
    scream_EE.initScreamAtomVdwHbFields()

    #(total_E, vdw_E, hb_E, coulomb_E) = Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS)

    chain_list = ['A', 'B']
    ntrlAA_list_t = SCREAM_PARAMS.getMutateResidueInfoList()

    #(All_EL_AA, All_EL_AA_V, All_EL_AA_C, All_EL_AA_H, All_EL_AB, All_EL_AB_V, All_EL_AB_C, All_EL_AB_H, All_Scsc_AA, All_Scsc_AA_V, All_Scsc_AA_C, All_Scsc_AA_H, All_Scsc_AB, All_Scsc_AB_V, All_Scsc_AB_C, All_Scsc_AB_H) = (0,0,0,0,0,0,0,0,0,0,   0,0,0,0,0,0)
    (All_E_list, All_E_A_list, All_E_B_list)=([], [], [])
    mI_E_dict = {}
    ntrlAA_list = []
    for t in ntrlAA_list_t:
        ntrlAA_list.append(t)
    ntrlAA_list.sort(cmp_MutInfo)
    # flag states:
    # 8: EL visible
    # 4: interaction visible (sc-sc) 4 == visible, 0 == invisible
    # 2: interaction moveable (sc-sc) 2 == fixed, 0 == moveable
    # 1: orig state; to scream or not to scream 1==not to scream 0 == will be scream'ed
    for mI in ntrlAA_list:
        print 'Doing %s' % mI
        (self_chain, other_chain) = determineChains(mI, chain_list)
        scream_EE.resetFlags()
        # First, do AA (self-self) terms.
        scream_EE.make_chain_invisible(other_chain) # i.e. make the other chain completely invisible.
        scream_EE.visible_mutInfo(MutInfo(mI))
        scream_EE.make_chain_EL_invisible(other_chain)
        
        scream_EE.initScreamAtomVdwHbFields()
        _initScreamAtomDeltaValuePy(scream_EE, SCREAM_PARAMS)

        AA_E_list = proper_EE_manipulation_MutInfoEnergies(ptn, scream_EE, SCREAM_PARAMS, mI)
        
        scream_EE.resetFlags()
        
        # Then, do AB (self-other) terms.
        scream_EE.make_chain_invisible(self_chain) # i.e. make own chain completely invisible.
        scream_EE.visible_mutInfo(MutInfo(mI))
        scream_EE.make_chain_EL_invisible(self_chain)
        
        scream_EE.initScreamAtomVdwHbFields()
        _initScreamAtomDeltaValuePy(scream_EE, SCREAM_PARAMS)

        AB_E_list = proper_EE_manipulation_MutInfoEnergies(ptn, scream_EE, SCREAM_PARAMS, mI)

        Intern = AA_E_list[0]
        (EL_AA, EL_AA_V, EL_AA_C, EL_AA_H) = (AA_E_list[1], AA_E_list[2], AA_E_list[3], AA_E_list[4])
        (EL_AB, EL_AB_V, EL_AB_C, EL_AB_H) = (AB_E_list[1], AB_E_list[2], AB_E_list[3], AB_E_list[4])
        Tot_EL = EL_AA + EL_AB
        (Scsc_AA, Scsc_AA_V, Scsc_AA_C, Scsc_AA_H) = (AA_E_list[5], AA_E_list[6], AA_E_list[7], AA_E_list[8])
        (Scsc_AB, Scsc_AB_V, Scsc_AB_C, Scsc_AB_H) = (AB_E_list[5], AB_E_list[6], AB_E_list[7], AB_E_list[8])
        Tot_Scsc = Scsc_AA + Scsc_AB
        Total_E = Intern + Tot_EL + Tot_Scsc/2

        Increment_list = (Intern, Tot_EL, EL_AA, EL_AA_V, EL_AA_C, EL_AA_H, EL_AB, EL_AB_V, EL_AB_C, EL_AB_H, Tot_Scsc/2, Scsc_AA/2, Scsc_AA_V/2, Scsc_AA_C/2, Scsc_AA_H/2, Scsc_AB/2, Scsc_AB_V/2, Scsc_AB_C/2, Scsc_AB_H/2, Total_E)
        All_E_list = All_E_Update(All_E_list, Increment_list)
        mI_E_dict[mI] = Increment_list
        if self_chain == 'A':
            All_E_A_list = All_E_Update(All_E_A_list, Increment_list)
        elif self_chain == 'B':
            All_E_B_list = All_E_Update(All_E_B_list, Increment_list)


    ### What Ravi wants: Tot_AA_intra  AA_intra_V  AA_intra_C  AA_intra_H  Tot_BB_intra  BB_intra_V  BB_intra_C  BB_intra_H  Tot_AB_inter  AB_inter_V  AB_inter_C  AB_inter_H
    # 0: Intern
    # 1: Tot_EL
    # 2: EL_AA, 3: EL_AA_V, 4: EL_AA_C, 5: EL_AA_H
    # 6: EL_AB, 7: EL_AB_V, 8: EL_AB_C, 9: EL_AB_H
    # 10: Tot_Scsc/2 (but after summing up, /2 factor gone)
    # 11: Scsc_AA/2, 12: Scsc_AA_V/2, 13: Scsc_AA_C/2, 14: Scsc_AA_H/2 (but after summing up, /2 factor gone)
    # 15: Scsc_AB/2, 16: Scsc_AB_V/2, 17: Scsc_AB_C/2, 18: Scsc_AB_H/2 (but after summing up, /2 factor gone)
    # 19: Total_E

    Tot_AA_intra = All_E_A_list[0] + All_E_A_list[2] + All_E_A_list[11]
    AA_intern = All_E_A_list[0]
    AA_intra_V = All_E_A_list[3] + All_E_A_list[12]
    AA_intra_C = All_E_A_list[4] + All_E_A_list[13]
    AA_intra_H = All_E_A_list[5] + All_E_A_list[14]
    Tot_BB_intra = All_E_B_list[0] + All_E_B_list[2] + All_E_B_list[11]
    BB_intern = All_E_B_list[0]
    BB_intra_V = All_E_B_list[3] + All_E_B_list[12]
    BB_intra_C = All_E_B_list[4] + All_E_B_list[13]
    BB_intra_H = All_E_B_list[5] + All_E_B_list[14]
    Tot_AB_inter = All_E_list[6] + All_E_list[15]
    AB_inter_V = All_E_list[7] + All_E_list[16]
    AB_inter_C = All_E_list[8] + All_E_list[17]
    AB_inter_H = All_E_list[9] + All_E_list[18]
    Tot_E =  Tot_AA_intra + Tot_BB_intra + Tot_AB_inter
    
    print >>OUTPUT, '%11s %11s %11s %11s %11s %11s %11s %11s %11s %11s %11s %11s %11s %11s %11s' % ('Tot_AA_intra', 'AA_Internal', 'AA_intra_V', 'AA_intra_C', 'AA_intra_H', 'Tot_BB_intra', 'BB_Internal', 'BB_intra_V', 'BB_intra_C', 'BB_intra_H', 'Tot_AB_inter', 'AB_inter_V', ' AB_inter_C', 'AB_inter_H', 'Tot_E')
    print >>OUTPUT, '%11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f %11.3f ' % (Tot_AA_intra, AA_intern, AA_intra_V, AA_intra_C, AA_intra_H, Tot_BB_intra, BB_intern, BB_intra_V, BB_intra_C, BB_intra_H, Tot_AB_inter, AB_inter_V, AB_inter_C, AB_inter_H, Tot_E)

#     print >>OUTPUT, '%7s' % 'All',
#     for i in range(0, len(All_E_list)):
#         print >>OUTPUT, '%7.3f' % All_E_list[i],
#     print >>OUTPUT, ''
#     print >>OUTPUT, '%7s' % 'ChainA',
#     for i in range(0, len(All_E_A_list)):
#         print >>OUTPUT, '%7.3f' % All_E_A_list[i],
#     print >>OUTPUT, ''
#     print >>OUTPUT, '%7s' % 'ChainB',
#     for i in range(0, len(All_E_B_list)):
#         print >>OUTPUT, '%7.3f' % All_E_B_list[i],
#     print >>OUTPUT, ''



#     keys = mI_E_dict.keys()
#     keys.sort(lambda x, y: cmp_MutInfo(x,y) )
#     for mI in keys:
#         E_list = mI_E_dict[mI]
#         print >>OUTPUT, '%7s' % mI,
#         for i in range(0, len(E_list)):
#             print >>OUTPUT, '%7.3f' % E_list[i],
#         print >>OUTPUT, ''
        
def cmp_MutInfo(x,y):
    if (cmp(x[-1],y[-1]) == 0):
        return cmp(int(x[1:-2]), int(y[1:-2]))
    else:
        return cmp(x[-1],y[-1])

def All_E_Update(All_E_list, Increment_list):
    new_E_list = []
    if len(All_E_list) == 0:
        return Increment_list
    for i in range(0, len(All_E_list)):
        new_E = All_E_list[i] + Increment_list[i]
        new_E_list.append(new_E)
    return new_E_list


def _returnEnergyMethod(SCREAM_PARAMS):

    method = SCREAM_PARAMS.getUseDeltaMethod()
    t = 0.0
    if SCREAM_PARAMS.getUseAsymmetricDelta() == 'YES':
        method += '_ASYM'
    if method[0:4] == 'FLAT':
        t = SCREAM_PARAMS.getFlatDeltaValue()
    elif method[0:4] == 'FULL':
        t = SCREAM_PARAMS.getDeltaStandardDevs()
    elif method[0:6] == 'SCALED':
        t = SCREAM_PARAMS.getInnerWallScalingFactor()
    if SCREAM_PARAMS.getCBGroundSpectrumCalc() == 'NO':
        method += '_NOCB'

    LJOption = SCREAM_PARAMS.getLJOption()
    method = method + '_' + LJOption

    return (method, t)

def proper_EE_manipulation_MutInfoEnergies(ptn, scream_EE, SCREAM_PARAMS, mutInfo):
    #ptn.printAtomFlagStates()
    
    mI = MutInfo(mutInfo)
    (method, t) = _returnEnergyMethod(SCREAM_PARAMS)

    chain = mI.getChn()
    pstn = mI.getPstn()
    AA = mI.getAA()

    # Want: PreCalc E, EL_E, Interaction_E.
    # PreCalc Energy.
    PreCalc_E = ptn.getPreCalcEnergy(chain, pstn)
    
    # First, Empty Lattice Energies.
    EL_rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, method, t)
    EL_rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, method, t)
    EL_rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
    EL_all = EL_rot_vdw_E + EL_rot_hb_E + EL_rot_coulomb_E

    # Second, Interaction Energies.
    scream_EE.fix_all()
    scream_EE.moveable_mutInfo(mI, None, 1)
    
    All_rot_vdw_E = scream_EE.calc_all_interaction_vdw_E_delta(method, t)
    All_rot_hb_E = scream_EE.calc_all_interaction_hb_E_delta(method, t)
    All_rot_coulomb_E = scream_EE.calc_all_interaction_coulomb_E_delta()
    All_E = All_rot_vdw_E + All_rot_hb_E + All_rot_coulomb_E

    Total_E = PreCalc_E + EL_all + All_E
    return (PreCalc_E, EL_all, EL_rot_vdw_E, EL_rot_coulomb_E,  EL_rot_hb_E, All_E, All_rot_vdw_E, All_rot_coulomb_E, All_rot_hb_E, Total_E)
    

def determineChains(mI, chain_list):
    self_chain = mI[-1]
    if not self_chain in chain_list:
        print 'A chain name other than \"A\" or \"B\" is encountered.  Program quitting.'
        sys.exit(2)
    other_chain = ''
    if self_chain == chain_list[0]:
        other_chain = chain_list[1]
    else:
        other_chain = chain_list[0]
    return (self_chain, other_chain)



def _initScreamAtomDeltaValuePy(scream_EE, SCREAM_PARAMS):
    if SCREAM_PARAMS.getUseDeltaMethod().strip()[0:4] == 'FULL':
        lib_name = SCREAM_PARAMS.getLibResolution()
        if lib_name == 0:
            lib_name = 'SCWRL'
        else:
            if lib_name <= 9:
                lib_name = '0' + str(lib_name)
            else:
                lib_name = str(lib_name)
        method = 'FULL'
        alpha = SCREAM_PARAMS.getDeltaStandardDevs()
        eachAtomDeltaFile = SCREAM_PARAMS.getEachAtomDeltaFile()
        scream_EE.initScreamAtomDeltaValue(lib_name, method, alpha, eachAtomDeltaFile)


#========================================================================================#
# below: modified from SCREAM.py

def initRotlibs_no_orig_rot(SCREAM_PARAMS, ptn):
    '''
    Initializes the following objects:
    self.Libraries_Dict                    # Dict { mutInfo_str : Rotlib* }
    self.Original_Conformers_Dict          # Dict { mutInfo_str : Rotamer* }
    self.Conformer_RotConnInfo_Dict        # Dict { mutInfo_str : rotConnInfo* } for Conformers.
    '''
    (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict) = return_Ntrl_Library_Dicts(SCREAM_PARAMS, ptn)

    # Next initialize the Arbitrary rotamer libraries.
    additional_list = SCREAM_PARAMS.getAdditionalLibraryInfo()
    (Add_Library_Dict, Add_Orig_Conformer_Dict, mutInfo_rotConnInfo_Dict) = ( {}, {}, {} )

    c = 1
    if len(additional_list) != 0:
        for lib in additional_list:
            # first load library
            library_file = lib
            library = Rotlib(library_file)
            print 'Done loading ' + library_file + '.'
            mutInfo = 'Z' + str(c) + '_Z'
            Add_Library_Dict[mutInfo] = library
            mutInfo_rotConnInfo_Dict[mutInfo] = library.getRotConnInfo()
            # then add original conformer.
            #originalConformer = ptn.conformerExtraction(library.getRotConnInfo())
            #Add_Orig_Conformer_Dict[mutInfo] = originalConformer
            c += 1

    # Put them together.
    Ntrl_Library_Dict.update(Add_Library_Dict)
    Libraries_Dict = Ntrl_Library_Dict.copy()     # Dict { mutInfo : Rotlib* }
    Ntrl_Orig_Rotamer_Dict.update(Add_Orig_Conformer_Dict)
    
    print  'Total Number of Libraries loaded: ' , len(Libraries_Dict)
    return (Libraries_Dict, mutInfo_rotConnInfo_Dict, Ntrl_Orig_Rotamer_Dict)

def return_Ntrl_Library_Dicts(SCREAM_PARAMS, ptn):
    # Returns two dictionaries: Ntrl_Library_Dict and Ntrl_Orig_Rotamer_Dict, according to entries in SCREAM_PARAMS.
    ntrlAA_list = SCREAM_PARAMS.getMutateResidueInfoList()
    (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict) = ( {} , {} )
    
    # Populating Ntrl library and original rotamers.
    if len(ntrlAA_list) != 0:
        if ntrlAA_list[0] == 'DESIGN':
            # setup multiple AA rotamer libraries from getDesignPositionAndClass(), getDesignAAClassDefns(), getDesignClassFromPosition(string), getDesignClassAAs(string).
            # First get list of Design positions, then get their corresponding mutation AA lists, set them up, done.
            library_path_first_half = SCREAM_PARAMS.determineLibDirPath()
            
            DesignPositions = SCREAM_PARAMS.getDesignPositions()
            for dP in DesignPositions:
                DesignClass = SCREAM_PARAMS.getDesignClassFromPosition(dP)
                DesignAAs = SCREAM_PARAMS.getDesignClassAAs(DesignClass)
                Resolution = SCREAM_PARAMS.getLibResolution()
                multipleAARotlib = Multiple_NtrlAARotlib(library_path_first_half, Resolution, DesignAAs)
                mutInfo = convertDesignPositionToMutInfoName(dP)
                Ntrl_Library_Dict[mutInfo] = multipleAARotlib

                (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo) 
                originalRotamer = AARotamer()
                originalRotamer.deepcopy(ptn.getAARotamer(mutChn, mutPstn))

                originalRotamer.is_Original = 1
                Ntrl_Orig_Rotamer_Dict[mutInfo] = originalRotamer
                return (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict)
                
        elif ntrlAA_list[0] == 'BINDING_SITE':
            ntrlAA_list = return_ntrlAA_list_from_BINDING_SITE_mode(SCREAM_PARAMS, ptn)

        (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict) = Load_Rotamer_Libraries(ntrlAA_list, ptn, SCREAM_PARAMS)
        
    else:
        print 'Warning: No Natural Amino Acids are specified to be SCREAM\'ed!  This is possible when only a ligand rotamer library is to be SCREAM\ed.'
            
    return (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict)

def Load_Rotamer_Libraries(ntrlAA_list, ptn, SCREAM_PARAMS):
    (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict) = ( {}, {} )
    for mutInfo in ntrlAA_list:
        (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
        #if mutAA == 'G' or mutAA == 'A':
        #continue
        print mutInfo

        library_path_first_half = SCREAM_PARAMS.determineLibDirPath()
        library_file_suffix = SCREAM_PARAMS.determineLibDirFileNameSuffix()
        cnn_file_path = SCREAM_PARAMS.determineCnnDirPath()
        library_file = ''
        # first populate the libraries
        if mutAA == 'J' or mutAA == 'H':
            H_library_file = library_path_first_half + '/' + 'H' + '/' + 'H' + library_file_suffix
            J_library_file = library_path_first_half + '/' + 'J' + '/' + 'J' + library_file_suffix
            H_cnn_file = cnn_file_path + '/H.cnn'
            J_cnn_file = cnn_file_path + '/J.cnn'
            library = HIS_NtrlAARotlib(H_library_file, J_library_file, H_cnn_file, J_cnn_file)
        else:
            library_file = library_path_first_half + '/' + mutAA + '/' + mutAA + library_file_suffix
            cnn_file = cnn_file_path + '/' + mutAA + '.cnn'
            library = NtrlAARotlib(library_file, cnn_file)

        Ntrl_Library_Dict[mutInfo] = library

        # then the original rotamers.
        originalRotamer = AARotamer()
        originalRotamer.deepcopy(ptn.getAARotamer(mutChn, mutPstn))

        originalRotamer.is_Original = 1
        Ntrl_Orig_Rotamer_Dict[mutInfo] = originalRotamer

    return (Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict)

def convertDesignPositionToMutInfoName(DesignName):
    '''convertDesignPositionToMutInfoName: takes in a DesignName (like A32, which means chain A position 32), returns a legal mutInfo name (like A32_A, alanine, position 32, chain A.  Alanine is set as the default.)'''
    chain = DesignName[0]
    position = DesignName[1:]
    mutInfo = 'A' + position + '_' + chain
    return mutInfo

def unpackMutInfo(mutInfo):
    """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""

    if mutInfo.find('|') != -1:
        return ('Cluster', 0, 'Cluster')
    else:
        mutAA = mutInfo[0]
        (mutPstn, mutChn) = mutInfo[1:].split('_')
        mutPstn = int(mutPstn)
        return (mutAA, mutPstn, mutChn)
