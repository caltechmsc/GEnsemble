#!/usr/bin/env python

import sys, timing, os
from Py_Scream_EE import *

def usage():
    print '''
Does SCREAM.
Usage: SCREAM.py <SCREAM ctl file>
E.g.: SCREAM.py PheRS_F258_F260.ctl
Remark: Please visit http://www.its.caltech.edu/~victor/Home_files/Research/SCREAM_usage.txt for more info.
'''
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        usage()

    # Initialization.
    timing.start()
    ctl_file = sys.argv[1]

    SCREAM_MODEL = ScreamModel(ctl_file)

    SCREAM_PARAMS = SCREAM_MODEL.scream_parameters
    BGF_HANDLER = SCREAM_MODEL.HANDLER
    ptn = SCREAM_MODEL.ptn
    scream_EE = SCREAM_MODEL.scream_EE


    # Rotamer Library init, and relevant info.
    (Libraries_Dict, mutInfo_rotConnInfo_Dict, ntrl_orig_rots) = initRotlibs(SCREAM_PARAMS, ptn)  # need ntrl_orig_rots so doesn't get deleted

    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    # scream_EE init.
    init_Scream_EE(scream_EE, SCREAM_PARAMS, ptn, Libraries_Dict, mutInfo_rotConnInfo_Dict)
    timing.finish()
    print 'SCREAM setup took ' + str(timing.micro() / 1000000.00) + ' seconds.'
    
    # Now do scream.  First, Empty Lattice Energy calculations.
    timing.start()
    Calc_EL_Energies(ptn, scream_EE, SCREAM_PARAMS, Libraries_Dict, mutInfo_rotConnInfo_Dict, BGF_HANDLER) # temp added BGF_HANDLER
    #Print_Library_EL_Energies(Libraries_Dict)
    timing.finish()
    print 'SCREAM singles took ' + str(timing.micro() / 1000000.00) + ' seconds.'
    # Clustering clashing rotamers.  Iteration until no longer detect clustering rotamers; i.e. final Libraries_Dict

    timing.start()
    Final_Libraries_Dict = Libraries_Dict.copy()

    #timing.start()

    if SCREAM_PARAMS.multiplePlacementMethod() == 'ExcitationWithClustering':
        print 'Doing ExcitationWithClustering!'
        #(scream_EE, Final_Libraries_Dict, mutInfo_rotConnInfo_Dict) = ground_state_calc_and_cluster(SCREAM_MODEL, scream_EE, Libraries_Dict, mutInfo_rotConnInfo_Dict)
        (scream_EE, Final_Libraries_Dict, mutInfo_rotConnInfo_Dict) = ground_state_calc_and_cluster(SCREAM_MODEL, scream_EE, Final_Libraries_Dict, mutInfo_rotConnInfo_Dict)

    timing.finish()
    print 'SCREAM Clustering took ' + str( timing.micro() / 1000000.00) + ' seconds.'

    # Brand new and final RotlibCollection, after all clashes have been eliminiated.

    timing.start()
    rotlibCollection = RotlibCollectionPy()
    rotlibCollection.setHighestAllowedRotamerE(SCREAM_PARAMS.StericClashCutoffEnergy)

    #Print_Library_EL_Energies(Final_Libraries_Dict)

    initialize_rotlibCollection(rotlibCollection, Final_Libraries_Dict)

    # Need to remember to add clashcollection!  Else crashes.
    clashCollection = ClashCollection(15)
    rotlibCollection.addClashCollection(clashCollection)
    scream_EE.addClashCollection(clashCollection)
    timing.finish()

    

    print 'SCREAM setup for Opportunity stage took ' + str( timing.micro() / 1000000.00) + ' seconds.'
    
    # Start final round.
    
    timing.start()
    Combinatorial_Time = 0.0
    theseExcitedConformers = ''
    previousExcitedConformers = theseExcitedConformers
    #theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
    theseExcitedConformers = rotlibCollection.getNextRotamersByELEnergy()

    total_count = 0
    count_since_last_best = 0
    max_count = SCREAM_PARAMS.getMaxSearchNumber()
    lowestE = 999999999

    while len(theseExcitedConformers) != 0:
        total_count += 1
        if total_count > max_count:
            break
        count_since_last_best = count_since_last_best +1

        #timing.start()
        #placeMultipleConformers(ptn, theseExcitedConformers, mutInfo_rotConnInfo_Dict)
        placeMultipleConformers_fastVersion(ptn, theseExcitedConformers, previousExcitedConformers, mutInfo_rotConnInfo_Dict) # ptn is attached to scream_EE
        #timing.finish()

        ##print ' ----- A New Loop -----'
        #print 'Timing: PlaceMultipleConformers time: ' + str(timing.micro() / 1000000.00)
        
        #all_interactions_E = scream_EE.calc_all_interaction_E() # where total energy is calculated

        #timing.start()
        
        all_interactions_E = Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS)
        crntEnergy = all_interactions_E
        #timing.finish()

        #print 'Timing: Calc_This_Interaction_Energy time: ' + str(timing.micro() / 1000000.00)

        #timing.start()
        for mutInfo in theseExcitedConformers.keys():
            crntConformer = theseExcitedConformers[mutInfo]
            crntEnergy += crntConformer.get_empty_lattice_E()
        #timing.finish()

        #print 'Timing: Adding up empty_lattice_E time: ' + str(timing.micro() / 1000000.00)

        print "Energy for current rotamer configuration: " + str(crntEnergy)
        print

        #timing.start()
        rotlibCollection.setEnergyForExcitedRotamers(theseExcitedConformers, crntEnergy)
        #timing.finish()

        #print 'Timing: setEnergyForExcitedRotamers time: ' + str(timing.micro() / 1000000.00)

        if crntEnergy < lowestE:
            lowestE = crntEnergy
            count_since_last_best = 0

        timing.finish()
        Combinatorial_Time = Combinatorial_Time + (timing.micro() / 1000000.00)
        timing.start()
        
        allowed_time = SCREAM_PARAMS.getMaxFinalStepRunTime()

        # TEMPORARY LINE
        # if total_count >= 100: # rachel's case: 2526 first one with energy < -42 kcal/mol
