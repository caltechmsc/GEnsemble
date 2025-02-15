
import sys, os
import math
#from Py_Scream_EE import *

def usage():
    print '''
Does This is a wrapper for SCREAM_standlone.
Usage: %s <bgffile> <rotlib_specs> <delta method> <value> <residue list>
E.g.:  %s PheRS.bgf 10 FLAT 0.4 F258_A F260_A
Function: Does SCREAM_standalone.  Writes out a SCREAM .par file.
Remark: If you don\'t know what "delta method" means, just use "FLAT" with a value of "0.4", i.e. use the parameters given in the example.
''' % (sys.argv[0], sys.argv[0])
    sys.exit()

def main():

    if len(sys.argv) <= 3:
        usage()
        
    bgf_file = sys.argv[1]
    rotlib_specs = sys.argv[2]
    delta_method = sys.argv[3]
    final_delta_value = float(sys.argv[4])

    #if delta_method == 'FULL':
    #confidence_interval = final_delta_value
    #final_delta_value = sp_funcs.erf_inv(confidence_interval)*math.sqrt(2.)-1  # formula is sigma * (1-t)

    
    mutInfo_list = sys.argv[5:]

    scream_delta_file_dir = os.environ.get('SCREAM_DELTA_PAR_FILE_PATH')

    scream_delta_file = scream_delta_file_dir + 'SCREAM_delta_Total_Min.par'
    ff_file = os.environ.get('FORCE_FIELD_FILE')
    eachAtomDelta_file = scream_delta_file_dir + 'SCREAM_EachAtomDeltaFileStub.par'
    polarExclusion_file = scream_delta_file_dir + 'SCREAM_PolarOptimizationExclusionsStub.par'


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

    print >>SCREAM_PAR_FILE, '%25s %s' % ('PlacementMethod', 'CreateCB')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('CreateCBParameters', '1.81 51.1 1.55 0.5')
    
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseScreamEnergyFunction', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaMethod', delta_method)

    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseDeltaForInterResiE', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('UseAsymmetricDelta', 'YES')

    print >>SCREAM_PAR_FILE, '%25s %f' % ('FlatDeltaValue', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('DeltaStandardDevs', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %f' % ('InnerWallScalingFactor', final_delta_value)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('MultiplePlacementMethod', 'ClusteringThenDoubletsThenSinglets')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('CBGroundSpectrumCalc', 'YES')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('KeepOriginalRotamer', 'NO')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('OneEnergyFFParFile', ff_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('DeltaParFile', scream_delta_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('EachAtomDeltaFile', eachAtomDelta_file)
    print >>SCREAM_PAR_FILE, '%25s %s' % ('PolarOptimizationExclusions', polarExclusion_file)

    print >>SCREAM_PAR_FILE, '%25s %s' % ('LJOption', '12-6')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('CoulombMode', 'Normal')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Dielectric', '2.5')
        
    print >>SCREAM_PAR_FILE, '%25s %s' % ('Selections', 1)

    print >>SCREAM_PAR_FILE, '%25s %s' % ('AbsStericClashCutoffEL', '999999999')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffEnergy', '250')
    print >>SCREAM_PAR_FILE, '%25s %s' % ('StericClashCutoffDist', '0.5')
    SCREAM_PAR_FILE.close()

    SCREAM_main_script_path = os.environ.get('PYTHON_EXE') + ' ' + os.environ.get('SCREAM_MAIN_SCRIPT_PATH')
    run_line_str = SCREAM_main_script_path + 'SCREAM.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    
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
