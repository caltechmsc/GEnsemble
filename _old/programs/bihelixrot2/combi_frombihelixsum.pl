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


$sbin = $FindBin::Bin;
$localmach = hostname;
#$USER = getlogin || getpwuid($<);

#print "i am here 1\n";

GetOptions ('h|help'                 => \$help,
        'p|protfile=s'               => \$protfile,
        'ener|energy=s'              => \$energy,
        'e|ecriteria=i'              => \$ecriteria,
        'n|ncombi=i'                 => \$ncombi,
        'r|rotate'                   => \$rotate,
        's|scream'                   => \$scream,
        'm|membsolv'                 => \$membsolv,
        'mp|mpsim:i'                 => \$mpsim,
        'rlib|rotalib=f'             => \$rotalib,
        'd|debug'                    => \$debug,
        'mach|machine=s'             => \$machine);

#print "i am here 2\n";

#if (not defined $help && not defined $protfile && not defined $ncombi && not defined $rotate && not defined $scream && not defined $membsolv) { &help; }

#print "i am here 3\n";

if (not defined $help and not defined $protfile) { &help; }
if (defined $help) { &help; }

if (defined $machine) { $jobmode = 'parallel'; }
if (not defined $machine) {
    ($machine) = $localmach =~ /([^.]*)/;
    $jobmode = 'serial';
}
print "$jobmode\n";

if (not defined $energy) { die "Specify \"scream\" or \"mpsim-befmin\" or \"mpsim-aftmin\" for -ener \n"; }

# Set default rotamer library to be 1.0 A
if (not defined $rotalib) { $rotalib = 1.0; }

if ($rotalib < 0.1 || $rotalib > 5.0) { die "specify a value from 0.1 to 5.0\n";}

$rdiv = floor(10*$rotalib+0.5);
if ($rdiv < 10) { $rdiv = "0"."$rdiv"; }

if (defined $debug) {
    $keep = 1;
} else {
    $keep = 0;
}

print "jobmode $jobmode\n";

$action = "no";
if ($rotate || $scream || $membsolv) { $action = "yes";}

if (defined $help)       { &help; }
if (not defined $protfile)  { die "specify the protein file\n"; }
if ($action eq "no") {
    die "specify action to rotate or scream\n";
} else {
    if ($rotate) {
        $flags = "-r";
    }
    if ($scream) {
        $flags = "-r -s -k $keep";
    }
    if ($membsolv) {
        $flags = "-r -s -m -k $keep";
    }
}

$defaultsfile = "${sbin}/../.gensemble/.bihelix";
open DEF, "$defaultsfile";
while (<DEF>) {
    if (/^queuetype\s+(\S+)/)          { $queuetype         = $1; }
}
close DEF;
print "queuetype $queuetype\n";

( $protprefix, $path, $suffix ) = fileparse( $protfile, qr/\.[^.]*/ );
if ($path || $suffix) {}; # Avoid warning

open (BGF, "<$protfile");
@bgf = <BGF>;
close (BGF);

$hpcfile = "hpcenter.dat";
my ($dum1,$dum2,$dum3);
open (HPC, ">$hpcfile");
foreach $bgfline (@bgf) {
    if ($bgfline =~ /HPC HELIX/) {
	($dum1,$dum2,$dum3,$hpc) = split /\ +/, $bgfline;
	print HPC "$dum3 $hpc";
    }
}
close (HPC);

if (not defined $ecriteria) { $ecriteria = 1; }
$ename="";
if (defined $energy) { $ename = "$energy"."_"; }
if ($ecriteria < 1 || $ecriteria > 4) { die "Specify 1, 2, 3, or 4 for energy criteria\n"; }
if (not defined $ncombi) { $ncombi = 100; }

$scoringfile[1] = $protprefix . ".bihelix_${ename}TotalE.out";
$sprefix[1] = "TotalE";
$scoringfile[2] = $protprefix . ".bihelix_${ename}NoInterHelVDW.out";
$sprefix[2] = "NoInterHelVDW";
$scoringfile[3] = $protprefix . ".bihelix_${ename}NoAllVDW.out";
$sprefix[3] = "NoAllVDW";
$scoringfile[4] = $protprefix . ".bihelix_${ename}HBond.out";
$sprefix[4] = "HBond";

$unique = `date +%Y%m%d.%H%M%S`;
chomp $unique;

