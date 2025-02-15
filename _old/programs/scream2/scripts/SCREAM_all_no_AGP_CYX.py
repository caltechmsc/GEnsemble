
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

    scream_delta_file_dir = os.environ.get('SCREAM_DELTA_PAR_FILE_PATH')
    scream_delta_file = scream_delta_file_dir + 'SCREAM_delta_Total_Min.par'

    scream_par_filename = 'scream.par'
    #SCREAM_par_writer_module.write_CreateCB_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, final_delta_value)
    SCREAM_par_writer_module.write_CreateCB_no_AGP_CYX_parfile(scream_par_filename, bgf_file, rotlib_specs, delta_method, final_delta_value)


    SCREAM_main_script_path = os.environ.get('PYTHON_EXE') + ' ' + os.environ.get('SCREAM_MAIN_SCRIPT_PATH')
    run_line_str = SCREAM_main_script_path + 'SCREAM.py' + ' ' + scream_par_filename + ' > ' + 'scream.out'
    os.system(run_line_str)
    os.system('gzip -9f scream.out')
    os.system('gzip -9f Field1.bgf')
    sys.exit()


if __name__ == '__main__':
    print '''
===================================================================================
Copyright Victor Wai Tak Kam and William A. Goddard III, Caltech, Pasadena, CA, USA, 
All rights Reserved
===================================================================================
'''
    main()
    print '''
===================================================================================
Copyright Victor Wai Tak Kam and William A. Goddard III, Caltech, Pasadena, CA, USA, 
All rights Reserved
===================================================================================
'''
