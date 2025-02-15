#!/usr/bin/env perl

use warnings;
use FindBin ();
use lib "$FindBin::Bin";
use Cwd;
use File::Copy;
use File::Basename;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;
use Math::Trig;
use myMath::VectorReal qw(:all);
use myMath::MatrixReal qw(:all);
use utils::Template;
use inout::readpdb_bbcoord;

my $sbin = $FindBin::Bin;

GetOptions ('h|help'                 => \$help,
        'm|mftafile=s'               => \$mftafile,
        'p|pdbfile=s'                => \$pdbfile,
        'nt|nter=s'                  => \$nter,
        'zo|zout=s'                  => \$zout,
        'tmo|tmatorigin=i'           => \$tmatorigin,
        'tmx|tmalongx=i'             => \$tmalongx);

# check command line options
if ($help)       { &help; }
if ((not defined $mftafile) and (not defined $pdbfile))  { &help; }
if (!$mftafile) { die "specify the modified fasta file with xtal TMs\n"; }
if (!$pdbfile) { die "specify the pdb file containing the z=0 aligned protein\n"; }

#Makes N-terminal point out of the cell by default (e.g., GPCRs)
if (not defined $nter) {
$nter = 'out';
}
if (($nter ne 'out') and ($nter ne 'in')) { die "specify in or out for nter\n"; }

# Makes the outside of the cell as +z direction from lipid middle by default
if (not defined $zout) {
$zout = 'plus';
}
if (($zout ne 'plus') and ($zout ne 'minus')) { die "specify plus or minus for zout\n"; }

# Translate the bundle so that helical axis of a specified helix (tmatorigin)
# passes through origin.
# If a zero value is given then make origin the geometric center of
# intersection points of all helical axes with the z=0 plane.
# If a negative value is given, then don't do any alignment.

if (not defined $tmatorigin) {
$tmatorigin=3; # Useful for Class A GPCRs as TM3 is in the middle
}


# Once the origin is set, rotate the helical bundle in x-y plane such that
# the axis of a specified helix (tmalongx) passes through the x-axis.
# If a negative value is given, then don't do any alignment.
if (not defined $tmalongx) {
    $tmalongx=2; # Useful convention for Class A GPCRs 
}

if (($tmatorigin == $tmalongx) && ($tmatorigin > 0)) {
die "Specify different TM helices for positioning at origin and along x-axis\n";
}

open (MFTA, "<$mftafile");
my @mfta = <MFTA>;
close (MFTA);

# Make sure that tmatorigin and tmalongx are within range
$helixid = 0;
foreach my $mftaline (@mfta) {
    if ($mftaline =~ /\* / && $mftaline =~/tm /) { $helixid++;}
}
my $numtms = $helixid;
if ($tmatorigin > $numtms) { die "Specify TM at origin <= $numtms\n"; }
if ($tmalongx > $numtms) { die "Specify TM along x-axis <= $numtms\n"; }

my @tmid =();
my @begintm =();
my @endtm =();
my @etares =();
my @etaresid =();
my @tmhpc=();
my @tmx=();
my @tmy=();
my @tmtheta=();
my @tmphi=();
my @tmeta=();
my $natoms;
my @num_bbatoms=();
my @bbatom_mass=();
my @bbatom_x=();
my @bbatom_y=();
my @bbatom_z=();
my @bbatom_resid=();
my @bbatom_name=();
my @bundle_bbatom_mass=();
my @bundle_bbatom_x=();
my @bundle_bbatom_y=();
my @bundle_bbatom_z=();
my @bundle_bbatom_resid=();
my @bundle_bbatom_name=();
my $bundlex = 0;
my $bundley = 0;
my ($i,$j,$k,$dum1,$dum2,$dum3,$dum4,$dum5,$dum6,$dum7,$dum8,$dumx,$dumy,$dumz);