#             print 'TEMPORARY BREAKPOINT, for rachels case'
#             break

        if rotlibCollection._shouldKeepGoing(count_since_last_best, Combinatorial_Time, allowed_time): # max_count < 1000: just evaluate them all.

            #timing.start()
            previousExcitedConformers = theseExcitedConformers
            #theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
            theseExcitedConformers = rotlibCollection.getNextRotamersByELEnergy()
            #            timing.finish()
            #print 'Timing: After getNextDynamicMemoryRotamers_And_ExpandPy time: ' + str(timing.micro() / 1000000.00)

        else:
            break

    timing.finish()
    Combinatorial_Time = Combinatorial_Time + (timing.micro() / 1000000.00)
    print 'SCREAM Combinatorial took ' + str(Combinatorial_Time) + ' seconds.'

    # SCREAM v2.1.  Scheme 1) adding a final round of iteration over all SCREAM'ed positions.
    # First, get best structure at this point.
    # print 'Redoing all rotamers after optimized structure...'
    #     (afterOptEnergy, bestRotamersAfterOptimizationRound) = placeBestStructureSoFar(ptn, rotlibCollection, mutInfo_rotConnInfo_Dict)

    # Then, iteratate through all SCREAM'ed position, starting from... an arbitrary one for now.  Accept only if a better structure is found.
    # for mutInfo in Libraries_Dict.keys():
#         library = Libraries_Dict[mutInfo]
#         library.sort_by_empty_lattice_E()
#         library.reset_pstn()
#         crntBestRotamer = ''
#         crntRotamer = library.get_next_rot()

#         count = 1
#         Total_E = 99999.99999

#         while crntRotamer != None:
#             EL_energy = crntRotamer.get_empty_lattice_E()
#             EL_coulomb_E = crntRotamer.get_sc_coulomb_E()
#             EL_vdw_E = crntRotamer.get_sc_vdw_E()
#             EL_hb_E = crntRotamer.get_sc_hb_E()
#             EL_preCalc_E = crntRotamer.get_preCalc_TotE()
#             print '\nIteration Round: ', mutInfo
#             print '\nRotamer', count
#             print 'EL energies: %5d %3s %10.5f %10.5f %10.5f %10.5f %10.5f' % (count, mutInfo, EL_energy, EL_vdw_E, EL_coulomb_E, EL_hb_E, EL_preCalc_E )

#             count += 1
#             placeSingleConformer(ptn, mutInfo, crntRotamer, mutInfo_rotConnInfo_Dict)
#             all_interactions_E = Calc_This_Interaction_Energy_For_Iteration(scream_EE, SCREAM_PARAMS)

#             new_Total_E = all_interactions_E + EL_energy

#             if new_Total_E < Total_E:
#                 print 'Better energy structure found for %s. New energy: %10.5f  Old energy: %10.5f ' % (mutInfo, new_Total_E, Total_E)
#                 Total_E = new_Total_E
#                 crntBestRotamer = crntRotamer
#             crntRotamer = library.get_next_rot()

#         placeSingleConformer(ptn, mutInfo, crntBestRotamer, mutInfo_rotConnInfo_Dict)
#         print 'Best Energy after %s iteration: %10.5f ' % (mutInfo, Total_E)
        
    # Then print the best structure from these guys.
    #filename = 'IteratedBestStructure.bgf'
    #BGF_HANDLER.printToFile(filename)
    
    # Then print the best structures.
    printBestStructures(ptn, BGF_HANDLER, rotlibCollection, SCREAM_PARAMS, mutInfo_rotConnInfo_Dict)
    printEnergyEvolution(rotlibCollection)

    print "Total number of rotamer configuration sets evaluated: " + str(total_count)

    if total_count > max_count:
        print "Maximum number of rotamer configuration searches reached, quitting."

    # calc individual energy components
    print 'Now calculate individual energy components.'
    selections = SCREAM_PARAMS.Selections
    for i in range(1,selections+1):
        if SCREAM_PARAMS.getKeepOriginalRotamer() == 'YES':
            os.system('/ul/victor/SCREAM_variants/SCREAM_only_energies.py %s best_%i.bgf' % (ctl_file, i))
        else:
            os.system('/ul/victor/SCREAM_variants/SCREAM_calc_interactions.py %s best_%i.bgf' % (ctl_file, i))
    print 'SCREAM all done!  Exiting.'


def make_new_rotlib(SCREAM_MODEL, Libraries_Dict, mutInfo_rotConnInfo_Dict = None):

    # First, Setups.
    new_Rotlib = SCREAM_MODEL.new_Rotlib()
    ptn = SCREAM_MODEL.ptn
    SCREAM_PARAMS = SCREAM_MODEL.scream_parameters
    rotlibCollection = RotlibCollectionPy()
    initialize_rotlibCollection(rotlibCollection, Libraries_Dict)

    scream_EE = Scream_EE() # not adding to SCREAM_MODEL because it's only being used in this routine.
    for mutInfoString in Libraries_Dict.keys():
        mI = MutInfo(mutInfoString)
        
        for arblib_mI in mutInfo_rotConnInfo_Dict:
            mI.searchAndAddRotConnInfo(MutInfo(arblib_mI), mutInfo_rotConnInfo_Dict[arblib_mI])
            
        scream_EE.addMutInfoRotConnInfo(mI)
    scream_EE.init_after_addedMutInfoRotConnInfo_neighbor_list(ptn, SCREAM_PARAMS.getOneEnergyFFParFile(), SCREAM_PARAMS.getDeltaParFile() )
    scream_EE.setDistanceDielectricPrefactor(SCREAM_PARAMS.getDistanceDielectricPrefactor()) # added 12-9-05
    _initScreamAtomDeltaValuePy(scream_EE, SCREAM_PARAMS) # added 9-23-06

    
    # First do excitations.
    theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
    total_count = 0
    count_since_last_best = 0
    max_count = SCREAM_PARAMS.getMaxSearchNumber()
    lowestE = 999999999

    #maxRotamerConfigurations = rotlibCollection.maxRotamerConfigurations
    isLessThan1000 = rotlibCollection.cmpMaxRotamerConfigurations(1000)
    print "Is the maximum number of rotamer configurations less than 1000?  If so, just evaluate all rotamers in positions in this cluster (1==YES, 0==NO): " + str(isLessThan1000)
    #sys.exit(2)

    new_mutInfo = MutInfo() # 11-29-05

    while len(theseExcitedConformers) != 0:
        total_count += 1
        if total_count > max_count:
            break
        count_since_last_best = count_since_last_best +1
        placeMultipleConformers(ptn, theseExcitedConformers, mutInfo_rotConnInfo_Dict)
        #all_interactions_E = scream_EE.calc_all_interaction_E() # where total energy is calculated
        all_interactions_E = Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS)
        crntEnergy = all_interactions_E
    
        for mutInfo in theseExcitedConformers.keys():
            crntConformer = theseExcitedConformers[mutInfo]
            #crntEnergy += crntConformer.get_sc_total_E()
            crntEnergy += crntConformer.get_empty_lattice_E()

        # Now add new rotamer to new rotlib.
        new_cluster_rotamer = new_Rotlib.new_rotamer_cluster()
        new_mutInfo = MutInfo()
        for mutInfo in theseExcitedConformers.keys():
            crntConformer = theseExcitedConformers[mutInfo]
            new_cluster_rotamer.addRotamerCluster(crntConformer)
            new_mutInfo.addMutInfo(mutInfo)
            
        
        new_cluster_rotamer.set_empty_lattice_E_abs(crntEnergy)
        new_cluster_rotamer.set_rotamer_n(total_count)

        # Keep going.
        rotlibCollection.setEnergyForExcitedRotamers(theseExcitedConformers, crntEnergy)
                
        if crntEnergy < lowestE:
            lowestE = crntEnergy
            count_since_last_best = 0


        if rotlibCollection._shouldKeepGoing(count_since_last_best, 0, 1) or isLessThan1000 == 1:
            theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
        else:
            break

    # cleaning up new_Rotlib.
    new_Rotlib.sort_by_empty_lattice_E()
    new_Rotlib.reset_pstn()

    rot = new_Rotlib.get_next_rot()
    while rot != None:
        print str(rot.get_rotamer_n())
        print ' Get_empty_lattice_E: ' + str(rot.get_empty_lattice_E())
        print ' Get_empty_lattice_E_abs: ' + str(rot.get_empty_lattice_E_abs())

        rot = new_Rotlib.get_next_rot()


    #Making new Library Dict.  commented out: 11-29-05
    # new_mutInfo = MutInfo()
