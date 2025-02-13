#!/usr/bin/env python

import sys, timing
from Py_Scream_EE import *

def usage():
    print '''
Does SCREAM.
Usage: SCREAM_standalone.py <SCREAM ctl file>
E.g.: SCREAM_standalone.py PheRS_F258_F260.ctl
Remark: Still experimental.
'''
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        usage()

    ctl_file = sys.argv[1]
    SCREAM_MODEL = ScreamModel(ctl_file)

    SCREAM_PARAMS = SCREAM_MODEL.scream_parameters

    # Initialize Protein

    BGF_HANDLER = SCREAM_MODEL.HANDLER
    ptn = SCREAM_MODEL.ptn

    # initialializing libraries
    (Libraries_Dict, mutInfo_rotConnInfo_Dict, ntrl_orig_rots) = initRotlibs(SCREAM_PARAMS, ptn)  # need ntrl_orig_rots so doesn't get deleted

    # init lists
    
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()


    # init Scream_EE
    scream_EE = SCREAM_MODEL.scream_EE
    #scream_EE = Scream_EE()
    #init_Scream_EE(scream_EE, SCREAM_PARAMS, ptn, mutInfo_rotConnInfo_Dict) 
    
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    

    # Now do scream.  First, Empty Lattice Energy calculations.
    timing.start()
    Calc_EL_Energies(ptn, scream_EE, SCREAM_PARAMS, Libraries_Dict, mutInfo_rotConnInfo_Dict, BGF_HANDLER) # temp added BGF_HANDLER
    timing.finish()
    EL_calculation_time = timing.micro() / 1000000.00
    
    Print_Library_EL_Energies(Libraries_Dict)


    # init ClashCollection object
    clashCollection = ClashCollection(50)


    # Then, excitation based on these empty lattice energy calculations.
    rotlibCollection = RotlibCollectionPy()
    rotlibCollection.setHighestAllowedRotamerE(SCREAM_PARAMS.StericClashCutoffEnergy)

    rotlibCollection.addClashCollection(clashCollection)
    scream_EE.addClashCollection(clashCollection)


    for mutInfo in Libraries_Dict.keys():
        library = Libraries_Dict[mutInfo]
        rotlibCollection.addRotlib(mutInfo, library)

    timing.start()
    
    rotlibCollection.initDynamicMemoryDataStructures()
    #theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
    theseExcitedConformers = rotlibCollection.getNextDynamicClashEliminatedRotamers_And_ExpandPy()
    total_count = 0
    count_since_last_best = 0
    max_count = SCREAM_PARAMS.getMaxSearchNumber()
    
    lowestE = 999999999

    while len(theseExcitedConformers) != 0:
       
        total_count += 1
        if total_count + clashCollection.get_total_clashing_rotamers_eliminated() > max_count:
            break
        
        count_since_last_best = count_since_last_best +1
        placeMultipleConformers(ptn, theseExcitedConformers, mutInfo_rotConnInfo_Dict)
        #all_interactions_E = scream_EE.calc_all_interaction_E()
        all_interactions_E = Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS)

        
        crntEnergy = all_interactions_E
        for mutInfo in theseExcitedConformers.keys():
            crntConformer = theseExcitedConformers[mutInfo]
            crntEnergy += crntConformer.get_sc_total_E()

        rotlibCollection.setEnergyForExcitedRotamers(theseExcitedConformers, crntEnergy)

        if crntEnergy < lowestE:
            lowestE = crntEnergy
            count_since_last_best = 0

        if rotlibCollection._shouldKeepGoing(count_since_last_best):
            theseExcitedConformers = rotlibCollection.getNextDynamicClashEliminatedRotamers_And_ExpandPy()
        else:
            break

    timing.finish()
    Combinatorial_Time = timing.micro() / 1000000.00

    # Then print the best structures.
    printBestStructures(ptn, BGF_HANDLER, rotlibCollection, SCREAM_PARAMS, mutInfo_rotConnInfo_Dict)
    printEnergyEvolution(rotlibCollection)

    clashing_n = clashCollection.get_total_clashing_rotamers_eliminated()

    
    print "Empty Lattice Calculation time: " + str(EL_calculation_time)
    print "Combinatorial Calculation time: " + str(Combinatorial_Time)
    print "Total number of rotamer configuration sets evaluated: " + str(total_count)
    print "Total number of clashing rotamer configuration sets discarded: " + str(clashing_n)
    print "Total number of rotamer configurations stepped through: " + str(total_count + clashing_n)
    print "Max search steps specified: " + str(max_count)

    if total_count + clashCollection.get_total_clashing_rotamers_eliminated() > max_count:
        print "Maximum number of rotamer configuration searches reached, quitting."

