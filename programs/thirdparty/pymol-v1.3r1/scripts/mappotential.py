#
# By Adam Griffith
# Modified from: apbsplugin.py
#
from pymol.cgo import *
from pymol import cmd
from pymol.vfont import plain

def mappotential( map , mol , low=-1 , mid=0 , high=1):
    '''
DESCRIPTION
"mappotential" maps an APBS potential object (dx file) onto the
solvent accessible surface of a molecule without using the
APBS Tools plugin.
 
USAGE
mappotential potential, molecule [, low, mid, high]

ARGUMENTS
potential = APBS potential object (dx file)
molecule  = Molecule to map potential onto
low       = low range    [default = -1]
mid       = middle range [default =  0]
high      = high range   [default =  1]

EXAMPLES
mappotential prot.dx, protA
mappotential prot.dx, protA, -5, 0, 5

NOTES
Function will create object necessary for the color map called:
r_{molecule}_{low}_{mid}_{high}
    '''

    # Print for user
    print "potential: %s" % map
    print "molecule:  %s" % mol
    print "range:    [%s, %s, %s]" % (low, mid, high)

    # Update Ramp
    ramp_name = "r_%s_%s_%s_%s" % (mol,low,mid,high)
    range = [low,mid,high]
    cmd.delete(ramp_name)
    cmd.ramp_new(ramp_name,map,range)
    cmd.set('surface_color',ramp_name,mol)

    # Show surface
    cmd.set('surface_solvent',0,mol)
    cmd.set('surface_ramp_above_mode',1,mol)
    cmd.show('surface',mol)
    cmd.refresh()
    cmd.recolor(mol)

cmd.extend('mappotential',mappotential)