#     for mutInfo in theseExcitedConformers.keys():
#         new_mutInfo.addMutInfo(mutInfo) # make merge string routine, modify from MutInfo   WORKING ON THIS!  

    new_Library_Dict = {}
    new_Library_Dict[new_mutInfo.getString()] = new_Rotlib

    t = new_Library_Dict

    return new_Library_Dict



def ground_state_calc_and_cluster(SCREAM_MODEL, scream_EE, Primieval_Libraries_Dict, mutInfo_rotConnInfo_Dict):
    # For now, mutInfo_rotConnInfo_Dict says nothing new.  all Libraries_Dict for ground_state_calc and cluster MUST be NtrlAARotlib.
    # I.e., all rotConnInfo == NULL.

    # RotlibCollection Init.
    ptn = SCREAM_MODEL.ptn
    SCREAM_PARAMS = SCREAM_MODEL.scream_parameters

    new_scream_EE = scream_EE
    new_Libraries_Dict = Primieval_Libraries_Dict
    new_mutInfo_rotConnInfo_Dict = mutInfo_rotConnInfo_Dict

    rotlibCollection = RotlibCollectionPy()
    rotlibCollection.setHighestAllowedRotamerE(SCREAM_PARAMS.StericClashCutoffEnergy)
    initialize_rotlibCollection_for_clash(rotlibCollection, new_Libraries_Dict)

    # ClashCollection Init.
    clashCollection = ClashCollection(15)
    new_scream_EE.addClashCollection(clashCollection)
    rotlibCollection.addClashCollection(clashCollection)
    
    # Keep going until the ClashCollection returns no clashes
    while (1):
        theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()

        placeClusters(ptn, theseExcitedConformers, mutInfo_rotConnInfo_Dict)
        all_interactions_E = Calc_This_Interaction_Energy(new_scream_EE, SCREAM_PARAMS)
        
        # get clash collection info
        print 'clash.getNumberOfClashes: ' + str(clashCollection.getNumberOfClashes())
        if clashCollection.getNumberOfClashes() == 0:
            print "All ground state clashes eliminated!"
            break
        else:
            print "Eliminating ground state clashes."
            # cluster rotlibs that correspond to rotamer, calc new cluster energies.
            list = clashCollection.getDiscreteClashPairList() # returns top clashing pair
            # For each clash component, do local multiple excitation.
            for mutInfoPair in list:
                mI1 = mutInfoPair.getMutInfo1()
                mI2 = mutInfoPair.getMutInfo2()

                local_Library_Dict = {}
                local_Library_Dict[mI1.getString()] = Primieval_Libraries_Dict[mI1.getString()]
                local_Library_Dict[mI2.getString()] = Primieval_Libraries_Dict[mI2.getString()]

                # build new Rotamers for this set of RotlibCollection and scream_EE

                clustered_Library_Dict = make_new_rotlib(SCREAM_MODEL, local_Library_Dict, mutInfo_rotConnInfo_Dict)


                # update Libraries_Dict, mutInfo_rotConnInfo_Dict
                del new_Libraries_Dict[mI1.getString()]
                del new_Libraries_Dict[mI2.getString()]

                new_Libraries_Dict.update(clustered_Library_Dict)
                
            # new round of RotlibCollection and scream_EE
            print "Second round of ground state clash elimination." 
            rotlibCollection = RotlibCollectionPy()
            new_scream_EE = Scream_EE()
            initialize_rotlibCollection_for_clash(rotlibCollection, new_Libraries_Dict)

            initialize_scream_EE(ptn, SCREAM_PARAMS, new_scream_EE, new_Libraries_Dict, mutInfo_rotConnInfo_Dict)
            
            # ClashCollection Init.
            clashCollection = ClashCollection(15)
            new_scream_EE.addClashCollection(clashCollection)
            rotlibCollection.addClashCollection(clashCollection)
            scream_EE.addClashCollection(clashCollection)

    print 'Exiting ground state calc and clashes!'
    return (new_scream_EE, new_Libraries_Dict, new_mutInfo_rotConnInfo_Dict)


def initialize_rotlibCollection_for_clash(rotlibCollection, Libraries_Dict):
    
    for mutInfo in Libraries_Dict.keys():
        library = Libraries_Dict[mutInfo]
        rotlibCollection.addRotlib(mutInfo, library)
    numberOfRotlib = len(Libraries_Dict)
    rotlibCollection.initDynamicMemoryDataStructures()


def initialize_rotlibCollection(rotlibCollection, Libraries_Dict):
    
    for mutInfo in Libraries_Dict.keys():
        library = Libraries_Dict[mutInfo]
        rotlibCollection.addRotlib(mutInfo, library)
    numberOfRotlib = len(Libraries_Dict)
    if numberOfRotlib <= 10:
        rotlibCollection.initDynamicMemoryDataStructures()
    else:
        #timing.start()
        rotlibCollection.initAllocationUnderEnergyThreshold(0.1) # 0.1 kcal.
        #timing.finish()
        #print "initAllocationUnderEnergyThreshold took: " + str(timing.micro() / 1000000.00)
    