# MAIN LOOP
# Get template information for each TM in the .mfta file
my $helixid = 0;
foreach my $mftaline (@mfta) {
    if ($mftaline =~ /\* / and $mftaline =~ /tm /) {
        $helixid++;
        $i = $helixid;

        # get TM information
        ($dum1,$tmid[$i],$begintm[$i],$endtm[$i],$dum2,$dum3,$dum4,$dum5,$dum6,$dum7,$etares[$i],$etaresid[$i],$dum8) = split /\ +/, $mftaline;

        # read backbone pdb coordinates for that TM
        ($natoms,$bbatom_mass_ref,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref,$bbatom_resid_ref,$bbatom_name_ref) = readpdb_bbcoord($pdbfile,$begintm[$i],$endtm[$i],$nter,$zout);
        $num_bbatoms[$i]=$natoms;

        my @bbatom_mass=@{$bbatom_mass_ref};
        my @bbatom_x=@{$bbatom_x_ref};
        my @bbatom_y=@{$bbatom_y_ref};
        my @bbatom_z=@{$bbatom_z_ref};
        my @bbatom_resid=@{$bbatom_resid_ref};
        if ($helixid == 3) {
        for ($j=0;$j<$natoms;$j++) {
#           printf '%8.4f %8.2f %8.2f %8.2f',$bbatom_mass[$j],$bbatom_x[$j],$bbatom_y[$j],$bbatom_z[$j];
#           print "\n";
        }
        }
        my @bbatom_name=@{$bbatom_name_ref};
        push(@bundle_bbatom_mass,\@bbatom_mass);
        push(@bundle_bbatom_x,\@bbatom_x);
        push(@bundle_bbatom_y,\@bbatom_y);
        push(@bundle_bbatom_z,\@bbatom_z);
        push(@bundle_bbatom_resid,\@bbatom_resid);
        push(@bundle_bbatom_name,\@bbatom_name);

        # calculate positions and tilts for that TM
        ($tmx[$i],$tmy[$i],$tmhpc[$i],$tmtheta[$i],$tmphi[$i],$tmeta[$i]) = Template($num_bbatoms[$i],\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z,\@bbatom_resid,\@bbatom_name,$i,$etaresid[$i],$nter,$zout);

    $bundlex += $tmx[$i];
    $bundley += $tmy[$i];
    }
}
# END of MAIN LOOP
@bbatom_x=();
@bbatom_y=();
@bbatom_z=();
@bbatom_mass=();
@bbatom_resid=();
@bbatom_name=();

#print "reached here 1\n";
$bundlex = $bundlex/$numtms;
$bundley = $bundley/$numtms;


#for ($i=1;$i<=$numtms;$i++) {
#    $helixid=$i;
#    printf '%3d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f', $helixid,$tmhpc[$helixid],$tmx[$helixid],$tmy[$helixid],$tmtheta[$helixid],$tmphi[$helixid],$tmeta[$helixid];
#    print "\n";
#}
#print "Geometric center of the bundle: $bundlex $bundley 0.0\n";
# Translate the geometric center or tmatorigin to origin
if ($tmatorigin == 0) {
    for ($i=1;$i<=$numtms;$i++) {
        $tmx[$i] -= $bundlex;
        $tmy[$i] -= $bundley;
        for ($j=0;$j<$num_bbatoms[$i];$j++) {
        $bundle_bbatom_x[$i-1][$j] = $bundle_bbatom_x[$i-1][$j] - $bundlex;
        $bundle_bbatom_y[$i-1][$j] = $bundle_bbatom_y[$i-1][$j] - $bundley;
        }
    $helixid=$i;
#    printf '%3d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f', $helixid,$tmhpc[$helixid],$tmx[$helixid],$tmy[$helixid],$tmtheta[$helixid],$tmphi[$helixid],$tmeta[$helixid];
#    print "\n";
    }
} elsif ($tmatorigin > 0) {
    $dumx = $tmx[$tmatorigin];
    $dumy = $tmy[$tmatorigin];
    for ($i=1;$i<=$numtms;$i++) {
        $tmx[$i] -= $dumx;
        $tmy[$i] -= $dumy;
        for ($j=0;$j<$num_bbatoms[$i];$j++) {
        $bundle_bbatom_x[$i-1][$j]=$bundle_bbatom_x[$i-1][$j]-$dumx;
        $bundle_bbatom_y[$i-1][$j]=$bundle_bbatom_y[$i-1][$j]-$dumy;
        }
    $helixid=$i;
#    printf '%3d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f', $helixid,$tmhpc[$helixid],$tmx[$helixid],$tmy[$helixid],$tmtheta[$helixid],$tmphi[$helixid],$tmeta[$helixid];
#    print "\n";
    }
}

# rotate the bundle to align tmalongx TM along x-axis
my $cosrefang=1.0;
my $sinrefang=0.0;

