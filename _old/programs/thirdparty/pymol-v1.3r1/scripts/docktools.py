from pymol.cgo import *
from pymol import cmd, stored
from pymol.vfont import plain
from operator import itemgetter
import os
import re
import time

# dockview #####################################################################
def dockview(obj,lig='chain X'):
    """
DESCRIPTION
    "dockview" applies a set of standard view options for one or more objects
    containing a ligand.  It additionally will find hydrogen bonds between the
    ligand and the pocket, and between residues within the pocket.  Each object,
    its selections, and associated hydrogen bonds will be placed into a group
    with the name {object}.grp

    Selections:
    * {object}.grp - group container for {object}
    * {object}.lig - target ligand in object
    * {object}.pkt - all residues within 5A of target ligand
    * {object}.het - all non-ligand hetatoms, excluding waters
    * {object}.wat - all waters (resn HOH or resn WAT)

    Hydrogen bonds:
    * Output file: {object}.hbonds.csv
    * lig-pkt.{object} subgroup containing individual distance objects
    * pkt-pkt.{object} subgroup containing individual distance objects

    Colors:
    * ligand             - magenta
    * pocket             - cyan
    * non-ligand hetatms - purple
    * all else           - white

    Show/Hide:
    * show cartoon, all
    * show nb_spheres, all
    * show sticks, ligand
    * show sticks, pocket
    * hide sticks, backbone
    * hide sticks, nonpolar hydrogens

    Global settings:
    * white background ('bg white')
    * ray_opaque_background = off
    * ray_orthoscopic = on
    * ortho = on
    * hash_max = 200
    * dash_length = 0.3
    * dash_gap = 0.2
    * ray_shadows = none

USAGE
    dockview object [,lig='selection' [,pse='psefile']]

ARGUMENTS
    object - object to apply settings to, 'all' for all objects
    lig    - selection for ligand, default is 'chain X'

EXAMPLES
    dockview all, lig='resi 999 & chain X'
    dockview all
    dockview b2.cau.pose1

NOTES
    The routine that identifies hydrogen bonds is somewhat overzealous and will
    show too many hydrogen bonds.  It is recommended that you deselect or delete
    hydrogen bonds that don't look right.  The hydrogen bond cutoffs are:
    * hydrogen-acceptor distance:    3.5 A
    * donor-hydrogen-acceptor angle: 90 degrees
    * hydrogen-acceptor-X angle:     75 degrees

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""

    # Standard Settings
    cmd.bg_color('white')
    cmd.set('ray_opaque_background','off')
    cmd.set('ray_orthoscopic',      'on')
    cmd.set('ortho',                'on')
    cmd.set('hash_max',             '200')
    cmd.set('dash_length',          '0.3')
    cmd.set('dash_gap',             '0.2')
    util.ray_shadows('none')
    util.performance(0)

    objlist = []
    if (obj == 'all'):
        objlist = cmd.get_object_list('all')
    else:
        objlist.append(obj)

    # For each object
    for o in objlist:
        print 'dockview: %s'%(o)

        # Ligand, Pocket, Backbone
        other_het = 0
        has_water = 0
        cmd.select('%s.lig'%(o), '%s & (%s)'%(o,lig))
        cmd.select('%s.pkt'%(o), '%s & byres (%s & (%s) around 5)'%(o,o,lig))
        if (cmd.count_atoms('%s & hetatm & (not (%s)) & (not resn HOH+WAT)'%(o,lig)) > 0):
            other_het = 1
            cmd.select('%s.het'%(o), '%s & hetatm & (not (%s)) & (not resn HOH+WAT)'%(o,lig))
        if (cmd.count_atoms('%s & hetatm & (not (%s)) & (resn HOH+WAT)'%(o,lig)) > 0):
            has_water = 1
            cmd.select('%s.wat'%(o), '%s & hetatm & (not (%s)) & (resn HOH+WAT)'%(o,lig))

        # Group
        grp = '%s.grp'%o
        cmd.group(grp)
        cmd.group(grp, '%s %s.lig %s.pkt'%(o,o,o))
        if (other_het): cmd.group(grp,'%s.het'%o)
        if (has_water): cmd.group(grp,'%s.wat'%o)

        # Show/hide
        util.cbaw(o)
        util.cbac('%s.pkt'%o)
        util.cbam('%s.lig'%o)
        cmd.hide('everything',o)
        cmd.show('cartoon',o)
        cmd.show('sticks','%s.lig'%o)
        cmd.show('sticks','%s.pkt'%o)
        if (other_het):
            cmd.show('sticks','%s.het'%o)
            cmd.show('nb_spheres','%s.het'%o)
            util.cbap('%s.het'%o)
        if (has_water):
            cmd.show('sticks','%s.wat'%o)
            cmd.show('nb_spheres','%s.wat'%o)
        hide_np_hyd(o)
        hide_bbn(o)

        # Donor Lig - Acceptor Pkt
        nhb = 0
        don = '%s & (%s)'%(o,lig)
        acc = '%s & byres (%s & %s around 5)'%(o,o,lig)
        nhb = show_hb_da(o,don,acc,label='lig-ptn',ctr=nhb)

        # Donor Pkt - Acceptor Lig
        don = '%s & byres (%s & %s around 5)'%(o,o,lig)
        acc = '%s & (%s)'%(o,lig)
        nhb = show_hb_da(o,don,acc,label='lig-ptn',ctr=nhb)

        # Donor/Acceptor Pkt
        don = '%s & byres (%s & %s around 5)'%(o,o,lig)
        acc = '%s & byres (%s & %s around 5)'%(o,o,lig)
        nhb = show_hb_da(o,don,acc,label='ptn-ptn',ctr=nhb)
        cmd.disable('ptn-ptn.%s'%o)

        # Finish
        cmd.deselect()

    # Global selections
    if (obj == 'all'):
        cmd.select('lig_all', '%s'%(lig))
        cmd.select('pkt_all', 'byres (%s around 5)'%(lig))
        cmd.select('bbn_all', '(n. c,o,h|(n. n&!r. pro))')
        cmd.deselect()
        cmd.zoom('pkt_all')

    # Close groups
    for o in objlist:
        cmd.group('%s.grp'%(o),'close')

    # Done
    print 'docview done\n'


# show_hb_in_sel ###############################################################
def show_hb_in_sel(o,sel,label='hb',fn='',ctr=0):
    """
