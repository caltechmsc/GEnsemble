#!/usr/bin/perl
#
# a utility that reads .bgf file and writes the delphi files needed to
# calculate solvation energies (one -vac and one -h2o file).
#
# usage:
#
# bgf2delphi.pl file.bgf
#
# KBr 5/12/97
#======================================================================
# jaw - modified for use in mscdock 7-27-06
#======================================================================

$bgffile = $ARGV[0];
chop($bgffile);
chop($bgffile);
chop($bgffile);
chop($bgffile);
open(PDB, ">$bgffile.pdb") ||
                die "Can't open a .pdb file in this directory\n"; 
open(CRG, ">$bgffile.crg") ||
                die "Can't open a .crg file in this directory\n"; 
open(SIZ, ">$bgffile.siz") ||
                die "Can't open a .siz file in this directory\n"; 
open(PRM1, ">$bgffile.prm.vac") ||
                die "Can't open a .prm-vac file in this directory\n"; 
open(PRM2, ">$bgffile.prm.h2o") ||
                die "Can't open a .prm-h2o file in this directory\n";

#now have to write the .prm files and the headers for the rest
#all the defaults have been set from biograf outputs

# ==================== file.prm-vac ===========================

print PRM1 "scale=2.0\n";
print PRM1 "prbrad=1.4\n";
print PRM1 "perfil=80.0\n";
print PRM1 "indi=1.0\n";
print PRM1 "exdi=1.0\n";
print PMR1 "maxc=0.0001\n";
print PMR1 "linit=1000";
print PRM1 "bndcon=4\n";
print PRM1 "salt=0.0\n";
print PRM1 "in(pdb,file=\"$bgffile.pdb\")\n";
print PRM1 "in(crg,file=\"$bgffile.crg\")\n";
print PRM1 "in(siz,file=\"$bgffile.siz\")\n";
print PRM1 "energy(s,c)\n";
close PRM1;

# ===================== file.prm-h2o ===============================

print PRM2 "scale=2.0\n";
print PRM2 "prbrad=1.4\n";
print PRM2 "perfil=80\n";
print PRM2 "indi=1.0\n";
print PRM2 "exdi=78.2\n";
print PRM2 "bndcon=4\n";
print PRM2 "salt=0.0\n";
print PRM2 "in(pdb,file=\"$bgffile.pdb\")\n";
print PRM2 "in(crg,file=\"$bgffile.crg\")\n";
print PRM2 "in(siz,file=\"$bgffile.siz\")\n";
print PRM2 "energy(s,c)\n";
close PRM2;

# ===================== file.pdb =========================

print PDB "HEADER\n";

# ===================== file.crg =========================

print CRG "atom__resnumbc_charge_\n";

# ===================== file.siz =========================

print SIZ "atom__res_radius_color_\n";

# ========================================================

