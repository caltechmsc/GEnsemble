#!/usr/bin/env perl

#####################################################################
#                                                                   #
# BiHelix (GEnsemble)                                               #
# all_bihelix_pairs.pl                                              #
# bihelixrot_scream2.pl                                             #
# combi_frombihelixsum.pl                                           #
# combihelixrot_membscream.pl                                       #
#                                                                   #
# Copyright (c) 2008                                                #
# Ravinder Abrol and William A. Goddard III                         #
# Materials and Process Simulation Center                           #
# California Institute of Technology                                #
# Pasadena, CA, USA                                                 #
# All Rights Reserved.                                              #
#####################################################################

BEGIN {
    # add these modules to @INC
    use FindBin ();
    use lib "$FindBin::Bin";
}

use Cwd;
use File::Copy;
use File::Basename;
use Getopt::Long;
use POSIX qw(ceil);
use Sys::Hostname;
use Time::Local;

$sbin = $FindBin::Bin;
$USER = getlogin || getpwuid($<);
$HOME = $ENV{HOME};
$tmpdir = "/temp1/$USER/ge_temp1";
system("mkdir -m 0755 $tmpdir >& /dev/null");
#print "$tmpdir\n";
$curdir = cwd();

GetOptions ('h|help'                 => \$help,
        'p|protfile=s'               => \$protfile,
        'c|hpcfile=s'                => \$hpcfile,
        'rdiv|rotadiv=s'             => \$rotadiv,
        'a|anglefile=s'              => \$anglefile,
        'r|rotate'                   => \$rotate,
        's|scream'                   => \$scream,
        'mp|mpsim:i'                 => \$mpsim,
        'k|keep=i'                   => \$keep,
        'j|jobid=s'                  => \$jobid,
        'm|membsolv'                 => \$membsolv);


if (defined $help)       { &help; }
if (not defined $protfile or not defined $anglefile)  { &help; }
if (defined $membsolv and not defined $hpcfile)  { &help; }


##### Read HPMCenter file to determine the number of helices #####
if (defined $hpcfile) {
open HPC, "$hpcfile"; @HPCLINES = <HPC>; close HPC;
$i = 0; foreach (@HPCLINES) { $i++; } $maxhelixnum = $i;
}

if (not defined $rotadiv) { $rotadiv = 10; }
if (not defined $keep) { $keep = 1; }

$mpsimstr = "";
if (defined $mpsim) {
    $mpsimstr = " -mp ";
    if ($mpsim > 0) {
        $mpsimstr = " -mp $mpsim ";
    }
}

( $protprefix, $path, $suffix ) = fileparse( $protfile, qr/\.[^.]*/ );
 if ($path || $suffix) {}; # Avoid warning

if (defined $jobid) {
$unique = $jobid;
} else {
$unique = `date +%Y%m%d.%H%M%S.%N`;
chomp $unique;
}
$projdir = $protprefix . "_combihelixrot_" . $unique;

mkdir("$tmpdir", 0755) unless (-d "$tmpdir");
mkdir("$tmpdir/$projdir", 0755) unless (-d "$tmpdir/$projdir");

$workdir = "$tmpdir" . "\/" . "$projdir";
print "$projdir\n";
print "$workdir\n";
print "$protfile\n";

system("cp $protfile $workdir/protein.bgf");
if (defined $hpcfile) { system("cp $hpcfile $workdir/hpcenter.dat"); }
system("cp $anglefile $workdir/my_combiangles.dat");

chdir("$workdir") || die "Cannot chdir to ($!)";

#ROTATE
    if ($rotate || $scream || $membsolv) {
    # ROTATE each helix by the angles specified in my_combiangles.dat
        print "Generating the combinatorial set of helix rotations now ...\n";
        $rotdir = "rotate_combi";
        mkdir("$rotdir", 0755);
        system("cp protein.bgf hpcenter.dat my_combiangles.dat $rotdir");
        chdir("$rotdir") || die "Cannot chdir to ($!)";
        print "I am here in $rotdir\n";
        system("$sbin/gen_combirotations.csh protein.bgf $protprefix my_combiangles.dat $sbin");
        system("rm -f protein.bgf hpcenter.dat my_combiangles.dat hel*.deg");
        system("rm -f ini.*");
        chdir("..");  
    }

#SCREAM
    if ($scream) {
    # SCREAM each structure generated from previous step
        print "Running scream now ...\n";
        $screamdir = "scream_combi";
        mkdir("$screamdir", 0755);
        system("cp $rotdir/*combirot.bgf $screamdir");
        system("cp hpcenter.dat $screamdir");
        chdir("$screamdir") || die "Cannot chdir to ($!)";
        print "I am here in $screamdir\n";
        if (defined $mpsim) {
        system("$sbin/scream_all_bgfs.pl -rdiv $rotadiv $mpsimstr");
        } else {
        system("$sbin/scream_all_bgfs.pl -rdiv $rotadiv");
        }
        system("rm -f *combirot.bgf");
        if (-e "core.*") {
            system("rm -f core.*");
            print "WARNING: Deleted core files from SCREAM directory.\n";
            print "WARNING: Check results to make sure they exist.\n";
        }
        chdir("..");
    }