DESCRIPTION
    "show_hb_in_sel" identifies all hydrogen bonds within the given selection,
    excluding backbone-backbone hydrogen bonds.  The specified object is placed
    in a group with the name {object}.grp if it is not already there.  Each
    hydrogen bond measurement is placed in {object}.grp/{label}.{object}.  The
    hydrogen bond data is placed in a CSV file, which defaults to
    {object}.hbonds.csv.

    The routine that identifies hydrogen bonds is somewhat overzealous and will
    show too many hydrogen bonds.  It is recommended that you deselect or delete
    hydrogen bonds that don't look right.  The hydrogen bond cutoffs are:
    * hydrogen-acceptor distance:    3.5 A
    * donor-hydrogen-acceptor angle: 90 degrees
    * hydrogen-acceptor-X angle:     75 degrees

USAGE
    show_hb_in_sel object, selection [,label='string' [,fn='file' [,ctr='num']]]

ARGUMENTS
    object    - object to search
    selection - part of object to search hydrogen bonds for
    label     - label for hydrogen bond objects and group, defaults to 'hb'
    fn        - CSV file for data, defaults to {object}.hbonds.csv
    ctr       - hydrogen bond counter, defaults to 0

EXAMPLES
    show_hb_in_sel obj, byres ((obj & chain X) expand 5)

NOTES
    It is best to be very specific with your selections if you have multiple
    objects present, as it is easy for your selections to cross between objects.
    For example, this selection:
        byres (chain X expand 5)
    will select the ligand and binding site around chain X in *all* objects.  It
    is better to use this:
        byres ((obj & chain X) expand 5)
    which will select the ligand and binding site around chain X in just the
    target object.

    Also note that the script will find the actual hydrogens and polar heavy
    atoms within your selection.  It is not necessary for you to do so in your
    input.

    Finally, this script does NOT identify hydrogen bonds between objects.  The
    target object and the target selection must be in the same object.

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""

    # Filename
    if (fn == ''): fn = '%s.hbonds.csv'%o

    # Show hydrogen bonds
    show_hb_da(o,sel,sel,label,fn,ctr)