while (<>) {
        if (/^ATOM/ || /^HETATM/) {
        $atomnum = substr($_, 7, 5);
        $atomlabel = substr($_, 13, 4);
        $resname = substr($_, 19, 3);
        $chain = substr($_, 23, 1);
        $resnumber = substr($_, 25, 4);
        $xcoord = substr($_, 31, 9);
        $ycoord = substr($_, 41, 9);
        $zcoord = substr($_, 51, 9);
        $fftype = substr($_, 61, 5);
        $nmbond = substr($_, 68, 1);
        $nmhydrogen = substr($_, 70, 1);
        $charge = substr($_, 72, 8);
        $fix_or_move = substr($_, 81, 1);
        $mass_correct = substr($_, 85, 1);
        $correct_mass = substr($_, 87, 9);
# have now read in all the important data
# next have to write the stuff to three files; .siz, .crg and .pdb

# format for PDB file
        $atomnum = sprintf("%4d", $atomnum);
        $atomlabel = sprintf("%4s", $atomlabel);
        $resnumber = sprintf("%4d", $resnumber);
        $x = sprintf("%8.3f", $xcoord);
        $y = sprintf("%8.3f", $ycoord);
        $z = sprintf("%8.3f", $zcoord);

print PDB "ATOM   $atomnum $atomlabel $resname $chain$resnumber    $x$y$z\n";

# format for CRG file

        $charge = sprintf("%10.6f", $charge);

print CRG "$atomlabel  $resname$resnumber$chain $charge\n";

# format for SIZ file

        $element = sprintf("%5s", $fftype);
           
if ($element =~ H_   ) {
        $radius = 1.5975;
        }elsif ($element =~ H___A) {
        $radius = 1.5975;
        }elsif ($element =~ H___b) {
        $radius = 1.5975;
        }elsif ($element =~ C_34 ) {
        $radius = 2.1185;
        }elsif ($element =~ C_33 ) {
        $radius = 2.0762;
        }elsif ($element =~ C_32 ) {
        $radius = 2.03385;
        }elsif ($element =~ C_31 ) {
        $radius = 1.9;
        }elsif ($element =~ C_3  ) {
        $radius = 1.94915;
        }elsif ($element =~ C_22 ) {
        $radius = 2.03385;
        }elsif ($element =~ C_21 ) {
        $radius = 1.9915;
        }elsif ($element =~ C_2  ) {
        $radius = 1.94915;
        }elsif ($element =~ C_R2 ) {
        $radius = 2.03385;
        }elsif ($element =~ C_R1 ) {
        $radius = 2.115;
        }elsif ($element =~ C_R  ) {
        $radius = 1.94915;
        }elsif ($element =~ C_1  ) {
        $radius = 1.9915;
        }elsif ($element =~ N_33 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_32 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_31 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_3  ) {
        $radius = 1.83105;
        }elsif ($element =~ N_22 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_21 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_2  ) {
        $radius = 1.83105;
        }elsif ($element =~ N_R2 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_R1 ) {
        $radius = 1.83105;
        }elsif ($element =~ N_R  ) {
        $radius = 1.83105;
        }elsif ($element =~ N_1  ) {
        $radius = 1.83105;
        }elsif ($element =~ O_32 ) {
        $radius = 1.7023;
        }elsif ($element =~ O_31 ) {
        $radius = 1.7023;
        }elsif ($element =~ O_3  ) {
        $radius = 1.7023;
        }elsif ($element =~ O_2  ) {
        $radius = 1.7023;
        }elsif ($element =~ O_R1 ) {
        $radius = 1.7023;
        }elsif ($element =~ O_R  ) {
        $radius = 1.7023;
        }elsif ($element =~ O_1  ) {
        $radius = 1.7023;
        }elsif ($element =~ F_   ) {
        $radius = 1.736;
        }elsif ($element =~ Al3  ) {
        $radius = 2.195;
        }elsif ($element =~ Si3  ) {
        $radius = 2.135;
        }elsif ($element =~ P_3  ) {
        $radius = 2.075;
        }elsif ($element =~ P_4  ) {
        $radius = 2.075;
        }elsif ($element =~ S_31 ) {
        $radius = 2.015;
        }elsif ($element =~ S_3  ) {
        $radius = 2.015;
        }elsif ($element =~ S_4  ) {
        $radius = 2.015;
        }elsif ($element =~ S_2  ) {
        $radius = 2.015;
        }elsif ($element =~ Cl   ) {
        $radius = 1.97515;
        }elsif ($element =~ Ga3  ) {
        $radius = 2.195;
        }elsif ($element =~ Ge3  ) {
        $radius = 2.135;
        }elsif ($element =~ As3  ) {
        $radius = 2.075;
        }elsif ($element =~ Se3  ) {
        $radius = 2.015;
        }elsif ($element =~ Br   ) {
        $radius = 1.975;
        }elsif ($element =~ In3  ) {
        $radius = 2.295;
        }elsif ($element =~ Sn3  ) {
        $radius = 2.235;
        }elsif ($element =~ Sb3  ) {
        $radius = 2.175;
        }elsif ($element =~ Te3  ) {
        $radius = 2.115;
        }elsif ($element =~ I_   ) {
        $radius = 2.075;
        }elsif ($element =~ Na   ) {
        $radius = 1.572;
        }elsif ($element =~ Ca   ) {
        $radius = 1.736;
        }elsif ($element =~ Ti   ) {
        $radius = 2.27;
        }elsif ($element =~ Fe   ) {
        $radius = 2.27;
        }elsif ($element =~ Zn   ) {
        $radius = 2.27;
        }elsif ($element =~ Tc   ) {
        $radius = 2.27;
        }elsif ($element =~ Ru   ) {
        $radius = 2.27;
        }else {
        $radius = 1.5100;
        }
$radius = sprintf("%10.6f", $radius);
print SIZ "$atomlabel  $resname $radius\n";

        }
}
print PDB "END\n";
close PDB;
close SIZ;
close CRG;