def initialize_scream_EE(ptn, SCREAM_PARAMS, scream_EE, Libraries_Dict, mutInfo_rotConnInfo_Dict):
    for mutInfoString in Libraries_Dict.keys():
        mI = MutInfo(mutInfoString)
        for arblib_mI in mutInfo_rotConnInfo_Dict:
            mI.searchAndAddRotConnInfo(MutInfo(arblib_mI), mutInfo_rotConnInfo_Dict[arblib_mI])
        
        scream_EE.addMutInfoRotConnInfo(mI)

    scream_EE.init_after_addedMutInfoRotConnInfo_neighbor_list(ptn, SCREAM_PARAMS.getOneEnergyFFParFile(), SCREAM_PARAMS.getDeltaParFile() )
    scream_EE.setDistanceDielectricPrefactor(SCREAM_PARAMS.getDistanceDielectricPrefactor()) # added 12-9-05
    
def init_Scream_EE(scream_EE, SCREAM_PARAMS, ptn, Libraries_Dict, mutInfo_rotConnInfo_Dict):
    '''
    Inits scream_EE using a protein structure and a SCREAM_PARAMs structure.
    '''
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    if ntrlMutInfo_list.size() == 1 and ntrlMutInfo_list[0] == 'DESIGN':
        ntrlMutInfo_list = []
    elif ntrlMutInfo_list.size() == 1 and ntrlMutInfo_list[0] == 'BINDING_SITE':
        ntrlMutInfo_list = []

    for mutInfo in Libraries_Dict:
        ntrlMutInfo_list.append(mutInfo)

    for mutInfo in ntrlMutInfo_list:
        mI = MutInfo(mutInfo)
        scream_EE.addMutInfoRotConnInfo(mI)
    for mutInfo in mutInfo_rotConnInfo_Dict.keys():
        mI = MutInfo(mutInfo)
        rotConnInfo_z = mutInfo_rotConnInfo_Dict[mutInfo]
        mI.setRotConnInfo(rotConnInfo_z) # 9-08-05: MutInfo() now contains info about RotConnInfo.
        scream_EE.addMutInfoRotConnInfo(mI, rotConnInfo_z)

    ff_file = SCREAM_PARAMS.getOneEnergyFFParFile()
    scream_delta_file = SCREAM_PARAMS.getDeltaParFile()

    #ff_file = 'dreidii322-mpsim-dielectric-2.5.par'
    #scream_delta_file = '/project/Biogroup/Software/SCREAM/lib/SCREAM_delta_par_files/SCREAM_delta.par'
    #scream_EE.init_after_addedMutInfoRotConnInfo(ptn, ff_file, scream_delta_file)
    if SCREAM_PARAMS.getUseRotamerNeighborList() == 'YES':
        scream_EE.init_after_addedMutInfoRotConnInfo_neighbor_list(ptn, ff_file, scream_delta_file)
        scream_EE.setDistanceDielectricPrefactor(SCREAM_PARAMS.getDistanceDielectricPrefactor()) # added 12-9-05, default = 2.5
    else:
        scream_EE.init_after_addedMutInfoRotConnInfo_on_the_fly_E(ptn, ff_file, scream_delta_file)
        print str( SCREAM_PARAMS.getDistanceDielectricPrefactor())
        scream_EE.setDistanceDielectricPrefactor(SCREAM_PARAMS.getDistanceDielectricPrefactor()) # added 12-9-05

    # Then, init FULL pre-initialization.
    _initScreamAtomDeltaValuePy(scream_EE, SCREAM_PARAMS)

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

def placeBestStructureSoFar(ptn, rotlibCollection, Conformer_RotConnInfo_Dict):
    rotlibCollection.resetTotalEnergyCrntPstn()
    bestRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()
    placeMultipleConformers(ptn, bestRotamers, Conformer_RotConnInfo_Dict)
    groundStateE = rotlibCollection.getEnergyForExcitedRotamers(bestRotamers)
    return (groundStateE, bestRotamers)
    

def printBestStructures(ptn, BGF_HANDLER, rotlibCollection, SCREAM_PARAMS, Conformer_RotConnInfo_Dict):
      """Prints best structures give a rotlibCollection, with the total number specfied by the Selections parameter in SCREAM param file."""
      print "Printing Best Structures!"
      count = 1
      filename_prefix = 'best_'
      rotlibCollection.resetTotalEnergyCrntPstn()
      theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()

      seqList = []

      # First print the one with the best energy.
      filename = filename_prefix + `count` + '.bgf'

      placeMultipleConformers(ptn, theseExcitedRotamers, Conformer_RotConnInfo_Dict)
      groundStateHandler = bgf_handler(BGF_HANDLER)
      groundStatePtn = Protein(groundStateHandler.getAtomList())
      groundStateE = 0
      
      if SCREAM_PARAMS.getJustOutputSequence() != 'YES':
          # Get energies, which positions have their rotamers changed, and CRMS among the changes.
          # 1. energies.
          groundStateE = rotlibCollection.getEnergyForExcitedRotamers(theseExcitedRotamers)
          # 2. Which ones changed?
          groundStatePtn.fix_toggle(0)
          groundStateHandler.printToFile(filename, ' Energy: ' + str(groundStateE) + ' kcal/mol Relative to ground state: 0 kcal/mol')
      else:
          seqString = str(count) + " " + BGF_HANDLER.returnSequence()
          seqList.append(seqString)
      theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()

      # Then proceed with the others
      while len(theseExcitedRotamers) != 0:
          count = count+1
          filename = filename_prefix + `count` + '.bgf'
          if count > SCREAM_PARAMS.Selections:
              break
          placeMultipleConformers(ptn, theseExcitedRotamers, Conformer_RotConnInfo_Dict)
          excitedRotamerInfo = rotlibCollection.emptyLatticeRankInfo(theseExcitedRotamers)
          if SCREAM_PARAMS.getJustOutputSequence() != 'YES':
              # Get energies, which positions have their rotamers changed, and CRMS among the changes.
              # 1. energies.
              E = rotlibCollection.getEnergyForExcitedRotamers(theseExcitedRotamers)
              E_string = '%10.4f' % E
              # 2. Which ones changed and CRMS.
              whichOnesChangedAndCRMSString = returnWhichSideChainsChangedAndCRMSString(groundStatePtn, ptn, rotlibCollection, theseExcitedRotamers, Conformer_RotConnInfo_Dict)
              differenceFromGroundStateE = E - groundStateE
              differenceFromGroundStateE_string = '%10.4f' % differenceFromGroundStateE
              ptn.fix_toggle(0)
              BGF_HANDLER.printToFile(filename, ' Energy: ' + E_string + ' kcal/mol Relative to ground state: ' + differenceFromGroundStateE_string + ' kcal/mol CRMS From Ground State is different for the following SideChains: ' + whichOnesChangedAndCRMSString)
          else:
              seqString = str(count) + " " + BGF_HANDLER.returnSequence()
              seqList.append(seqString)
          theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()

      # Printing seqList to a file.
      if SCREAM_PARAMS.getJustOutputSequence() == 'YES':
          SeqOutput = open('Sequences.txt', 'w')
          for seq in seqList:
              SeqOutput.write(seq)
              SeqOutput.write('\n')
          SeqOutput.close()
          
      print 'Done printing Best Structures.'