if ($tmalongx > 0) {
    my $refangr = atan2($tmy[$tmalongx],$tmx[$tmalongx]);
    if ($refangr < 0.0) { $refangr = 2*pi+$refangr; }
    my $refangd=rad2deg($refangr);
#    print "$refangd\n";
    $cosrefang=cos($refangr);
    $sinrefang=sin($refangr);
}

my $rmvecx = vector($cosrefang,-$sinrefang,0.0);
my $rmvecy = vector($sinrefang,$cosrefang,0.0);
my $rmvecz = vector(0.0,0.0,1.0);

# rotation matrix.
# Each of the three arguments to vector_matrix should be row vectors.
my $rmat = vector_matrix( $rmvecx, $rmvecy, $rmvecz );

for ($i=1;$i<=$numtms;$i++) {
    my $scoord = vector($tmx[$i],$tmy[$i],0.0);
    my $rcoord = $scoord * $rmat;
    $tmx[$i]=$rcoord . X;
    $tmy[$i]=$rcoord . Y;
    for ($j=0;$j<$num_bbatoms[$i];$j++) {
        my $scoord = vector($bundle_bbatom_x[$i-1][$j],$bundle_bbatom_y[$i-1][$j],$bundle_bbatom_z[$i-1][$j]);
        my $rcoord = $scoord * $rmat;
        $bundle_bbatom_x[$i-1][$j] = $rcoord . X;
        $bundle_bbatom_y[$i-1][$j] = $rcoord . Y;
        $bundle_bbatom_z[$i-1][$j] = $rcoord . Z;
    }
    $helixid=$i;
#    printf '%3d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f', $helixid,$tmhpc[$helixid],$tmx[$helixid],$tmy[$helixid],$tmtheta[$helixid],$tmphi[$helixid],$tmeta[$helixid];
#    print "\n";
}

#print "reached here 2\n";
# recalculate the tilts and centers
for ($i=1;$i<=$numtms;$i++) {
    $helixid=$i;
    for ($j=0;$j<$num_bbatoms[$i];$j++) {
        $bbatom_x[$j]=$bundle_bbatom_x[$i-1][$j];
        $bbatom_y[$j]=$bundle_bbatom_y[$i-1][$j];
        $bbatom_z[$j]=$bundle_bbatom_z[$i-1][$j];
        $bbatom_resid[$j]=$bundle_bbatom_resid[$i-1][$j];
        $bbatom_name[$j]=$bundle_bbatom_name[$i-1][$j];
        $bbatom_mass[$j]=$bundle_bbatom_mass[$i-1][$j];
        }
    # calculate positions and tilts for that TM
        ($tmx[$i],$tmy[$i],$tmhpc[$i],$tmtheta[$i],$tmphi[$i],$tmeta[$i]) = Template($num_bbatoms[$i],\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z,\@bbatom_resid,\@bbatom_name,$i,$etaresid[$i],$nter,$zout);
     printf '*%3dtmpl %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %4s%5d', $helixid,$tmx[$helixid],$tmy[$helixid],$tmhpc[$helixid],$tmtheta[$helixid],$tmphi[$helixid],$tmeta[$helixid],$etares[$i],$etaresid[$i];
     print "\n";
}
    print "* TM          X        Y       HPC     Theta      Phi      Eta    EtaRes\n";



sub help {
    $help_message = "
                      Adam-style Script Info
Program:
 :: GetTemplate.pl

Location:
 :: /project/Biogroup/Software/GEnsemble/programs/templates/OPM/GetTemplate.pl

Release:
 :: Version 1.0 (17 Jan 2008)

Authors:
 :: Ravi Abrol (abrol\@wag.caltech.edu)

Usage:
 :: GetTemplate.pl -m {mftafile} -p {pdbfile}

GetOptions ('h|help'                 => \$help,
        'm|mftafile=s'               => \$mftafile,
        'p|pdbfile=s'                => \$pdbfile,
        'nt|nter=s'                  => \$nter,
        'zo|zout=s'                  => \$zout,
        'tmo|tmatorigin=i'           => \$tmatorigin,
        'tmx|tmalongx=i'             => \$tmalongx);

 :: -h | --help             :: Optional    :: No Input
 :: Prints this help message.


Usage (repeated):
 :: GetTemplate.pl -m {mftafile} -p {pdbfile}

";
    die $help_message;
}
