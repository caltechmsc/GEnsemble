#!/usr/bin/perl

use File::Copy;
use Getopt::Long;

### What the program does
# 1) a) Get Energy of BGF Pair
#    b) (Optional) Minimize BGF Pair and Get Energy of BGF Pair
# 2) Split pair
# 3) Get Energy of Helix A
# 4) Get energy of Helix B
# 5) Report Energies

if (@ARGV == 0) { help(); }

#$ff          = "/project/Biogroup/FF/dreiding-0.3.par";
#$runMPSim    = "/ul/caglar/Perl/runMPSim.pl";
#$playWithBGF = "/project/Biogroup/scripts/playWithBGF/playWithBGF";

GetOptions ('h|help'        => \$help,
            'b|bgf=s'       => \$bgf_input,
	    'pwb=s'         => \$playWithBGF,
	    'mpsim=s'       => \$runMPSim,
	    'ff=s'          => \$ff,
	    's|steps=i'     => \$steps);

if ($help) { help() }

`touch tic`;
#################################################################
##### AB
#################################################################
copy("$bgf_input","AB.bgf");

if ($steps > 0) {
    `$runMPSim AB.bgf -f $ff -s $steps minvac`;
    unlink "AB_minvac.ctl";
    unlink glob "AB_minvac.snap*";
    unlink "AB_minvac.traj1";
    unlink "AB.bgf";
    move("AB_minvac.fin.bgf","AB.bgf");
    move("AB_minvac.out","AB_oneEvac.out");
} else {
    `$runMPSim AB.bgf -f $ff oneEvac`;
    unlink "AB_oneEvac.ctl";
    unlink "AB_oneEvac.traj1";
}

#################################################################
##### A / B
#################################################################
`$playWithBGF AB.bgf -c A -o A.bgf`;
`$runMPSim A.bgf -f $ff oneEvac`;
unlink "A_oneEvac.ctl";
unlink "A_oneEvac.traj1";
unlink "A.bgf";


`$playWithBGF AB.bgf -c B -o B.bgf`;
`$runMPSim B.bgf -f $ff oneEvac`;
unlink "B_oneEvac.ctl";
unlink "B_oneEvac.traj1";
unlink "B.bgf";

unlink "AB.bgf";

#################################################################
##### Energies
#################################################################

open ENG, "AB_oneEvac.out";
while (<ENG>) {
    if (/TOTAL ENERGY = (\S+)/) {
	$energy{AB}{total} = $1;
    } elsif (/Bonds      :\s+(\S+)\s+Nonbond     :\s+(\S+)/) {
	$energy{AB}{bonds}   = $1;
	$energy{AB}{nonbond} = $2;
    } elsif (/Angles     :\s+(\S+)\s+Coulomb     :\s+(\S+)/) {
	$energy{AB}{angles}  = $1;
	$energy{AB}{coulomb} = $2;
    } elsif (/Torsion    :\s+(\S+)\s+VDW         :\s+(\S+)/) {
	$energy{AB}{torsion} = $1;
	$energy{AB}{vdw}     = $2;
    } elsif (/Inversions :\s+(\S+)\s+Hbonds      :\s+(\S+)/) {
	$energy{AB}{inversions} = $1;
	$energy{AB}{hbonds}     = $2;
    }
}
close ENG;
unlink "AB_oneEvac.out";

open ENG, "A_oneEvac.out";
while (<ENG>) {
    if (/TOTAL ENERGY = (\S+)/) {
	$energy{A}{total} = $1;
    } elsif (/Bonds      :\s+(\S+)\s+Nonbond     :\s+(\S+)/) {
	$energy{A}{bonds}   = $1;
	$energy{A}{nonbond} = $2;
    } elsif (/Angles     :\s+(\S+)\s+Coulomb     :\s+(\S+)/) {
	$energy{A}{angles}  = $1;
	$energy{A}{coulomb} = $2;
    } elsif (/Torsion    :\s+(\S+)\s+VDW         :\s+(\S+)/) {
	$energy{A}{torsion} = $1;
	$energy{A}{vdw}     = $2;
    } elsif (/Inversions :\s+(\S+)\s+Hbonds      :\s+(\S+)/) {
	$energy{A}{inversions} = $1;
	$energy{A}{hbonds}     = $2;
    }
}
close ENG;
unlink "A_oneEvac.out";