# show_hb_da ###################################################################
def show_hb_da(o,hsel,asel,label='hb',fn='',ctr=0):
    """
DESCRIPTION
    "show_hb_da" shows hydrogen bonds between the donor and acceptor atom
    selections within the specified object, excluding backbone-backbone hydrogen
    bonds.  Each hydrogen bond is given its own measurement object.  The
    specified object is placed in a group with the name {object}.grp if it is
    not already there.  Each hydrogen bond measurement is placed in
    {object}.grp/{label}.{object}.  The hydrogen bond data is placed in a CSV
    file, which defaults to {object}.hbonds.csv.

    The routine that identifies hydrogen bonds is somewhat overzealous and will
    show too many hydrogen bonds.  It is recommended that you deselect or delete
    hydrogen bonds that don't look right.  The hydrogen bond cutoffs are:
    * hydrogen-acceptor distance:    3.5 A
    * donor-hydrogen-acceptor angle: 90 degrees
    * hydrogen-acceptor-X angle:     75 degrees

USAGE
    show_hb_da object, donor selection, acceptor selection
               [,label='string' [,fn='file' [,ctr='num']]]

ARGUMENTS
    object   - object to search
    donor    - h-bond donor selection
    acceptor - h-bond acceptor selection
    label    - label for hydrogen bond objects and group, defaults to 'hb'
    fn       - CSV file for data, defaults to {object}.hbonds.csv
    ctr      - hydrogen bond counter, defaults to 0

EXAMPLES
    show_hb_da obj, obj & chain X, byres ((obj & chain X) around 5)

NOTES
    It is best to be very specific with your donor/acceptor selections if you
    have multiple objects present, as it is easy for your selections to cross
    between objects.  For example, this selection:
        byres (chain X around 5)
    will select the binding site around chain X in *all* objects.  It is better
    to use this:
        byres ((obj & chain X) around 5
    This selection only finds the binding site around chain X in the target
    object.

    Also note that the script will find the actual hydrogens and polar heavy
    atoms within your selection.  It is not necessary for you to do so in your
    input.

    Finally, this script does NOT identify hydrogen bonds between objects.  If
    your donor selection comes from one object, but your acceptor selection
    comes from a different object, then bad things will happen!

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""

    # Filename & Settings
    if (fn == ''): fn = '%s.hbonds.csv'%o
    f = open(fn,'a')
    f.write('show_hb\n'
            'object,%s\n'
            'donor sel,"%s"\n'
            'acceptor sel,"%s"\n'
            'label,%s\n'
            'file,%s\n'
            'ctr start,%s\n'%\
            (o,hsel,asel,label,fn,ctr))
    f.write('molecule,interaction,count,'
            'D resname,D resnum,D chain,'
            'A resname,A resnum,A chain,'
            'dist,angle,'
            'D name,H name,A name,'
            'D num,H num,A num\n')
    print('show_hb:\n'
          '  object:       %s\n'
          '  donor sel:    %s\n'
          '  acceptor sel: %s\n'
          '  label:        %s\n'
          '  file:         %s\n'
          '  ctr start:    %s\n'%\
          (o,hsel,asel,label,fn,ctr))

    # Ensure object is in group
    grp = '%s.grp'%o
    hbgrp = '%s.%s'%(label,o)
    cmd.group(grp,o)

    # Get atoms
    hyd     = []
    acc     = []
    xyz     = cmd.get_model(o,1).get_coord_list()
    hsel2   = '%s & (%s) & (ele h & (ele n+o+s extend 1))'%(o,hsel)
    asel2   = '%s & (%s) & (ele n+o+s)'%(o,asel)
    iterstr = 'append((index,resn,resi,chain,name,type))'
    cmd.iterate(hsel2, 'hyd.%s'%iterstr, space=locals())
    cmd.iterate(asel2, 'acc.%s'%iterstr, space=locals())

    # Iterate over hydrogens
    for h in hyd:
        # Hydrogen data
        h_id   = h[0]
        h_rnam = h[1]
        h_num  = h[2]
        h_chn  = h[3]
        h_anam = h[4]
        h_type = h[5]
        h_xyz  = xyz[h_id - 1]

        # Iterate over acceptors
        for a in acc:
            # Acceptor data
            a_id   = a[0]
            a_rnam = a[1]
            a_num  = a[2]
            a_chn  = a[3]
            a_anam = a[4]
            a_type = a[5]
            a_xyz  = xyz[a_id - 1]

            # Same residue? Skip
            if ((h_num == a_num) and (h_chn == a_chn)): continue

            # hydrogen-acceptor distance must be <= 3.5
            d_ha = distAB(h_xyz, a_xyz)
            if (d_ha > 3.5): continue

            # Donor heavy atom
            don = []
            cmd.iterate('%s & (not index %s) & (index %s extend 1)'% \
                        (o,h_id,h_id), 'don.%s'%iterstr, space=locals())
            d_id   = don[0][0]
            d_rnam = don[0][1]
            d_num  = don[0][2]
            d_chn  = don[0][3]
            d_anam = don[0][4]
            d_type = don[0][5]
            d_xyz  = xyz[d_id - 1]

            # Backbone - Backbone hydrogen bond? (N - HN - O)? Skip
            if ((d_type == 'ATOM') and (a_type == 'ATOM') and \
                (d_anam == 'N')    and (a_anam == 'O')):
                continue

            # donor-hydrogen-acceptor angle must be >= 90
            a_dha = angleABC(d_xyz, h_xyz, a_xyz)
            if (a_dha < 90): continue

            # hydrogen-acceptor-X angle must be >= 75 for all X connected to acceptor
            cnn = []
            cmd.iterate('%s & (not index %s) & (index %s extend 1)'% \
                        (o,a_id,a_id), 'cnn.%s'%iterstr, space=locals())

            haxfail = 0
            for x in cnn:
                x_id  = x[0]
                x_xyz = xyz[x_id - 1]
                a_hax = angleABC(h_xyz, a_xyz, x_xyz)
                if (a_hax < 75):
                    haxfail = 1
                    break
            if (haxfail): continue

            # We have a hydrogen bond!
            ctr += 1
            measure = '%s.%s.%s'%(label,ctr,o)
            cmd.distance(measure, '%s & index %s'%(o,h_id), '%s & index %s'%(o,a_id))
            cmd.color('red',measure)
            cmd.group(hbgrp,measure)
            if ((d_type == 'ATOM') and (d_anam == 'N')):
                show_bbn('%s & (resi %s) & (chain %s)'%(o,d_num,d_chn))
                hide_np_hyd('%s & (resi %s) & (chain %s)'%(o,d_num,d_chn))
            if ((a_type == 'ATOM') and (a_anam == 'O')):
                show_bbn('%s & (resi %s) & (chain %s)'%(o,a_num,a_chn))
                hide_np_hyd('%s & (resi %s) & (chain %s)'%(o,a_num,a_chn))
            if (d_rnam != 'RES'):
                label_res('%s & (resi %s) & (chain %s)'%(o,d_num,d_chn))
            if (a_rnam != 'RES'):
                label_res('%s & (resi %s) & (chain %s)'%(o,a_num,a_chn))

            # Write data to file
            f.write('%s,%s,%s,'
                    '%s,%s,%s,'
                    '%s,%s,%s,'
                    '%.2f,%.1f,'
                    '%s,%s,%s,'
                    '%s,%s,%s\n'%
                    (o,       label,  ctr,    \
                     d_rnam,  d_num,  d_chn,  \
                     a_rnam,  a_num,  a_chn,  \
                     d_ha,    a_dha,          \
                     d_anam,  h_anam, a_anam, \
                     d_id,    h_id,   a_id))

    # Done
    cmd.group(grp,hbgrp)
    f.write('\n')
    f.close()
    return ctr


# distAB #######################################################################
def distAB(a_xyz,b_xyz):
    d = math.sqrt(math.pow((a_xyz[0] - b_xyz[0]),2) + \
                  math.pow((a_xyz[1] - b_xyz[1]),2) + \
                  math.pow((a_xyz[2] - b_xyz[2]),2))
    return d


# angleABC #####################################################################
def angleABC(a_xyz,b_xyz,c_xyz):
    v1 = [0,0,0]
    v1[0] = a_xyz[0] - b_xyz[0]
    v1[1] = a_xyz[1] - b_xyz[1]
    v1[2] = a_xyz[2] - b_xyz[2]

    v2 = [0,0,0]
    v2[0] = c_xyz[0] - b_xyz[0]
    v2[1] = c_xyz[1] - b_xyz[1]
    v2[2] = c_xyz[2] - b_xyz[2]

    dot = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    d1 = distAB(b_xyz,a_xyz)
    d2 = distAB(b_xyz,c_xyz)

    a = math.degrees( math.acos( dot / (d1 * d2) ) )

    return a


# hide_np_hyd ##################################################################
def hide_np_hyd(sel):
    """
