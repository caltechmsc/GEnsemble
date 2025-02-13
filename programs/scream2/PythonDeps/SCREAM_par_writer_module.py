#!/usr/bin/python

# Authorship: Victor Kam.
# Summary: This file contains module for writing a SCREAM par file.
# Feel free to modify this.


import BgfTools, PyResidue, re, sys, os


####################################################
# Section 1.  The main Create Parfile function. ####
####################################################

def write_CreateCB_playWithBGF_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, delta, playWithBgfMutInfo_line):
    (delta_method, final_delta_value) = ('FULL', float(delta))
    ff_file = get_ff_file()

    pwb_mI_line = run_and_grep_PlayWithBGF(bgf_file, playWithBgfMutInfo_line)
    mutInfo_string = return_processedPlayWithBGFLine_and_filter(pwb_mI_line, bgf_file)
    #print playWithBgfMutInfo_line
    #print pwb_mI_line
    #print mutInfo_string
    
    rotlib_specs_string = returnRotSpecString(rotlib_specs)
    
    write_CreateCB_parfile(scream_par_filename, bgf_file, delta_method, final_delta_value, ff_file, mutInfo_string, rotlib_specs_string)

def write_CreateCB_no_AGP_CYX_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, delta, LJ='12-6'):
    (delta_method, final_delta_value) = ('FULL', float(delta))
    ff_file = get_ff_file()
    
    mutInfo_string = returnAll_no_AGP_CYX(bgf_file)
    rotlib_specs_string = returnRotSpecString(rotlib_specs)
    
    write_CreateCB_parfile(scream_par_filename, bgf_file, delta_method, final_delta_value, ff_file, mutInfo_string, rotlib_specs_string, LJ)

def write_CreateCB_no_AGP_CYX_terminals_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, delta, LJ='12-6'):
    (delta_method, final_delta_value) = ('FULL', float(delta))

    ff_file = get_ff_file()

    mutInfo_string = returnAll_no_AGP_CYX_terminals(bgf_file)
    rotlib_specs_string = returnRotSpecString(rotlib_specs)
    
    write_CreateCB_parfile(scream_par_filename, bgf_file, delta_method, final_delta_value, ff_file, mutInfo_string, rotlib_specs_string, LJ)


