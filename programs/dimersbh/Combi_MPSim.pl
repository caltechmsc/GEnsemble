#!/usr/bin/perl

use File::Copy;
use Getopt::Long;

### What the program does
# 1) a) Get Energy of BGF
#    b) (Optional) Minimize BGF and Get Energy of minimized BGF
# 2) Report Energies

if (@ARGV == 0) { help(); }

$ff          = "/project/Biogroup/FF/dreiding-0.3.par";
$runMPSim    = "/ul/caglar/Perl/runMPSim.pl";
$playWithBGF = "/project/Biogroup/scripts/playWithBGF/playWithBGF";

GetOptions ('h|help'        => \$help,
            'b|bgf=s'       => \$bgf_input,
	    'pwb=s'         => \$playWithBGF,
	    'mpsim=s'       => \$runMPSim,
	    'ff=s'          => \$ff,
	    's|steps=i'     => \$steps);

if ($help) { help() }
copy("$bgf_input","ComBiX.bgf");
($prefix = $bgf_input) =~ s/.bgf//;

#`touch tic`;
#################################################################
##### ComBiX Non-Min
#################################################################
`$runMPSim ComBiX.bgf -f $ff oneEvac`;
unlink "ComBiX_oneEvac.ctl";
unlink "ComBiX_oneEvac.traj1";

#################################################################
##### ComBiX Min
#################################################################
if ($steps > 0) {
    `$runMPSim ComBiX.bgf -f $ff -s $steps minvac`;
    unlink "ComBiX_minvac.ctl";
    unlink glob "ComBiX_minvac.snap*";
    unlink "ComBiX_minvac.traj1";
    move ("ComBiX_minvac.fin.bgf","${prefix}.min.bgf");
}


#################################################################
##### Energies
#################################################################
# ComBiX Non-min energies
open ENG, "ComBiX_oneEvac.out";
while (<ENG>) {
    if (/TOTAL ENERGY = (\S+)/) {
	$energy{ComBiX}{nonmin}{total} = $1;
    } elsif (/Bonds      :\s+(\S+)\s+Nonbond     :\s+(\S+)/) {
	$energy{ComBiX}{nonmin}{bonds}   = $1;
	$energy{ComBiX}{nonmin}{nonbond} = $2;
    } elsif (/Angles     :\s+(\S+)\s+Coulomb     :\s+(\S+)/) {
	$energy{ComBiX}{nonmin}{angles}  = $1;
	$energy{ComBiX}{nonmin}{coulomb} = $2;
    } elsif (/Torsion    :\s+(\S+)\s+VDW         :\s+(\S+)/) {
	$energy{ComBiX}{nonmin}{torsion} = $1;
	$energy{ComBiX}{nonmin}{vdw}     = $2;
    } elsif (/Inversions :\s+(\S+)\s+Hbonds      :\s+(\S+)/) {
	$energy{ComBiX}{nonmin}{inversions} = $1;
	$energy{ComBiX}{nonmin}{hbonds}     = $2;
    }
}
close ENG;
unlink "ComBiX_oneEvac.out";

$TotalE_bundle = $energy{ComBiX}{nonmin}{total};
$HBond_bundle = $energy{ComBiX}{nonmin}{hbonds};

printf
    "%.2f %.2f\n",
    $TotalE_bundle,$HBond_bundle;

if ($steps > 0) {
    # ComBiX Min energies
    open ENG, "ComBiX_minvac.out";
    while (<ENG>) {
	if (/TOTAL ENERGY = (\S+)/) {
	    $energy{ComBiX}{min}{total} = $1;
	} elsif (/Bonds      :\s+(\S+)\s+Nonbond     :\s+(\S+)/) {
	    $energy{ComBiX}{min}{bonds}   = $1;
	    $energy{ComBiX}{min}{nonbond} = $2;
	} elsif (/Angles     :\s+(\S+)\s+Coulomb     :\s+(\S+)/) {
	    $energy{ComBiX}{min}{angles}  = $1;
	    $energy{ComBiX}{min}{coulomb} = $2;
	} elsif (/Torsion    :\s+(\S+)\s+VDW         :\s+(\S+)/) {
	    $energy{ComBiX}{min}{torsion} = $1;
	    $energy{ComBiX}{min}{vdw}     = $2;
	} elsif (/Inversions :\s+(\S+)\s+Hbonds      :\s+(\S+)/) {
	    $energy{ComBiX}{min}{inversions} = $1;
	    $energy{ComBiX}{min}{hbonds}     = $2;
	}
    }
    close ENG;
    unlink "ComBiX_minvac.out";
    
    $TotalE_bundle = $energy{ComBiX}{min}{total};
    $HBond_bundle = $energy{ComBiX}{min}{hbonds};
    
    printf
	"%.2f %.2f\n",
	$TotalE_bundle,$HBond_bundle;
}

#`touch toc`;
system("rm -f ComBiX*bgf");

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
 :: of steps.

 :: If minimization is performed, then two sets of
 :: energies are provided.  The first set of numbers
 :: is for the non-minimized structure.  The second
 :: set is for the minimized structure.

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
