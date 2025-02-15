#!/usr/bin/python

import sys, os
#from Py_Scream_EE import *
import SCREAM_par_writer_module

def usage():
    print '''
Wrapper for SCREAMing all residues minus A, G, P, CYX.
Usage: %s <bgffile> <rotlib_specs> <delta method> <value> 
E.g.:  %s  PheRS.bgf 10 FULL 0.0
Remark: If you don\'t know what "delta method" means, just use "FLAT" with a value of "0.4", i.e. use the parameters given in the example.  Please visit https://wiki.wag.caltech.edu/twiki/bin/view/Biogroup/ScreamPage for more details.
''' % (sys.argv[0], sys.argv[0])
    sys.exit()

def main():

    if len(sys.argv) <= 3:
        usage()
        
    bgf_file = sys.argv[1]
    rotlib_specs = sys.argv[2]
    delta_method = sys.argv[3].upper()
    final_delta_value = float(sys.argv[4])

#   ff_file = '/ul/victor/ForceFieldFiles/PS330_mpsim.par'
    ff_file = '/project/Biogroup/FF/dreiding-0.3.par'
    scream_delta_file = '/project/Biogroup/Software/SCREAM/lib/SCREAM_delta_par_files/SCREAM_delta.par'

    scream_par_filename = 'scream.par'
    #SCREAM_par_writer_module.write_CreateCB_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, final_delta_value)
    SCREAM_par_writer_module.write_CreateCB_no_AGP_CYX_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, final_delta_value)

    run_line_str = '/project/Biogroup/Software/SCREAM/builds/current_build/SCREAM.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    os.system(run_line_str)
    os.system('gzip -9f scream.out')
    os.system('gzip -9f Field1.bgf')
    sys.exit()


if __name__ == '__main__':
    main()