for ($nec=$ecriteria;$nec<=$ecriteria;$nec++) {
    if (! -e $scoringfile[$nec]) { die "$scoringfile[$nec] doesn't exist\n"; }
    
    $combidir1[$nec] = $protprefix.".CombiSCREAM_FromBiHelixSums_${ename}".$sprefix[$nec].".".$unique; 
    mkdir $combidir1[$nec];
    chdir $combidir1[$nec];
    copy("../${protfile}",${protfile});
    copy("../${hpcfile}",${hpcfile});
    copy("../$scoringfile[$nec]",$scoringfile[$nec]);
    
    $ncount=0;
    open (SCORE,$scoringfile[$nec]);
    while ($datae = <SCORE>) {
        chomp $datae;
        if ($datae =~ /\d/) {
            $ncount++;
            @datacols=split(/\s+/, $datae);
            $anglestr = $datacols[1];
            print "$anglestr\n";
            $combidir2 = $protprefix."CombiSCREAM_".$anglestr;
            mkdir $combidir2;
            chdir $combidir2;
            @angles = split("_",$anglestr);
            open (ANGS,'>>myangles.dat');
            for ($ia=0;$ia<7;$ia++) {
                print ANGS "$angles[$ia]\n";
            }
            close (ANGS);
            $subcommand = "$sbin/combihelixrot_membscream.pl -rdiv $rdiv -p ../$protfile -c ../$hpcfile -a myangles.dat $flags";
	    
	    if (defined $mpsim) {
		$subcommand = "$subcommand"."  -mp";
		if ($mpsim > 0) {
		    $subcommand = "$subcommand"." $mpsim";
		}
	    }
	    
	    $curdir = cwd();
	    if ($jobmode eq 'serial') {
		system("echo $protprefix combihelix job running.; $subcommand > ${protprefix}_serial.out; echo $protprefix combihelix job finished.");
#	        system("echo $protprefix combihelix job running.; $subcommand ; echo $protprefix combihelix job finished.");
	    } else {
		$runfile = "run_combihelix";
		if ($queuetype eq "sge") {
            $subcommand = "$subcommand -j \$JOB_ID.\$HOST";
            my $sge = "\#!/bin/csh\n".
                "#\$ -N $protprefix\n".
                "#\$ -j y\n".
                "$subcommand\n";
            open SGE, ">$runfile.sge";
            print SGE "$sge";
            close SGE;
            system("ssh $machine 'cd $curdir; qsub -cwd $runfile.sge'");

        } elsif ($queuetype eq "pbs") {
            $subcommand = "$subcommand -j \$PBS_JOBID";
            my $pbs = "#PBS -l nodes=1,walltime=01:00:00\n".
                "#PBS -q workq\n".
                "#PBS -j oe\n".
                "#PBS -N $protprefix\n".
                "#!/bin/csh\n".
                "cd \$PBS_O_WORKDIR\n".
                "$subcommand\n";
            open PBS, ">$runfile.pbs";
            print PBS "$pbs";
            close PBS;
            system("ssh $machine 'cd $curdir; qsub $runfile.pbs'");

        } elsif ($queuetype eq "sbatch") {
            $subcommand = "$subcommand -j \$SLURM_JOB_ID";
            my $sbatch = "#!/bin/bash\n".
                "#SBATCH --job-name=$protprefix\n".
                "#SBATCH --output=$protprefix.out\n".
                "#SBATCH --error=$protprefix.err\n".
                "#SBATCH --time=01:00:00\n".
                "$subcommand\n";
            open SBATCH, ">$runfile.sbatch";
            print SBATCH "$sbatch";
            close SBATCH;
            system("ssh $machine 'cd $curdir; sbatch $runfile.sbatch'");
        }
		print "$protprefix combihelix job submitted on $machine.\n";
		my $wait = 1;
		while ($wait) {
		    $wait = 0;
		    if (! -e "_combihelix_done_") {
			$wait = 1;
			sleep 60;
		    }
		}
	    }
	    chdir "..";
	    if ($scream) {
		$allscreamout = $protprefix."_allcombi_scream.out";
		$allmpsimout = $protprefix."_allcombi_mpsim.out";
		if ($ncount == 1) {
		    system("cat $combidir2/*_scream.out > $allscreamout");
		    system("cat $combidir2/*_mpsim.out > $allmpsimout");
		} else {
		    system("tail -1 $combidir2/*_scream.out >> $allscreamout");
		    system("tail -1 $combidir2/*_mpsim.out >> $allmpsimout");
		}
            }
            if ($membsolv) {
		$allmembsolvout = $protprefix."_allcombi_membsolv.out";
		if ($ncount == 1) {
		    system("cat $combidir2/*_membsolv.out > $allmembsolvout");
		} else {
		    system("tail -1 $combidir2/*_membsolv.out >> $allmembsolvout");
		}
            }
        }
        if ($ncount == $ncombi) { goto donecombis;}
    }
    close SCORE;
  donecombis:
    chdir "..";
}