def init_Scream_EE(scream_EE, SCREAM_PARAMS, ptn, mutInfo_rotConnInfo_Dict):
    '''
    Inits scream_EE using a protein structure and a SCREAM_PARAMs structure.
    '''
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    for mutInfo in ntrlMutInfo_list:
        mI = MutInfo()
        mI.init(mutInfo)
        scream_EE.addMutInfoRotConnInfo(mI)
    for mutInfo in mutInfo_rotConnInfo_Dict.keys():
        mI = MutInfo()
        mI.init(mutInfo)
        rotConnInfo_z = mutInfo_rotConnInfo_Dict[mutInfo]
        scream_EE.addMutInfoRotConnInfo(mI, rotConnInfo_z)

    ff_file = SCREAM_PARAMS.getOneEnergyFFParFile()
    scream_delta_file = SCREAM_PARAMS.getDeltaParFile()

    #ff_file = 'dreidii322-mpsim-dielectric-2.5.par'
    #scream_delta_file = '/project/Biogroup/Software/SCREAM/lib/SCREAM_delta_par_files/SCREAM_delta.par'
    #scream_EE.init_after_addedMutInfoRotConnInfo(ptn, ff_file, scream_delta_file)
    scream_EE.init_after_addedMutInfoRotConnInfo_on_the_fly_E(ptn, ff_file, scream_delta_file)
    

def printBestStructures(ptn, BGF_HANDLER, rotlibCollection, SCREAM_PARAMS, Conformer_RotConnInfo_Dict):
      """Prints best structures give a rotlibCollection, with the total number specfied by the Selections parameter in SCREAM param file."""
      print "Printing Best Structures!"
      count = 0
      filename_prefix = 'best_'
      rotlibCollection.resetTotalEnergyCrntPstn()
      theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()
      
      while len(theseExcitedRotamers) != 0:
          count = count+1
          filename = filename_prefix + `count` + '.bgf'
          if count > SCREAM_PARAMS.Selections:
              break
          #self.placeMultipleSideChains(theseExcitedRotamers)
          placeMultipleConformers(ptn, theseExcitedRotamers, Conformer_RotConnInfo_Dict)
          excitedRotamerInfo = rotlibCollection.emptyLatticeRankInfo(theseExcitedRotamers)
          BGF_HANDLER.printToFile(filename)
          theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()
      print 'Done printing Best Structures.'

    