def returnWhichSideChainsChangedAndCRMSString(groundStatePtn, excitedPtn, rotlibCollection, excitedRotamers, Conformer_RotConnInfo_Dict):
    completeBreakdownDict = rotlibCollection.emptyLatticeRankInfo_completeBreakdown(excitedRotamers, Conformer_RotConnInfo_Dict)
    SC_PlacementInfo_String = ''
    
    for k in completeBreakdownDict.keys():
        CRMS = 0
        if k[0] == 'Z':
            # arb lib CRMS calculation
            rotConnInfo = Conformer_RotConnInfo_Dict[k]
            CRMS = groundStatePtn.conformer_CRMS(excitedPtn, rotConnInfo)
        else:
            (AA_type, pstn, chain) = unpackMutInfo(k)
            CRMS = groundStatePtn.sc_CRMS(chain, pstn, excitedPtn)
        
        if CRMS <= 0.001:
            continue
        else:
            CRMS_string = '%5.3f' % CRMS
            SC_PlacementInfo_String = SC_PlacementInfo_String + k + ' ' + CRMS_string + ' '
    return SC_PlacementInfo_String

    


def placeClusters(ptn, clustersDict, clusterRotConnInfoDict = None):
    '''
    Places rotamer clusters.
    '''
    # Need to add arblib info to MutInfo, else can't place arb libs.
    for mutInfo in clustersDict.keys():
        cluster = clustersDict[mutInfo]
        
        mI = MutInfo(mutInfo)

        for arblib_mI in clusterRotConnInfoDict:
            mI.searchAndAddRotConnInfo(MutInfo(arblib_mI), clusterRotConnInfoDict[arblib_mI])

        ptn.rotamerClusterPlacement(cluster, mI)
        