DESCRIPTION
    "hide_np_hyd" is a very simple command to hide non-polar hydrogens within a
    given selection.  It executes this command:
        hide everything, {selection} & (ele h & (ele c extend 1))

USAGE
    hide_np_hyd selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    cmd.hide('everything','%s & (ele h & (ele c extend 1))'%(sel))


# hide_np_res ##################################################################
def hide_np_res(sel):
    """
DESCRIPTION
    "hide_np_res" is a very simple command to hide non-polar residues.
    It executes these commands:
        hide sticks, {selection} & (resn A+G+P+F+I+L+M+Y+V+W)
        hide lines,  {selection} & (resn A+G+P+F+I+L+M+Y+V+W)

USAGE
    hide_np_res selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    cmd.hide('sticks','(%s) & (resn A+G+P+F+I+L+M+Y+V+W)')
    cmd.hide('lines', '(%s) & (resn A+G+P+F+I+L+M+Y+V+W)')


# hide_bbn #####################################################################
def hide_bbn(sel):
    """
DESCRIPTION
    "hide_bbn" is a very simple command to hide backbone atoms within a given
    selection.  It executes these commands:
        hide sticks, {selection} & (n. c,o,h|(n. n&!r. pro))
        hide lines,  {selection} & (n. c,o,h|(n. n&!r. pro))

