#!/usr/bin/env python

import sys, os, re
from Py_Scream_EE import *

def usage():
    message = 'Usage: %s <scream par file> <new filename>\nOutput: Energy components, in a file. ' % sys.argv[0]
    print message
    sys.exit(0)

def main():
    if len(sys.argv) < 3:
        usage()


    ctl_file = sys.argv[1]
    new_filename = sys.argv[2]

    print new_filename

    new_ctl_file = '%s.par' % new_filename
    NEW_CTL_FILE = open(new_ctl_file, 'w')
    OLD_CTL = open(ctl_file, 'r')
    InputFileName_pat = re.compile(r'InputFileName')
    for l in OLD_CTL:
        if InputFileName_pat.search(l):
            #print "===================================================================="
            print >>NEW_CTL_FILE, 'InputFileName %s' % new_filename
        else:
            print >>NEW_CTL_FILE, l,
    OLD_CTL.close()
    NEW_CTL_FILE.close()

    ctl_file = new_ctl_file
    
    SCREAM_MODEL = ScreamModel(ctl_file)
    SCREAM_PARAMS = SCREAM_MODEL.scream_parameters
    BGF_HANDLER = SCREAM_MODEL.HANDLER
    originalStatePtn = SCREAM_MODEL.ptn
    scream_EE = SCREAM_MODEL.scream_EE
    alpha = 0
    method = ''
    if SCREAM_PARAMS.getUseDeltaMethod() == 'FLAT' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'NO':
        method = 'FLAT'
        alpha = SCREAM_PARAMS.getFlatDeltaValue()
    elif SCREAM_PARAMS.getUseDeltaMethod() == 'FULL' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'NO':
        method = 'FULL'
        alpha = SCREAM_PARAMS.getDeltaStandardDevs()
    elif SCREAM_PARAMS.getUseDeltaMethod() == 'FLAT' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'YES':
        method = 'FLAT_ASYM'
        alpha = SCREAM_PARAMS.getFlatDeltaValue()
    elif SCREAM_PARAMS.getUseDeltaMethod() == 'FULL' and SCREAM_PARAMS.getUseAsymmetricDelta() == 'YES':
        method = 'FULL_ASYM'
        alpha = SCREAM_PARAMS.getDeltaStandardDevs()
    else:
        print 'Not Implemented method! in SCREAM_calc_interactions.py, quitting.'
        sys.exit(0)
    
    # Rotamer Library init, and relevant info.
    (Libraries_Dict, mutInfo_rotConnInfo_Dict, ntrl_orig_rots) = initRotlibs(SCREAM_PARAMS, originalStatePtn)  # need ntrl_orig_rots so doesn't get deleted
    ntrlMutInfo_list = SCREAM_PARAMS.getMutateResidueInfoList()
    additionalLib_list = SCREAM_PARAMS.getAdditionalLibraryInfo()

    # scream_EE init.
    init_Scream_EE(scream_EE, SCREAM_PARAMS, originalStatePtn, Libraries_Dict, mutInfo_rotConnInfo_Dict)

    # Now need to identify which rotamer is actually the one placed.
    # 1. replicate protein
    newStateHandler = bgf_handler(BGF_HANDLER)
    newStatePtn = Protein(newStateHandler.getAtomList())

    # 2. then compare CRMS for all loaded rotamer libraries.
    crntRotamers = {} # {mutInfoString: rot*}
    crntRotamersEnergies = {} # {mutInfoString: [vdw_rot-selfBB, vdw_rot-otherBB, vdw_rot-otherSC, -selfBB, coulomb_rot-otherBB, coulomb_rot-otherSC, vdw_rot-selfBB, vdw_rot-otherBB, vdw_rot-otherSC]}
    for mIString in ntrlMutInfo_list:
        match_flag = 0
        crntRotlib = Libraries_Dict[mIString]

        crntRotlib.reset_pstn() # doesn't sort
        crntRotamer = crntRotlib.get_next_rot()

        mI = MutInfo(mIString)
        
        while (crntRotamer != None):
            newStatePtn.ntrlRotamerPlacement(mI.getChn(), mI.getPstn(), crntRotamer)
            CRMS = originalStatePtn.sc_CRMS(mI.getChn(), mI.getPstn(), newStatePtn)
            
            if CRMS <= 0.001:
                match_flag = 1
                crntRotamers[mIString] = crntRotamer
                # Calculate energies need: rot-selfBB, rot-otherBB, rot-otherSC
                internal_energy = crntRotamer.get_preCalc_TotE()
                vdw_selfBB_E = scream_EE.calc_EL_vdw_rot_selfBB(mI, method, alpha)
                vdw_otherBB_E = scream_EE.calc_EL_vdw_rot_otherBB(mI, method, alpha)
                vdw_otherSC_E = scream_EE.calc_EL_vdw_rot_fixedSC(mI, method, alpha)
                coulomb_selfBB_E = scream_EE.calc_EL_coulomb_rot_selfBB(mI)
                coulomb_otherBB_E = scream_EE.calc_EL_coulomb_rot_otherBB(mI)
                coulomb_otherSC_E = scream_EE.calc_EL_coulomb_rot_fixedSC(mI)
                hb_selfBB_E = scream_EE.calc_EL_hb_rot_selfBB(mI, method, alpha)
                hb_otherBB_E = scream_EE.calc_EL_hb_rot_otherBB(mI, method, alpha)
                hb_otherSC_E = scream_EE.calc_EL_hb_rot_fixedSC(mI, method, alpha)
                crntRotamersEnergies[mIString] = [internal_energy, vdw_selfBB_E, vdw_otherBB_E, vdw_otherSC_E, coulomb_selfBB_E, coulomb_otherBB_E, coulomb_otherSC_E, hb_selfBB_E, hb_otherBB_E, hb_otherSC_E]
                break
            else:
                crntRotamer = crntRotlib.get_next_rot()
                continue
            if match_flag != 0:
                print 'No rotamers matched! For ', mI, ' Error.  Exiting.'
                sys.exit(0)


    # 3. then calculate one point energy for this configuration.
    interaction_E = Calc_This_Interaction_Energy(scream_EE, SCREAM_PARAMS)

    # 4. then print all the energy numbers.
    OUTPUT = open('%s.Energies.txt' % new_filename[0:-4], 'w')
    print >>OUTPUT, '%7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s' % ('Res', 'Intern', 'V-sBB', 'V-oBB', 'V-fSC', 'C-sBB', 'C-oBB', 'C-fSC', 'H-sBB', 'H-oBB', 'H-fSC', 'V-Tot', 'C-Tot', 'H-Tot', 'Tot', 'SC-SC')
    tot_E_array = [0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0]
                
    for mI in crntRotamersEnergies.keys():
        print >>OUTPUT, '%7s' % mI ,
        tot_E = 0
        #for i in crntRotamersEnergies[mI]:
        for i in range(0,len(crntRotamersEnergies[mI]) ):
            this_E = crntRotamersEnergies[mI][i]
            print >>OUTPUT, ' %6.2f' % this_E,
            tot_E += this_E
            tot_E_array[i] += this_E

        tot_vdw = crntRotamersEnergies[mI][1] + crntRotamersEnergies[mI][2] + crntRotamersEnergies[mI][3]
        tot_coulomb = crntRotamersEnergies[mI][4] + crntRotamersEnergies[mI][5] + crntRotamersEnergies[mI][6]
        tot_hb = crntRotamersEnergies[mI][7] + crntRotamersEnergies[mI][8] + crntRotamersEnergies[mI][9]

        tot_E_array[10] += tot_vdw
        tot_E_array[11] += tot_coulomb
        tot_E_array[12] += tot_hb
        tot_E_array[13] += tot_E
        print >>OUTPUT, ' %6.2f' % tot_vdw,
        print >>OUTPUT, ' %6.2f' % tot_coulomb,
        print >>OUTPUT, ' %6.2f' % tot_hb,
        print >>OUTPUT, ' %6.2f' % tot_E,
        print >>OUTPUT, ' %6.2f' % interaction_E

    print >>OUTPUT, '%7s' % 'Tot',
    for E in tot_E_array:
        print >>OUTPUT, ' %6.2f' % E,
    print >>OUTPUT, ' %6.2f' % interaction_E
    os.system('rm %s' % new_ctl_file)

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
            lib_name = str(lib_name)
        method = 'FULL'
        alpha = SCREAM_PARAMS.getDeltaStandardDevs()
        eachAtomDeltaFile = SCREAM_PARAMS.getEachAtomDeltaFile()
        scream_EE.initScreamAtomDeltaValue(lib_name, method, alpha, eachAtomDeltaFile)

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

def unpackMutInfo(mutInfo):
    """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""

    if mutInfo.find('|') != -1:
        return ('Cluster', 0, 'Cluster')
    else:
        mutAA = mutInfo[0]
        (mutPstn, mutChn) = mutInfo[1:].split('_')
        mutPstn = int(mutPstn)
        return (mutAA, mutPstn, mutChn)


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
    




if __name__ == '__main__':
    main()
