#!/usr/bin/python

import sys, os
#from Py_Scream_EE import *

def usage():
    print '''
Does This is a wrapper for running SCREAM BindingSite mode..
Usage: SCREAM_BindingSite_wrap.py <bgffile> <rotlib_specs> <chn_to_SCREAM_around> <radius>
E.g.:  SCREAM_BindingSite_wrap.py PheRS.bgf 10 X 3.5
Means: In bgf file PheRS.bgf, SCREAM all residues that are within 3.5 angstroms of chain X, while using a rotamer library of the 1.0 resolution.
'''
    sys.exit()

def main():

    if len(sys.argv) <= 3:
        usage()
        
    bgf_file = sys.argv[1]
    rotlib_specs = sys.argv[2]
    chn = sys.argv[3]
    radius = float(sys.argv[4])

    #ff_file = '/ul/victor/ForceFieldFiles/dreidii322-scream-EE.par'
    ff_file = '/ul/victor/ForceFieldFiles/PS330_mpsim.par'
    scream_delta_file = '/project/Biogroup/Software/SCREAM/lib/SCREAM_delta_par_files/SCREAM_delta.par'

    scream_par_filename = 'scream.par'
    SCREAM_PAR_FILE = open(scream_par_filename, 'w')

    extra_lib_string = ''

    rotlib_specs_string = ''
    if rotlib_specs == 'SCWRL':
        rotlib_specs_string = rotlib_specs
    else:
        rotlib_specs_string = 'V' + rotlib_specs
    
    print >>SCREAM_PAR_FILE, '%25s %s' % ('InputFileName', bgf_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MutateResidueInfo', 'BINDING_SITE')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('AdditionalLibraryInfo', extra_lib_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Library', rotlib_specs_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseScreamEnergyFunction', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaMethod', 'FLAT')

    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaForInterResiE', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseAsymmetricDelta', 'YES')
    print >>SCREAM_PAR_FILE, '%30s %f' % ('DistanceDielectricPrefactor', 2.5)
    
    print >>SCREAM_PAR_FILE, '%25s %f' % ('FlatDeltaValue', 0.35)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('DeltaStandardDevs', -0.8)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('InnerWallScalingFactor', 0.1)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MultiplePlacementMethod', 'ExcitationWithClustering')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('KeepOriginalRotamer', 'NO')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('OneEnergyFFParFile', ff_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('DeltaParFile', scream_delta_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Selections', 1)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffEnergy', '250')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffDist', '0.5')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('BindingSiteMode', 'AroundChain')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('AroundChain', chn)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('AroundDistance', radius)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('FixedResidues', chn)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('AroundDistanceDefn', 'SideChainOnly')

                                          
    SCREAM_PAR_FILE.close()

    #run_line_str = '/ul/victor/Matrix_ModSim/cmdf/SCREAM/python/app/SCREAM_standalone.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    run_line_str = '/project/Biogroup/Software/SCREAM/builds/current_build/SCREAM.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    os.system(run_line_str)
    sys.exit()

def unpackMutInfo(mutInfo):
    """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""
    mutAA = mutInfo[0]
    (mutPstn, mutChn) = mutInfo[1:].split('_')
    mutPstn = int(mutPstn)
    return (mutAA, mutPstn, mutChn)


if __name__ == '__main__':
    main()