USAGE
    hide_bbn selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    cmd.hide('sticks','(%s) & (n. c,o,h|(n. n&!r. pro))'%sel)
    cmd.hide('lines', '(%s) & (n. c,o,h|(n. n&!r. pro))'%sel)


# show_bbn #####################################################################
def show_bbn(sel):
    """
DESCRIPTION
    "show_bbn" is a very simple command to show backbone atoms as sticks without
    turning on the sidechains in a given selection.  It executes this command:
        show sticks, {selection} & (n. c,o,h|(n. n&!r. pro))

USAGE
    show_bbn selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    cmd.show('sticks','(%s) & (n. c,o,h|(n. n&!r. pro))'%sel)


# label_res ####################################################################
def label_res(sel):
    """
DESCRIPTION
    "label_res" places a single label on each residue within the selection
    showing the residue name and number.  For standard residues other than GLY,
    the label is placed on the CB atom.  For GLY the label is placed on the CA
    atom.  For HETATM residues the label is placed on a pseudoatom at the center
    of the residue.

USAGE
    label_res selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    reslist = get_reslist(sel)
    for r in reslist:
        robj  = r[0]
        rname = r[1]
        rnum  = r[2]
        rchn  = r[3]
        rtype = r[4]
        if (rtype == 'HETATM'):
            cmd.pseudoatom(robj,'%s & (resi %s) & (chain %s)'%(robj,rnum,rchn),\
                           'hetlabel',rname,rnum,rchn)
            cmd.label('%s & (resi %s) & (chain %s) & (segi PSDO)'%(robj,rnum,rchn),\
                      'resn+resi')
        elif (rname == 'GLY'):
            cmd.label('%s & (resi %s) & (chain %s) & (name CA)'%\
                      (robj,rnum,rchn), 'resn+resi')
        else:
            cmd.label('%s & (resi %s) & (chain %s) & (name CB)'%\
                      (robj,rnum,rchn), 'resn+resi')


# get_reslist ##################################################################
def get_reslist(sel):
    """
DESCRIPTION
    "get_reslist" returns a dictionary containing each residue within the
    selection.  The dictionary is structured thusly:
       reslist[(model,resn,resi,chain,type)] = 1
    'model' is the name of the object
    'resn' is the residue name
    'resi' is the residue number
    'chain' is the chain of the residue
    'type' is either ATOM or HETATM

USAGE
    reslist = get_reslist(selection)

NOTE
    If you want to loop over the residues in some sort of order, you can do this:
       for r in sorted(reslist, key = itemgetter(0,3,2))
    This specific command will sort by model > chain > residue number

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    reslist = dict()
    cmd.iterate(sel,'reslist[(model,resn,resi,chain,type)] = 1',space=locals())
    return reslist


# print_reslist ################################################################
def print_reslist(sel):
    """
DESCRIPTION
    "print_reslist" prints a very ugly table listing the residues within the
    selection.  The table is printed in CSV format showing for each residue:
       model,residue name,residue number,chain
    The output is sorted by model > chain > residue number

USAGE
    print_reslist selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    reslist = get_reslist(sel)
    for r in sorted(reslist, key = itemgetter(0,3,2)):
        print '%s,%s,%s,%s'%(r[0:4])


