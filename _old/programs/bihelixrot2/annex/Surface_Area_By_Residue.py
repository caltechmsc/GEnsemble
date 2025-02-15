#!/usr/bin/env python

# Command is: fsm-linux -s HisRS_FSM.bgf -f ~/ForceFieldFiles/dreidii322-mpsim.par -v 1 > out

import sys, os
import BgfTools
import FsmTools

# AA_Sidechain_SASA for AA sidechain in a Tripeptide.

AA_Sidechain_SASA = { 'ALA' :    74.36000,
                      'ARG' :   253.94000,
                      'ASN' :  142.12000,
                      'ASP' :  123.51000,
                      'CYS' :  108.41000,
                      'GLN' :  178.16000,
                      'GLU' :  160.09000,
                      'GLY' :    0.00000,
                      'HIS' :  163.48000,
                      'HSD' :  163.48000,
                      'HSE' :  163.48000,
                      'HSP' :  163.48000,
                      'ILE' :  172.97000,
                      'LEU' :  171.03000,
                      'LYS' :  186.43000,
                      'MET' :  183.81000,
                      'PHE' :  184.17000,
                      'PRO' :  144.31000,
                      'PRO' :  144.31000,
                      'SER' :   96.66000,
                      'THR' :  123.05000,
                      'TRP' :  230.83000,
                      'TYR' :  208.74000,
                      'VAL' :  130.80000 }



def Surface_Area_By_Residue_usage():
    message = 'This program calls FSM to calculate surface area (SASA) of a protein and returns surface area by residue.\n'
    usage = sys.argv[0] + ' bgf_file '

    print message, '\n', usage, '\n'


def Surface_Area_By_Residue(structure_file, forcefield_file, output_fh):
    output_fh = sys.stdout
    fsm_output_file = 'tmp16584.fsm.out'
    text = run_surface_area_by_residue(structure_file, forcefield_file, fsm_output_file)
    for l in text:
        print >>output_fh, l
        

def run_surface_area_by_residue(structure_file, forcefield_file, fsm_output_file):
    # comment: should put everything below in a single routine in FsmTools.  The exposition of inner workings too great for my comfort and perfectionalism.
    (ATOM_lines, CONECT_lines) = BgfTools.return_ATOM_and_CONECT_lines(structure_file)
    bgf_atom_list = BgfTools.make_PyAtom_list(ATOM_lines)
    
    os.system('/ul/victor/bin/fsm-linux -s ' + structure_file + ' -f ' + forcefield_file + ' -r 1.4 ' + ' -v 1 > ' + fsm_output_file)
    atom_area_atom_list = FsmTools.get_atom_area(fsm_output_file)

    residue_list = FsmTools.return_residue_list_with_area_info(atom_area_atom_list, bgf_atom_list)

    text_lines = []
    
    for res in residue_list:
        ratio = '     ?'
        try:
            default_area = AA_Sidechain_SASA[res.res_name]
            ratio = res.surface_area / default_area * 100
            ratio = '%6.2f' % (ratio)
            ratio += ' %'
        except KeyError, e:
            pass
        except ZeroDivisionError, e:
            ratio = '  0.00 %'
            
        text = '%3s %5d %1s : %10.5f  ' % (res.res_name, res.res_pstn, res.chain_name, res.surface_area)
        text += ratio
        text_lines.append(text)

    return text_lines


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:
        Surface_Area_By_Residue_usage()
        sys.exit(2)

    bgf_file = args[0]
    ff_file = '/project/Biogroup/FF/dreiding-0.3.par'
    output = sys.stdout

    Surface_Area_By_Residue(bgf_file, ff_file, output)