open ENG, "B_oneEvac.out";
while (<ENG>) {
    if (/TOTAL ENERGY = (\S+)/) {
	$energy{B}{total} = $1;
    } elsif (/Bonds      :\s+(\S+)\s+Nonbond     :\s+(\S+)/) {
	$energy{B}{bonds}   = $1;
	$energy{B}{nonbond} = $2;
    } elsif (/Angles     :\s+(\S+)\s+Coulomb     :\s+(\S+)/) {
	$energy{B}{angles}  = $1;
	$energy{B}{coulomb} = $2;
    } elsif (/Torsion    :\s+(\S+)\s+VDW         :\s+(\S+)/) {
	$energy{B}{torsion} = $1;
	$energy{B}{vdw}     = $2;
    } elsif (/Inversions :\s+(\S+)\s+Hbonds      :\s+(\S+)/) {
	$energy{B}{inversions} = $1;
	$energy{B}{hbonds}     = $2;
    }
}
close ENG;
unlink "B_oneEvac.out";

$Tot_11_Intra = $energy{A}{total};
$Tot_22_Intra = $energy{B}{total};
$TotalE_H1_H2 = $energy{AB}{total};
$Tot_12_Inter = $energy{AB}{total} - $energy{A}{total} - $energy{B}{total};

$VDW_11_Intra = $energy{A}{vdw};
$VDW_22_Intra = $energy{B}{vdw};
$TotVDW_H1_H2 = $energy{AB}{vdw};
$VDW_12_Inter = $energy{AB}{vdw} - $energy{A}{vdw} - $energy{B}{vdw};
$NoVDWE_H1_H2 = $TotalE_H1_H2 - $TotVDW_H1_H2;

$HBE_11_Intra = $energy{A}{hbonds};
$HBE_22_Intra = $energy{B}{hbonds};
$TotHBE_H1_H2 = $energy{AB}{hbonds};
$HBE_12_Inter = $energy{AB}{hbonds} - $energy{A}{hbonds} - $energy{B}{hbonds};

printf "%.2f  %.2f  %.2f  %.2f  %.2f  %.2f  %.2f  %.2f  %.2f\n",
    $Tot_11_Intra,
    $Tot_22_Intra,
    $Tot_12_Inter,
    $TotalE_H1_H2,
    $VDW_11_Intra,
    $VDW_22_Intra,
    $VDW_12_Inter,
    $NoVDWE_H1_H2,
    $HBE_12_Inter;

`touch toc`;

exit;

#################################################################
##### Help Subroutine
#################################################################

sub help {

    my $help = "
Program:
 :: BiHelix_MPSim.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: BiHelix_MPSim.pl -b {bgf file} -s {steps}

Required Input:
 :: -b | --bgf       :: Filename
 :: Single BGF file with two helices.  Helices must
 :: be chain A and B.

Optional Input:
 :: -s | --steps     :: Positive Integer
 :: Number of steps of minimization for the pair.
 :: Default is zero (no minimization).

 :: --pwb            :: Filename
 :: This is the playWithBGF executable.  Defaults to
 :: /project/Biogroup/scripts/playWithBGF/playWithBGF

 :: --mpsim          :: Filename
 :: This is the runMPSim executable.  Defaults to
 :: /ul/caglar/Perl/runMPSim.pl

 :: --ff             :: Filename
 :: Forcefield Par File.  Defaults to
 :: /project/Biogroup/FF/dreiding-0.3.par

 :: -h | --help      :: No Input
 :: Display this help information

Description:
 :: This program calculates various energies for a
 :: pair of helices in a single BGF file.  It also
 :: will optionally minimize the pair for a number
 :: of steps before calculating the energies.

 :: Output consists of 9 numbers printed to the
 :: screen, separated by spaces:
 ::   1) Tot_11_Intra
 ::   2) Tot_22_Intra
 ::   3) Tot_12_Inter
 ::   4) TotalE_H1-H2
 ::   5) VDW_11_Intra
 ::   6) VDW_22_Intra
 ::   7) VDW_12_Inter
 ::   8) NoVDWE_H1-H2
 ::   9) HBE_12_Inter

";

    die "$help";


}