# print_reslist ################################################################
def mappotential( map , mol , low=-1 , mid=0 , high=1):
    """
DESCRIPTION
    "mapotential" maps an APBS potential from a DX file onto the solvent
    accessible surface of a molecule, bypassing te APBS Tools plugin.

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

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)

SOURCE
    Modified from apbsplugin.py

"""

    # Print for user
    print 'mappotential:'
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


# load_bgf #####################################################################
def load_bgf(bgf,name='',color=''):
    """
DESCRIPTION
    "load_bgf" loads individual BGF files into PyMol by converting the BGF file
    to a temporary PDB file and loading that PDB file.  The command also does
    some very basic visualization changes:
     * color everything white (by atom), or to specified color (see 'list_colors'
       for a list of valid PyMol colors)
     * hide everything, then show protein as lines, hetatms as stick/nb_sphere

USAGE
    load_bgf bgf [, color]

ARGUMENTS
    bgf   = BGF file
    color = valid PyMol color [default: white]

EXAMPLES
    load_bgf beta2.cau.bgf, magenta
    load_bgf beta2.cau.bgf
    load_bgf path/to/file/beta2.cau.bgf

NOTES
    In order to generate the PDB file, the following records are identified
    in the BGF file, with the expected column numbers listed:
    * record         [ 0 -  6] - ATOM/HETATM record
    * atom number    [ 7 - 11]
    * atom name      [13 - 17]
    * residue name   [19 - 21]
    * chain          [23]
    * residue number [25 - 29]
    * x coordinate   [30 - 39]
    * y coordinate   [40 - 49]
    * z coordinate   [50 - 59]

    'CONECT' records are read simply by splitting the line by whitespace.

EXAMPLE ATOM/HETATM BGF LINE:
    ATOM       1  N    GLU A   39   42.81651   4.16191   2.85598 N_R    0 0 -0.47000

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    # Exists?
    if (not os.path.exists(bgf)):
        print 'ERROR: load_bgf: BGF file not found: %s'%bgf
        return -1

    # Prefix
    base = os.path.basename(bgf)
    pfx  = base[0:-4]
    if (name == ''):
        name = pfx

    # Open BGF for reading
    bgff = open(bgf,'r')

    # Temporary PDB file
    pdb = '_%s.pdb'%(pfx)
    pdbf = open(pdb,'w')

    # Read BGF, Write PDB
    for l in bgff:
        # ATOM/HETATM
        if(re.match('^(ATOM|HETATM)',l)):
            record = l[ 0: 7].strip()
            anum   = l[ 7:12].strip()
            aname  = l[13:18].strip()
            rname  = l[19:22].strip()
            chain  = l[23]
            rnum   = l[25:30].strip()
            x      = l[30:40].strip()
            y      = l[40:50].strip()
            z      = l[50:60].strip()
            pdbf.write('%-6s%5d %-4s %-3s %s%4d    %8.3f%8.3f%8.3f\n'%\
                       (record, int(anum), aname, rname, chain, int(rnum),\
                        float(x), float(y), float(z)))

        # CONECT
        if (re.match('^CONECT',l)):
            s = l.split()
            pdbf.write('%6s%5d'%(s[0],int(s[1])))
            for a in s[2:]:
                pdbf.write('%5d'%int(a))
            pdbf.write('\n')
    pdbf.write('END\n')

    # Close
    bgff.close()
    pdbf.close()

    # Load PDB
    cmd.load(pdb,name)

    # Cleanup
    os.remove(pdb)

    # View settings
    cmd.hide('everything',name)
    cmd.show('cartoon',name)
    cmd.show('sticks','%s & hetatm'%name)
    cmd.show('nb_spheres','%s & hetatm'%name)
    util.cbaw(name)
    if (color != ''):
        carbon_color(color,name)


# load_sph #####################################################################
def load_sph(sph,name='',color='',box='',boxcolor=''):
    """
DESCRIPTION
    "load_sph" loads individual SPH files into PyMol by converting the SPH file
    to a temporary PDB file and loading that PDB file.  A bounding-box PDB file
    can also be loaded at the same time.  The spheres will be displayed as a
    surface, the box will be displayed as lines.  The spheres and box can be
    given individual colors (see 'list_colors' for list of valid colors). Also,
    if a bounding box PDB is given, the spheres and box will be grouped together.