#MembSOLV
    if ($membsolv) {
    # MembSOLV each structure from previous step
        print "Running membsolv now ...\n";
        $msdir = "membsolv_combi";
        mkdir("$msdir", 0755);
        if ($scream) {
            if (-e "*scream.min.bgf*") {
                system("cp $screamdir/*scream.min.bgf $msdir");
            } else {
                system("cp $screamdir/*scream.bgf $msdir");
            }
        } else {
            system("cp $rotdir/*combirot.bgf $msdir");
        }
        system("cp hpcenter.dat $msdir");
        chdir("$msdir") || die "Cannot chdir to ($!)";
        print "I am here in $msdir\n";
        system("$sbin/membsolv_all_bgfs.pl hpcenter.dat");
#       system("rm -f *combirot.bgf");
#       system("rm -f *scream.bgf");
        chdir("..");
    }

if (defined $scream) {system("$sbin/annex/get_scream_output_combi.pl $protprefix"); }
if (defined $mpsim) {system("$sbin/annex/get_mpsim_output_combi.pl $protprefix");}

$iscream=0;
if ($scream) { $iscream=1; }
if ($membsolv) {system("$sbin/annex/get_membsolv_output_combi.pl $protprefix $iscream");}

#zip mostly everything
if ($rotate || $scream || $membsolv) { system("gzip -r $rotdir/*"); }
if ($scream)   { system("gzip -r $screamdir/*"); }
if ($membsolv) { system("gzip -r $msdir/*"); }
if ($keep == 0) {
    system("mv -f $screamdir/*scream.bgf.gz .");
    system("mv -f $screamdir/*scream.min.bgf.gz .");
    system("rm -f protein.bgf");
    system("rm -rf $rotdir $screamdir $msdir");
}

chdir("$curdir");
system("cp -r -p $workdir/* .");
system("rm -rf $workdir");
system("touch _combihelix_done_");