def placeMultipleConformers(ptn, conformersDict, conformerRotConnInfoDict = None):
    '''
    More general than placeMultipleSideChains.  Should replace all instances of placeMultipleSideChains.
    '''
    for mutInfo in conformersDict.keys():
        conformer = conformersDict[mutInfo]
        (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
        if mutAA == 'Z' and mutChn == 'Z': # should not enter this conditional if conformersDict contains only rotamers.
            rotConnInfo = conformerRotConnInfoDict[mutInfo]
            ptn.conformerPlacement(conformer, rotConnInfo)
        #elif mutAA == 'H' or mutAA == 'J': # special HIS singly protonation case.  might not be necessary.
        #ptn.ntrlRotamerPlacement(mutChn, mutPstn, castRotamerToAARotamer(conformer))
        else:
            ptn.ntrlRotamerPlacement(mutChn, mutPstn, castRotamerToAARotamer(conformer))

    

def Calc_EL_Energies(ptn, scream_EE, SCREAM_PARAMS, Libraries_Dict, mutInfo_rotConnInfo_Dict, BGF_HANDLER): # temp added BGF_HANDLER
    # This subroutine invokes the desired energy calculation routines.
    # First print which method is being used.
    print '##################################'
    print 'Calculating Empty Lattice Energies'
    print 'Method used: ', SCREAM_PARAMS.getUseDeltaMethod()
    print '##################################'

    for mutInfo in Libraries_Dict.keys():
        (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
        mI = MutInfo()
        mI.init(mutInfo)
        library = Libraries_Dict[mutInfo]
        library.reset_pstn()
        currentRotamer = library.get_next_rot()
        count = 1

        print ''
        print mutInfo
        while currentRotamer != None:
            if mutAA != 'Z':
                ptn.ntrlRotamerPlacement(mutChn, mutPstn, currentRotamer)
            else:
                rotConnInfo_Z = mutInfo_rotConnInfo_Dict[mutInfo]
                ptn.conformerPlacement(currentRotamer, rotConnInfo_Z)

            print ''
            print 'Rotamer', count
            count += 1
            rot_E = 0
            rot_vdw_E  = 0
            rot_hb_E = 0
            rot_coulomb_E = 0 
            # Now decide which SCREAM energy function to use
            if SCREAM_PARAMS.getUseScreamEnergyFunction() == 'YES':
                value = 0

                if SCREAM_PARAMS.getUseDeltaMethod() == 'FLAT':
                    t = SCREAM_PARAMS.getFlatDeltaValue()
                    
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'FLAT', t)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'FLAT', t)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'FLAT', t)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    
                    #rot_E = scream_EE.calc_empty_lattice_E_full_delta(mI, t)
                    
                elif SCREAM_PARAMS.getUseDeltaMethod() == 'FULL':

                    d = SCREAM_PARAMS.getDeltaStandardDevs()
                    print 'FULL method. d value: ' + str(d)
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'FULL', d)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'FULL', d)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'FLAT', d)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    #rot_E = scream_EE.calc_empty_lattice_E_flat_delta(mI, d)

                elif SCREAM_PARAMS.getUseDeltaMethod() == 'SCALED':
                    s = SCREAM_PARAMS.getInnerWallScalingFactor()
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'SCALED', s)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'SCALED', s)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'SCALED', s)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    
                elif SCREAM_PARAMS.getUseDeltaMethod() == 'RESIDUE':
                    # not implemented
                    #rot_E = scream_EE.calc_empty_lattice_E_residue_delta(mI)
                    pass
                else:
                    rot_E = scream_EE.calc_empty_lattice_E(mI)
            else:
                print 'SCREAM standalone version can only use SCREAM energy functions.'
                sys.exit(2)
            currentRotamer.set_empty_lattice_E_abs(rot_E)
            currentRotamer.set_sc_coulomb_E(rot_coulomb_E)
            #currentRotamer.set_sc_vdw_E(rot_vdw_E + rot_vdw_hb_exclusion_E)
            currentRotamer.set_sc_vdw_E(rot_vdw_E)
            currentRotamer.set_sc_hb_E(rot_hb_E)
            currentRotamer = library.get_next_rot()

def Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS):
    deltaForInteractionE = SCREAM_PARAMS.getUseDeltaForInterResiE() # YES/NO
    DeltaMethod = SCREAM_PARAMS.getUseDeltaMethod()
    t = SCREAM_PARAMS.getFlatDeltaValue()

    if deltaForInteractionE == 'YES':
        vdw_E = scream_EE.calc_all_interaction_vdw_E_delta(DeltaMethod, t)
        hb_E = scream_EE.calc_all_interaction_hb_E_delta(DeltaMethod, t)
        coulomb_E = scream_EE.calc_all_interaction_coulomb_E_delta()
        total_E = vdw_E + hb_E + coulomb_E
        return total_E
    else:
        return scream_EE.calc_all_interaction_E()
    

            