def write_CreateCB_parfile(scream_par_filename, bgf_file, delta_method, final_delta_value, ff_file, mutInfo_string, rotlib_specs_string, LJ='12-6'):
    scream_delta_file = get_SCREAM_delta_file()
    eachAtomDelta_file = get_EachAtomDeltaFile()
    polarExclusion_file = get_PolarOptimizationExclusions()
    
    
    extra_lib_string = ''
    SCREAM_PAR_FILE = open(scream_par_filename, 'w')
    
    print >>SCREAM_PAR_FILE, '%25s %s' % ('InputFileName', bgf_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MutateResidueInfo', mutInfo_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('AdditionalLibraryInfo', extra_lib_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Library', rotlib_specs_string)

    print >>SCREAM_PAR_FILE, '%25s %s' % ('PlacementMethod', 'CreateCB')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('CreateCBParameters', '1.81 51.1 1.55 0.5')

    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseScreamEnergyFunction', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaMethod', delta_method)
    
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaForInterResiE', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseAsymmetricDelta', 'YES')

    print >>SCREAM_PAR_FILE, '%25s %s' % ('EachAtomDeltaFile', eachAtomDelta_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('PolarOptimizationExclusions', polarExclusion_file)

    print >>SCREAM_PAR_FILE, '%25s %s' % ('LJOption', LJ)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('CoulombMode', 'Normal')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Dielectric', '2.5')
    

    print >>SCREAM_PAR_FILE, '%25s %f' % ('FlatDeltaValue', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('DeltaStandardDevs', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('InnerWallScalingFactor', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MultiplePlacementMethod', 'ClusteringThenDoubletsThenSinglets')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('KeepOriginalRotamer', 'NO')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('OneEnergyFFParFile', ff_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('DeltaParFile', scream_delta_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Selections', 1)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffEnergy', '250')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffDist', '0.5')
    SCREAM_PAR_FILE.close()

###############################################################################################################
# Section 2.  Functions that return a string that contains all the residues to be included in the calculation.#
##############################################################################################################


def returnAll_no_AGP_CYX(bgf_file):
    '''Returns a SCREAM string like S123_A T234_A, excluding AGP and CYX.'''
    al = BgfTools.make_PyAtom_list_from_bgf_file(bgf_file)
    rl = PyResidue.make_PyResidue_list(al)

    s = ''
    (currentChain, currentPstn, lastChain, lastPstn) = ('', '', '' , '')
    added_flag = 0

    for r in rl:
        if not r.res_name in ['CYX', 'ALA', 'GLY', 'PRO']:
            s += '%s ' % r.return_SCREAM_string()

    return s
    

def returnAll_no_AGP_CYX_terminals(bgf_file):
    '''Returns a SCREAM string like S123_A T234_A, that includes all non-AGP, CYX residues, but not terminal residues.'''
    al = BgfTools.make_PyAtom_list_from_bgf_file(bgf_file)
    rl = PyResidue.make_PyResidue_list(al)

    s = ''
    (currentChain, currentPstn, lastChain, lastPstn) = ('', '', '' , '')
    added_flag = 0

    for r in rl:
        (lastChain, lastPstn) = (currentChain, currentPstn)
        (currentChain, currentPstn) = (r.chain_name, r.res_pstn)

        if currentChain != lastChain and added_flag == 1:
            # Remove residue at the end of last chain, if it was added.
            s = s.rstrip()
            s = s[0:s.rfind(' ') ]
            if s != '':
                s += ' '
        if not r.res_name in ['CYX', 'ALA', 'GLY', 'PRO']:
            if currentChain != lastChain: # don't add beginning of chain
                added_flag = 0 
                continue
            else:
                s += '%s ' % r.return_SCREAM_string()
                added_flag = 1
        else:
            added_flag = 0

    # now remove very last one
    if added_flag == 1:
        s = s.rstrip()
        s = s[0:s.rfind(' ')]
    return s

def return_processedPlayWithBGFLine_and_filter(playWithBGF_line, bgf_file):
    'Uses output line from playWithBGF'
    # 2 lines from playWithBGF.  1: selection for scream 2:  entire residue list
    # Want: entire residue list. V1_A K2_A D3_A G4_A Y5_A I6_A V7_A D8_A D9_A V10_A N11_A T13_A Y14_A F15_A G17_A R18_A N19_A A20_A Y21_A N23_A E24_A E25_A T27_A K28_A L29_A K30_A G31_A E32_A S33_A G34_A Y35_A Q37_A W38_A A39_A S40_A P41_A Y42_A G43_A N44_A A45_A Y47_A Y49_A K50_A L51_A P52_A D53_A V55_A R56_A T57_A K58_A G59_A P60_A G61_A R62_A H64_A CYX12_A CYX16_A CYX22_A CYX26_A CYX36_A CYX46_A CYX48_A HSE54_A CYX63_A
    
    aL = BgfTools.make_PyAtom_list_from_bgf_file(bgf_file)
    rL = PyResidue.make_PyResidue_list(aL)

    num_chain_res_type_dict = {} # e.g.: {123_A : H}

    for r in rL:
        if r.is_canonical_amino_acid():
            SCREAM_mutInfo = r.return_SCREAM_string()
            num_chain = SCREAM_mutInfo[1:].strip()
            res_type = SCREAM_mutInfo[0].strip()
            num_chain_res_type_dict[num_chain] = res_type
        else:
            continue

    scream_line = _processPlayWithBgf_entireResidueList_line(playWithBGF_line)
    mI_fields = scream_line.split()
    new_l = ''
    for mI in mI_fields:
        new_mI = mI
        if mI[0] in ['.']: # keep original residue type.
            num_chain = mI[1:].strip()
            if num_chain_res_type_dict.has_key(num_chain):
                new_mI = num_chain_res_type_dict[num_chain] + num_chain
            else:
                print 'Warning: chain name and residue number cannot be found in bgf file!  Skipping over this residue.'
                continue
        if mI[0] in ['A', 'G', 'P', 'X']:
            print 'Skipping over Ala, Gly, Pro or Cyx residue.'
            continue
        new_l += new_mI
        new_l += ' '
    return new_l
    


###################################
# Section 3.  Helper functions.####
###################################


def unpackMutInfo(mutInfo):
    """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""
    mutAA = mutInfo[0]
    (mutPstn, mutChn) = mutInfo[1:].split('_')
    mutPstn = int(mutPstn)
    return (mutAA, mutPstn, mutChn)


def returnRotSpecString(rotlib_specs):
    rotlib_specs_string = ''
    if rotlib_specs == 'SCWRL':
        rotlib_specs_string = rotlib_specs
    else:
        rotlib_specs_string = 'V' + rotlib_specs
    return rotlib_specs_string
    

def run_and_grep_PlayWithBGF(bgf_file, playWithBGF_options_string):
    playWithBGF = '/project/Biogroup/scripts/playWithBGF/playWithBGF'
    os.system('%s %s %s > play.out' % (playWithBGF, bgf_file, playWithBGF_options_string) )
    INPUT = open('play.out', 'r')
    p = re.compile(' entire residue list')
    return_line = ''
    for l in INPUT.xreadlines():
        if p.search(l):
            return_line = l
            break
    if return_line == '':
        print 'No SCREAM style output detected in playWithBGF output!  Reminder: the string being grepped is \' entire residue list\'.'
        print 'Quitting.'
        sys.exit(2)
    return return_line

def _processPlayWithBgf_entireResidueList_line(l):
    # returns a mutInfo line, including '.' if they are present.
    #  entire residue list  : V1_A K2_A D3_A G4_A Y5_A I6_A V7_A D8_A D9_A V10_A N11_A T13_A Y14_A F15_A G17_A R18_A N19_A A20_A Y21_A N23_A E24_A E25_A T27_A K28_A L29_A K30_A G31_A E32_A S33_A G34_A Y35_A Q37_A W38_A A39_A S40_A P41_A Y42_A G43_A N44_A A45_A Y47_A Y49_A K50_A L51_A P52_A D53_A V55_A R56_A T57_A K58_A G59_A P60_A G61_A R62_A H64_A CYX12_A CYX16_A CYX22_A CYX26_A CYX36_A CYX46_A CYX48_A HSE54_A CYX63_A
    f = l.split()
    pwb_mI_list = f[4:]

    scream_mI_string = ''
    
    for pwb_mI in pwb_mI_list:
        scream_mI = _processPlayWithBgf_mutInfo(pwb_mI)
        if scream_mI != '':
            scream_mI_string += scream_mI
            scream_mI_string += ' '
    return scream_mI_string


def _processPlayWithBgf_mutInfo(pwb_mI):
    # Function: processes a playWithBgf mutInfo to a SCREAM mutInfo.
    # E.g.: CYX48_A, .23_B, A12_   '.' is "any", A12_ is one without a chain name.
    # 
    (res, pstn, chain) = ('', '', '')
    res_p = re.compile('^([.A-Za-z]+)')
    pstn_p = re.compile('([0-9]+)_')
    chain_p = re.compile('([A-Z])$')

    res_m = res_p.search(pwb_mI)
    pstn_m = pstn_p.search(pwb_mI)
    chain_m = chain_p.search(pwb_mI)
    
    if res_m:
        res = res_m.group(1)
        if len(res) != 1: # need to do mapping
            if PyResidue.AminoAcids_321_SCREAM.has_key(res):
                res = PyResidue.AminoAcids_321_SCREAM[res]
            else:
                print 'Residue specified in SCREAM style mutInfo from playWithBGF contains a non-canonical amino acid designation.  Ignoring this mutInfo: ', pwb_mI
                return ''
            
    else:
        print 'Irrecoverable error in SCREAM style mutInfo from playWithBGF!  No matching residue name found in: ', pwb_mI
        #sys.exit(2)
        
    if pstn_m:
        pstn = pstn_m.group(1)
    else:
        print 'Irrecoverable error in SCREAM style mutInfo from playWithBGF!  No matching residue pstn found in: ', pwb_mI
        #sys.exit(2)
        
    if chain_m:
        chain = chain_m.group(1)
    else:
        print 'No chain number specified in SCREAM style mutInfo from playWithBGF!  Ignoring this mutInfo: ', pwb_mI
        return ''

    mI = res + pstn + '_' + chain
    return mI

def get_ff_file():
    ff_file = os.environ.get('FORCE_FIELD_FILE')
    return ff_file

def get_SCREAM_delta_file():
    delta_ff_file_path = os.environ.get('SCREAM_DELTA_PAR_FILE_PATH')
    delta_file = delta_ff_file_path + 'SCREAM_delta_Total_Min.par'
    return delta_file

def get_EachAtomDeltaFile():
    delta_ff_file_path = os.environ.get('SCREAM_DELTA_PAR_FILE_PATH')
    delta_file = delta_ff_file_path + 'SCREAM_EachAtomDeltaFileStub.par'
    return delta_file

def get_PolarOptimizationExclusions():
    delta_ff_file_path = os.environ.get('SCREAM_DELTA_PAR_FILE_PATH')
    delta_file = delta_ff_file_path + 'SCREAM_PolarOptimizationExclusionsStub.par'
    return delta_file
