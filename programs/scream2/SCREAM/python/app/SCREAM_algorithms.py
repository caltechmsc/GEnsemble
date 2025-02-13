#!/usr/bin/env python

import sys
from ModSCREAM import *
from ModulaSim import *
#from Py_Scream_EE import *
from cmdf.pymodsim.model.Model import MdModel
from cmdf.pymodsim.force.setup_forces import setup_forces
#from cmdf.pymodsim.min import minimize

import re
import time

def doSCREAM(model, SCREAM_ctl_file):
    print "doing SCREAM on SCREAM_ctl_file named: ", SCREAM_ctl_file
    starttime = time.time()
    # better if SCREAM_ctl_file Ptr is passed in instead of string.
    SCREAM = SCREAM_c(model, SCREAM_ctl_file)
    SCREAM.doSCREAM()

    stoptime = time.time()
    elapsed = stoptime - starttime
    print 'Total time elasped:', elapsed, ' seconds.'

    #print 'Correctin output for best_x.bgf files:'
    top_n = SCREAM.scream_parameters.Selections
    
    for i in range(1, top_n+1):
        filename = 'best_' + str(i) + '.bgf'
        print '  ' , filename
        import os
        #os.system("perl /ul/victor/temp/cmdf/SCREAM/python/app/Tests/fix_output.pl " + filename + " > temp_24682" + str(i) + '.bgf')
        #os.system("mv temp_24682" + str(i) + '.bgf' + ' best_' + str(i) + '.bgf')

    #print 'Done Correction!'
        
    

        
# SCREAM class.  Derived from ModSimSCREAMInterface, added new functionalities/algorithms.