def Print_Library_EL_Energies(Libraries_Dict):
    filename = ''
    i = 1
    for mutInfo in Libraries_Dict.keys():
        filename = mutInfo + '.lib.EL'
        library = Libraries_Dict[mutInfo]
        library.sort_by_empty_lattice_E()
        library.reset_pstn()
        crntRotamer = library.get_next_rot()


        OUTPUT = open(filename, 'w')
        print >>OUTPUT, '%5s %3s %10s %10s %10s %10s' % ('Rank', 'RES', 'Tot Energy', 'VDW', 'Coulomb', 'HB')
        while crntRotamer != None:
            resName = crntRotamer.get_resName()
            EL_energy = crntRotamer.get_empty_lattice_E()
            EL_coulomb_E = crntRotamer.get_sc_coulomb_E()
            EL_vdw_E = crntRotamer.get_sc_vdw_E()
            EL_hb_E = crntRotamer.get_sc_hb_E()
            
            print >>OUTPUT, '%5d %3s %10.5f %10.5f %10.5f %10.5f' % (i, resName, EL_energy, EL_vdw_E, EL_coulomb_E, EL_hb_E )
            i = i+1
            crntRotamer = library.get_next_rot()
        OUTPUT.close()
        i = 1
    

def EmptyLatticeExcitationWithArbLib_scream_EE():
    pass

def printEnergyEvolution(rotlibCollection):
    """Prints the estimated and actual energy evolution.  Sorted by estimated energy."""
    Evolution_File = open('Evolution.dat', 'w')
    #rotlibCollection.resetTotalEnergyCrntPstn()
    rotlibCollection.resetEmptyLatticeCrntPstn()
    theseExcitedRotamers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()

    info = rotlibCollection.emptyLatticeRankInfo(theseExcitedRotamers)
    mutInfo_ordering = []
    
    header_line = 'Index    Estimated     Actual'
    cc = 1
    for i in info.split():
        if cc%2 == 1:
            header_line = header_line + ' ' + i
            mutInfo_ordering.append(i)
        cc = cc+1
    
    print >>Evolution_File, header_line

    c = 1
    while len(theseExcitedRotamers) != 0:
        rankInfo = rotlibCollection.emptyLatticeRankInfo(theseExcitedRotamers)
        estimated_E = rotlibCollection.getEstimatedEnergyForExcitedRotamers(theseExcitedRotamers)
        actual_E = rotlibCollection.getEnergyForExcitedRotamers(theseExcitedRotamers)
        
        if estimated_E >= 99999999:
            break
        ranking_info_dict = rotlibCollection.emptyLatticeRankInfo_in_dict_form(theseExcitedRotamers)
        ranks_line = ' '
        for mutInfo in mutInfo_ordering:
            n = ranking_info_dict[mutInfo]
            ranks_line = ranks_line + n + ' '

        print >>Evolution_File, '%5d %10.5f %10.5f' % ( c ,estimated_E, actual_E) + ranks_line
        theseExcitedRotamers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
        c += 1
        
    Evolution_File.close()
    