USAGE
    load_sph sph [, name [, color [, box [, boxcolor]]]]

ARGUMENTS
    sph      = sphere SPH file
    name     = rename SPH object and box using specified name
               Default: {sph prefix}.sph, {sph prefix}.box, {sph prefix}.grp
    color    = valid PyMol color [default: white]
    box      = bounding box PDB file
    boxcolor = valid PyMol color [default: red]

EXAMPLES
    load_sph b2.ala.r10.sph, r10.sph, blue, b2.ala-box10.pdb, red
    load_sph b2.ala.r10.sph, color=blue
    load_sph b2.ala.r10.sph
    load_sph path/to/file/b2.ala.r10.sph, box=different/path/b2.ala-box10.pdb

NOTES
    Visualization of the spheres as a surface can time/memory intensive.

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    # Exists?
    if (not os.path.exists(sph)):
        print 'ERROR: load_sph: SPH file not found: %s'%sph
        return -1
    if (box != ''):
        # Exists?
        if (not os.path.exists(box)):
            print 'ERROR: load_sph: BOX.pdb file not found: %s'%box
            return -1

    # Prefix
    base = os.path.basename(sph)
    pfx = base[0:-4]
    if (name == ''):
        name = '%s.sph'%pfx

    # Open SPH for reading
    sphf = open(sph,'r')

    # Temporary PDB file
    pdb = '_%s.sph.pdb'%pfx
    pdbf = open(pdb,'w')

    # Group
    grp = '%s.grp'%name
    boxname = '%s.box'%name

    # Read SPH, Write PDB
    for l in sphf:
        if (re.match('(\s+)?\d+',l)):
            n = l[ 0: 5].strip()
            x = l[ 5:15].strip()
            y = l[15:25].strip()
            z = l[25:35].strip()
            pdbf.write('%-6s%5d %-4s %-3s %s%4d    %8.3f%8.3f%8.3f\nTER\n'%\
                       ('ATOM',int(n),'C','SPH','Z',888,float(x),float(y),float(z)))
    pdbf.write('END\n')

    # Close
    sphf.close()
    pdbf.close()

    # Load PDB
    cmd.load(pdb,name)

    # Load Box
    if (box != ''):
        cmd.load(box,boxname)

    # Cleanup
    os.remove(pdb)

    # View settings
    cmd.hide('everything',name)
    cmd.show('surface',name)
    cmd.zoom('all')
    if (color == ''):
        cmd.color('white',name)
    else:
        carbon_color(color,name)

    if (box != ''):
        if (boxcolor == ''):
            cmd.color('red',boxname)
        else:
            cmd.color(boxcolor,boxname)
        cmd.group(grp)
        cmd.group(grp,name)
        cmd.group(grp,boxname)
        cmd.group(grp,'close')


# carbon_colors ################################################################
def carbon_color(c,s):
    """
DESCRIPTION
    "carbon_color" is like using 'util.cba?(selection)', but with more color
    options.  For a list of all valid colors, see 'list_colors'.  This command
    does the two following operations:
    1) util.cbaw(selection) - All atoms set to normal colors (oxygen = red,
       nitrogen = blue, sulfur = yellow, etc.), but all carbons are made white
    2) cmd.color(color,'(selection) & (ele C)') - Color all carbons in selection
       using the specified color.

USAGE
    carbon_color color, selection

ARGUMENTS
    color     = valid PyMol color [no default]
    selection = valid PyMol selection

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    util.cbaw(s)
    cmd.color(c,'(%s) & (ele C)'%s)


# list_colors ##################################################################
def list_colors():
    """
DESCRIPTION
    "list_colors" basically lists the colors that can be called by a single name.

USAGE
    list_colors

AUTHOR
    Adam Griffith (griffith@wag.caltech.edu)