class SCREAM_c(ModSimSCREAMInterface):
    "SCREAM class.  Contains algorithms to perform various sidechain placement algorithms."
    def __init__(self, model_t, SCREAM_ctl_file):
        print "Initializing SCREAM_c: SCREAM_ctl_file is: ", SCREAM_ctl_file

        print '============='
        print model_t.parameters
        print '============='
        j = model_t.parameters
        print j
        import SCREAM_parameters
        a = SCREAM_parameters.SCREAM_parameters()
        
        ModSimSCREAMInterface(a, model_t.ff_properties, model_t.atom_properties, model_t.unit_cell_properties, None, None, None, model_t.thermo_properties, SCREAM_ctl_file)
        
        #        ModSimSCREAMInterface.__init__(self, model_t.parameters, model_t.ff_properties, model_t.atom_properties, model_t.unit_cell_properties, None, None, None, model_t.thermo_properties, SCREAM_ctl_file)
        self.model = model_t
        
        self.Libraries_Dict = {}                    # Dict { mutInfo : Rotlib* }
        self.Original_Conformers_Dict = {}          # Dict { mutInfo : Rotamer* }
        self.Conformer_RotConnInfo_Dict = {}          # Dict { mutInfo : rotConnInfo* } for Conformers.
        self.scream_EE = ''
        
        self.KeepOriginalRotamer = self.scream_parameters.getKeepOriginalRotamer()
        self.UseScreamEnergyFunction = self.scream_parameters.getUseScreamEnergyFunction()
        
        if ( self.KeepOriginalRotamer == 'YES'):
            self.KeepOriginalRotamer = 1
        else:
            self.KeepOriginalRotamer = 0

        # Below: need to initialize scream_EE!!!
        if ( self.UseScreamEnergyFunction == 'YES'):
            self.UseScreamEnergyFunction = 1
            
        else:
            self.UseScreamEnergyFunction = 0
            
        #scream_parameters is initialized, through the ModSimSCREAMInterface constructor call
        print "printing libpath" , self.scream_parameters.determineLibDirPath()

    def _del__(self):
        '''
        Call me before exiting SCREAM.py!
        '''
        # if KeepOriginalRotamer not true, need to delete the newed AARotamers* and Rotamers* in self.Original_Conformers_Dict.  Otherwise taken care in Rotlib after they're appended.  Actually, not entirely sure on this.  Probably need to delete them, because of the setDeclaredInRotlibScope(0) line.
        
    def doSCREAM(self):
        ntrlAAPlacement_n = len(self.scream_parameters.getMutateResidueInfoList())
        additionLibrary_n = len(self.scream_parameters.getAdditionalLibraryInfo())

        TotalNumberOfPlacements = ntrlAAPlacement_n + additionLibrary_n

        # WORKING ON THIS.  Generalize this code so that accepting a AARotamer is just as straightforward as accepting a Conformer.
        # Break this into the following parts:
        # 1.  Prepare Rotlib*'s.  Including NtrlRotlib* Conformer Rotlib*'s.  Along the way, need to make copies of original rotamer structure.
        self.initRotlibs()
        # 2.  Then you can pass this onto the Energy Excitation SCREAM right away.

        # self.Libraries_Dict has now been initialized.
        if self.UseScreamEnergyFunction == 1:
            # need to initialize Scream_EE!
            ptn = self.getProtein()
            #self._init_scream_EE(ptn, "/ul/victor/ForceFieldFiles/dreidii322-modsim-scream.par")
            self._init_scream_EE(ptn, "/ul/victor/ForceFieldFiles/dreidii322-modsim-scream-VDW-90-epsin-2.5.par")
            #self._init_scream_EE(ptn, "/ul/victor/ForceFieldFiles/dreidii322-scream-EE.par")

            if TotalNumberOfPlacements == 1:
                if ntrlAAPlacement_n == 1:
                    self.SinglePlacement_scream_EE()
                if additionLibrary_n == 1:
                    self.SingleConformerPlacement_scream_EE()

            else:
                self.EmptyLatticeExcitationWithArbLib_scream_EE()
        else:
            if TotalNumberOfPlacements == 1:
                if ntrlAAPlacement_n == 1:
                    self.SinglePlacement()
                if additionLibrary_n == 1:
                    self.SingleConformerPlacement()

            else:
                #self.GroundStateExcitationWithArbLib()
                self.EmptyLatticeExcitationWithArbLib()

        # WORKING ON THIS!!!!!!!!!
    def initRotlibs(self):
        '''
        Initializes the following objects:
        self.Libraries_Dict                    # Dict { mutInfo : Rotlib* }
        self.Original_Conformers_Dict          # Dict { mutInfo : Rotamer* }
        self.Conformer_RotConnInfo_Dict        # Dict { mutInfo : rotConnInfo* } for Conformers.
        '''
        # First initialize the ntrlAARotlibs.

        ntrlAA_list = self.scream_parameters.getMutateResidueInfoList()
        Ntrl_Library_Dict = {}
        Ntrl_Orig_Rotamer_Dict = {}
                
        if len(ntrlAA_list) != 0:
            Ntrl_Library_Dict = self._populateNtrlLibraryDict(ntrlAA_list)
            Ntrl_Orig_Rotamer_Dict = self._populateNtrlOriginalRotamerDict(ntrlAA_list)

        print 'value of self.KeepOriginalRotamer: ', self.KeepOriginalRotamer

        if self.KeepOriginalRotamer:
            self._appendOriginalRotamersToRotlibs(Ntrl_Library_Dict, Ntrl_Orig_Rotamer_Dict)

        # Next initialize the Arbitrary rotamer libraries.

        additional_list = self.scream_parameters.getAdditionalLibraryInfo()
        Add_Library_Dict = {}
        Add_Orig_Conformer_Dict = {}
        mutInfo_rotConnInfo_Dict = {}
        
        if len(additional_list) != 0:
            (Add_Library_Dict, mutInfo_rotConnInfo_Dict) = self._populateAddLibraryDict(additional_list)
            Add_Orig_Conformer_Dict = self._populateAddOriginalRotamerDict(mutInfo_rotConnInfo_Dict)

        if self.KeepOriginalRotamer:
            self._appendOriginalConformersToRotlibs(Add_Library_Dict, Add_Orig_Conformer_Dict)
        
        # Put them together.
        Ntrl_Library_Dict.update(Add_Library_Dict)
        self.Libraries_Dict = Ntrl_Library_Dict.copy()     # Dict { mutInfo : Rotlib* }
        print  'Total Number of Libraries: ' , len(self.Libraries_Dict)
        print 'They are: '
        print self.Libraries_Dict
        
        Ntrl_Orig_Rotamer_Dict.update(Add_Orig_Conformer_Dict)
        self.Original_Conformers_Dict = Ntrl_Orig_Rotamer_Dict.copy()  # Dict { mutInfo : Rotamer* }
        
        self.Conformer_RotConnInfo_Dict = mutInfo_rotConnInfo_Dict.copy()           # Dict { mutInfo : rotConnInfo* } for Conformers.
        
                
    def SinglePlacement(self):
        # Might need major upgrade.
        assert(len(self.scream_parameters.getMutateResidueInfoList()) == 1), "Doing Single Placement Without Minimizaztion, yet residue list has more than just one sidechain to be replaced."
            
        # Initializing variables

        KeepOriginalRotamer = self.KeepOriginalRotamer

        mutResInfo = self.scream_parameters.getMutateResidueInfoList()[0]
        print "mutResInfo is " , mutResInfo

        mutAA = self.scream_parameters.residueToScreamName(mutResInfo)
        mutPstn = self.scream_parameters.residueToScreamPstn(mutResInfo)
        mutChn = self.scream_parameters.residueToScreamChn(mutResInfo)
        tolerance = self.scream_parameters.StericClashCutoffDist
        top_n = self.scream_parameters.Selections

        # print self.scream_parameters.determineLibDirPath()
        library_path_first_half = self.scream_parameters.determineLibDirPath()
        library_file_suffix = self.scream_parameters.determineLibDirFileNameSuffix()
        
        library_file = library_path_first_half + '/' + mutAA + '/' + mutAA + library_file_suffix
        library = NtrlAARotlib(library_file)
        print 'Done loading ' + library_file + '.'

        # take care of original rotamer
        originalRotamer = AARotamer()
        originalRotamer.deepcopy(self.getAARotamer(mutChn, mutPstn))
        originalRotamer.is_Original = 1

        mutInfo = mutResInfo
        originalRotamerDict = {}
        originalRotamerDict[mutInfo] = originalRotamer
        libraryDict = {}
        libraryDict[mutInfo] = library

        if KeepOriginalRotamer:
            self._appendOriginalRotamersToRotlibs(libraryDict, originalRotamerDict)
        
          
        self._SinglePlacementOverLibrary(mutAA, mutPstn, mutChn, library, tolerance, top_n=1)

        # print out top n structures

        i = 1
        library.reset_pstn()
        currentRotamer = library.get_next_rot()
        
        while (currentRotamer != None and i <= top_n):
            self.placeSideChain(mutChn, mutPstn, currentRotamer)
            filename = 'best_' + `i` + '.bgf'
            self.printToFile(filename)
            i = i+1
            currentRotamer = library.get_next_rot()
        else:
            #print 'Rotamer library contains no rotamer!'
            pass

    def SinglePlacement_scream_EE(self):
        # Recycles code from SinglePlacement(self).
        assert(len(self.scream_parameters.getMutateResidueInfoList()) == 1), "Doing Single Placement Without Minimizaztion, yet residue list has more than just one sidechain to be replaced."
        # Initializing variables

        KeepOriginalRotamer = self.KeepOriginalRotamer

        mutResInfo = self.scream_parameters.getMutateResidueInfoList()[0]
        print "mutResInfo is " , mutResInfo

        mutAA = self.scream_parameters.residueToScreamName(mutResInfo)
        mutPstn = self.scream_parameters.residueToScreamPstn(mutResInfo)
        mutChn = self.scream_parameters.residueToScreamChn(mutResInfo)
        tolerance = self.scream_parameters.StericClashCutoffDist
        top_n = self.scream_parameters.Selections

        # print self.scream_parameters.determineLibDirPath()
        library_path_first_half = self.scream_parameters.determineLibDirPath()
        library_file_suffix = self.scream_parameters.determineLibDirFileNameSuffix()
        
        library_file = library_path_first_half + '/' + mutAA + '/' + mutAA + library_file_suffix
        library = NtrlAARotlib(library_file)
        print 'Done loading ' + library_file + '.'

        # take care of original rotamer
        originalRotamer = AARotamer()
        originalRotamer.deepcopy(self.getAARotamer(mutChn, mutPstn))
        originalRotamer.is_Original = 1

        mutInfo = mutResInfo
        originalRotamerDict = {}
        originalRotamerDict[mutInfo] = originalRotamer
        libraryDict = {}
        libraryDict[mutInfo] = library

        if KeepOriginalRotamer:
            self._appendOriginalRotamersToRotlibs(libraryDict, originalRotamerDict)
        
        # Do Scream_EE stuff here.
        
        self._SinglePlacementOverLibrary_scream_EE(mutAA, mutPstn, mutChn, library, tolerance, top_n=1)

        i = 1
        library.reset_pstn()
        currentRotamer = library.get_next_rot()

        while (currentRotamer != None and i <= top_n):
            self.placeSideChain(mutChn, mutPstn, currentRotamer)
            filename = 'best_' + `i` + '.bgf'
            self.printToFile(filename)
            i = i+1
            currentRotamer = library.get_next_rot()
        else:
            #print 'Rotamer library contains no rotamer!'
            pass
        

    def SingleConformerPlacement(self):
        '''
        Single point conformer placement.
        Only instance when this function is called: no mutation specified, one Arb Lib specified.
        '''
        assert(len(self.Libraries_Dict) == 1)
        
        mutInfo = self.Libraries_Dict.keys()[0]
        library = self.Libraries_Dict[mutInfo]
        rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
        CLASH_THRESHOLD = self.scream_parameters.StericClashCutoffDist
        top_n = self.scream_parameters.Selections
        print 'Placing single conformer...'
        print 'Clash Threshold is set to ', CLASH_THRESHOLD

        self._SinglePlacementOverLibrary('Z', 1, 'Z', library, CLASH_THRESHOLD, top_n)
        # print out Top n structures.

        i = 1
        library.reset_pstn()
        currentRotamer = library.get_next_rot()
        top_n = self.scream_parameters.Selections
        
        while (currentRotamer != None and i <= top_n):
            rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
            self.placeConformer(currentRotamer, rotConnInfo)
            filename = 'best_' + `i` + '.bgf'
            self.printToFile(filename)
            i = i+1
            currentRotamer = library.get_next_rot()
        else:
            #print 'Rotamer library contains no rotamer!'
            pass
                

    def SingleConformerPlacement_scream_EE(self):
        '''
        Single point conformer placement using scream_EE.
        Only instance when this function is called: no mutation specified, one Arb Lib specified.
        '''
        assert(len(self.Libraries_Dict) == 1)
        
        mutInfo = self.Libraries_Dict.keys()[0]
        library = self.Libraries_Dict[mutInfo]
        rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
        CLASH_THRESHOLD = self.scream_parameters.StericClashCutoffDist
        top_n = self.scream_parameters.Selections
        print 'Placing single conformer...'
        print 'Clash Threshold is set to ', CLASH_THRESHOLD

        self._SinglePlacementOverLibrary_scream_EE('Z', 1, 'Z', library, CLASH_THRESHOLD, top_n)
        # print out Top n structures.

        i = 1
        library.reset_pstn()
        currentRotamer = library.get_next_rot()
        top_n = self.scream_parameters.Selections
        
        while (currentRotamer != None and i <= top_n):
            rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
            self.placeConformer(currentRotamer, rotConnInfo)
            filename = 'best_' + `i` + '.bgf'
            self.printToFile(filename)
            i = i+1
            currentRotamer = library.get_next_rot()
        else:
            #print 'Rotamer library contains no rotamer!'
            pass

    

    def _SingleEmptyLatticePlacementOverLibrary(self, mutAA, mutPstn, mutChn, rotamerLibrary, CLASH_THRESHOLD=0, top_n = 1):
        '''
        This function is same as _SinglePlacementOverLibrary except it populates the EmptyLatticeEnergy Field in Rotamer
        '''
        print "Residue replacement info: " , mutAA, mutPstn, mutChn
        print 'Tolerance: ', CLASH_THRESHOLD , 'Angstroms.'
        # place side chain, remaps everything, then calc energy, then store it.

        mutInfo = mutAA + str(mutPstn) + '_' + mutChn
        rotamerLibrary.reset_pstn()
        currentRotamer = rotamerLibrary.get_next_rot()

        Passed_Clash_Check = 0
        n_Passed_Clash_Check = 0
        
        while currentRotamer != None:
            if mutAA == 'Z' and mutChn == 'Z':             # if it's a conformer
                rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                self.placeConformer(currentRotamer, rotConnInfo)
                if self._conformerClashAboveThreshold(CLASH_THRESHOLD, rotConnInfo):
                    Passed_Clash_Check = 1
            else:                                          # if it's a ntrlRotamer
                self.placeSideChain(mutChn, mutPstn, currentRotamer)
                # self.remapModSimAtomList() #unnecessary; already taken care of in placeSideChain
                if self._sideChainsAboveClashThreshold(CLASH_THRESHOLD, mutChn, mutPstn):
                    Passed_Clash_Check = 1
            
            if Passed_Clash_Check:
                n_Passed_Clash_Check = n_Passed_Clash_Check +1
                self.model.compute_tot_forces()
                self.model.compute_thermo()
                currentRotamer.setPassedDistanceCutoff()
                currentRotamer.set_empty_lattice_E_abs(self.model.thermo_properties.te)
                print 'Rotamer ' + `currentRotamer.get_rotamer_n()` + " profile:"
                print_energy(self.model.thermo_properties)
                print 'Rotamer ' + `currentRotamer.get_rotamer_n()` + " energy: " + str(self.model.thermo_properties.te)
                print ''

            else:
                print 'This rotamer has a clash of below', CLASH_THRESHOLD
                print ''
                currentRotamer.set_empty_lattice_E_abs(999999999)
                currentRotamer.setFailedDistanceCutoff()

            currentRotamer = rotamerLibrary.get_next_rot()
            Passed_Clash_Check = 0
        else:
            rotamerLibrary.reset_pstn()
            pass

        # sort rotamer library.
        rotamerLibrary.sort_by_empty_lattice_E()

        currentRotamer = rotamerLibrary.get_next_rot()
        i = 1
        while currentRotamer != None:
            print 'Rotamer', i, 'empty Lattice Energy (abs):', currentRotamer.get_empty_lattice_E_abs()
            print 'Rotamer', i, 'empty Lattice Energy:', currentRotamer.get_empty_lattice_E()
            i = i+1
            currentRotamer = rotamerLibrary.get_next_rot()
        else:
            pass

        if n_Passed_Clash_Check == 0:
            print 'None of the rotamers in this library passed steric clash check!  Try relaxing your steric clash threshold, or check rotamer library.  Quiting.'
            import sys
            sys.exit()
                    
    
    def _SinglePlacementOverLibrary(self, mutAA, mutPstn, mutChn, rotamerLibrary, CLASH_THRESHOLD = 0, top_n = 1):
        '''
        This function takes in the position to be mutated/replaced and places all rotamers provided in the rotamerLibrary on the protein and evaluates the energy.
        These energies are then stored in the rotamerLibrary.
        If mutAA is 'Z' and mutChn is 'Z' conformer placement is done.
        '''
        print "Residue replacement info: " , mutAA, mutPstn, mutChn
        
        # place side chain, remaps everything, then calc energy, then store it.
        mutInfo = mutAA + str(mutPstn) + '_' + mutChn
        rotamerLibrary.reset_pstn()
        currentRotamer = rotamerLibrary.get_next_rot()
        n_Passed_Clash_Check = 0
        Passed_Clash_Check = 0
        print 'CLASH_THRESHOLD in SinglePlacementOverLibrary is ', CLASH_THRESHOLD
        while currentRotamer != None:
            if mutAA == 'Z' and mutChn == 'Z':             # if it's a conformer
                rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                self.placeConformer(currentRotamer, rotConnInfo)
                if self._conformerClashAboveThreshold(CLASH_THRESHOLD, rotConnInfo):
                    Passed_Clash_Check = 1
            else:                                          # if it's a ntrlRotamer
                self.placeSideChain(mutChn, mutPstn, currentRotamer)
                # self.remapModSimAtomList() #unnecessary; already taken care of in placeSideChain
                if self._sideChainsAboveClashThreshold(CLASH_THRESHOLD, mutChn, mutPstn):
                    Passed_Clash_Check = 1
            
            if Passed_Clash_Check:
                n_Passed_Clash_Check = n_Passed_Clash_Check +1
                self.model.compute_tot_forces()
                self.model.compute_thermo()
                currentRotamer.set_sc_total_E(self.model.thermo_properties.te)
                print 'Rotamer ' + `currentRotamer.get_rotamer_n()` + " profile:"
                print_energy(self.model.thermo_properties)
                print 'Rotamer ' + `currentRotamer.get_rotamer_n()` + " energy: " + str(self.model.thermo_properties.te)
                print ''
            else:
                print 'This rotamer has a clash of below', CLASH_THRESHOLD
                print ''
                currentRotamer.set_sc_total_E(999999999)
                currentRotamer.set_empty_lattice_E_abs(999999999)
                currentRotamer.setFailedDistanceCutoff()
            currentRotamer = rotamerLibrary.get_next_rot()
            Passed_Clash_Check = 0
        else:
            rotamerLibrary.reset_pstn()
            pass


        if n_Passed_Clash_Check == 0:
            print 'None of the rotamers in this library passed steric clash check!  Try relaxing your steric clash threshold, or check rotamer library.  Quiting.'
            import sys
            sys.exit()

        # sort rotamer library.
        rotamerLibrary.sort_by_self_E()
        currentRotamer = rotamerLibrary.get_next_rot()
        i = 1
        while currentRotamer != None:
            print 'Rotamer', i, 'energy:', currentRotamer.get_sc_total_E()
            i = i+1
            currentRotamer = rotamerLibrary.get_next_rot()
        else:
            pass


    def _SinglePlacementOverLibrary_scream_EE(self, mutAA, mutPstn, mutChn, rotamerLibrary, CLASH_THRESHOLD = 0, top_n = 1):
         '''
         This function takes in the position to be mutated/replaced and places all rotamers provided in the rotamerLibrary on the protein and evaluates the energy using scream_EE.
         These energies are then stored in the rotamerLibrary.
         If mutAA is 'Z' and mutChn is 'Z' conformer placement is done.
         '''
         print "Residue replacement info: " , mutAA, mutPstn, mutChn
         
         # place side chain, remaps everything, then calc energy, then store it.
         mutInfo = mutAA + str(mutPstn) + '_' + mutChn
         mI = MutInfo()
         mI.init(mutInfo)
         rotamerLibrary.reset_pstn()
         currentRotamer = rotamerLibrary.get_next_rot()
         n_Passed_Clash_Check = 0
         Passed_Clash_Check = 0
         print 'CLASH_THRESHOLD in SinglePlacementOverLibrary is ', CLASH_THRESHOLD
         while currentRotamer != None:
             if mutAA == 'Z' and mutChn == 'Z':             # if it's a conformer
                 rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                 self.placeConformer(currentRotamer, rotConnInfo)
                 if self._conformerClashAboveThreshold(CLASH_THRESHOLD, rotConnInfo):
                     Passed_Clash_Check = 1
             else:                                          # if it's a ntrlRotamer
                 self.placeSideChain(mutChn, mutPstn, currentRotamer)
                 if self._sideChainsAboveClashThreshold(CLASH_THRESHOLD, mutChn, mutPstn):
                     Passed_Clash_Check = 1
                     
             if Passed_Clash_Check:
                 n_Passed_Clash_Check = n_Passed_Clash_Check +1
                 rot_E = self.scream_EE.calc_empty_lattice_E(mI)
                 #rotlib_E = currentRotamer.get_rotlib_E()
                 rotlib_E = 0
                 currentRotamer.set_empty_lattice_E_abs(rot_E + rotlib_E)
                 print 'Rotamer ' + `currentRotamer.get_rotamer_n()` + " energy: " + str(currentRotamer.get_empty_lattice_E_abs())
             else:
                 print 'This rotamer has a clash of below', CLASH_THRESHOLD
                 print ''
                 currentRotamer.set_sc_total_E(999999999)
                 currentRotamer.set_empty_lattice_E_abs(999999999)
                 currentRotamer.setFailedDistanceCutoff()
             currentRotamer = rotamerLibrary.get_next_rot()
             Passed_Clash_Check = 0
         else:
             rotamerLibrary.reset_pstn()
             pass


         if n_Passed_Clash_Check == 0:
             print 'None of the rotamers in this library passed steric clash check!  Try relaxing your steric clash threshold, or check rotamer library.  Quiting.'
             import sys
             sys.exit()
             
         # sort rotamer library.
         print 'Sorting library... done'
         rotamerLibrary.sort_by_empty_lattice_E()
         currentRotamer = rotamerLibrary.get_next_rot()
         i = 1
         while currentRotamer != None:
             print 'Rotamer', i, 'energy:', currentRotamer.get_empty_lattice_E()
             i = i+1
             currentRotamer = rotamerLibrary.get_next_rot()
         else:
             pass
        

    def EnergyExcitationPlacement(self, replacementList):
        print 'EnergyExcitationPlacement currently under work!'
        # Plan:
        # Step 1: instantiate as many Rotlib as is necessary.  Make a distionary between replacementList members and these Rotlibs.
        
        KeepOriginalRotamer = self.scream_parameters.KeepOriginalRotamer  # THis gives 1 or 0.
        
        self.printToFile("tempTest.bgf")
        
        Mutation_Library_Dict = self._populateNtrlLibraryDict(replacementList)
        Original_Rotamer_Dict = self._populateNtrlOriginalRotamerDict(replacementList)
        # if running real job, appendOriginalRotamersToRotlibs. 
        if KeepOriginalRotamer:
            self._appendOriginalRotamersToRotlibs(Mutation_Library_Dict, Original_Rotamer_Dict)

        # init rotlibCollection
        rotlibCollection = RotlibCollectionPy()
        rotlibCollection.setHighestAllowedRotamerE(self.scream_parameters.StericClashCutoffEnergy)
        for mutInfo in replacementList:
            library = Mutation_Library_Dict[mutInfo]
            rotlibCollection.addRotlib(mutInfo, library)


        print "Mutation_library_dict:" 
        print Mutation_Library_Dict.keys()
        print Mutation_Library_Dict.values()

        print "Original_Rotamer_Dict:"
        print Original_Rotamer_Dict.keys()
        print Original_Rotamer_Dict.values()
        
        # Step 2a: make all sidechains involved in placement invisible.

        # check energy
        print "Before making visible and invisible, energy profile: " 
        self._calcEnergyAndPrint()
        self._makeTheseResiduesInvisible(replacementList)
                
        # Step 2b: Getting Empty Lattice Energyies.  Go through all sidechains invovled one after another, make Visible, and call ModSim to get energies for each rotamer.  Order rotamer energies in Rotlib.
        for mutInfo in replacementList:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            self.makeResidueVisible(mutChn, mutPstn)
            library = Mutation_Library_Dict[mutInfo]
            self._SingleEmptyLatticePlacementOverLibrary(mutAA, mutPstn, mutChn, library, CLASH_THRESHOLD=1.5, top_n=1)
            self.makeResidueInvisible(mutChn, mutPstn)

        self.restoreVisibility()
        # Step 3: now we have zeroth order excitation for all sidechains.  This is our ZEROTH order structure.  Calculate the energy of this structure.  Is this a lot worse than linear addition of the individual rotamers?


        # below: a mere test to see if restore visibility if working.
        self.placeMultipleSideChains(Original_Rotamer_Dict)
        
        #self.restoreVisibility()
        print "After making them visible and invisible, energy profile: "
        self._calcEnergyAndPrint()

        # Zeroth excitation structures output:
        for mutInfo in replacementList:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            library = Mutation_Library_Dict[mutInfo]
            library.reset_pstn()
            zerothRotamer = library.get_next_rot()
            library.reset_pstn()
            self.placeSideChain(mutChn, mutPstn, zerothRotamer)

        filename = 'ZerothExcitation.bgf'
        self.printToFile(filename)
        
        filename = 'originalAligned.bgf'
        self.placeMultipleSideChains(Original_Rotamer_Dict)
        self.printToFile(filename)

        # Step 4: Armed with knowledge of Empty Lattice Energies, now we can start excitating the rotamers!
        # a) initialize RotlibCollection

        # // old memory intensive way
        #rotlibCollection.initEmptyLatticeDataStructures()

        #rotlibCollection.printEmptyLatticeTable()
        #rotlibCollection.printEmptyLatticeLinearEnergyTable()

        # // new memory not so intensive method.
        rotlibCollection.initDynamicMemoryDataStructures()

        # b) keep getting next excited state until a certain point
        # this algorithm: does not re-calc reference states.  just uses empty lattice energies.  perhaps recalc reference states might work better.

        # // old memory intensive
        #theseExcitedRotamers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()

        # // new memory safe
        theseExcitedRotamers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
        
        count_since_last_best = 0
        lowestE = 999999999
        sizeOfSystem = len(Mutation_Library_Dict)
        
        while len(theseExcitedRotamers) != 0:
            count_since_last_best = count_since_last_best + 1
            self.placeMultipleSideChains(theseExcitedRotamers)
            
            self._calcEnergyAndPrint()
            crntEnergy = self.model.thermo_properties.te
            print "ABOUT TO SET ENERGY: ", crntEnergy
            
            rotlibCollection.setEnergyForExcitedRotamers(theseExcitedRotamers, crntEnergy)
            
            if crntEnergy < lowestE:
                lowestE = crntEnergy
                count_since_last_best = 0

            if rotlibCollection._shouldKeepGoing(count_since_last_best):
                # old memory intensive
                #@theseExcitedRotamers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
                # new memory safe
                theseExcitedRotamers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
            else:
                break
        #print 'Now print rotlibCollection.printExcitationEnergyTable()'
        #rotlibCollection.printExcitationEnergyTable()

        
        # Step 4 addendum: Chances are, a few of the rotamers will clash badly with each other.  Check forces on these atoms.  If forces are too high for a few atoms, we know which sidechains to "excite".  i) First excite the sidechain that possesses the atom with the highest force (perhaps do a minimization before this step).  Recalculate, repeat step i), until forces on atoms good enough.
        # Step 5.  Minimize, output structure.
        # for now, just output structure
        self._printBestStructures(rotlibCollection)
        self._printEnergyEvolution(rotlibCollection)

    def EmptyLatticeExcitationWithArbLib(self):
        '''
        More general than the previous generation of EnergyExcitation.  Albeit uses object member.
        '''
        
        #print 'Doing EnergyExcitation with User Provided Rotamer libraries.'
        '''
        self.Libraries_Dict = {}                    # Dict { mutInfo : Rotlib* }
        self.Original_Conformers_Dict = {}          # Dict { mutInfo : Rotamer* }
        self.Conformer_RotConnInfo_Dict = {}          # Dict { mutInfo : rotConnInfo* } for Conformers.
        '''
        # 1. init rotlibCollection
        rotlibCollection = RotlibCollectionPy()
        rotlibCollection.setHighestAllowedRotamerE(self.scream_parameters.StericClashCutoffEnergy)
        for mutInfo in self.Libraries_Dict.keys():
            library = self.Libraries_Dict[mutInfo]
            rotlibCollection.addRotlib(mutInfo, library)
        # 2. Make all Sidechains invovled in placement invisible.
        self._makeResiduesAndConformersInvisible(self.Libraries_Dict.keys(), self.Conformer_RotConnInfo_Dict)

        # 3. Getting Empty Lattice energies.
        clash_threshold = self.scream_parameters.StericClashCutoffDist
        print "CLASH_THRESHOLD is" , clash_threshold
        
        for mutInfo in self.Libraries_Dict.keys():
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            library = self.Libraries_Dict[mutInfo]
            # First make them visible.
            if mutAA == 'Z' and mutChn == 'Z':
                rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                self.makeConformerVisible(rotConnInfo)
            else:
                self.makeResidueVisible(mutChn, mutPstn)
            
            self._SingleEmptyLatticePlacementOverLibrary(mutAA, mutPstn, mutChn, library, clash_threshold, 1)  # Works for both rotamer and conformer
            # Turn them back to invisible after the fact.
            if mutAA == 'Z' and mutChn == 'Z':
                rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                self.makeConformerInvisible(rotConnInfo)
            else:
                self.makeResidueInvisible(mutChn, mutPstn)
            
        self.restoreVisibility()

        # Here: need to test if visibility is working.  

        originalAligned_filename = 'originalAligned.bgf'
        self.placeMultipleConformers(self.Original_Conformers_Dict, self.Conformer_RotConnInfo_Dict)
        self.printToFile(originalAligned_filename)

        # 4. Excitation algorithm.
        #rotlibCollection.initEmptyLatticeDataStructures()
        rotlibCollection.initDynamicMemoryDataStructures()

        #theseExcitedConformers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
        theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()

        count_since_last_best = 0
        lowestE = 999999999
        sizeOfSystem = len(self.Libraries_Dict)

        while len(theseExcitedConformers) != 0:
            count_since_last_best = count_since_last_best +1
            self.placeMultipleConformers(theseExcitedConformers, self.Conformer_RotConnInfo_Dict)
            self._calcEnergyAndPrint()

            crntEnergy = self.model.thermo_properties.te
            rotlibCollection.setEnergyForExcitedRotamers(theseExcitedConformers, crntEnergy)

            if crntEnergy < lowestE:
                lowestE = crntEnergy
                count_since_last_best = 0

            if rotlibCollection._shouldKeepGoing(count_since_last_best):
                #theseExcitedConformers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
                theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
            else:
                break
        
        # 5. Output.

        self._printBestStructures(rotlibCollection)
        self._printEnergyEvolution(rotlibCollection)


    def GroundStateExcitationWithArbLib(self):
    #def EmptyLatticeExcitationWithArbLib(self):
        '''
        Gets ground state energies from empty lattice excitations, then does 1st order excitation, and use those orders to do configuration excitation scheme.
        '''

        # Need to do similar things as in EnergyExcitationWithArbLib

        # 1. init rotlibCollection
        rotlibCollection = RotlibCollectionPy()
        rotlibCollection.setHighestAllowedRotamerE(self.scream_parameters.StericClashCutoffEnergy)
        for mutInfo in self.Libraries_Dict.keys():
            library = self.Libraries_Dict[mutInfo]
            rotlibCollection.addRotlib(mutInfo, library)
            
        # 2. Make all Sidechains invovled in placement invisible--for empty lattice calculations.
        self._makeResiduesAndConformersInvisible(self.Libraries_Dict.keys(), self.Conformer_RotConnInfo_Dict)

        # 3. Getting Empty Lattice energies.
        clash_threshold = self.scream_parameters.StericClashCutoffDist
        print "CLASH_THRESHOLD is" , clash_threshold
        
        for mutInfo in self.Libraries_Dict.keys():
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            library = self.Libraries_Dict[mutInfo]
            # First make them visible.
            if mutAA == 'Z' and mutChn == 'Z':
                rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                self.makeConformerVisible(rotConnInfo)
            else:
                self.makeResidueVisible(mutChn, mutPstn)
            
            self._SingleEmptyLatticePlacementOverLibrary(mutAA, mutPstn, mutChn, library, clash_threshold, 1)  # Works for both rotamer and conformer
            # Turn them back to invisible after the fact.
            if mutAA == 'Z' and mutChn == 'Z':
                rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
                self.makeConformerInvisible(rotConnInfo)
            else:
                self.makeResidueInvisible(mutChn, mutPstn)
            
        self.restoreVisibility()

        # Here: need to test if visibility is working.  

        originalAligned_filename = 'originalAligned.bgf'
        self.placeMultipleConformers(self.Original_Conformers_Dict, self.Conformer_RotConnInfo_Dict)
        self.printToFile(originalAligned_filename)

        # 4. Now use these orderings, use ground state excitation.
        # 4.1 Place ground state configurations on original protein.
        groundStateConformers = {}
        for mutInfo in self.Libraries_Dict.keys():
            rotLib = self.Libraries_Dict[mutInfo]
            rotLib.sort_by_empty_lattice_E()
            rotLib.reset_pstn()
            groundStateConformers[mutInfo] = rotLib.get_next_rot()
            rotLib.reset_pstn()
        self.placeMultipleConformers(groundStateConformers, self.Conformer_RotConnInfo_Dict) # CHECK THESE STRUCTURES!!! 12/28/04
        # 4.2 Now use this new structure to do ground state excitation, and repopulate values for empty_lattice_E.
        # No need to make the sidechains invisible.
        print 'Now doing GROUND STATE EXCITATION (i.e. first iteration after empty lattice calculations)'
        for mutInfo in self.Libraries_Dict.keys():
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            library = self.Libraries_Dict[mutInfo]
            self._SingleEmptyLatticePlacementOverLibrary(mutAA, mutPstn, mutChn, library, clash_threshold, 1)  # Works for both rotamer and conformer
            # now restore
            self.placeMultipleConformers(groundStateConformers, self.Conformer_RotConnInfo_Dict)
        # 5. now place sidechains using these energies instead--same excitation algorithm.
        rotlibCollection.initDynamicMemoryDataStructures()
        theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
        count_since_last_best = 0
        lowestE = 999999999
        sizeOfSystem = len(self.Libraries_Dict)
        
        while len(theseExcitedConformers) != 0:
            count_since_last_best = count_since_last_best +1
            self.placeMultipleConformers(theseExcitedConformers, self.Conformer_RotConnInfo_Dict)
            self._calcEnergyAndPrint()
            
            crntEnergy = self.model.thermo_properties.te
            rotlibCollection.setEnergyForExcitedRotamers(theseExcitedConformers, crntEnergy)
            
            if crntEnergy < lowestE:
                lowestE = crntEnergy
                count_since_last_best = 0
                
            if rotlibCollection._shouldKeepGoing(count_since_last_best):
                #theseExcitedConformers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
                theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
            else:
                break
        
        # 5. Output.

        self._printBestStructures(rotlibCollection)
        self._printEnergyEvolution(rotlibCollection)

    def EmptyLatticeExcitationWithArbLib_scream_EE(self):
        '''
        Gets ground state energies from empty lattice excitations, use those orders to do configuration excitation scheme, using Scream EE.
        '''
        
        # 1. init rotlibCollection
        rotlibCollection = RotlibCollectionPy()
        rotlibCollection.setHighestAllowedRotamerE(self.scream_parameters.StericClashCutoffEnergy)
        for mutInfo in self.Libraries_Dict.keys():
            library = self.Libraries_Dict[mutInfo]
            rotlibCollection.addRotlib(mutInfo, library)
            
        # 2. Make all Sidechains invovled in placement invisible--for empty lattice calculations.
        self._makeResiduesAndConformersInvisible(self.Libraries_Dict.keys(), self.Conformer_RotConnInfo_Dict)

        # 3. Getting Empty Lattice energies.
        clash_threshold = self.scream_parameters.StericClashCutoffDist
        print "CLASH_THRESHOLD is" , clash_threshold
        
        for mutInfo in self.Libraries_Dict.keys():
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            library = self.Libraries_Dict[mutInfo]
            # making them invisible unnecessary as Scream_EE is set up that way.
            self._SinglePlacementOverLibrary_scream_EE(mutAA, mutPstn, mutChn, library, clash_threshold, 1)  # Works for both rotamer and conformer

        originalAligned_filename = 'originalAligned.bgf'
        self.placeMultipleConformers(self.Original_Conformers_Dict, self.Conformer_RotConnInfo_Dict)
        self.printToFile(originalAligned_filename)

        # 4. excitation algorithm.
        rotlibCollection.initDynamicMemoryDataStructures()
        theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
        count_since_last_best = 0
        lowestE = 999999999
        sizeOfSystem = len(self.Libraries_Dict)
        
        while len(theseExcitedConformers) != 0:
            count_since_last_best = count_since_last_best +1
            self.placeMultipleConformers(theseExcitedConformers, self.Conformer_RotConnInfo_Dict)
            all_interactions_E = self.scream_EE.calc_all_interaction_E()
            #self._calcEnergyAndPrint()
            
            crntEnergy = all_interactions_E
            # Need to add these interaction energies to: side-chain-backbone interaction and side-chain valence E.
            for mutInfo in theseExcitedConformers.keys():
                crntConformer = theseExcitedConformers[mutInfo]
                crntEnergy += crntConformer.get_sc_total_E()
                
            rotlibCollection.setEnergyForExcitedRotamers(theseExcitedConformers, crntEnergy)
            
            if crntEnergy < lowestE:
                lowestE = crntEnergy
                count_since_last_best = 0
                
            if rotlibCollection._shouldKeepGoing(count_since_last_best):
                #theseExcitedConformers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
                theseExcitedConformers = rotlibCollection.getNextDynamicMemoryRotamers_And_ExpandPy()
            else:
                break
        
        # 5. Output.

        self._printBestStructures(rotlibCollection)
        self._printEnergyEvolution(rotlibCollection)


        
    def placeMultipleSideChains(self, rotamerDict):
        for key in rotamerDict.keys():
            mutInfo = str(key)
            print mutInfo, ' in placeMultipleSideChains'
            aaRotamer = rotamerDict[mutInfo]
            #aaRotamer = derefAARotamer(rotamerDict[mutInfo]) # need to use derefAARotamer because SWIG doesn't do a good job of swigging Rotamer*.  Rotamer* becomes a _p_p_ 
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            self.placeSideChain(mutChn, mutPstn, aaRotamer)
            print "placeMultipleSideChains successful!"
        pass

    def placeMultipleConformers(self, conformersDict, conformerRotConnInfoDict = None):
        '''
        More general than placeMultipleSideChains.  Should replace all instances of placeMultipleSideChains.
        '''
        for mutInfo in conformersDict.keys():
            conformer = conformersDict[mutInfo]
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            if mutAA == 'Z' and mutChn == 'Z': # should not enter this conditional if conformersDict contains only rotamers.
                rotConnInfo = conformerRotConnInfoDict[mutInfo]
                self.placeConformer(conformer, rotConnInfo)
            else:
                self.placeSideChain(mutChn, mutPstn, conformer)
            #print 'Done placing mutliple conformers.'
        pass
    
    def SinglePlacementWithMinimization(self):
        self._SinglePlacementWithMinimization(mutResInfo)
    
    
    def _unpackMutInfo(self, mutInfo):
        """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""
        mutAA = mutInfo[0]
        (mutPstn, mutChn) = mutInfo[1:].split('_')
        mutPstn = int(mutPstn)
        return (mutAA, mutPstn, mutChn)
    
    def _calcEnergyAndPrint(self):
        self.model.compute_tot_forces()
        self.model.compute_thermo()
        print_energy(self.model.thermo_properties)
    
    def _populateNtrlLibraryDict(self, replacementList):
        Mutation_Library_Dict = {}
        for mutInfo in replacementList:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            library_path_first_half = self.scream_parameters.determineLibDirPath()

            library_file_suffix = self.scream_parameters.determineLibDirFileNameSuffix()
            #'_10.lib'
            
            library_file = library_path_first_half + '/' + mutAA + '/' + mutAA + library_file_suffix
            library = NtrlAARotlib(library_file)
            print 'Done loading ' + library_file + '.'
            Mutation_Library_Dict[mutInfo] = library
            
        return Mutation_Library_Dict

    def _populateNtrlOriginalRotamerDict(self, replacementList):
        Original_Rotamer_Dict = {}
        for mutInfo in replacementList:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            originalRotamer = AARotamer()
            print mutAA
            print mutPstn
            print mutChn
            originalRotamer.deepcopy(self.getAARotamer(mutChn, mutPstn))
            originalRotamer.is_Original = 1
            Original_Rotamer_Dict[mutInfo] = originalRotamer
        return Original_Rotamer_Dict

    def _populateAddLibraryDict(self, additional_list):
        '''
        Passes a list of filenames as Arbitrary rotamer libraries.
        Returns a (Additional_Rotamer_Library_Dict, mutInfo_RotConnInfo_Dict) tuple.
        Additional_Rotamer_Library_Dict has the form: {('Z1_Z' : Arb_Rotlib)}.
        mutInfo_RotConnInfo_Dict has the form: {('Z1_Z' : RotConnInfo*)}.
        '''
        Add_Rotamer_Lib_Dict = {}
        mutInfo_connInfo_map = {}
        c = 1
        for lib in additional_list:
            library_file = lib
            library = Rotlib(library_file)
            print 'Done loading ' + library_file + '.'
            mutInfo = 'Z' + str(c) + '_Z'
            Add_Rotamer_Lib_Dict[mutInfo] = library
            mutInfo_connInfo_map[mutInfo] = library.getRotConnInfo()
            c = c + 1
        return (Add_Rotamer_Lib_Dict, mutInfo_connInfo_map);

    
    def _populateAddOriginalRotamerDict(self, mutInfo_connInfo_map):
        '''
        Pass a (MutInfo : RotConnInfo) dictionary in and returns a (MutInfo : OriginalRotamer) dictionary.
        MutInfo, here, will have distinctive names of Z1_Z, Z2_Z since these are not ntrl AA Rotamers, thus no one name symbols are used.
        '''
        Original_Conformer_Dict = {}
        for mutInfo in mutInfo_connInfo_map.keys():
            connInfo = mutInfo_connInfo_map[mutInfo]
            ptn = self.getProtein()
            originalConformer = ptn.conformerExtraction(connInfo)
            Original_Conformer_Dict[mutInfo] = originalConformer
        return Original_Conformer_Dict

    def _makeTheseResiduesInvisible(self, replacementList):
        for mutInfo in replacementList:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            self.makeResidueInvisible(mutChn, mutPstn)
            # self._calcEnergyAndPrint()

    def _makeResiduesAndConformersInvisible(self, mutInfo_list, conformer_mutInfo_rotConnInfo_dict):
        for mutInfo in mutInfo_list:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(mutInfo)
            if mutAA == 'Z' and mutChn == 'Z':
                rotConnInfo = conformer_mutInfo_rotConnInfo_dict[mutInfo]
                self.makeConformerInvisible(rotConnInfo)
            else:
                self.makeResidueInvisible(mutChn, mutPstn)

    def _appendOriginalRotamersToRotlibs(self, Mutation_Library_Dict, Original_Rotamer_Dict):
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

    def _appendOriginalConformersToRotlibs(self, Conformer_Library_Dict, Original_Conformer_Dict):
        # Actually identical code to _appendOriginalRotamersToRotlibs
        self._appendOriginalRotamersToRotlibs(Conformer_Library_Dict, Original_Conformer_Dict)

    def _printBestStructures(self, rotlibCollection):
        """Prints best structures give a rotlibCollection, with the total number specfied by the Selections parameter in SCREAM param file."""
        print "Printing Best Structures!"
        count = 0
        filename_prefix = 'best_'
        rotlibCollection.resetTotalEnergyCrntPstn()
        theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()
        
        print 'starting print bgf files loop'
        while len(theseExcitedRotamers) != 0:
            count = count+1
            filename = filename_prefix + `count` + '.bgf'
            if count > self.scream_parameters.Selections:
                break
            #self.placeMultipleSideChains(theseExcitedRotamers)
            self.placeMultipleConformers(theseExcitedRotamers, self.Conformer_RotConnInfo_Dict)
            excitedRotamerInfo = rotlibCollection.emptyLatticeRankInfo(theseExcitedRotamers)
            self.printToFile(filename, excitedRotamerInfo)
            theseExcitedRotamers = rotlibCollection.getNextTotalEnergyExcitationRotamersPy()

    def _printEnergyEvolution(self, rotlibCollection):
        """Prints the estimated and actual energy evolution.  Sorted by estimated energy."""
        Evolution_File = open('Evolution.dat', 'w')
        #rotlibCollection.resetTotalEnergyCrntPstn()
        rotlibCollection.resetEmptyLatticeCrntPstn()
        theseExcitedRotamers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()

        c = 1
        print >>Evolution_File, 'Index    Estimated     Actual'
        while len(theseExcitedRotamers) != 0:
            rankInfo = rotlibCollection.emptyLatticeRankInfo(theseExcitedRotamers)
            estimated_E = rotlibCollection.getEstimatedEnergyForExcitedRotamers(theseExcitedRotamers)
            actual_E = rotlibCollection.getEnergyForExcitedRotamers(theseExcitedRotamers)

            if estimated_E >= 99999999:
                break
            
            print >>Evolution_File, str(c) + ' ' + str(estimated_E) + ' ' + str(actual_E)
            theseExcitedRotamers = rotlibCollection.getNextEmptyLatticeExcitationRotamersPy()
            c += 1
            
        Evolution_File.close()

    
    def _sideChainsAboveClashThreshold(self, CLASH_THRESHOLD, mutChn, mutPstn):
        clash = self.sc_clash(mutChn, mutPstn)
        print "clash for this rotamer is", clash
        if clash < CLASH_THRESHOLD:
            return false
        else:
            return true

    def _conformerClashAboveThreshold(self, clash_threshold, rotConnInfo):
        clash = self.conformer_clash(rotConnInfo)
        print "clash for this conformer is", clash
        if clash < clash_threshold:
            return false
        else:
            return true
    
    def _init_scream_EE(self, ptn, ff_file):
        '''
        uses these information:
        self.Original_Conformer_Dict     # Dict {mutInfo : Rotamer* }
        self.Conformer_RotConnInfo_Dict  # Dict {mutInfo : rotConnInfo* }
        '''
        self.scream_EE = Scream_EE()

        for mutInfo in self.Original_Conformers_Dict.keys():
            mI = MutInfo()
            mI.init(mutInfo)
            self.scream_EE.addMutInfoRotConnInfo(mI)
            
        for mutInfo in self.Conformer_RotConnInfo_Dict.keys():
            mI = MutInfo()
            mI.init(mutInfo)
            rotConnInfo = self.Conformer_RotConnInfo_Dict[mutInfo]
            self.scream_EE.addMutInfoRotConnInfo(mI, rotConnInfo)
            
        self.scream_EE.init_after_addedMutInfoRotConnInfo(ptn, ff_file)

        
    def minimize(self, steps):
        '''
        Calls the minimize(model) function in the minimize.py module.
        Minimizes model for n steps.
        '''
        self.model.parameters.min_method = 'c'
        self.model.parameters.min_limit = steps
        self.model.parameters.min_error = 0.00001 # set this to something small so always does this number of steps
        #minimize.minimize(self.model)  # commented out
    
    def _makeAllButTheseResiduesMoveable(self, *mutInfoList):
        # First make all atoms immoveable.
        self.makeAllImmoveable()
        # Then make those residues moveable.
        for entry in mutInfoList:
            (mutAA, mutPstn, mutChn) = self._unpackMutInfo(entry)
            self.makeResidueMoveable(mutChn, mutPstn)
    

    def minimizeJustTheseResidues(self, steps, *mutInfoList):
        self._makeAllButTheseResiduesMoveable(*mutInfoList)
        self.minimize(steps)
        print_energy(self.model.thermo_properties)
        
    
# RotlibCollectionPy class, derived from RotlibCollection, added convenience functions.

class RotlibCollectionPy(RotlibCollection):
    "RotlibCollection clas.  Convenience class derived from C++ RotlibCollection to make data transfer easier and cleaner."
    def __init__(self):
        RotlibCollection.__init__(self)
    
    def _shouldKeepGoing(self, count_since_last_best):
        """Primitive decision whether or not to keep going."""
        sizeOfSystem = self.sizeOfSystem()
        testBlockSize = 1.8**(sizeOfSystem+1)
        if testBlockSize < 20:
            testBlockSize = 20
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
    
    def getNextEmptyLatticeExcitationRotamersPy(self ):
        """Returns a dictionary of Python useable {string, AARotamer*} pairs instead of the C++ returned {_p_string, _p_p_AARotamer} format."""
        excitedRotamersRightFormat = dict()
        excitedRotamersWrongFormat = self.getNextEmptyLatticeExcitationRotamers()
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            rightString = derefString(wrongFormatString)
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            rightRotamer = derefRotamer(wrongFormatRotamer)
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat

    def getNextDynamicMemoryRotamers_And_ExpandPy(self):
        '''Returns a distionary of Python useable {string, Rotamer*} pairs instead of the C++ returned types {_p_string, _p_pAARotamer} or _p_pRotamer format.'''
        excitedRotamersRightFormat = dict()
        excitedRotamersWrongFormat = self.getNextDynamicMemoryRotamers_And_Expand()
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            rightString = derefString(wrongFormatString)
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            rightRotamer = derefRotamer(wrongFormatRotamer)
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat



    def getNextTotalEnergyExcitationRotamersPy(self):
        """Returns a dictionary of Python useable {string, AARotamer*} pairs instead of the C++ returned {_p_string, _p_p_AARotamer} format from Total Energy dict."""
        excitedRotamersRightFormat = {}
        excitedRotamersWrongFormat = self.getNextTotalEnergyExcitationRotamers()
        for wrongFormatString in excitedRotamersWrongFormat.keys():
            rightString = derefString(wrongFormatString)
            wrongFormatRotamer = excitedRotamersWrongFormat[wrongFormatString]
            rightRotamer = derefRotamer(wrongFormatRotamer)
            excitedRotamersRightFormat[rightString] = rightRotamer
        return excitedRotamersRightFormat

    
    def setEnergyForExcitedRotamers(self, excitedRotamers, energy):
        """Takes a ExcitedRotamer structure ( dict{mutInfo, AARotamer*} ) and stores its energy in RotlibCollection."""
        EE = {}
        for mutInfo in excitedRotamers.keys():
            rotamer = excitedRotamers[mutInfo]
            EmptyLatticeRank = rotamer.get_empty_lattice_energy_rank()
            EE[mutInfo] = EmptyLatticeRank
        self.setExcitationEnergy(EE, energy)
        
    def getEnergyForExcitedRotamers(self, excitedRotamers):
        EE = {}
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


def unpackModel(model):
    #    modsim_struct = ModSimStructs(p, ff, a, ucp, cl, nl, nhl, tp)
    modsim_struct = ModSimStructs(model.parameters, model.ff_properties, model.atom_properties, model.unit_cell_properties, None, None, None, model.thermo_properties)
    return modsim_struct