sub help {
    $help_message = "
                      Adam-style Script Info
Program:
 :: combi_frombihelixsum.pl

Location:
 :: \$ge_path/programs/bihelixrot2/combi_frombihelixsum.pl

Release:
 :: Version 1.3 (29 April 2008)

Authors:
 :: Ravi Abrol (abrol\@wag.caltech.edu)
 :: Jenelle Bray and Amy Guili (Final Analysis Scripts)

Usage:
 :: combi_frombihelixsum.pl -p {protein_bgf_file} -rlib {Rotamer Library} -ener {scream or mpsim} -e {Energy Criteria} -n {number of combinations for combi_scream} -r -s -m -mp {minimization steps} -d -mach {machine}

Options:
 :: -h | --help             :: Optional    :: No Input
 :: Prints this help message.

GetOptions ('h|help'                 => \$help,
        'p|protfile=s'               => \$protfile,
        'ener|energy=s'              => \$energy,
        'e|ecriteria=i'              => \$ecriteria,
        'n|ncombi=i'                 => \$ncombi,
        'r|rotate'                   => \$rotate,
        's|scream'                   => \$scream,
        'm|membsolv'                 => \$membsolv,
        'mp|mpsim:i'                 => \$mpsim,
        'rlib|rotalib=f'             => \$rotalib,
        'd|debug'                    => \$debug,
        'mach|machine=s'             => \$machine);

 :: -p | --protfile         :: Required    :: Filename
 :: This is the protein BGF file

 :: -rlib | --rotalib       :: Optional    :: Float
 :: Diversity of the rotamer library requested in Angstroms.
 :: Acceptable inputs 0.1 through 5.0
 :: Default is 1.0

 :: -ener | --energy        :: Required    :: String
 :: Specify \"scream\" or \"mpsim\"

 :: -e | --ecriteria        :: Optional    :: Integer
 :: Energy criteria to use to build combinatorial sets on.
 :: 1 = Total Energy (Default if not specified)
 :: 2 = Total Energy - InterHelical vdW
 :: 3 = Total Energy - All vdW
 :: 4 = InterHelical HBond

 :: -n | --ncombi           :: Optional    :: Integer
 ::  Number of top combinations from bihelix energy sum to perform
 ::  combiscream on. Default is 100.

 :: -r | --rotate           :: Conditional-Optional    :: No Input
 :: Specify this option, if you only want to generate
 :: structure files corresponding to angles specified
 :: in the file given as an input to the -a option above.

 :: -s | --scream           :: Conditional-Optional    :: No Input
 :: Using this option will enable the -r option and
 :: then perform SCREAM on each of the rotated structures.

 :: -m | --membsolv         :: Optional    :: No Input
 :: Using this option will enable the -r and -s options and
 :: then perform MembSOLV on each of the rotated/screamed structures.

 :: -mp | --mpsim            :: Optional    :: No Input
 :: Use this option to evaluate MPSim energies for SCREAMed structures.
 :: Provide an interger number as input to perform that many minimization
 :: steps using MPSim.

 :: -d | --debug            :: Optional    :: No Input
 :: Specify this flag to keep all files for debugging or any other reason.
 :: Otherwise, minimal files will be kept (Default)

 :: -mach | --machine          :: Optional
 :: The machine to run the combihelix jobs.
 :: If the machine is specified, then jobs are submitted in serial
 :: fasion using the qsub queue on that machine.
 :: If machine is not specified, then local machine is used
 :: and jobs run in serial fashion.

Description:
 :: This wrapper script sets up the combinatorial helix rotational
 :: MembSCREAM step, where each helix is rotated simultaneously
 :: by angles corresponding to those identified by bihelix.
 :: This is followed by a full side-chain
 :: optimization using SCREAM and an implicit membrane solvation
 :: calculation using MembSOLV.

Output:
 :: ALL ENERGIES in kcal/mol.
 ::
 :: SCREAM output (proteinprefix_allcombi_scream.out):
 :: ...To Update...
 ::
 :: MembSOLV output (proteinprefix_allcombi_membsolv.out):
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
 :: combi_frombihelixsum.pl -p {protein_bgf_file} -rlib {Rotamer Library} -ener {scream or mpsim} -e {Energy Criteria} -n {number of combinations for combi_scream} -r -s -m -mp {minimization steps} -d -mach {machine}

";
    die $help_message;
}