def initRotlibs(SCREAM_PARAMS, ptn):
    '''
    Initializes the following objects:
    self.Libraries_Dict                    # Dict { mutInfo : Rotlib* }
    self.Original_Conformers_Dict          # Dict { mutInfo : Rotamer* }
    self.Conformer_RotConnInfo_Dict        # Dict { mutInfo : rotConnInfo* } for Conformers.
    '''
    # First initialize the ntrlAARotlibs.
    
    ntrlAA_list = SCREAM_PARAMS.getMutateResidueInfoList()
    Ntrl_Library_Dict = {}
    Ntrl_Orig_Rotamer_Dict = {}

    # populating ntrl library and original rotamers
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
        else:
            for mutInfo in ntrlAA_list:
                (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)

                library_path_first_half = SCREAM_PARAMS.determineLibDirPath()
                library_file_suffix = SCREAM_PARAMS.determineLibDirFileNameSuffix()
                library_file = ''
                # first populate the libraries
                if mutAA == 'J' or mutAA == 'H':
                    H_library_file = library_path_first_half + '/' + 'H' + '/' + 'H' + library_file_suffix
                    J_library_file = library_path_first_half + '/' + 'J' + '/' + 'J' + library_file_suffix
                    library = HIS_NtrlAARotlib(H_library_file, J_library_file)
                else:
            
                    library_file = library_path_first_half + '/' + mutAA + '/' + mutAA + library_file_suffix
                    library = NtrlAARotlib(library_file)
                print 'Done loading ' + library_file + '.'
                Ntrl_Library_Dict[mutInfo] = library
            
                # then the original rotamers.
                originalRotamer = AARotamer()
                originalRotamer.deepcopy(ptn.getAARotamer(mutChn, mutPstn))


                originalRotamer.is_Original = 1
                Ntrl_Orig_Rotamer_Dict[mutInfo] = originalRotamer

    # print 'value of self.KeepOriginalRotamer: ', self.KeepOriginalRotamer
        
    if SCREAM_PARAMS.getKeepOriginalRotamer() == 'YES':
        appendOriginalRotamersToRotlibs(Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict)

    # Next initialize the Arbitrary rotamer libraries.
        
    additional_list = SCREAM_PARAMS.getAdditionalLibraryInfo()
    Add_Library_Dict = {}
    Add_Orig_Conformer_Dict = {}
    mutInfo_rotConnInfo_Dict = {}

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
            originalConformer = ptn.conformerExtraction(library.getRotConnInfo())
            Add_Orig_Conformer_Dict[mutInfo] = originalConformer
            c += 1

    if SCREAM_PARAMS.getKeepOriginalRotamer() == 'YES':
        appendOriginalConformersToRotlibs(Add_Library_Dict, Add_Orig_Conformer_Dict)
        
    # Put them together.
    Ntrl_Library_Dict.update(Add_Library_Dict)
    Libraries_Dict = Ntrl_Library_Dict.copy()     # Dict { mutInfo : Rotlib* }
    Ntrl_Orig_Rotamer_Dict.update(Add_Orig_Conformer_Dict)
    
    print  'Total Number of Libraries: ' , len(Libraries_Dict)
    print 'They are: '
    print Libraries_Dict
        
    #Ntrl_Orig_Rotamer_Dict.update(Add_Orig_Conformer_Dict)
    #self.Original_Conformers_Dict = Ntrl_Orig_Rotamer_Dict.copy()  # Dict { mutInfo : Rotamer* }
    
    #self.Conformer_RotConnInfo_Dict = mutInfo_rotConnInfo_Dict.copy()           # Dict { mutInfo : rotConnInfo* } for Conformers.
    return (Libraries_Dict, mutInfo_rotConnInfo_Dict, Ntrl_Orig_Rotamer_Dict)
    
                
