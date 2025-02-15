#!/usr/bin/python

import sys, os
#from Py_Scream_EE import *

def usage():
    print '''
Does This is a wrapper for SCREAM_standlone.
Usage: SCREAM_standalone_wrap.py <bgffile> <rotlib_specs> <delta method> <value> <residue list>
E.g.:  SCREAM_standalone_wrap.py PheRS.bgf 10 FLAT 0.4 F258_A F260_A
Function: Does SCREAM_standalone.  Writes out a SCREAM .par file.
Remark: If you don\'t know what "delta method" means, just use "FLAT" with a value of "0.4", i.e. use the parameters given in the example.
'''
    sys.exit()

def main():

    if len(sys.argv) <= 3:
        usage()
        
    bgf_file = sys.argv[1]
    rotlib_specs = sys.argv[2]
    delta_method = sys.argv[3]
    final_delta_value = float(sys.argv[4])
    mutInfo_list = sys.argv[5:]
    ff_file = '/project/Biogroup/FF/PS330_mpsim.par'
    scream_delta_file = '/project/Biogroup/Software/SCREAM/lib/SCREAM_delta_par_files/SCREAM_delta.par'

    scream_par_filename = 'scream.par'
    SCREAM_PAR_FILE = open(scream_par_filename, 'w')
    mutInfo_string = ''
    extra_lib_string = ''
    for mutInfo in mutInfo_list:
        import re
        CNN_REGEX = re.compile("cnn")
        if CNN_REGEX.search(mutInfo):\
               extra_lib_string = mutInfo
        else:
            mutInfo_string += mutInfo
            mutInfo_string += ' '
    rotlib_specs_string = ''
    if rotlib_specs == 'SCWRL':
        rotlib_specs_string = rotlib_specs
    else:
        rotlib_specs_string = 'V' + rotlib_specs
    
    print >>SCREAM_PAR_FILE, '%25s %s' % ('InputFileName', bgf_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MutateResidueInfo', mutInfo_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('AdditionalLibraryInfo', extra_lib_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Library', rotlib_specs_string)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseScreamEnergyFunction', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaMethod', delta_method)

    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaForInterResiE', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseAsymmetricDelta', 'YES')
    print >>SCREAM_PAR_FILE, '%30s %f' % ('DistanceDielectricPrefactor', 2.5)
    
    print >>SCREAM_PAR_FILE, '%25s %f' % ('FlatDeltaValue', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('DeltaStandardDevs', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('InnerWallScalingFactor', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MultiplePlacementMethod', 'ExcitationWithClustering')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('KeepOriginalRotamer', 'NO')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('OneEnergyFFParFile', ff_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('DeltaParFile', scream_delta_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Selections', 5)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffEnergy', '250')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffDist', '0.5')
    SCREAM_PAR_FILE.close()

    #run_line_str = '/ul/victor/Matrix_ModSim/cmdf/SCREAM/python/app/SCREAM_standalone.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    run_line_str = '/project/Biogroup/Software/SCREAM/builds/current_build/SCREAM.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    os.system(run_line_str)
    os.system('gzip -9qf scream.out')
    os.system('gzip -9qf Evolution.dat')

    sys.exit()

def unpackMutInfo(mutInfo):
    """_unpackMutInfo: unpacks a string like C123_X, i.e. returns a (C, 123, X) tuple."""
    mutAA = mutInfo[0]
    (mutPstn, mutChn) = mutInfo[1:].split('_')
    mutPstn = int(mutPstn)
    return (mutAA, mutPstn, mutChn)


if __name__ == '__main__':
    main()