"""
    print('Available colors:\n'
          '  simple:\n'
          '    green, cyan, magenta, yellow, salmon, white, slate, orange, purple\n'
          '  reds:\n'
          '    red, tv_red, raspberry, darksalmon, salmon, deepsalmon, warmpink, firebrick,\n'
          '    ruby, chocolate, brown\n'
          '  greens:\n'
          '    green, tv_green, chartreuse, splitpea, smudge, palegreen, limegreen, lime,\n'
          '    limon, forest\n'
          '  blues:\n'
          '    blue, tv_blue, marine, slate, lightblue, skyblue, purpleblue, deepblue,\n'
          '    density\n'
          '  yellows:\n'
          '    yellow, tv_yellow, paleyellow, yelloworange, limon, wheat, sand\n'
          '  magentas:\n'
          '    magenta, lightmagenta, hotpink, pink, lightpink, dirtyviolet, violet,\n'
          '    violetpurple, purple, deeppurple\n'
          '  cyans:\n'
          '    cyan, palecyan, aquamarine, greencyan, teal, deepteal, lightteal\n'
          '  oranges:\n'
          '    orange, tv_orange, brightorange, lightorange, yelloworange, olive, deepolive\n'
          '  tints:\n'
          '    wheat, palegreen, lightblue, paleyellow, lightpink, palecyan, lightorange,\n'
          '    bluewhite\n'
          '  grays:\n'
          '    white, grey90, grey80...grey20, grey10, black\n')


# help #########################################################################
def docktools_help():
    """
docktools.py adds the following commands:
  - load_bgf       - load BGF file (single), minor visual settings
  - load_sph       - load SPH file (single), minor visual settings
  - dockview       - standard visual formatting, h-bonds, selections, groups
  - show_hb_in_sel - find/display hydrogen bonds within selection for one object
  - show_hb_da     - find/display hydrogen bonds between donor and acceptor
                     selections within one object
  - hide_np_hyd    - hide sticks/lines for nonpolar hydrogensin selection
  - hide_np_res    - hide sticks/lines for nonpolar residues (AGPFILMYVW) in
                     selection
  - hide_bbn       - hide sticks/lines for backbone atomsin selection
  - show_bbn       - show sticks for backbone atoms in selection
  - label_res      - label individual residues in selection
  - get_reslist    - get dictionary containing all residues in selection
  - print_reslist  - print ugly, CSV list of all residues in selection
  - carbon_color   - set non-carbons in selection to normal colors, carbons in
                     selection set to specified color
  - list_colors    - list valid PyMol colors
  - mappotential   - quickly map APBS electrostatic potential from DX file onto
                     surface of object

  To get detailed help info, type 'help {command}'
  To print this list again, type 'help docktools'
"""

    print('\ndocktools.py adds the following commands:\n'
          '  - load_bgf       - load BGF file, minor visual settings\n'
          '  - load_sph       - load SPH file, minor visual settings\n'
          '  - dockview       - standard visual formatting, h-bonds, selections, groups\n'
          '  - show_hb_in_sel - find/display hydrogen bonds within selection for one object\n'
          '  - show_hb_da     - find/display hydrogen bonds between donor and acceptor\n'
          '                     selections within one object\n'
          '  - hide_np_hyd    - hide sticks/lines for nonpolar hydrogensin selection\n'
          '  - hide_np_res    - hide sticks/lines for nonpolar residues (AGPFILMYVW) in\n'
          '                     selection\n'
          '  - hide_bbn       - hide sticks/lines for backbone atomsin selection\n'
          '  - show_bbn       - show sticks for backbone atoms in selection\n'
          '  - label_res      - label individual residues in selection\n'
          '  - get_reslist    - get dictionary containing all residues in selection\n'
          '  - print_reslist  - print ugly, CSV list of all residues in selection\n'
          '  - carbon_color   - set non-carbons in selection to normal colors, carbons in\n'
          '                     selection set to specified color\n'
          '  - list_colors    - list valid PyMol colors\n'
          '  - mappotential   - quickly map APBS electrostatic potential from DX file onto\n'
          '                     surface of object\n'
          '\n  To get detailed help info, type \'help {command}\'\n'
          '  To print this list again, type \'help docktools\'\n')


# extend #######################################################################
cmd.extend('dockview', dockview)
cmd.extend('show_hb_in_sel', show_hb_in_sel)
cmd.extend('show_hb_da', show_hb_da)
cmd.extend('hide_np_hyd', hide_np_hyd)
cmd.extend('hide_np_res', hide_np_res)
cmd.extend('hide_bbn', hide_bbn)
cmd.extend('show_bbn', show_bbn)
cmd.extend('label_res', label_res)
cmd.extend('get_reslist', get_reslist)
cmd.extend('print_reslist', print_reslist)
cmd.extend('mappotential', mappotential)
cmd.extend('load_bgf', load_bgf)
cmd.extend('load_sph', load_sph)
cmd.extend('list_colors', list_colors)
cmd.extend('carbon_color', carbon_color)
cmd.extend('docktools', docktools_help)
docktools_help()