sub help {
    $help_message = "
                      Adam-style Script Info
Program:
 :: combihelixrot_membscream.pl

Location:
 :: \$ge_path/programs/bihelixrot2/combihelixrot_membscream.pl

Release:
 :: Version 1.1 (25 April 2008)

Authors:
 :: Ravi Abrol (abrol\@wag.caltech.edu)
 :: Jenelle Bray (Nonpolar Solvation and Final Analysis Scripts)
 :: Amy Guili (Final Analysis Scripts)

Usage:
 :: combihelixrot_membscream.pl -p {protein_bgf_file} -c {hydrophobic center file} -rdiv {rotamer diversity} -a {combinatorial_rotation_angle_data_file} -r -s -m -mp {min steps} -k {0 or 1} -j {jobid or jobtag}

GetOptions ('h|help'                 => \$help,
        'p|protfile=s'               => \$protfile,
        'c|hpcfile=s'                => \$hpcfile,
        'rdiv|rotadiv=s'             => \$rotadiv,
        'a|anglefile=s'              => \$anglefile,
        'r|rotate'                   => \$rotate,
        's|scream'                   => \$scream,
        'mp|mpsim:i'                 => \$mpsim,
        'k|keep=i'                   => \$keep,
        'j|jobid=s'                  => \$jobid,
        'm|membsolv'                 => \$membsolv);

Options:
 :: -h | --help             :: Optional    :: No Input
 :: Prints this help message.

 :: -p | --protfile         :: Required    :: Filename
 :: This is the protein BGF file

 :: -c | --hpcfile          :: Optional    :: Filename
 :: This is the file with hydrophobic centers in format
 :: HELIX1 45.30
 :: HELIX2 84.86
 :: ...
 :: ...

 :: -rdiv | --rotadiv       :: Optional    :: String
 :: Scream rotamer library diversity to use.
 :: To use 0.5A library, set this flag to 05
 :: To use 2.0A library, set this flag to 20
 :: Default value is 10 (corresponding to 1.0A library)
 :: Allowed range 01 ... 50

 :: -a | --anglefile        :: Required    :: Filename
 :: This is the file containing the angles for each Helix
 :: to generate the combinatorial set of structures.
 :: An example anglefile that will generate 96 combinations:
 :: (First line corresponds to helix1 choices, second line
 :: corresponds to helix2 choices and so on. Also we have
 :: retired negative angles as they cause confusion in
 :: file names)
    0 30
    0 90
    30 180
    0
    0 60 300
    90 210
    30 330

 :: -r | --rotate           :: Optional    :: No Input
 :: Specify this option, if you only want to generate
 :: structure files corresponding to angles specified
 :: in the file given as an input to the -a option above.

 :: -s | --scream           :: Optional    :: No Input
 :: Using this option will enable the -r option and
 :: then perform SCREAM on each of the rotated structures.

 :: -m | --membsolv         :: Optional    :: No Input
 :: Using this option will enable the -r option and
 :: then perform MembSOLV on each of the rotated structures.

 :: -mp | --mpsim            :: Optional    :: No Input
 :: Use this option to evaluate MPSim energies for SCREAMed structures.
 :: Provide an interger number as input to perform that many minimization
 :: steps using MPSim.

 :: -k | --keep             :: Optional    :: Integer
 :: Allowed values: 0 (Only keep minimal files necessary)
 ::                 1 (Keep everything: Default Mode)

 :: -j | --jobid            :: Optional    :: String
 :: Allows you specify a name/number as a tag for your job
 :: When this script is called by the main combihelix script
 :: in batch mode then this corresponds to the actual jobid in queue.

Description:
 :: This wrapper script sets up the combinatorial helix rotational
 :: MembSCREAM step, where each helix is rotated simultaneously
 :: by angles provided as an input by the user to generate a
 :: combinatorial set. This is followed by a full side-chain
 :: optimization using SCREAM and an implicit membrane solvation
 :: calculation using MembSOLV.

Output:
 :: ALL ENERGIES in kcal/mol.
 ::
 :: SCREAM output (proteinprefix_combirot_scream.out):
 ::  H1  H2  H3  H4  H5  H6  H7      Intern       V_fsc     Vtot_fm    CHtot_fm      Tot_fm      V_scsc     CH_scsc    Tot_scsc   Total(Ep)
 ::   0  30   0   0   0   0  90      1515.3        -2.4      -317.6      -297.6       900.0     26140.5       -15.0     26125.5     27025.5
 ::   0  30   0   0   0   0 150      1532.5       -24.9      -344.2      -297.5       890.8     19971.0        -8.7     19962.3     20853.2
 ::   0 120   0   0   0   0  90      1567.6       -12.3      1429.0      -302.5      2694.1     28850.8       -27.0     28823.8     31517.9
 ::   0 120   0   0   0   0 150      1583.7       -34.9      1391.3      -304.1      2670.8     19608.7       -18.5     19590.2     22261.0
 :: Intern: Valence energy terms of the SCREAMed residues.
 :: V_fsc=van der Waals energy between SCREAMed residue sidechains and fixed residue sidechains.
 :: Vtot_fm= V_fsc + van der Waals energy between SCREAMed residue sidechains and all backbones.
 :: CHtot_fm=Coulomb and HBond energy between fixed residues and SCREAMed residue sidechains.
 :: Tot_fm=Intern+V_fsc+Vtot_fm+CHtot_fm
 :: V_scsc=van der Waals energy among SCREAMed residue sidechains.
 :: CH_scsc=Coulomb and HBond energy among SCREAMed residue sidechains.
 :: Tot_scsc=V_scsc+CH_scsc
 :: Ep=Total=Tot_fm+Tot_scsc=Total interaction energy involving SCREAMed residues.
 ::
 :: MembSOLV output (proteinprefix_combirot_membsolv.out):
 ::   H1  H2  H3  H4  H5  H6  H7   PolMemb5(E1)   PolWater(E2)   NonPolar(E3)   E1-E2+E3(Es)
 ::    0  30   0   0   0   0  90         -453.8         -527.2         -170.6          -97.1
 ::    0  30   0   0   0   0 150         -450.7         -531.2         -171.8          -91.3
 ::    0 120   0   0   0   0  90         -415.9         -500.1         -171.2          -87.1
 ::    0 120   0   0   0   0 150         -414.1         -504.9         -172.5          -81.7
 :: Each line corresponds to one protein conformation comprising of rotation angles given by
 :: the first seven columns for seven helices respectively.
 :: E1=Polar solvation energy of the protein in a multi-dielectric (80|7|2|7|80)
 ::    implicit membrane.
 :: E2=Polar solvation energy of the protein in implicit bulk water.
 :: E3=NonPolar solvation free energy change corresponding to transfer of
 ::    protein from implicit bulk water to multi-dielectric (80|7|2|7|80)
 ::    implicit membrane, approximated as Gamma*Lipidexposed_SASA.
 :: Es=E1-E2+E3=Total Solvation Free Energy change associated with transfer of
 ::    protein from implicit bulk water to multi-dielectric (80|7|2|7|80)
 ::    implicit membrane.

Timing:
 :: Allow about 4-5 minutes per angle combination on borg or matrix
 :: for SCREAM and MembSOLV combined.

Usage (repeated):
 :: combihelixrot_membscream.pl -p {protein_bgf_file} -c {hydrophobic center file} -rdiv {rotamer diversity} -a {combinatorial_rotation_angle_data_file} -r -s -m -mp {min steps} -k {0 or 1} -j {jobid or jobtag}

";
    die $help_message;
}