def _populateNtrlLibraryDict(replacementList):
    Mutation_Library_Dict = {}
    for mutInfo in replacementList:
        (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
        library_path_first_half = SCREAM_PARAMS.determineLibDirPath()
        
        library_file_suffix = SCREAM_PARAMS.determineLibDirFileNameSuffix()
        #'_10.lib'
        
        library_file = library_path_first_half + '/' + mutAA + '/' + mutAA + library_file_suffix
        library = NtrlAARotlib(library_file)
        print 'Done loading ' + library_file + '.'
        Mutation_Library_Dict[mutInfo] = library
            
    return Mutation_Library_Dict


def unpackMutInfo(mutInfo):
    """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""
    mutAA = mutInfo[0]
    (mutPstn, mutChn) = mutInfo[1:].split('_')
    mutPstn = int(mutPstn)
    return (mutAA, mutPstn, mutChn)

def convertDesignPositionToMutInfoName(DesignName):
    '''convertDesignPositionToMutInfoName: takes in a DesignName (like A32, which means chain A position 32), returns a legal mutInfo name (like A32_A, alanine, position 32, chain A.  Alanine is set as the default.)'''
    chain = DesignName[0]
    position = DesignName[1:]
    mutInfo = 'A' + position + '_' + chain
    return mutInfo

    
# Two functions that help setup Rotamer libraries.

def appendOriginalRotamersToRotlibs(Mutation_Library_Dict, Original_Rotamer_Dict):
    assert(len(Mutation_Library_Dict) == len(Original_Rotamer_Dict))
    for mutInfo in Original_Rotamer_Dict.keys():
        crntRotlib = Mutation_Library_Dict[mutInfo]
        crntRotlib.sort_by_rotlib_E()
        crntRotlib.reset_pstn()
        lowestRotlibERot = crntRotlib.get_current_rot()
        lowest_E = lowestRotlibERot.get_rotlib_E()
        # need to set an energy for original rotamer... right now just takes the lowset energy from rotlib_E.  need to be improved.
        crntRotamer = Original_Rotamer_Dict[mutInfo]
        crntRotamer.setDeclaredInRotlibScope(0)
        crntRotamer.set_rotlib_E(lowest_E)
        crntRotlib.add_rotamer(crntRotamer)
    
    
def appendOriginalConformersToRotlibs(Conformer_Library_Dict, Original_Conformer_Dict):
    # Actually identical code to appendOriginalRotamersToRotlibs
    appendOriginalRotamersToRotlibs(Conformer_Library_Dict, Original_Conformer_Dict)


# RotlibCollectionPy class, derived from RotlibCollection, added convenience functions.

class RotlibCollectionPy(RotlibCollection):
    "RotlibCollection clas.  Convenience class derived from C++ RotlibCollection to make data transfer easier and cleaner."
    def __init__(self):
        RotlibCollection.__init__(self)
    
    def _shouldKeepGoing(self, count_since_last_best):
        """Primitive decision whether or not to keep going."""
        sizeOfSystem = self.sizeOfSystem()
        testBlockSize = 1.8**(sizeOfSystem+1)
        #         if testBlockSize < 20:
        #             testBlockSize = 20
        if testBlockSize < 100: # temporary, for design cases.
            testBlockSize = 100
        if testBlockSize > 5000:
            testBlockSize = 5000
        if count_since_last_best > testBlockSize:
            return 0
        else:
            return 1

    def emptyLatticeRankInfo(self, excitedRotamers):
        """Returns a string in the format C3_A 2 D4_A 0 E5_A 5, i.e. name of residue, Empty lattice rank.  ExcitedRotamers is in a format compatible to usage in Python, i.e. PyStr and <C_instance_AARotamer_p>."""
        outputString = ''
        for mutInfo in excitedRotamers.keys():
            rotamer = excitedRotamers[mutInfo]
            Rank = rotamer.get_empty_lattice_energy_rank()
            outputString = outputString + mutInfo + " " + `Rank` + " "
        return outputString

    def emptyLatticeRankInfo_in_dict_form(self, excitedRotamers):
        '''returns a dict with: {'C3_A', 2; 'D4_A', 14; ...} etc.
        '''
        rankInfo_line = self.emptyLatticeRankInfo(excitedRotamers)
        mutInfo_rank_dict = {}
        mutInfo_list = rankInfo_line.split()
        c = 0
        while c < len(mutInfo_list):
            mutInfo_rank_dict[mutInfo_list[c]] = mutInfo_list[c+1]
            c += 2
        return mutInfo_rank_dict
        
    
    def getNextEmptyLatticeExcitationRotamersPy(self ):
        """Returns a dictionary of Python useable {string, AARotamer*} pairs instead of the C++ returned {_p_string, _p_p_AARotamer} format."""
        excitedRotamersRightFormat = dict()
        excitedRotamersWrongFormat = self.getNextEmptyLatticeExcitationRotamers()
        if excitedRotamersWrongFormat.size() == 0:
            return {}
        
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            #rightString = derefString(wrongFormatString)
            rightString = wrongFormatString
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            #rightRotamer = derefRotamer(wrongFormatRotamer)
            rightRotamer = wrongFormatRotamer
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat

    def getNextDynamicMemoryRotamers_And_ExpandPy(self):
        '''Returns a distionary of Python useable {string, Rotamer*} pairs instead of the C++ returned types {_p_string, _p_pAARotamer} or _p_pRotamer format.'''
        excitedRotamersRightFormat = dict()
        excitedRotamersWrongFormat = self.getNextDynamicMemoryRotamers_And_Expand()
        if excitedRotamersWrongFormat.size() == 0:
            return {}
        # Don't go through following loop if size == 0.
        
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            #rightString = derefString(wrongFormatString)
            rightString = wrongFormatString
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            #rightRotamer = derefRotamer(wrongFormatRotamer)
            rightRotamer = wrongFormatRotamer
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat

    def getNextDynamicClashEliminatedRotamers_And_ExpandPy(self):
        excitedRotamersRightFormat = dict()
        excitedRotamersWrongFormat = self.getNextDynamicClashEliminatedRotamers_And_Expand()
        if excitedRotamersWrongFormat.size() == 0:
            return {}
        # Don't go through following loop if size == 0.
        
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            #rightString = derefString(wrongFormatString)
            rightString = wrongFormatString
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            #rightRotamer = derefRotamer(wrongFormatRotamer)
            rightRotamer = wrongFormatRotamer
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat


    def getNextTotalEnergyExcitationRotamersPy(self):
        """Returns a dictionary of Python useable {string, AARotamer*} pairs instead of the C++ returned {_p_string, _p_p_AARotamer} format from Total Energy dict."""
        excitedRotamersRightFormat = {}
        excitedRotamersWrongFormat = self.getNextTotalEnergyExcitationRotamers()
        if excitedRotamersWrongFormat.size() == 0:
            return {}
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            #rightString = derefString(wrongFormatString)
            rightString = wrongFormatString
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            #rightRotamer = derefRotamer(wrongFormatRotamer)
            rightRotamer = wrongFormatRotamer
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat

    
    def setEnergyForExcitedRotamers(self, excitedRotamers, energy):
        """Takes a ExcitedRotamer structure ( dict{mutInfo, AARotamer*} ) and stores its energy in RotlibCollection."""
        #EE = {}
        EE = ExcitationEnumeration({})
        for mutInfo in excitedRotamers.keys():
            rotamer = excitedRotamers[mutInfo]
            EmptyLatticeRank = rotamer.get_empty_lattice_energy_rank()
            EE[mutInfo] = EmptyLatticeRank
        self.setExcitationEnergy(EE, energy)
        
    def getEnergyForExcitedRotamers(self, excitedRotamers):
        EE = ExcitationEnumeration({})
        for mutInfo in excitedRotamers.keys():
            rotamer = excitedRotamers[mutInfo]
            EmptyLatticeRank = rotamer.get_empty_lattice_energy_rank()
            EE[mutInfo] = EmptyLatticeRank
        energy = self.getExcitationEnergy(EE)
        return energy

    def getEstimatedEnergyForExcitedRotamers(self, excitedRotamers):
        total_estimated_E = 0
        for mutInfo in excitedRotamers.keys():
            rotamer = excitedRotamers[mutInfo]
            this_estimated_E = rotamer.get_empty_lattice_E()
            total_estimated_E += this_estimated_E
        return total_estimated_E





if __name__ == '__main__':
    main()