def placeSingleConformer(ptn, mutInfo, conformer, mutInfo_rotConnInfo_Dict):
     (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
     mI = MutInfo()
     mI.init(mutInfo)

     if mutAA != 'Z':
         ptn.ntrlRotamerPlacement(mutChn, mutPstn, conformer)
         if ptn.mutationDone():
             int_map = ptn.getNewMapping()
             for i in mutInfo_rotConnInfo_Dict.keys():
                 mutInfo_rotConnInfo_Dict[i].modifyMappingInProteinAtoms(int_map)
     else:
         rotConnInfo_Z = mutInfo_rotConnInfo_Dict[mutInfo]
         ptn.conformerPlacement(conformer, rotConnInfo_Z)
     

def placeMultipleConformers(ptn, conformersDict, conformerRotConnInfoDict = None):
    '''
    More general than placeMultipleSideChains.  Should replace all instances of placeMultipleSideChains.
    '''
    #print ' ----------------- placeMultipleConformers timing ------------------------'
    for mutInfo in conformersDict.keys():
        conformer = conformersDict[mutInfo]
        (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
        
        if mutAA == 'Cluster' and mutChn == 'Cluster':
            clusterDict = {}
            clusterDict[mutInfo] = conformer
            placeClusters(ptn, clusterDict, conformerRotConnInfoDict)
            
        elif mutAA == 'Z' and mutChn == 'Z': # should not enter this conditional if conformersDict contains only rotamers.
            rotConnInfo = conformerRotConnInfoDict[mutInfo]
            ptn.conformerPlacement(conformer, rotConnInfo)
            
        #elif mutAA == 'H' or mutAA == 'J': # special HIS singly protonation case.  might not be necessary.
        #ptn.ntrlRotamerPlacement(mutChn, mutPstn, castRotamerToAARotamer(conformer))
        else:
            ptn.ntrlRotamerPlacement(mutChn, mutPstn, castRotamerToAARotamer(conformer))
            if ptn.mutationDone():
                int_map = ptn.getNewMapping()
                for i in conformerRotConnInfoDict.keys():
                    conformerRotConnInfoDict[i].modifyMappingInProteinAtoms(int_map)

    #print ' ================= end placeMultipleConformers timing ========================'

def placeMultipleConformers_fastVersion(ptn, conformersDict, previousConformerDict, conformerRotConnInfoDict = None):
    '''
    More general than placeMultipleSideChains.  Should replace all instances of placeMultipleSideChains.
    '''
    #print ' ----------------- placeMultipleConformers_fastVersion timing ------------------------'
    if previousConformerDict == '':
        placeMultipleConformers(ptn, conformersDict, conformerRotConnInfoDict)
    else:
        for mutInfo in conformersDict.keys():
            conformer = conformersDict[mutInfo] # mutInfo is a string, not MutInfo()
            previousConformer = previousConformerDict[mutInfo]

            # string comparisons of conformers: swig use strings to represent C pointers.
            if str(conformer) != str(previousConformer):
                (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)

                if mutAA == 'Cluster' and mutChn == 'Cluster':
                    clusterDict = {}
                    clusterDict[mutInfo] = conformer
                    placeClusters(ptn, clusterDict, conformerRotConnInfoDict)

                elif mutAA == 'Z' and mutChn == 'Z': # should not enter this conditional if conformersDict contains only rotamers.
                    rotConnInfo = conformerRotConnInfoDict[mutInfo]
                    ptn.conformerPlacement(conformer, rotConnInfo)

                #elif mutAA == 'H' or mutAA == 'J': # special HIS singly protonation case.  might not be necessary.
                #ptn.ntrlRotamerPlacement(mutChn, mutPstn, castRotamerToAARotamer(conformer))
                else:
                    ptn.ntrlRotamerPlacement(mutChn, mutPstn, castRotamerToAARotamer(conformer))
                    if ptn.mutationDone():
                        int_map = ptn.getNewMapping()
                        for i in conformerRotConnInfoDict.keys():
                            conformerRotConnInfoDict[i].modifyMappingInProteinAtoms(int_map)
            else:
                pass
            
    #print ' ================= end placeMultipleConformers_fastVersion timing ========================'


    
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

            print '' 
            print 'Rotamer', count
            count += 1

            rot_E = 0
            rot_vdw_E  = 0
            rot_hb_E = 0
            rot_coulomb_E = 0
            rot_preCalc_E = 0
            
            if mutAA != 'Z':
                ptn.ntrlRotamerPlacement(mutChn, mutPstn, currentRotamer)
                if ptn.mutationDone():
                    int_map = ptn.getNewMapping()
                    for i in mutInfo_rotConnInfo_Dict.keys():
                        mutInfo_rotConnInfo_Dict[i].modifyMappingInProteinAtoms(int_map)
                if currentRotamer.get_is_Original_flag() == 1:
                    pass
                else:
                    rot_preCalc_E = currentRotamer.get_preCalc_TotE()
                    #print 'rot_preCalc_E is : ' + str(rot_preCalc_E)

            else:
                rotConnInfo_Z = mutInfo_rotConnInfo_Dict[mutInfo]
                ptn.conformerPlacement(currentRotamer, rotConnInfo_Z)
                
             # Now decide which SCREAM energy function to use
            if SCREAM_PARAMS.getUseScreamEnergyFunction() == 'YES':
                value = 0
                # Add big IF block here to take care of ASYM cases.
                if SCREAM_PARAMS.getUseDeltaMethod() == 'FLAT' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'NO':
                    
                    t = SCREAM_PARAMS.getFlatDeltaValue()

                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'FLAT', t)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'FLAT', t)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)

                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'FLAT', t)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E + rot_preCalc_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'PreCalc: ' + str(rot_preCalc_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    
                    #rot_E = scream_EE.calc_empty_lattice_E_full_delta(mI, t)
                    
                elif SCREAM_PARAMS.getUseDeltaMethod() == 'FULL' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'NO':

                    d = SCREAM_PARAMS.getDeltaStandardDevs()
                    #print 'FULL method. d value: ' + str(d)
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'FULL', d)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'FULL', d)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'FLAT', d)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E + rot_preCalc_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'PreCalc: ' + str(rot_preCalc_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    #rot_E = scream_EE.calc_empty_lattice_E_flat_delta(mI, d)

                elif SCREAM_PARAMS.getUseDeltaMethod() == 'SCALED' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'NO':
                    s = SCREAM_PARAMS.getInnerWallScalingFactor()
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'SCALED', s)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'SCALED', s)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'SCALED', s)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E + rot_preCalc_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'PreCalc: ' + str(rot_preCalc_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    
                elif SCREAM_PARAMS.getUseDeltaMethod() == 'RESIDUE':
                    # not implemented
                    #rot_E = scream_EE.calc_empty_lattice_E_residue_delta(mI)
                    pass

                # INSERT ASYM STUFF HERE
                elif SCREAM_PARAMS.getUseDeltaMethod() == 'FLAT' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'YES':

                    t = SCREAM_PARAMS.getFlatDeltaValue()

                    #print "IN FLAT ASYM" 

                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'FLAT_ASYM', t)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'FLAT_ASYM', t)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)

                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'FLAT', t)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E + rot_preCalc_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'PreCalc: ' + str(rot_preCalc_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    
                    #rot_E = scream_EE.calc_empty_lattice_E_full_delta(mI, t)
                    
                elif SCREAM_PARAMS.getUseDeltaMethod() == 'FULL' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'YES':

                    d = SCREAM_PARAMS.getDeltaStandardDevs()
                    #print 'FULL method. d value: ' + str(d)
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'FULL_ASYM', d)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'FULL_ASYM', d)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'FLAT', d)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E + rot_preCalc_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'PreCalc: ' + str(rot_preCalc_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)
                    #rot_E = scream_EE.calc_empty_lattice_E_flat_delta(mI, d)

                elif SCREAM_PARAMS.getUseDeltaMethod() == 'SCALED' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'YES':
                    s = SCREAM_PARAMS.getInnerWallScalingFactor()
                    rot_vdw_E = scream_EE.calc_empty_lattice_vdw_E_delta(mI, 'SCALED_ASYM', s)
                    rot_hb_E = scream_EE.calc_empty_lattice_hb_E_delta(mI, 'SCALED_ASYM', s)
                    rot_coulomb_E = scream_EE.calc_empty_lattice_coulomb_E_delta(mI)
                    #rot_vdw_hb_exclusion_E = scream_EE.calc_empty_lattice_vdw_hb_exclusion_E_delta(mI, 'SCALED', s)
                    rot_E = rot_vdw_E + rot_hb_E + rot_coulomb_E + rot_preCalc_E
                    #+ rot_vdw_hb_exclusion_E

                    print 'Total:   ' + str(rot_E)
                    print 'PreCalc: ' + str(rot_preCalc_E)
                    print 'VDW:     ' + str(rot_vdw_E)
                    print 'HB:      ' + str(rot_hb_E)
                    print 'Coulomb: ' + str(rot_coulomb_E)
                    #print 'VDW-HB Exclusion: ' + str(rot_vdw_hb_exclusion_E)

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

    # Then check to see if Absolute Energy > AbsStericClashCutoffEL.
    overall_steric_clash_flag = 1 # 1 means everything passes.  Needs all 1's to pass.
    AbsStericClashCutoffEL = SCREAM_PARAMS.getAbsStericClashCutoffEL()

    for mutInfo in Libraries_Dict.keys():
        (mutAA, mutPstn, mutChn) = unpackMutInfo(mutInfo)
        mI = MutInfo()
        mI.init(mutInfo)
        library = Libraries_Dict[mutInfo]
        library.reset_pstn()
        rot = library.get_next_rot()

        steric_clash_flag = 0 # 0 means none < AbsStericClashCutoffEL.  1 false is enough to fail.
        
        while rot != None:
            if rot.get_empty_lattice_E_abs() < AbsStericClashCutoffEL:
                steric_clash_flag = 1 # if there exist 1 candidate, return true.
                break
            rot = library.get_next_rot()

        if steric_clash_flag == 0:
            print ' No rotamers pass AbsStericClashCutoffEL test for library ' + mutInfo
            
        overall_steric_clash_flag = overall_steric_clash_flag and steric_clash_flag

    if overall_steric_clash_flag == 0:
        print ' Quiting! There are rotamer libraries for which no rotamers pass the AbsStericClashCutoffEL test. '
        sys.exit()

def Calc_This_Interaction_Energy_For_Iteration(scream_EE, SCREAM_PARAMS):
    #timing.start()
    deltaForInteractionE = SCREAM_PARAMS.getUseDeltaForInterResiE() # YES/NO
    DeltaMethod = SCREAM_PARAMS.getUseDeltaMethod()
    AsymFlag = SCREAM_PARAMS.getUseAsymmetricDelta()
    if AsymFlag == 'YES':
        DeltaMethod = DeltaMethod + '_ASYM'
    
    t = SCREAM_PARAMS.getFlatDeltaValue()
    #timing.finish()

    #print 'Timing: in python Calc_This_Interaction_Energy, getting values' + str(timing.micro() / 1000000.00)

    if deltaForInteractionE == 'YES':
        
        #timing.start()
        vdw_E = scream_EE.calc_all_interaction_vdw_E_delta(DeltaMethod, t)
        #timing.finish()
        #print 'Timing: vdw calc time: ' + str(timing.micro() / 1000000.00)
        
        #timing.start()
        hb_E = scream_EE.calc_all_interaction_hb_E_delta(DeltaMethod, t)
        #timing.finish()
        #print 'Timing: hb calc time: ' + str(timing.micro() / 1000000.00)        
        #timing.start()
        coulomb_E = scream_EE.calc_all_interaction_coulomb_E_delta()
        #timing.finish()
        #print 'Timing: coulomb calc time: ' + str(timing.micro() / 1000000.00)
        
        print "VDW Energy: " + str(vdw_E)
        print "HB Energy: " + str(hb_E)
        print "Coulomb Energy: " + str(coulomb_E)

        total_E = vdw_E + hb_E + coulomb_E
        print "Total Energy: " + str(total_E)
        
        return total_E
    else:
        return scream_EE.calc_all_interaction_E() # curently this is the default; soon won't be.  12-6-05.
    


            
def Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS):
    #timing.start()
    deltaForInteractionE = SCREAM_PARAMS.getUseDeltaForInterResiE() # YES/NO
    DeltaMethod = SCREAM_PARAMS.getUseDeltaMethod()
    AsymFlag = SCREAM_PARAMS.getUseAsymmetricDelta()
    if AsymFlag == 'YES':
        DeltaMethod = DeltaMethod + '_ASYM'
    
    t = SCREAM_PARAMS.getFlatDeltaValue()
    #timing.finish()

    #print 'Timing: in python Calc_This_Interaction_Energy, getting values' + str(timing.micro() / 1000000.00)

    if deltaForInteractionE == 'YES':
        
        #timing.start()
        vdw_E = scream_EE.calc_all_interaction_vdw_E_delta(DeltaMethod, t)
        #timing.finish()
        #print 'Timing: vdw calc time: ' + str(timing.micro() / 1000000.00)
        
        #timing.start()
        hb_E = scream_EE.calc_all_interaction_hb_E_delta(DeltaMethod, t)
        #timing.finish()
        #print 'Timing: hb calc time: ' + str(timing.micro() / 1000000.00)        
        #timing.start()
        coulomb_E = scream_EE.calc_all_interaction_coulomb_E_delta()
        #timing.finish()
        #print 'Timing: coulomb calc time: ' + str(timing.micro() / 1000000.00)
        
        print "VDW Energy: " + str(vdw_E)
        print "HB Energy: " + str(hb_E)
        print "Coulomb Energy: " + str(coulomb_E)

        total_E = vdw_E + hb_E + coulomb_E
        print "Total Energy: " + str(total_E)
        
        return total_E
    else:
        return scream_EE.calc_all_interaction_E() # curently this is the default; soon won't be.  12-6-05.
    


def Print_Library_EL_Energies(Libraries_Dict):
    filename = ''
    i = 1
    for mutInfo in Libraries_Dict.keys():
        filename = mutInfo + '.lib.EL'
        library = Libraries_Dict[mutInfo]
        library.sort_by_empty_lattice_E()
        library.reset_pstn()
        crntRotamer = library.get_next_rot()

        mI = MutInfo(mutInfo)
        
        OUTPUT = open(filename, 'w')
        print >>OUTPUT, '%5s %3s %10s %10s %10s %10s %10s' % ('Rank', 'RES', 'Tot Energy', 'VDW', 'Coulomb', 'HB', 'PreCalc')
        while crntRotamer != None:
            resName = ''
            if mI.isClusterMutInfo():
                resName = ' | '
            elif mutInfo[0] == 'Z':
                resName = mutInfo[0:3]
            else:
                resName = crntRotamer.get_resName()            

            EL_energy = crntRotamer.get_empty_lattice_E()
            EL_coulomb_E = crntRotamer.get_sc_coulomb_E()
            EL_vdw_E = crntRotamer.get_sc_vdw_E()
            EL_hb_E = crntRotamer.get_sc_hb_E()
            EL_preCalc_E = crntRotamer.get_preCalc_TotE()
            
            print >>OUTPUT, '%5d %3s %10.5f %10.5f %10.5f %10.5f %10.5f' % (i, resName, EL_energy, EL_vdw_E, EL_coulomb_E, EL_hb_E, EL_preCalc_E )
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
                
        if ntrlAA_list[0] == 'BINDING_SITE':

            aroundWhatEntity = SCREAM_PARAMS.getBindingSiteMode()
            aroundDistance = SCREAM_PARAMS.getAroundDistance()
            aroundDistanceDefn = SCREAM_PARAMS.getAroundDistanceDefn()
            mI_list = []
            
            if aroundWhatEntity == 'AroundAtom':
                list = SCREAM_PARAMS.getAroundAtom()
                if len(list) == 0:
                    print 'AroundAtom not defined!  Please specify AroundAtom parameters.'
                    sys.exit()
                mI_list = ptn.residuesAroundAtomN(list, aroundDistance, aroundDistanceDefn)
 
            if aroundWhatEntity == 'AroundResidue':
                list = SCREAM_PARAMS.getAroundResidue() # vector<MutInfo>
                if len(list) == 0:
                    print 'AroundResidue not defined!  Please specify AroundResidue parameters.'
                    sys.exit()
                mI_list = ptn.residuesAroundResidue(list, aroundDistance, aroundDistanceDefn) # vector<MutInfo>
                # Now, modify mI_list so that if a mutation is specified in AroundResidue, mI_list reflects this.
                getChnAndPstn = lambda mutInfo : mutInfo.getChn() + str(mutInfo.getPstn())
                mI_list_new = []
                print "##################"
                print mI_list
                map(lambda mI : mI.print_Me(), mI_list)
                print "\n"
                flag = 0 # if already added, has flag 1.  else flag 0.
                for mI in mI_list:
                    for aroundResidueMI in list:
                        #aroundResidueMI = MutInfo(aroundResidueStr)
                        if getChnAndPstn(aroundResidueMI) == getChnAndPstn(mI):
                            print aroundResidueMI.getString()
                            mI_list_new.append(MutInfo(aroundResidueMI.getString()))
                            flag = 1
                            break
                    if flag == 0:
                        mI_list_new.append(MutInfo(mI.getString()))
                    if flag == 1:
                        flag = 0
                map(lambda mI : mI.print_Me(), mI_list_new)
                print "#########"
                mI_list = [MutInfo(mI.getString()) for mI in mI_list_new]
                
            if aroundWhatEntity == 'AroundChain':
                list = SCREAM_PARAMS.getAroundChain()
                if len(list) == 0:
                    print 'AroundChain ot defined! Please specify AroundChain parameters.'
                mI_list = ptn.residuesAroundChain(list, aroundDistance, aroundDistanceDefn)

            fixedResidue_list = SCREAM_PARAMS.getFixedResidues()

            ntrlAA_list = []
            for mI in mI_list:
                mI_string = mI.getString()
                mutChn = mI_string[-1]
                if mI_string in fixedResidue_list:
                    continue
                if mutChn in fixedResidue_list:
                    continue
                if mI_string[0] == 'A' or mI_string[0] == 'G':
                    continue
                ntrlAA_list.append(mI_string)

            print 'List of Residues that would be replaced: ',
            for mIStr in ntrlAA_list:
                print mIStr,
            print ''


            
        if ntrlAA_list[0] != 'DESIGN': # 'DESIGN' has its own initialization loop above
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

                print 'Done loading ' + library_file + '.'
                Ntrl_Library_Dict[mutInfo] = library
            
                # then the original rotamers.
                originalRotamer = AARotamer()
                originalRotamer.deepcopy(ptn.getAARotamer(mutChn, mutPstn))

                originalRotamer.is_Original = 1
                Ntrl_Orig_Rotamer_Dict[mutInfo] = originalRotamer

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

    if mutInfo.find('|') != -1:
        return ('Cluster', 0, 'Cluster')
    else:
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
        #crntRotlib.sort_by_rotlib_E()
        crntRotlib.reset_pstn()
        lowestRotlibERot = crntRotlib.get_current_rot()
        #lowest_E = lowestRotlibERot.get_rotlib_E()
        lowest_preCalc_E  = crntRotlib.get_best_preCalc_E()
        
        # need to set an energy for original rotamer... right now just takes the lowset energy from rotlib_E.  need to be improved.
        crntRotamer = Original_Rotamer_Dict[mutInfo]
        crntRotamer.setDeclaredInRotlibScope(0)
        #crntRotamer.set_rotlib_E(lowest_E)
        crntRotamer.set_preCalc_TotE(lowest_preCalc_E)

        # if there is mutation, don't add rotamer.
        if crntRotamer.sameResidueTypeAs(lowestRotlibERot):
            crntRotlib.add_rotamer(crntRotamer) # if not, there is mutation , don't add rotamer.  There might be problems with this in design cases where you may possibly want the original rotamer.  That would have a more complicated decision tree.
    
    
def appendOriginalConformersToRotlibs(Conformer_Library_Dict, Original_Conformer_Dict):
    # Actually identical code to appendOriginalRotamersToRotlibs
    appendOriginalRotamersToRotlibs(Conformer_Library_Dict, Original_Conformer_Dict)


def cavityAnalysis(ptn, scream_EE, probeMutInfo, mutInfo_rotConnInfo_Dict, SCREAM_PARAM):
    # Does simple cavity analysis.
    mI_list = []
    if len(probeMutInfo) == 1:
        mI_list = ptn.residuesAroundChain(probeMutInfo, 3.5, 'SideChainOnly')
    else:
        mI_list = ptn.residuesAroundResidue(probeMutInfo, 3.5, 'SideChainOnly')

    for mI in mI_list:
        scream_EE
    pass

    

# RotlibCollectionPy class, derived from RotlibCollection, added convenience functions.

class RotlibCollectionPy(RotlibCollection):
    "RotlibCollection clas.  Convenience class derived from C++ RotlibCollection to make data transfer easier and cleaner."
    def __init__(self):
        RotlibCollection.__init__(self)
    
    def _shouldKeepGoing(self, count_since_last_best, elapsed_time, allowed_time):
        """Primitive decision whether or not to keep going."""
        #if count_since_last_best > 250:
        #return 0
        #else:
        #    return 1
        #print 'elapsed_time: ' + str(elapsed_time)
        #print 'allowed_time: ' + str(allowed_time)
        print 'Timing data (elapsed/allowed): ' + str(elapsed_time) + '/' + str(allowed_time)
        if elapsed_time > allowed_time:
            return 0
        
        sizeOfSystem = self.sizeOfSystem()
        testBlockSize = 1.8**(sizeOfSystem+1)
        #         if testBlockSize < 20:
        #             testBlockSize = 20
        #if testBlockSize < 300: # temporary, for design cases.
        #testBlockSize = 300
        if testBlockSize < 100:
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

    def emptyLatticeRankInfo_completeBreakdown(self, excitedRotamers, Conformer_RotConnInfo_Dict):
        '''Returns a A1_A B2_B C3_C string instead of a A1_A|B2_B||C3_C string, for instance.'''
        mutInfo_rank_dict = self.emptyLatticeRankInfo_in_dict_form(excitedRotamers)
        completeBreakdownDict = {}
        for k in mutInfo_rank_dict.keys():
            if '|' in k:
                splitList = k.split('|')
                for s in splitList:
                    if s == '':
                        continue
                    else:
                        if s in Conformer_RotConnInfo_Dict.keys():
                            completeBreakdownDict[s] = Conformer_RotConnInfo_Dict[s]
                        else:
                            completeBreakdownDict[s] = None
            else:
                #print 'size of Conformer_RotConnInfo_Dict: ' + str(len(Conformer_RotConnInfo_Dict))
                if k in Conformer_RotConnInfo_Dict.keys():
                    completeBreakdownDict[k] = Conformer_RotConnInfo_Dict[k]
                else:
                    completeBreakdownDict[k] = None
                
        return completeBreakdownDict
    
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

    def getNextRotamersByELEnergy_Py(self):
        '''Wrapper for getNextRotamersByELEnergy in RotlibCollection.'''
        excitedRotamersRightFormat = dict()
        excitedRotamersRightFormat = self.getNextRotamersByELEnergy()
        if excitedRotamersRightFormat.size() == 0:
            return {}
        return excitedRotamersRightFormat

    def getNextDynamicMemoryRotamers_And_ExpandPy(self):
        '''Returns a distionary of Python useable {string, Rotamer*} pairs instead of the C++ returned types {_p_string, _p_pAARotamer} or _p_pRotamer format.'''
        excitedRotamersRightFormat = dict()

        #timing.start()
        
        #excitedRotamersWrongFormat = self.getNextDynamicMemoryRotamers_And_Expand()
        excitedRotamersRightFormat = self.getNextDynamicMemoryRotamers_And_Expand()

        #timing.finish()

        #print ' getNextDynamicMemoryRotamers_And_Expand timing: ' + str(timing.micro() / 1000000.00)
        
        #if excitedRotamersWrongFormat.size() == 0:
        if excitedRotamersRightFormat.size() == 0:
            return {}
        # Don't go through following loop if size == 0.

        #timing.start()
        
        #for wrongFormatString in excitedRotamersWrongFormat.keys():
            #rightString = derefString(wrongFormatString)
            #   rightString = wrongFormatString
            #  wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            #rightRotamer = derefRotamer(wrongFormatRotamer)
            # rightRotamer = wrongFormatRotamer
            #excitedRotamersRightFormat[rightString] = rightRotamer

        #timing.finish()

        #print ' getNextDynamicMemoryRotamers_And_Expand python string conversion part timing: ' + str(timing.micro() / 1000000.00)
            
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
